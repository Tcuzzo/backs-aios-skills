"""Real local HTTP consumer contract; fixture replaces only paid upstream HTTP."""
import asyncio
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_portable_messages_preserve_tools_stream_and_explicit_model(tmp_path):
    # The subprocess imports the installed aiohttp dependency, real gateway and
    # real stdlib runtime. No database, filesystem, socket or inference mocks.
    runner = tmp_path / "proof.py"
    runner.write_text('''
import asyncio, json, sys
from aiohttp import web, ClientSession
from pathlib import Path
sys.path.insert(0, sys.argv[1])
from portable_gateway import create_app

async def main():
    received=[]
    async def upstream(request):
        body=await request.json(); received.append(body)
        if body.get("stream"):
            response=web.StreamResponse(headers={"Content-Type":"text/event-stream", "x-request-id":"upstream-real"})
            await response.prepare(request)
            await response.write(b'event: message_start\\ndata: {"type":"message_start"}\\n\\n')
            await response.write(b'event: message_stop\\ndata: {"type":"message_stop"}\\n\\n')
            await response.write_eof(); return response
        return web.json_response({"id":"transport-fixture", "model":body["model"], "content":body["messages"][-1]["content"]})
    remote=web.Application(); remote.router.add_post("/v1/messages",upstream)
    rr=web.AppRunner(remote); await rr.setup(); rs=web.TCPSite(rr,"127.0.0.1",0); await rs.start()
    port=rs._server.sockets[0].getsockname()[1]
    config={"upstream":{"endpoint":f"http://127.0.0.1:{port}","model":"owner-selected", "provider":"fixture-paid-transport"},
            "receipt_path":sys.argv[2]}
    app=create_app(config); gr=web.AppRunner(app,handler_cancellation=True); await gr.setup(); gs=web.TCPSite(gr,"127.0.0.1",0); await gs.start()
    gp=gs._server.sockets[0].getsockname()[1]
    try:
      async with ClientSession() as client:
        body={"model":"owner-explicit", "max_tokens":17, "messages":[{"role":"assistant","content":[{"type":"tool_use","id":"t1","name":"read","input":{"path":"x"}}]},
              {"role":"user","content":[{"type":"tool_result","tool_use_id":"t1","content":"real fixture file result"}]}],"tools":[{"name":"read","input_schema":{"type":"object"}}]}
        async with client.post(f"http://127.0.0.1:{gp}/v1/messages?beta=true",json=body) as response:
          assert response.status==200, await response.text()
          result=await response.json(); assert result["model"]=="owner-explicit"
        assert received[0]==body
        body["stream"]=True
        async with client.post(f"http://127.0.0.1:{gp}/v1/messages",json=body) as response:
          assert response.status==200
          assert response.headers["x-request-id"]=="upstream-real"
          data=await response.read(); assert b'message_start' in data and b'message_stop' in data
        assert received[1]==body
        body["model"]="backs/claude-auto"; body["stream"]=False
        async with client.post(f"http://127.0.0.1:{gp}/v1/messages",json=body) as response:
          assert response.status==200, await response.text()
        assert received[2]["model"]=="owner-selected"
        assert received[2]["messages"]==body["messages"]
        # A real filesystem reporting error must not turn a real answer into a failure.
        config["receipt_path"]=str(Path(sys.argv[2]).parent)
        async with client.post(f"http://127.0.0.1:{gp}/v1/messages",json=body) as response:
          assert response.status==200, await response.text()
          await response.read()
        for _ in range(20):
          async with client.get(f"http://127.0.0.1:{gp}/health") as response: health=await response.json()
          if health["receipt_failures"]:break
          await asyncio.sleep(.03)
        assert health["receipt_failures"]==1 and health["last_receipt_error"]=="IsADirectoryError"
      print(json.dumps({"ok":True,"requests":len(received)}))
    finally:
      await gr.cleanup(); await rr.cleanup()
asyncio.run(main())
''')
    python = Path(sys.executable)
    result = subprocess.run([str(python), str(runner), str(ROOT / "provider"), str(tmp_path / "receipts.jsonl")],
                            capture_output=True, text=True, timeout=40)
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["requests"] == 4
    receipts = [json.loads(line) for line in (tmp_path / "receipts.jsonl").read_text().splitlines()]
    assert receipts[-1]["model"] == "owner-selected"
    assert receipts[-1]["source"] == "fleet_fallback"
    assert "messages" not in receipts[-1]


def test_client_disconnect_reaps_only_its_credential_helper(tmp_path):
    isolated = Path(sys.executable)
    runner = tmp_path / "cancel.py"
    runner.write_text('''
import asyncio, json, os, shlex, sys
from pathlib import Path
from aiohttp import web, ClientSession
sys.path.insert(0, sys.argv[1])
from portable_gateway import create_app
async def main():
    home=Path(sys.argv[2]); pidfile=home/"owned-helper.pid"
    helper=home/"helper.sh"
    helper.write_text("#!/bin/sh\\necho $$ > "+shlex.quote(str(pidfile))+"\\nexec "+shlex.quote(sys.executable)+" -c 'import time; time.sleep(60)'\\n")
    helper.chmod(0o700)
    receipt=home/"cancel-receipts.jsonl"
    app=create_app({"upstream":{"endpoint":"https://provider.example.invalid","model":"owner-selected","api_key_helper":shlex.quote(str(helper))},"receipt_path":str(receipt)})
    runner=web.AppRunner(app,handler_cancellation=True); await runner.setup()
    site=web.TCPSite(runner,"127.0.0.1",0); await site.start(); port=site._server.sockets[0].getsockname()[1]
    try:
      async with ClientSession() as client:
        task=asyncio.create_task(client.post(f"http://127.0.0.1:{port}/v1/messages",json={"model":"explicit","messages":[{"role":"user","content":"hi"}]}))
        for _ in range(100):
          if pidfile.exists(): break
          await asyncio.sleep(.03)
        assert pidfile.exists(), "actual configured helper did not start"
        pid=int(pidfile.read_text())
        assert Path(f"/proc/{pid}").exists()
        task.cancel()
        try: await task
        except asyncio.CancelledError: pass
        for _ in range(100):
          if not Path(f"/proc/{pid}").exists() and receipt.exists():break
          await asyncio.sleep(.03)
        assert not Path(f"/proc/{pid}").exists(), "owned helper survived disconnected request"
        rows=[json.loads(line) for line in receipt.read_text().splitlines()]
        assert rows[-1]["status"]=="cancelled", rows
        print(json.dumps({"ok":True,"owned_helper_reaped":True}))
    finally:await runner.cleanup()
asyncio.run(main())
''')
    result = subprocess.run([str(isolated), str(runner), str(ROOT / "provider"), str(tmp_path)],
                            capture_output=True, text=True, timeout=15)
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["owned_helper_reaped"]


def test_capability_routes_bind_credentials_to_their_destination(tmp_path):
    runner = tmp_path / "credentials.py"
    runner.write_text('''
import asyncio, json, os, sys
from aiohttp import web, ClientSession
sys.path.insert(0, sys.argv[1])
from portable_gateway import create_app
async def main():
    received=[]
    async def upstream(request):
        received.append({"path":request.path,"auth":request.headers.get("Authorization"),"key":request.headers.get("x-api-key")})
        return web.json_response({"ok":True})
    remote=web.Application(); remote.router.add_post("/{provider}/v1/messages",upstream)
    rr=web.AppRunner(remote); await rr.setup(); rs=web.TCPSite(rr,"127.0.0.1",0); await rs.start()
    base=f"http://127.0.0.1:{rs._server.sockets[0].getsockname()[1]}"
    os.environ["ANTHROPIC_API_KEY"]="ambient-fixture-key"
    os.environ["EXPLICIT_ROUTE_TEST_KEY"]="route-fixture-key"
    try:
      for explicit_key in (False,True):
        route={"endpoint":base+"/other","model":"other-model"}
        if explicit_key:route["api_key_env"]="EXPLICIT_ROUTE_TEST_KEY"
        config={"upstream":{"endpoint":base+"/owner","model":"owner-model", "credential_env":{"ANTHROPIC_API_KEY":"owner-fixture-key"}},
                "routes":{tier:route for tier in ("plan","build","work")}}
        gr=web.AppRunner(create_app(config)); await gr.setup(); gs=web.TCPSite(gr,"127.0.0.1",0); await gs.start()
        url=f"http://127.0.0.1:{gs._server.sockets[0].getsockname()[1]}/v1/messages"
        try:
          async with ClientSession() as client:
            for model in ("owner-explicit","backs/claude-auto"):
              async with client.post(url,json={"model":model,"messages":[{"role":"user","content":"work"}]},
                  headers={"Authorization":"Bearer incoming-host-fixture", "x-api-key":"incoming-host-fixture"}) as response:
                assert response.status==200,await response.text()
                await response.read()
        finally:await gr.cleanup()
        assert received[-2]=={"path":"/owner/v1/messages","auth":None,"key":"owner-fixture-key"},received[-2]
        expected="route-fixture-key" if explicit_key else None
        assert received[-1]=={"path":"/other/v1/messages","auth":None,"key":expected},received[-1]
      print(json.dumps({"ok":True,"requests":len(received)}))
    finally:await rr.cleanup()
asyncio.run(main())
''')
    result = subprocess.run([sys.executable, str(runner), str(ROOT / "provider")],
                            capture_output=True, text=True, timeout=15)
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["requests"] == 4
