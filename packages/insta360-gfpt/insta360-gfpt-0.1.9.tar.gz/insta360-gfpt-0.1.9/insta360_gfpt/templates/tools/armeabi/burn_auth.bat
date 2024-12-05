
set adb_serial=b0282c26

adb -s %adb_serial% push auth_device         /data/local/tmp/
adb -s %adb_serial% push auth_device_offline /data/local/tmp/

adb -s %adb_serial% push libAuthDeviceHal.so /vendor/lib/

adb -s %adb_serial% shell rm -rf /mnt/vendor/persist/sst_path

adb -s %adb_serial% shell < burn_auth_board.sh


adb -s %adb_serial% shell chmod -R 777 /mnt/vendor/persist/sst_path
