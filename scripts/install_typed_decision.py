#!/usr/bin/env python3
"""Install measured CPU dependencies/checkpoints in an isolated owned release.

No model is loaded, no listener starts, and no host provider is activated. The
same stdlib installer and manifest are usable without a BACKS backend checkout.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import time


def run(command, **kwargs):
    subprocess.run(command, check=True, **kwargs)


def install(manifest_path, root, *, source=None, reuse_cache=None):
    raw=Path(manifest_path).read_bytes(); manifest=json.loads(raw)
    required=manifest['platform']
    if (platform.system()!=required['system'] or platform.machine()!=required['machine']
            or list(sys.version_info[:2])!=required['python']):
        raise RuntimeError('This measured CPU bundle requires '+json.dumps(required)+'. No shared environment was changed.')
    root=Path(root).expanduser().resolve(); digest=hashlib.sha256(raw).hexdigest()
    release=root/'releases'/digest[:16]; release.mkdir(parents=True,exist_ok=True)
    receipt_path=release/'receipt.json'; source_dir=release/'src'; venv=release/'venv'; cache=release/'hf'
    revision=manifest['source']['revision']
    if not source_dir.exists():
        run(['git','clone','--no-checkout','--no-hardlinks',str(source or manifest['source']['url']),str(source_dir)])
        run(['git','-C',str(source_dir),'checkout','--detach',revision])
    actual=subprocess.check_output(['git','-C',str(source_dir),'rev-parse','HEAD'],text=True).strip()
    if actual!=revision or subprocess.check_output(['git','-C',str(source_dir),'status','--porcelain'],text=True).strip():
        raise RuntimeError('Isolated source differs from the exact measured revision; preserved without overwrite.')
    (release/'manifest.json').write_bytes(raw)
    lock=release/'requirements.txt';lock.write_text('\n'.join(manifest['requirements'])+'\n')
    uv=shutil.which('uv')
    if not (venv/'bin/python').exists():
        if uv:run([uv,'venv','--python',sys.executable,str(venv)])
        else:run([sys.executable,'-m','venv',str(venv)])
    python=str(venv/'bin/python')
    installer=[uv,'pip','install','--python',python] if uv else [python,'-m','pip','install']
    run(installer+['-r',str(lock),'torch @ '+manifest['torch_wheel'],str(source_dir)+'[serve]'])
    if reuse_cache and not cache.exists():
        # Copy only supplied immutable cache bytes; never edit the source cache.
        def copy(source_file,target_file):
            try:return os.link(source_file,target_file)
            except OSError:return shutil.copy2(source_file,target_file)
        shutil.copytree(Path(reuse_cache).expanduser(),cache,symlinks=True,copy_function=copy)
    download='''import os,json,hashlib,sys
from pathlib import Path
from huggingface_hub import snapshot_download
import zipfile,shutil
manifest=json.loads(Path(sys.argv[1]).read_text());rows=[]
for item in manifest['snapshots']:
 p=Path(snapshot_download(item['repo'],revision=item['revision'],allow_patterns=list(item['files']),max_workers=2,token=False))
 for name,expected in item['files'].items():
  f=p/name
  if f.stat().st_size!=expected['bytes'] or hashlib.file_digest(f.open('rb'),'sha256').hexdigest()!=expected['sha256']:
   raise RuntimeError('Pinned checkpoint content mismatch: '+name)
 if item['repo']==manifest.get('needle',{}).get('repo'):
  spec=manifest['needle'];out=Path(sys.argv[1]).parent/'needle';out.mkdir(exist_ok=True)
  shutil.copyfile(p/spec['weights'],out/'needle3.cact')
  lib=spec['shared_library']
  with zipfile.ZipFile(p/lib['archive']) as archive:data=archive.read(lib['member'])
  if len(data)!=lib['bytes'] or hashlib.sha256(data).hexdigest()!=lib['sha256']:
   raise RuntimeError('Pinned Needle shared library content mismatch')
  (out/'libneedle3.so').write_bytes(data)
 rows.append({'repo':item['repo'],'revision':item['revision'],'verified_files':len(item['files'])})
Path(sys.argv[2]).write_text(json.dumps(rows,indent=2))
'''
    env=dict(os.environ,HF_HOME=str(cache))
    run([python,'-c',download,str(release/'manifest.json'),str(release/'snapshots.json')],env=env)
    with (release/'requirements.freeze.txt').open('w') as stream:
        run(([uv,'pip','freeze','--python',python] if uv else [python,'-m','pip','freeze']),stdout=stream)
    receipt={'manifest_sha256':digest,'source_revision':revision,'release':str(release),
             'python':python,'hf_home':str(cache),'needle_assets':str(release/'needle'),'models_loaded':False,'host_provider_changed':False,
             'listener_started':False,'snapshots':json.loads((release/'snapshots.json').read_text()),'installed_at':time.time()}
    receipt_path.write_text(json.dumps(receipt,indent=2)+'\n')
    current=root/'current'; temporary=root/('current.'+str(os.getpid()))
    if current.exists() and not current.is_symlink():
        raise RuntimeError('Existing current is not an installer symlink; preserved. Verified release is ready at '+str(release))
    temporary.symlink_to(release, target_is_directory=True);temporary.replace(current)
    return receipt


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest',type=Path,default=Path(__file__).resolve().parents[1]/'config/typed_decision_install.json')
    parser.add_argument('--root',type=Path,default=Path.home()/'.local/share/backs-aios/typed-decision')
    parser.add_argument('--source',type=Path,help='Existing local upstream checkout; exact revision is still validated.')
    parser.add_argument('--reuse-cache',type=Path,help='Existing downloaded cache to copy and verify; never modified.')
    args=parser.parse_args();print(json.dumps(install(args.manifest,args.root,source=args.source,reuse_cache=args.reuse_cache)))


if __name__=='__main__':main()
