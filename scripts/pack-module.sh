#!/usr/bin/env bash
# Package the Magisk module zip. Expects maaweb + libMaaNativeExt.so to be present.
set -euo pipefail

here="$(cd "$(dirname "$0")/.." && pwd)"
mod="$here/module"
ver="$(sed -n 's/^version=//p' "$mod/module.prop" | head -1)"
ver="${ver:-v0.0.0}"
out="$here/maa_android-${ver}.zip"

for f in "$mod/system/bin/maaweb" "$mod/common/libMaaNativeExt.so"; do
  [ -f "$f" ] || { echo "missing: $f" >&2; exit 1; }
done

rm -f "$out"
( cd "$mod" && zip -r -X "$out" . -x '.git*' )
echo "packed: $out"
