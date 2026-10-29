#!/usr/bin/env bash
# Build the site and publish it to the gh-pages branch (GitHub Pages, legacy branch build).
set -euo pipefail
cd "$(dirname "$0")/.."
OUT=$(mktemp -d)
python3 build.py --out "$OUT"
touch "$OUT/.nojekyll"
SRC=$(git rev-parse --short HEAD)
URL=$(git remote get-url origin)
cd "$OUT"
git init -q -b gh-pages
git add -A
git commit -qm "Publish site from main $SRC"
git push -f "$URL" gh-pages
