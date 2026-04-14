#!/bin/bash
set -e
SRC=/home/duchaufm/doctorat/fresh/GreenhousesJL
MSG="${1:-Update site}"

# Rebuild docs only if --docs flag passed
if [[ "$2" == "--docs" ]]; then
  echo "→ Rebuilding docs..."
  cd "$SRC" && julia --project=. docs/make.jl
fi

# Sync
echo "→ Syncing files..."
cp -r "$SRC/presentation/." ~/GreenhousesJL-site/presentation/
cp -r "$SRC/docs/build/." ~/GreenhousesJL-site/docs/build/

# Commit + push
cd ~/GreenhousesJL-site
git add -A
if git diff --cached --quiet; then
  echo "No changes to push."
  exit 0
fi
git commit -m "$MSG"
git push
echo "✓ Pushed. Site redeploys in ~30s."
echo "  https://melchiorduchaufour.github.io/GreenhousesJL/presentation/"
