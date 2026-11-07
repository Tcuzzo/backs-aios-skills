"""Real-file fixtures shared without inheriting unrelated test cases."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
TEST_TEMP = ROOT / 'sandbox' / 'hook-tests'
RUNTIMES = {'js': 'node', 'py': sys.executable}

class FloorFixture:
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
            'skills/backs-build-flow/SKILL.md': '# Build Flow fixture\nOne integration owner.\n',
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


class FoundationManifestFixture(FloorFixture):
    def setUp(self):
        super().setUp()
        self.bodies.update({
            "skills/yoke/profiles/architect.md": "# Validated architect fixture\nRespect the operator.\n",
            "skills/human-calibration/SKILL.md": "# Human calibration fixture\nApply the human profile.\n",
        })
        for name, body in self.bodies.items():
            target = self.deploy / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(body.encode())
        manifest = self.deploy / "config/foundation_manifest.json"
        manifest.parent.mkdir(parents=True)
        manifest.write_text(json.dumps({"version": 1, "bodies": [
            {"path": name, "sha256": hashlib.sha256(body.encode()).hexdigest()}
            for name, body in self.bodies.items()
        ]}))

    def load(self, suffix, *, discard=False):
        return subprocess.run(
            ["node" if suffix == "js" else sys.executable,
             str(self.pack / "hooks" / ("aios_gate." + suffix)),
             "--load", "backs-aios:optimus", "manifest-contract"],
            env=self.env, text=True,
            stdout=subprocess.DEVNULL if discard else subprocess.PIPE,
            stderr=subprocess.PIPE, timeout=10,
        )

