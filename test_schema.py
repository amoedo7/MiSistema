#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
p = subprocess.run([sys.executable, str(HERE / 'misistema.py'), '--compact'], capture_output=True, text=True, check=True)
r = json.loads(p.stdout)
assert r['schema'] == 'desarrollamo.misistema.v1'
assert isinstance(r['system'], dict)
assert isinstance(r['runtimes'], dict)
assert r['privacy']['environment_values_collected'] is False
assert r['privacy']['secret_files_read'] is False
assert r['privacy']['credentials_collected'] is False
assert 'python' in r['runtimes']
print('MiSistema schema OK')
