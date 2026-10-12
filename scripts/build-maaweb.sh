#!/usr/bin/env bash
# Cross-compile the MAA web console for arm64 Android.
# Requires: Go 1.22+, Android NDK r26/r27.
set -euo pipefail

here="$(cd "$(dirname "$0")/.." && pwd)"
out="${1:-$here/maaweb/maaweb}"

: "${ANDROID_NDK_HOME:?set ANDROID_NDK_HOME to the NDK root}"
case "$(uname -s)" in
  MINGW*|MSYS*|CYGWIN*) host=windows-x86_64 ;;
  Darwin)                host=darwin-x86_64 ;;
  *)                     host=linux-x86_64 ;;
esac

export GOOS=android
export GOARCH=arm64
export CGO_ENABLED=1
export CC="$ANDROID_NDK_HOME/toolchains/llvm/prebuilt/$host/bin/aarch64-linux-android21-clang"
export CGO_CFLAGS='--target=aarch64-linux-android21 -O2'
export CGO_LDFLAGS='--target=aarch64-linux-android21'

cd "$here/maaweb"
go build -trimpath -ldflags '-s -w' -o "$out" .
echo "built: $out"
