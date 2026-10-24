"""Real host subprocess contract: deliver grounding without refusing tools."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
TEST_TEMP = ROOT / 'sandbox' / 'hook-tests'
RUNTIMES = {'js': 'node', 'py': sys.executable}

class FloorAutoloadTest(unittest.TestCase):
    def setUp(self):
        TEST_TEMP.mkdir(parents=True, exist_ok=True)
        self.tmp = tempfile.TemporaryDirectory(dir=TEST_TEMP)
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.pack = self.root / 'pack'
        (self.pack / 'hooks').mkdir(parents=True)
        for suffix in ('js', 'py'):
            shutil.copyfile(ROOT / 'hooks' / ('aios_gate.' + suffix), self.pack / 'hooks' / ('aios_gate.' + suffix))
        shutil.copyfile(ROOT / 'hooks/opencode-plugin.js', self.pack / 'hooks/opencode-plugin.mjs')
        self.deploy = self.root / 'deploy'
        self.bodies = {
            'backend/prompts/BACKS_CODEX_HARNESS.md': '# Real harness fixture\nRepository source owns the rules.\n',
            'skills/optimus/SKILL.md': '# Optimus fixture\nLoad the canonical floor.\n',
            'skills/yoke/SKILL.md': '# Yoke fixture\nPreserve operator intent.\n',
        }
        for name, body in self.bodies.items():
            target = self.deploy / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(body.encode())
        home = str(self.root / 'home')
        self.env = {**os.environ, 'HOME': home, 'USERPROFILE': home, 'BACKS_DEPLOY_ROOT': str(self.deploy), 'AIOS_GATE': 'on'}

    def run_gate(self, suffix, event, **payload):
        return subprocess.run([RUNTIMES[suffix], str(self.pack / 'hooks' / ('aios_gate.'+suffix))], input=json.dumps({'session_id': 'floor-contract', 'hook_event_name':event, **payload}), text=True, capture_output=True, env=self.env, timeout=10)

    def context(self, result):
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertNotIn('permission', data)
        hook = data.get('hookSpecificOutput', {})
        self.assertNotIn('permissionDecision', hook)
        return data.get('additional_context', hook.get('additionalContext',''))

    def test_start_and_compact_deliver_real_bodies_without_revoking_floor(self):
        for suffix in ('js','py'):
            with self.subTest(runtime=suffix):
                for event in ('SessionStart', 'SessionStart'):
                    result = self.run_gate(suffix, event, source='compact')
                    context = self.context(result)
                    for body in self.bodies.values(): self.assertIn(body, context)
                    self.assertTrue((self.root/'home/.aios/state/aios_floor_floor-contract.state').is_file())
                self.assertFalse((self.root/'home/.claude/state/backs_ground_floor-contract.state').exists(), 'context delivery must not invent a Skill event')

    def test_missing_session_grounding_autoloads_before_mutation_without_deny(self):
        for suffix in ('js','py'):
            with self.subTest(runtime=suffix):
                shutil.rmtree(self.root/'home', ignore_errors=True)
                result = self.run_gate(suffix,'PreToolUse',tool_name='Bash',tool_input={'command':'git commit -m repair > evidence.log'})
                context = self.context(result)
                for body in self.bodies.values(): self.assertIn(body, context)
                again = self.run_gate(suffix,'PreToolUse',tool_name='Write',tool_input={'path':'example.txt'})
                self.assertEqual(again.returncode,0,again.stderr)
                self.assertEqual(again.stdout,'')

    def test_missing_bodies_warn_without_tool_denial_or_false_receipt(self):
        shutil.rmtree(self.deploy)
        for suffix in ('js','py'):
            with self.subTest(runtime=suffix):
                shutil.rmtree(self.root/'home', ignore_errors=True)
                result=self.run_gate(suffix,'PreToolUse',tool_name='Write',tool_input={})
                self.assertEqual(result.returncode,0,result.stderr)
                self.assertNotIn('"deny"',result.stdout)
                self.assertIn('unavailable',result.stderr.lower())
                self.assertFalse((self.root/'home/.aios/state/aios_floor_floor-contract.state').exists())

    def assert_receipt(self, session, expected):
        marker = self.root / 'home/.aios/state' / f'aios_floor_{session}.state'
        self.assertTrue(marker.is_file())
        receipt = json.loads(Path(str(marker) + '.load.json').read_text())
        self.assertEqual(receipt['session_id'], session)
        self.assertEqual(receipt['kind'], 'context_delivery')
        expected_paths = {Path(path): body for path, body in expected.items()}
        self.assertEqual({Path(row['path']) for row in receipt['bodies']}, set(expected_paths))
        for row in receipt['bodies']:
            self.assertEqual(row['sha256'], hashlib.sha256(expected_paths[Path(row['path'])].encode()).hexdigest())

    def test_receipt_binds_exact_delivered_unicode_and_line_endings(self):
        name = 'skills/optimus/SKILL.md'
        self.bodies[name] = '# Optimus\r\nOperator sovereignty — loaded.\r\n'
        (self.deploy/name).write_bytes(self.bodies[name].encode())
        for suffix in ('js', 'py'):
            context = self.context(self.run_gate(suffix, 'SessionStart'))
            for body in self.bodies.values(): self.assertIn(body, context)
            self.assert_receipt('floor-contract', {str(self.deploy/n): b for n,b in self.bodies.items()})

    def test_portable_pack_and_installed_native_pointer_discovery(self):
        self.env.pop('BACKS_DEPLOY_ROOT')
        self.env.pop('BACKS_AI_ROOT', None)
        for name in ('optimus', 'human-calibration'):
            target = self.pack/'skills'/name/'SKILL.md'
            target.parent.mkdir(parents=True)
            target.write_text('# Portable ' + name + '\n')
        for suffix in ('js', 'py'):
            context = self.context(self.run_gate(suffix, 'SessionStart'))
            self.assertIn('# Portable optimus', context)
            self.assertNotIn('# Real harness fixture', context)
        pointer = self.root/'home/.codex/skills/optimus'
        pointer.parent.mkdir(parents=True)
        pointer.symlink_to(self.deploy/'skills/optimus', target_is_directory=True)
        for suffix in ('js', 'py'):
            context = self.context(self.run_gate(suffix, 'SessionStart'))
            for body in self.bodies.values(): self.assertIn(body, context)
            self.assert_receipt('floor-contract', {str(self.deploy/n): b for n,b in self.bodies.items()})

    def test_closed_output_never_creates_load_marker(self):
        for suffix in ('js', 'py'):
            for args in ([], ['--load', 'optimus', 'floor-contract']):
                shutil.rmtree(self.root/'home', ignore_errors=True)
                reader, writer = os.pipe()
                os.close(reader)
                try:
                    result = subprocess.run([RUNTIMES[suffix], str(self.pack/'hooks'/('aios_gate.'+suffix)), *args],
                        input=json.dumps({'session_id':'floor-contract','hook_event_name':'SessionStart'}),
                        text=True, stdout=writer, stderr=subprocess.PIPE, env=self.env, timeout=10)
                finally:
                    os.close(writer)
                self.assertIn('failed' if args else 'unavailable', result.stderr)
                self.assertEqual(result.returncode, 1 if args else 0)
                self.assertFalse((self.root/'home/.aios/state/aios_floor_floor-contract.state').exists())

    def test_unknown_skill_event_does_not_fabricate_co_evidence(self):
        known = self.pack/'skills/optimus/SKILL.md'
        known.parent.mkdir(parents=True)
        known.write_text('# Known pack skill\n')
        for suffix in ('js','py'):
            shutil.rmtree(self.root/'home', ignore_errors=True)
            result=self.run_gate(suffix,'PostToolUse',tool_name='Skill',tool_input={'skill':'not-a-pack-skill'})
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertFalse((self.root/'home/.claude/state/backs_ground_floor-contract.state').exists())

    def test_explicit_loader_emits_every_recorded_digest_and_sanitizes_session(self):
        for suffix in ('js', 'py'):
            shutil.rmtree(self.root/'home', ignore_errors=True)
            result = subprocess.run([RUNTIMES[suffix],
                str(self.pack/'hooks'/('aios_gate.'+suffix)), '--load', 'optimus', 'floor/session'],
                capture_output=True, env=self.env, timeout=10)
            self.assertEqual(result.returncode, 0, result.stderr)
            for name in ('optimus', 'yoke'):
                body = (self.deploy/'skills'/name/'SKILL.md').read_bytes()
                self.assertIn(body, result.stdout)
            state = self.root/'home/.claude/state'
            receipts = list(state.glob('backs_ground_*.hashes.json'))
            self.assertEqual(len(receipts), 1)
            digests = json.loads(receipts[0].read_text())
            self.assertEqual(digests, {name: hashlib.sha256(
                (self.deploy/'skills'/name/'SKILL.md').read_bytes()).hexdigest()
                for name in ('optimus','yoke')})
            self.assertFalse((state/'backs_ground_floor').exists())

    def test_opencode_existing_kill_switch_warns_without_loading_or_denial(self):
        script = """
import plugin from './hooks/opencode-plugin.mjs';
const hooks = await plugin({});
const output = {system:['existing system']};
await hooks['experimental.chat.system.transform']({sessionID:'disabled-context'}, output);
console.log(JSON.stringify(output));
"""
        result = subprocess.run(['node','--input-type=module','--eval',script], cwd=self.pack,
            env={**self.env,'AIOS_GATE':'off','BACKS_AIOS_RUNTIME_ROOT':str(self.pack)},
            text=True,capture_output=True,timeout=10)
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertEqual(json.loads(result.stdout), {'system':['existing system']})
        self.assertIn('disabled', result.stderr)
        self.assertFalse((self.root/'home/.aios/state/aios_floor_disabled-context.state').exists())

    def test_opencode_real_adapter_delivers_context_before_recording(self):
        script = '''
import plugin from './hooks/opencode-plugin.mjs';
import fs from 'node:fs';
import path from 'node:path';
const hooks = await plugin({});
await hooks['tool.execute.before']({sessionID:'before-context',tool:'write'},{args:{path:'file.txt'}});
const anonymous = {system:[]};
await hooks['experimental.chat.system.transform']({}, anonymous);
if (!anonymous.system.join('').includes('Optimus fixture')) throw new Error('optional sessionID dropped context');
const marker = path.join(process.env.HOME,'.aios/state/aios_floor_open-code.state');
let delivered = 'existing system';
const system = ['existing system','preserve second'];
Object.defineProperty(system,'0',{get(){return delivered},set(value){
  if (fs.existsSync(marker)) throw new Error('marker preceded actual delivery');
  delivered=value;
}});
await hooks['experimental.chat.system.transform']({sessionID:'open-code'}, {system});
await hooks['tool.execute.before']({sessionID:'open-code',tool:'write'},{args:{path:'file.txt'}});
await hooks['experimental.chat.system.transform']({sessionID:'failed-context'}, {system:Object.freeze(['locked host array'])});
console.log(JSON.stringify({system, marker:fs.existsSync(marker)}));
'''
        result = subprocess.run(['node','--input-type=module','--eval',script],cwd=self.pack,
            env={**self.env,'BACKS_AIOS_RUNTIME_ROOT':str(self.pack)},text=True,capture_output=True,timeout=10)
        self.assertEqual(result.returncode,0,result.stderr)
        data=json.loads(result.stdout)
        self.assertTrue(data['marker'])
        self.assertTrue(data['system'][0].startswith('existing system\n\n'))
        self.assertEqual(data['system'][1], 'preserve second')
        for body in self.bodies.values(): self.assertIn(body,data['system'][0])
        self.assert_receipt('open-code',{str(self.deploy/n):b for n,b in self.bodies.items()})
        self.assertFalse((self.root/'home/.aios/state/aios_floor_failed-context.state').exists())
        self.assertFalse((self.root/'home/.aios/state/aios_floor_before-context.state').exists())

if __name__ == '__main__': unittest.main()
