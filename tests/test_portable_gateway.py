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
      print(json.dumps({"ok":True,"requests":len(received)}))
    finally:
      await gr.cleanup(); await rr.cleanup()
asyncio.run(main())
''')
    python = Path.home() / ".local/share/backs-aios/typed-decision/current/venv/bin/python"
    assert python.is_file(), "Install the pinned isolated runtime before this real consumer test"
    result = subprocess.run([str(python), str(runner), str(ROOT / "provider"), str(tmp_path / "receipts.jsonl")],
                            capture_output=True, text=True, timeout=40)
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["requests"] == 3
    receipts = [json.loads(line) for line in (tmp_path / "receipts.jsonl").read_text().splitlines()]
    assert receipts[-1]["model"] == "owner-selected"
    assert receipts[-1]["source"] == "fleet_fallback"
    assert "messages" not in receipts[-1]
