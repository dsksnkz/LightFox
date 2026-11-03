#!/bin/bash
# After a successful native build: smoke test, package and install.
set -euo pipefail
cd "$(dirname "$0")/.."
export MOZCONFIG="$PWD/lightfox/mozconfig"
out="$HOME/Projects/.lightfox-smoke/native"
python3 lightfox/smoke.py obj-lightfox/dist/bin/lightfox "$out" --wait 20 | tee "$out.json"
python3 -c "import json,sys; r=json.load(open(sys.argv[1])); sys.exit(1 if r.get('fatal') or r.get('kept_but_missing') else 0)" "$out.json"
./mach package
lightfox/install.sh
echo "Done. Open LightFox from your launcher."
