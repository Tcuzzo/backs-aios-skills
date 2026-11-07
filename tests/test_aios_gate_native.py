"""Native-path physical coverage for the Python grounding hook."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import time
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load_hook():
    spec = importlib.util.spec_from_file_location('native_aios_gate', ROOT/'hooks/aios_gate.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class NativePythonGateTest(unittest.TestCase):
    def setUp(self):
        (ROOT/'sandbox/hook-tests').mkdir(parents=True, exist_ok=True)
        self.tmp = tempfile.TemporaryDirectory(dir=ROOT/'sandbox/hook-tests')
        self.home = Path(self.tmp.name)/'home'
        self.deploy = Path(self.tmp.name)/'deploy'
        (self.home/'.claude/state').mkdir(parents=True)
        (self.deploy/'config').mkdir(parents=True)
        (self.deploy/'body').mkdir()
        self.body = self.deploy/'body/floor.md'
        self.body.write_bytes(b'floor-body\n')
        self.row = {'path': 'body/floor.md', 'sha256': hashlib.sha256(self.body.read_bytes()).hexdigest()}
        (self.deploy/'config/foundation_manifest.json').write_text(json.dumps({'bodies': [self.row]}))
        self.old = {key: os.environ.get(key) for key in ('HOME', 'BACKS_DEPLOY_ROOT')}
        os.environ.update(HOME=str(self.home), BACKS_DEPLOY_ROOT=str(self.deploy))
        self.gate = load_hook()

    def tearDown(self):
        for key, value in self.old.items():
            if value is None: os.environ.pop(key, None)
            else: os.environ[key] = value
        self.tmp.cleanup()

    def receipt(self, **changes):
        session = 'native-session'
        value = {'kind': 'foundation_delivery', 'session_id': session,
                 'source_root': str(self.deploy.resolve()), 'order': [self.row['path']],
                 'sha256': {self.row['path']: self.row['sha256']},
                 'expires_at': time.time() + 60}
        value.update(changes)
        key = hashlib.sha256(session.encode()).hexdigest()
        (self.home/'.claude/state'/f'backs_load_{key}.json').write_text(json.dumps(value))
        return session

    def test_real_manifest_and_receipt_validation(self):
        self.assertEqual(self.gate._foundation_manifest_bodies(str(self.deploy)), b'floor-body\n\n\n')
        session = self.receipt()
        self.assertTrue(self.gate._canonical_receipt_valid(session))
        for changes in ({'expires_at': time.time()-1}, {'order': []}, {'sha256': {}}, {'source_root': '/escape'}):
            self.receipt(**changes)
            self.assertFalse(self.gate._canonical_receipt_valid(session), changes)

    def test_canonical_route_never_writes_portable_marker(self):
        with tempfile.TemporaryFile(mode='w+', encoding='utf-8') as output:
            prior = self.gate.sys.stdout
            self.gate.sys.stdout = output
            self.gate.handle({'hook_event_name': 'PreToolUse', 'tool_name': 'Write',
                              'session_id': 'native-session', 'tool_input': {}})
            self.gate.sys.stdout = prior
            output.seek(0)
            self.assertIn('BACKS FOUNDATION', output.read())
        self.assertFalse((self.home/'.aios/state/aios_floor_native-session.state').exists())
