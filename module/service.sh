#!/system/bin/sh
MODDIR=${0%/*}
DATA=/data/adb/maa
LIBDIR=$DATA/lib
RESDIR=$DATA/resource
LOG=$DATA/maaweb.log

# Wait for Android to finish booting before network/download/start.
until [ "$(getprop sys.boot_completed)" = "1" ]; do sleep 2; done

mkdir -p "$DATA" "$LIBDIR" "$RESDIR" "$DATA/run"
chcon -R u:object_r:magisk_file:s0 "$DATA" 2>/dev/null || true

# One-time/repair download of the official arm64 core and resource.
/system/bin/maactl ensure >> "$LOG" 2>&1 &

(
  while true; do
    if [ -f "$LIBDIR/libMaaCore.so" ] && [ -f "$RESDIR/config.json" ]; then
      if ! pgrep -f /system/bin/maaweb >/dev/null 2>&1; then
        chcon -R u:object_r:magisk_file:s0 "$DATA" 2>/dev/null || true
        HOME="$DATA" LD_LIBRARY_PATH="$LIBDIR" /system/bin/maaweb -data "$DATA" -lib "$LIBDIR" >> "$LOG" 2>&1 &
      fi
    fi
    sleep 10
  done
) &
