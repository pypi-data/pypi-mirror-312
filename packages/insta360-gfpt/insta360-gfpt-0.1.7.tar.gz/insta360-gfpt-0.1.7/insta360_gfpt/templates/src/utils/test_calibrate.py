import time

from adb_util import Adb
class Calibrate:
    def __init__(self):
        self.adb = Adb()
        self.device = self.adb.get_devices()
        self.adb.get_root()

    def get_af_table(self):
        """
        获取标定对照表
        :return:
        """
        res =self.adb.send_command("cat /data/local/camera/af_dac_table.txt", False)
        print(res)

    def get_info(self):
        """
        获取设备信息
        :return:
        """
        res = self.adb.get_vb_info()
        print(res)

    def open_app(self):
        self.adb.start_app("com.example.vb_testtool/.MainActivity")

    def close_app(self):
        self.adb.close_app("com.example.vb_testtool")

    def open_dual_acitvity(self, remote_path="/sdcard/image"):
        self.adb.send_command("setprop vendor.select.mulicamera 0")
        self.adb.send_command("setprop vendor.multicamera.tracking.visualize false")
        # self.adb.send_command("setprop vendor.debug.camera.af.manual 1")
        self.close_app()
        time.sleep(2)
        self.open_app()
        time.sleep(2)
        self.adb.send_broadcast("com.example.vb_testtool.setDualOption",
                            [["isSupportRaw", "OFF"], ["isAemode", "ON"],
                             ["logicPicFile", remote_path + "_maincam.jpg"],
                             ["subPicFile", remote_path + "_subcam.jpg"]])
        self.adb.send_broadcast(f"com.example.vb_testtool.startDualCamera")

    def take_photo(self):
        self.adb.d.keyevent(19)

    def pull_file(self,  local_path, remote_path):
        self.adb.pull_file(local_path, remote_path)

    def set_len(self, lens):
        print(f"set lens {lens}")
        if(int(lens)<0):
            print("未设置正确的lens")
            return False
        self.adb.send_command("setprop vendor.debug.camera.af.manual 2")
        self.adb.send_command(f"setprop vendor.debug.camera.af.ctrl.lenspos {lens}")

    def get_len(self):
        self.adb.send_command("setprop vendor.debug.camera.af.manual 0")
        self.adb.send_command(f"setprop vendor.debug.camera.af.fullsweep 1")
        time.sleep(5)
        result = False
        lens = -1
        while not result:
            get_res = self.adb.send_command(f"getprop persist.vendor.fullscan.finallens")
            if type(get_res) is bool:
                print("wait get lens")
                time.sleep(1)
                continue
            if len(get_res) <=1:
                print("get lens is mistake")
                time.sleep(1)
                continue
            else:
                lens = self.adb.send_command(f"getprop persist.vendor.fullscan.finallens")
                print(lens)
                print(len(lens))
                time.sleep(1)
                break
        return lens

if __name__ == '__main__':
    remote_path = "/sdcard/image"
    main_remote_path = "/sdcard/image_maincam.jpg"
    main_local_path = "image_maincam.jpg"
    sub_remote_path = "/sdcard/image_subcam.jpg"
    sub_local_path = "image_subcam.jpg"
    test = Calibrate()
    test.get_af_table()
    test.get_info()
    test.open_dual_acitvity(remote_path)
    lens = test.get_len() #需要新固件支持，或者给你推so库
    test.set_len(lens)
    time.sleep(10)
    test.take_photo()
    test.pull_file(main_local_path, main_remote_path)
    test.pull_file(sub_local_path, sub_remote_path)