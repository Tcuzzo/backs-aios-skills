"""Cloud/local credential collisions through the shipped helper and launcher.

Only synthetic runtime files are used. Subprocess output is never replayed by an
assertion, and the production HOME/environment are not inherited.
"""
from __future__ import annotations

import hmac
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]

ENV_LOADER = '''\
import os

def load_runtime_env(*, repo_root, override=False):
    for path in (repo_root / "backend/.env", repo_root / ".env"):
        if path.is_file():
            for line in path.read_text().splitlines():
                if "=" in line:
                    key, value = line.split("=", 1)
                    if override or key not in os.environ:
                        os.environ[key] = value
'''

# This fixture implements the existing env_secret_text source-order contract:
# nonempty direct variables, then explicitly referenced files, then credentials.
ENV_UTILS = '''\
import os
from pathlib import Path

def env_secret_text(name, default="", *, aliases=(), file_aliases=(), credential_names=()):
    for key in (name, *aliases):
        value = os.environ.get(key, "").strip()
        if value:
            return value
    for key in (name + "_FILE", *file_aliases):
        value = os.environ.get(key, "").strip()
        if value and Path(value).is_file():
            secret = Path(value).read_text().strip()
            if secret:
                return secret
    directory = os.environ.get("CREDENTIALS_DIRECTORY", "").strip()
    if directory:
        for key in credential_names:
            path = Path(directory) / key
            if path.is_file():
                secret = path.read_text().strip()
                if secret:
                    return secret
    return default
'''


class CloudCredentialSelectionTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name)
        self.project = self.home / "fixture-project"
        core = self.project / "backend/core"
        core.mkdir(parents=True)
        (core / "__init__.py").write_text("")
        (core / "env_loader.py").write_text(ENV_LOADER)
        (core / "env_utils.py").write_text(ENV_UTILS)
        self.dotenv = self.project / ".env"
        self.dotenv.write_text("")
        self.env = {"HOME": str(self.home), "PATH": os.defpath, "LANG": "C.UTF-8",
                    "PYTHONDONTWRITEBYTECODE": "1", "PYTHONNOUSERSITE": "1"}
        config = self.home / ".config/backs-aios/provider-control"
        config.mkdir(parents=True)
        (config / "project-root").write_text(str(self.project) + "\n")
        (config / "python-executable").write_text(sys.executable + "\n")
        runtime = self.home / ".local/share/backs-aios/provider-control/current"
        runtime.parent.mkdir(parents=True)
        runtime.symlink_to(ROOT, target_is_directory=True)
        bindir = self.home / ".local/bin"
        bindir.mkdir(parents=True)
        for source, name in ((ROOT / "bin/backs-provider", "backs-provider"),
                             (ROOT / "provider/ollama-key-helper.sh", "backs-ollama-key")):
            target = bindir / name
            shutil.copyfile(source, target)
            target.chmod(0o755)
        self.helper = bindir / "backs-ollama-key"

    def invoke(self):
        before = {p: p.read_bytes() for p in (self.dotenv, self.project / "backend/.env") if p.exists()}
        result = subprocess.run([str(self.helper)], cwd=self.home, env=self.env,
                                capture_output=True, timeout=20, check=False)
        self.assertTrue(all(p.read_bytes() == value for p, value in before.items()),
                        "Runtime env file was modified")
        self.assertFalse((self.home / ".config/backs-aios/secrets").exists())
        self.assertFalse((self.home / ".claude/settings.json").exists())
        return result

    def expect(self, value):
        result = self.invoke()
        self.assertEqual(0, result.returncode, "Helper failed; output withheld")
        self.assertTrue(hmac.compare_digest(value.encode(), result.stdout),
                        "Wrong credential selected; values withheld")
        self.assertEqual(0, len(result.stderr), "Helper emitted stderr; output withheld")

    def test_cloud_alias_wins_over_local_key_in_both_runtime_env_files(self):
        text = "LOCAL_OLLAMA_API_KEY=fixture-local\nOLLAMA_CLOUD_API_KEY=fixture-cloud\n"
        self.dotenv.write_text(text)
        (self.project / "backend/.env").write_text(text)
        self.expect("fixture-cloud")

    def test_explicit_cloud_alias_wins_over_generic_and_local(self):
        self.dotenv.write_text("OLLAMA_CLOUD_API_KEY=fixture-cloud\n")
        self.env.update({"OLLAMA_API_KEY": "fixture-generic", "LOCAL_OLLAMA_API_KEY": "fixture-local"})
        self.expect("fixture-cloud")

    def test_canonical_cloud_name_retains_highest_priority(self):
        self.dotenv.write_text("CLOUD_OLLAMA_API_KEY=fixture-canonical\n"
                              "OLLAMA_CLOUD_API_KEY=fixture-cloud\n"
                              "OLLAMA_API_KEY=fixture-generic\nLOCAL_OLLAMA_API_KEY=fixture-local\n")
        self.expect("fixture-canonical")

    def test_generic_key_remains_supported(self):
        self.dotenv.write_text("OLLAMA_API_KEY=fixture-generic\nLOCAL_OLLAMA_API_KEY=fixture-local\n")
        self.expect("fixture-generic")

    def test_local_only_is_rejected_without_outputting_credential(self):
        self.dotenv.write_text("LOCAL_OLLAMA_API_KEY=fixture-local-only\n")
        result = self.invoke()
        self.assertNotEqual(0, result.returncode)
        self.assertEqual(0, len(result.stdout), "Local credential must not be emitted for cloud use")
        self.assertFalse(b"fixture-local-only" in result.stderr, "Credential appeared in stderr")

    def test_credential_directory_is_reached_instead_of_local_key(self):
        directory = self.home / "fixture-credentials"
        directory.mkdir()
        (directory / "ollama_api_key").write_text("fixture-directory")
        self.dotenv.write_text("LOCAL_OLLAMA_API_KEY=fixture-local\n"
                              "CREDENTIALS_DIRECTORY=" + str(directory) + "\n")
        self.expect("fixture-directory")

    def test_existing_explicit_key_file_is_reached_instead_of_local_key(self):
        file = self.home / "fixture-key-file"
        file.write_text("fixture-file")
        self.dotenv.write_text("LOCAL_OLLAMA_API_KEY=fixture-local\n"
                              "OLLAMA_API_KEY_FILE=" + str(file) + "\n")
        self.expect("fixture-file")

    def test_cloud_direct_value_precedes_existing_credential_directory(self):
        directory = self.home / "fixture-credentials"
        directory.mkdir()
        (directory / "ollama_api_key").write_text("fixture-directory")
        self.dotenv.write_text("OLLAMA_CLOUD_API_KEY=fixture-cloud\n"
                              "CREDENTIALS_DIRECTORY=" + str(directory) + "\n")
        self.expect("fixture-cloud")

    def test_backend_env_precedence_is_not_changed(self):
        (self.project / "backend/.env").write_text("OLLAMA_CLOUD_API_KEY=fixture-backend\n")
        self.dotenv.write_text("OLLAMA_CLOUD_API_KEY=fixture-root\nLOCAL_OLLAMA_API_KEY=fixture-local\n")
        self.expect("fixture-backend")


if __name__ == "__main__":
    unittest.main()
