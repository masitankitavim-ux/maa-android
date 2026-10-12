#!/sbin/sh
ui_print "- Installing MAA Android"
ui_print "- Device: ARCH=$ARCH IS64BIT=$IS64BIT API=$API"
if [ "$IS64BIT" != "true" ] || [ "$ARCH" != "arm64" ]; then
  ui_print "! This module supports arm64 only."
  abort "Unsupported architecture: $ARCH (is64bit=$IS64BIT)"
fi
mkdir -p /data/adb/maa/lib /data/adb/maa/resource /data/adb/maa/run
chcon -R u:object_r:magisk_file:s0 /data/adb/maa 2>/dev/null || true
mkdir -p /data/adb/maa/ocr-ncnn
cp -a "$MODPATH/common/ocr-ncnn/." /data/adb/maa/ocr-ncnn/
chmod -R 0755 /data/adb/maa/ocr-ncnn
cp -f "$MODPATH/common/libMaaNativeExt.so" /data/adb/maa/lib/libMaaNativeExt.so
chmod 0755 /data/adb/maa/lib/libMaaNativeExt.so
set_perm_recursive "$MODPATH/system/bin" 0 0 0755 0755
chcon u:object_r:system_file:s0 "$MODPATH/system/bin/maaweb" "$MODPATH/system/bin/maactl" 2>/dev/null || true
ui_print "- MAA Android installed. Console: http://<phone>:8790"
