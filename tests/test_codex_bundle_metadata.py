"""Packaging preserves public metadata and creates a real nested destination."""
import json
import pytest
from test_refresh_codex_local import REFRESH, source_fixture


@pytest.mark.parametrize('interface_location', ['root', 'extension'])
def test_nested_bundle_preserves_public_metadata(tmp_path, interface_location):
    source = source_fixture(tmp_path)
    path = source / 'plugin.json'
    portable = json.loads(path.read_text())
    interface = {'displayName': 'Café tools', 'shortDescription': 'A public skill pack'}
    portable['description'] = 'Public description'
    if interface_location == 'root':
        portable['interface'] = interface
    else:
        portable['extensions'] = {'com.openai': {'interface': interface}}
    path.write_text(json.dumps(portable))
    before = path.read_bytes()
    stage = REFRESH.stage_bundle(source, tmp_path / 'new-parent' / 'plugins', 'nested-contract')
    result = json.loads((stage / '.codex-plugin/plugin.json').read_text())
    assert result['interface'] == interface
    assert result['description'] == portable['description']
    assert result['version'] == portable['version']
    assert path.read_bytes() == before
    assert (stage / 'hooks/hooks.json').read_bytes() == (source / 'hooks/hooks.json').read_bytes()
