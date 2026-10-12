#!/system/bin/sh
# Stop the running daemon on uninstall.
pkill -f /system/bin/maaweb 2>/dev/null || true
# Keep /data/adb/maa by default so re-install reuses downloaded components.
