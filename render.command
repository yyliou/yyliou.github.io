#!/bin/bash
# Double-click this in Finder to re-render the whole Quarto site.
cd "$(dirname "$0")" || exit 1
Q="$(command -v quarto || echo /usr/local/bin/quarto)"
[ -x "$Q" ] || { echo "quarto not found in PATH."; read -r -p "Press return to close."; exit 1; }
"$Q" render "$@"
status=$?
echo
if [ $status -eq 0 ]; then
  echo "Changed files:"
  git status --porcelain 2>/dev/null | sed 's/^/  /'
fi
read -r -p "Done (exit $status). Press return to close."
exit $status
