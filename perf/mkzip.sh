#!/bin/bash
set -e
cd /workspace/vepa; export PATH=/workspace/tools/node22/node-v22.23.3-linux-x64/bin:$PATH
H=$(git rev-parse --short HEAD); B=$(git branch --show-current)
rm -rf /tmp/zipbuild; mkdir -p /tmp/zipbuild
npx vite build --outDir /tmp/zipbuild/vepa-test-build --emptyOutDir >/dev/null 2>&1
cp /workspace/perf/zipextra/serve-local.py /workspace/perf/zipextra/README-TEST-BUILD.txt /tmp/zipbuild/vepa-test-build/
sed -i "1s|.*|VEPA test build — branch $B @ $H (not pushed)|" /tmp/zipbuild/vepa-test-build/README-TEST-BUILD.txt
mkdir -p /tmp/zipbuild/vepa-test-build/docs; cp -r docs/systems /tmp/zipbuild/vepa-test-build/docs/
python3 -c "import shutil; shutil.make_archive('/workspace/out/vepa-test-build','zip','/tmp/zipbuild','vepa-test-build')"
ls -la /workspace/out/vepa-test-build.zip; head -1 /tmp/zipbuild/vepa-test-build/README-TEST-BUILD.txt
