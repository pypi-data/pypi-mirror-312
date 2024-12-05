import audioop
import ctypes
import datetime
import json
import os
import re
import socket
import subprocess
import threading
import time
import traceback
import wave
import numpy as np
from src.utils.adb_util import Adb
from loguru import logger

class api_vbTestTool(Adb):
    def __init__(self, vb_sn):
        super(api_vbTestTool, self).__init__(vb_sn)
        self.cam_info: dict = {}
        self.sn = vb_sn
        self.start_flag = False
        self.stop_flag = False
        self.auth_result = None
        self.get_root()
        # self.get_device_info()



    def get_device_info(self):
        # self.get_root()
        logger.debug("rain_test, 获取vb_info")
        return self.get_vb_info()




    def get_factory_mode(self):


        action = "com.example.vb_testtool.getOldTestStatus"
        resp = self.send_broadcast(action)
        res = None
        get_result = self.send_command("cat /storage/emulated/0/test_result.json")
        try:
            result = json.loads(get_result)
            logger.info(result)
        except:
            traceback.print_exc()
            return None
        if result['oldTestStatus']:
            res = True
        if not result['oldTestStatus']:
            res = False
        logger.debug(f"是否在老化: {res}")
        return res



    def get_old_test_result(self):
        self.send_broadcast("com.example.vb_testtool.oldTestStatus")
        for i in range(3):
            get_result = self.send_command("cat /storage/emulated/0/test_result.json")
            try:
                # logger.info(get_result)
                result = json.loads(get_result)
                return result
            except:
                traceback.print_exc()
        return None


    def get_mic_test_result(self):
        get_result = self.send_command("cat /storage/emulated/0/test_result.json")
        try:
            result = json.loads(get_result)
        except:
            traceback.print_exc()
            return None
        return result
    def save_device_log(self, local_path):
        log_path = self.get_device_log_path()
        if log_path:
            result = self.pull_file(local_path, log_path)
            return result
        else:
            return False
    def get_device_log_path(self):
        get_result = self.send_command("cat /storage/emulated/0/test_result.json")
        try:
            result = json.loads(get_result)
            if result["logPath"] != "null":
                return result["logPath"]
            else:
                return None
        except:
            traceback.print_exc()
            return None

    def get_len_pos(self):
        logpath = self.get_device_log_path()
        if logpath:
            result = self.send_command(f'cat {logpath} | grep "FULL Sweep AF ENDs here - success"')
            if not result:
                return False
            result = result.split("\n")
            for res in result:
                re_result = re.search(r"FULL Sweep AF ENDs here - success, Lens pos: (\d+) next_pos: (\d+)", res)

                if re_result:
                    logger.info("正则到了！！")
                    if int(re_result[1]) != 0 and re_result[1] == re_result[2] and int(re_result[1]) != 399:
                        logger.info("AF确认成功")
                        len_pos = int(re_result[1])
                        next_pos = int(re_result[2])
                        return [len_pos, next_pos]
            return False
        else:
            return None
    def connect_bt(self, addr):
        result = self.send_broadcast("com.example.vb_testtool.connectBlueTooth", [["DEVICE_ADDRESS", addr]])
        rss = self.get_old_test_result()
        if rss:
            connect_result = rss['ConnectResult']
            return connect_result
        return False
    def disconnect_bt(self):
        result = self.send_broadcast("com.example.vb_testtool.disconnectBlueTooth")
        return result
    def set_product_serial(self, serial_number):
        rrr = self.send_command(f'rw_reservepartition w serialno "{serial_number}"', False)
        os.system(f"adb -s {self.sn} reboot")
        time.sleep(4)
        res = self.wait_device_online(serial_number, 80)
        # res = True
        return res

    def reset_info(self):
        self.send_command("rm -rf /data/local/tmp/test.txt")
        return True

    def open_hdmi(self):
        time.sleep(1)
        self.init_test_app()
        time.sleep(1)
        self.send_broadcast("com.example.vb_testtool.startHdmiIn")
    def disable_verity(self):
        os.system(f"adb -s {self.sn} disable-verity")
        os.system(f"adb -s {self.sn} reboot")
        os.system(f"adb wait-for-device")
    def remount_device(self):
        try:
            self.disable_verity()


            self.get_root()
            os.system(f"adb -s {self.sn} remount")
        except:
            traceback.print_exc()
            return False
    def open_AF_log(self):
        try:
            root = os.getcwd()
            txt = f"{root}\\tools\\test_data\\camxoverridesettings.txt"
            # os.system(f"adb -s {self.sn} disable-verity")
            # os.system(f"adb -s {self.sn} reboot")
            # time.sleep(1)
            # self.wait_device_online(self.sn, 40)
            self.get_root()
            # os.system(f"adb -s {self.sn} remount")
            self.push_file(txt, "/vendor/etc/camera/camxoverridesettings.txt")
            # self.send_command("setenforce 0")
            os.system(f"adb -s {self.sn} reboot")
            time.sleep(1)
            self.wait_device_online(self.sn, 60)
            self.get_root()
            # os.system(f"adb -s {self.sn} remount")
            return True
        except:
            traceback.print_exc()
            return False
    def close_bt_protect(self):
        try:
            root = os.getcwd()
            txt = f"{root}\\tools\\test_data\\test.txt"
            # os.system(f"adb -s {self.sn} disable-verity")
            # os.system(f"adb -s {self.sn} reboot")
            # time.sleep(1)
            # self.wait_device_online(self.sn, 40)
            self.get_root()
            # os.system(f"adb -s {self.sn} remount")
            self.push_file(txt, "/data/local/tmp/test.txt")
            self.send_command("sync")
            self.send_command("sync")
            self.send_command("sync")
            # self.send_command("setenforce 0")
            # os.system(f"adb -s {self.sn} reboot")
            # time.sleep(1)
            # self.wait_device_online(self.sn, 60)
            # self.get_root()
            # os.system(f"adb -s {self.sn} remount")
            return True
        except:
            traceback.print_exc()
            return False


    def iperf_tx_stop(self):
        cmd = "ps -ef | grep iperf | grep -v grep | awk '{print $2}' | xargs -I {} kill -9 {}"
        output = self.send_command(cmd)
        self.send_command("svc wifi disable")
        if "Killed" in output:
            return True
        return output

    def get_gateway_address(self):
        host_name = socket.gethostname()  # 获取本机的主机名
        ip_address = socket.gethostbyname(host_name)  # 根据主机名获取对应的IPv4地址

        return ip_address
        # wifi_route = self.send_command("ip route list table 0")
        # def_regularity = re.compile(r'default via(.*?)dev')
        # try:
        #     def_regularity_list = def_regularity.findall(wifi_route)
        #     if len(def_regularity_list) != 0:
        #         gateway_address = def_regularity_list[0].strip()
        #         return gateway_address
        # except:
        #     return None
        # return None
    def iperf_tx_start(self, duration):
        server_ip = self.get_gateway_address()

        if not server_ip:
            return ""
        cmd = f"/data/iperf -c {server_ip} -p 5001 -t {str(duration)} -i 1 -f Mbytes"
        logger.info(f"iperf指令：{cmd}")
        resp = self.start_check_app(cmd)
        if resp and "Connection refused" in str(resp):
            logger.error("iperf连接失败")
            return None
        # resp = self.calc_perf_bw(output)
        return resp
    def connect_wifi(self, ssid, pwd):
        self.send_command("svc wifi enable")
        time.sleep(1)
        res = self.send_broadcast("com.example.vb_testtool.connectWifi", [["SSID", f"{ssid}"], ["PASSWORD", f"{pwd}"]])
        return res
    def scran_bt(self,addr, bt_device, count=0):

        for i in range(count):
            self.send_broadcast("com.example.vb_testtool.scanForMac", [["DEVICE_ADDRESS", addr]])
            time.sleep(10)
            scanFlag = True
            now_time = datetime.datetime.now()
            retry_flag = False
            while scanFlag:
                res = self.get_old_test_result()
                if res:
                    scanFlag = res['ScanFlag']
                    bt_device.scan_result = res['scanResult']
                if (datetime.datetime.now() - now_time).seconds >=10 and scanFlag:
                    if not retry_flag:
                        self.init_test_app()
                        self.send_broadcast("com.example.vb_testtool.scanForMac", [["DEVICE_ADDRESS", addr]])
                        retry_flag = True
                if (datetime.datetime.now() - now_time).seconds >=30 and scanFlag:
                    return bt_device
                time.sleep(1)
            rss = self.get_old_test_result()
            if rss:
                bt_device.scan_result = rss['scanResult']
                bt_device.addr = rss['mac']
                if rss['rssi'] != 0:
                    bt_device.rssi.append(rss['rssi'])

                if bt_device.scan_result:
                    break
            # time.sleep(6)

        return bt_device

    def check_auth_result(self):
        res = self.check_adb_device_authorized()

        return res

    def clear_auth(self):
        res = self.get_root()
        res = self.send_command("cd /mnt/vendor/persist/; rm -rf sst_path/; ls /mnt/vendor/persist/")
        logger.info(f"persist ls : {res}")
        res = self.send_command("cd /data/local/tmp/; rm -rf *; ls /data/local/tmp/")
        logger.info(f"/data/local/tmp/ ls : {res}")
        if res == "":
            return True
        else:
            return False


    def binding_ble(self, ble_mac):
        rrr = self.send_command(f'rw_reservepartition w blemac "{ble_mac}"', False)
        os.system(f"adb -s {self.sn} reboot")
        time.sleep(2)
        res = self.wait_device_online(self.sn, 60)
        if self.format_mac(ble_mac) == self.get_ble_mac():
            return True
        else:
            return False

    def auth_device(self):
        try:
            ress = self.clear_auth()
            if ress:
                dll = self.init_auth_pc()
                self.start_flag = True
                t = threading.Thread(target=self.start_auth_pc, args=[dll, ])
                t.start()
                time.sleep(2)
                logger.info("启动会议机鉴权程序")
                res = self.start_auth_app()
                self.start_flag = False
                if dll.is_device_burning() != 0:
                    logger.info(type(dll.is_device_burning()))
                    logger.info("关闭设备连接")
                    dll.ls_oem_dev_stop()
                logger.info("关闭鉴权方法")

                dll.iot_sam_stop()

                logger.info(f"auth_result: {self.auth_result}")
                now_time = datetime.datetime.now()
                while (not self.stop_flag and (datetime.datetime.now() - now_time) < 30):
                    logger.info("等待pc鉴权方法停止")
                    time.sleep(2)
                self.stop_flag = True
                # self.send_command("cd /data/local/tmp/; rm -rf *; ls /data/local/tmp/")
                self.send_command("chmod -R 777 /mnt/vendor/persist/sst_path/")
                return self.auth_result

            else:
                logger.info("初始化失败")
                return False
        except:
            traceback.print_exc()
            return False

    def start_auth_app(self):
        push_res = self.push_device_armeabi()
        if push_res:
            logger.info("启动会议机程序")
            res = self.start_check_app("cd /data/local/tmp/; ./auth_device")
            logger.info("启动上位机鉴权验证程序")
            res = self.start_check_app("cd /data/local/tmp/; ./auth_device_offline")
            logger.info("判断是否鉴权")
            if res:
                if "App Authorized!" in res:
                    self.auth_result = True
                else:
                    self.auth_result = False
            return res
        else:
            return False

    def install_test_app(self):
        try:
            root = os.getcwd()
            apk_path = f"{root}\\tools\\apk\\vb_testtool.apk"
            self.install_app(apk_path)
            self.push_scripy()
            return True
        except:
            traceback.print_exc()
            return False
    def push_iperf_app(self):
        try:
            root = os.getcwd()
            apk_path = f"{root}\\tools\\iperf\\iperf"
            remote_path = "/data/iperf"
            self.push_file(apk_path, remote_path)
            self.send_command("chmod +x /data/iperf")
            return True
        except:
            traceback.print_exc()
            return False
    def init_auth_pc(self):
        root = os.getcwd()
        cfg_file = f"{root}\\tools\\cfg".encode("utf-8")
        tmp_file = f"{root}\\tools\\tmp".encode("utf-8")
        logger.info(f"{root}\\tools\\lib\\lib\\Release\\libIotSam.dll")
        cfg_folder = ctypes.create_string_buffer(cfg_file)  # 这个很重要否则只会传一个字符
        tmp_folder = ctypes.create_string_buffer(tmp_file)

        dll = ctypes.windll.LoadLibrary(f"{root}\\tools\\lib\\lib\\Release\\libIotSam.dll")
        sn = ctypes.create_string_buffer(self.sn.encode("utf-8"))
        dll.iot_set_adb_serial(sn)
        dll.iot_set_pc_cfg_folder(cfg_folder)
        dll.iot_set_pc_tmp_folder(tmp_folder)
        dll.iot_sam_init()
        return dll

    def start_auth_pc(self, dll: init_auth_pc):

        while self.start_flag:
            logger.info("循环")
            dll.iot_sam_process()
            result = self.check_auth_result()
            self.auth_result = result
            if result:
                break

        self.stop_flag = True

    def led_test(self):
        for i in range(1,5):
            self.send_command(f"echo {i} > /sys/devices/platform/soc/984000.i2c/i2c-0/0-0035/leds/led_red/effect")
            self.send_command(f"echo {i} > /sys/devices/platform/soc/984000.i2c/i2c-0/0-0034/leds/led_blue/effect")
            time.sleep(1)
        self.send_command(f"echo 4 > /sys/devices/platform/soc/984000.i2c/i2c-0/0-0035/leds/led_red/effect")
        self.send_command(f"echo 4 > /sys/devices/platform/soc/984000.i2c/i2c-0/0-0034/leds/led_blue/effect")

    def lan_test(self):

        self.send_command("svc wifi disable", False)

        wifi_route = self.send_command("ip route list table 0", False)
        def_regularity = re.compile(r'default via(.*?)dev')
        def_regularity_list = def_regularity.findall(wifi_route)
        if len(def_regularity_list) != 0:
            gateway_address = def_regularity_list[0].strip()
            ping_gateway_result = self.send_command("ping -c 5 {}".format(gateway_address), False)
            self.send_command("svc wifi enable", False)
            if ping_gateway_result and "packets transmitted" not in ping_gateway_result:
                return False

            elif ping_gateway_result:
                return True
            else:
                return False
        else:
            self.send_command("svc wifi enable", False)
            return False
    def stop_auth_pc(self, dll: init_auth_pc):

        dll.iot_sam_stop()

    def push_device_armeabi(self):

        data_name = ["auth_device", "auth_device_offline", "burn_auth_board.sh"]
        try:
            root = os.getcwd()
            for name in data_name:
                local_path = f"{root}\\tools\\armeabi\\{name}"
                remote_path = f"/data/local/tmp/{name}"
                self.push_file(local_path, remote_path)
            self.send_command("export LD_LIBRARY_PATH=/data/local/tmp/")
            self.send_command("chmod +x /data/local/tmp/auth_device")
            self.send_command("chmod +x /data/local/tmp/auth_device_offline")

            return True

        except Exception as e:
            logger.info(e)
            return False
    def usb_test(self):
        flag = False
        self.send_command("setprop persist.sys.KEY_WORD_USB_DEBUG false")
        res = self.send_command("ls /mnt/media_rw")
        if res != "":
            result = res.split(" ")
            logger.info(result)
            logger.info(len(result))
            if len(result) >= 2:
                for usb in result:
                    self.send_command(f"rm -rf /mnt/media_rw/{usb}/test.txt", False)
                    res = self.send_command(f"cat /mnt/media_rw/{usb}/test.txt")

                    self.send_command(f'echo vb_test > /mnt/media_rw/{usb}/test.txt', False)
                    rest = self.send_command(f"cat /mnt/media_rw/{usb}/test.txt")
                    if "vb_test" == rest:
                        flag = True
                    else:
                        flag = False
                        logger.info("确认错误")
            else:
                logger.info(f"只插入了{len(result)}个接口")
                flag = False
        else:
            logger.info("没有识别到一个usb接口有插入")
        self.send_command("setprop persist.sys.KEY_WORD_USB_DEBUG true")
        return flag
    def check_target_folder_exists(self):

        res = self.send_command("ls /mnt/vendor/persist")
        if "sst_path" in res:
            return True
        else:
            return False

    def check_license_folder_exists(self):

        res = self.send_command("ls /mnt/vendor/persist")
        if "sk_license" in res:
            return True
        else:
            return False

    def check_tencent_folder_exists(self):

        res = self.send_command("ls /mnt/vendor/persist")
        if "Tencent" in res:
            return True
        else:
            return False

    def check_adb_device_authorized(self):
        # 检查license是否为空
        license_res = self.check_license_folder_exists()
        if not license_res:
            return False
        res = self.send_command("cat ls /mnt/vendor/persist/sk_license/license")
        if "license=" not in res and len(res) < 14+8:
            return False
        tencent_res = self.check_tencent_folder_exists()
        if not tencent_res:
            return False
        res = self.send_command("ls /mnt/vendor/persist/Tencent")
        if len(res) < 3:
            return False
        return True
        # 检查腾讯证书文件存在
        # check_res = self.check_target_folder_exists()
        # if check_res:
        #     res = self.send_command("ls /mnt/vendor/persist/sst_path")
        #     if len(res) > 5:
        #         return True
        #     else:
        #         return False
        # return False
    def mic_test(self, test_time=5):
        self.send_command("mkdir /storage/emulated/0/record_test")
        self.send_command('tinymix "MultiMedia1 Mixer PRI_TDM_TX_0" 1')
        res = self.send_command(f'tinycap /storage/emulated/0/record_test/test.wav -c 16 -r 48000 -b 16 -T {test_time}', timeout=test_time+5)
        return res

    def get_wav_info(self, path):
        # 获取wav音频数据
        f = wave.open(path, "rb")
        params = f.getparams()
        nchannels, sampwidth, framerate, nframes = params[:4]
        logger.info(f"声道数={nchannels}\n量化位数={sampwidth}, \n采样频率={framerate}, \n采样点数={nframes}")
        return nchannels

    def is_wav_ok(self, path):
        #确认声道是否正常
        with wave.open(path, 'rb') as wf:
            # 获取声道数和采样宽度
            num_channels = wf.getnchannels()
            sample_width = wf.getsampwidth()
            # 检查各个声道状态
            for i in range(num_channels):
                wf.setpos(0)
                channel_samples = np.frombuffer(wf.readframes(
                    wf.getnframes()), dtype=np.int16)[i::num_channels]
                if channel_samples.max() == 0 and channel_samples.min() == 0:
                    if i+1 <= 2:
                        #前两个声道为电子声道不做处理
                        logger.info('第{}个声道损坏,属于虚拟声道，跳过'.format(i + 1))
                        continue
                    logger.info('第{}个声道损坏'.format(i + 1))
                    return i+1
                else:
                    logger.info('第{}个声道正常'.format(i + 1))
        return True
    def is_wav_hassound(self, path):
        with wave.open(path, "rb") as wav:
            # 获取文件的格式信息
            params = wav.getparams()
            # 确定每个采样点的大小（字节）
            sample_size = params[1]
            # 读取文件中的所有数据
            startframe = int(0.1 * params[2])  # 开始帧数
            wav.setpos(startframe)  # 将位置设置到开始帧
            data = wav.readframes(params[3] - startframe)  # 使用rms函数计算音频信号的均方根（RMS）幅度
        rms = audioop.rms(data, sample_size)  # 如果rms值大于0，则表示有声音
        logger.info(rms)
        if rms > 0:
            logger.info("此wav文件有声音")
            return True
        else:
            logger.info("此wav文件没有声音")
            return False

    def is_pcm_has_sound(self, path, threshold=0.1):
        with wave.open(path, 'rb') as wav:
            num_channels = wav.getnchannels()
            sample_width = wav.getsampwidth()
            frames = wav.getnframes()
            pcm_data = wav.readframes(frames)
            pcm_array = np.frombuffer(pcm_data, dtype=np.int16)
            for channel in range(num_channels):
                channel_data = pcm_array[channel::num_channels]
                average_amplitude = np.abs(channel_data).mean() / (2 ** (8 * sample_width - 1))
                if average_amplitude > threshold:
                    logger.info("此pcm有声")
                    return True
            logger.info("此PCM无声")
            return False

    def init_socket(self):
        if self.d:
            self.get_root()
            # self.send_command("pm disable-user com.insta360.vb.setupwizard")
            return True
        else:
            res = self.login_adb(self.sn)

            return res

    def start_camera(self, camera_id=0):
        self.init_camera()
        self.stop_test_app()
        time.sleep(1)
        self.start_test_app()
        time.sleep(2)
        self.send_broadcast(f"com.example.vb_testtool.startCamera{camera_id}")

    def dual_take_photo(self, remote_path="/storage/emulated/0/near"):
        self.init_camera()
        self.stop_test_app()
        time.sleep(1)
        self.start_test_app()
        time.sleep(1)
        self.send_broadcast("com.example.vb_testtool.setDualOption",
                            [["isSupportRaw", "OFF"], ["isAemode", "ON"], ["logicPicFile", remote_path + "_maincam.jpg"], ["subPicFile", remote_path + "_subcam.jpg"]])
        self.send_broadcast(f"com.example.vb_testtool.startDualCamera")
        time.sleep(3)
        self.d.keyevent(19)
        time.sleep(1)
        self.d.keyevent(19)
        logger.info("该回去了")
        time.sleep(10)
        return True

    def take_photo(self, camera_id=0, remote_path="/storage/emulated/0/near_1.dng", local_path="", station="default", is_reopen=True):
        if camera_id == 0:
            self.send_broadcast("com.example.vb_testtool.setDngFile", [["dng_file", remote_path + ".dng"], ["jpg_file", remote_path+ ".jpg"]])
        else:
            self.send_broadcast("com.example.vb_testtool.setDngFile",
                                [["dng_file", remote_path + ".raw"], ["jpg_file", remote_path + ".jpg"]])
        if is_reopen:
            self.init_camera()
            self.stop_test_app()
            time.sleep(1)
            self.start_test_app()
            time.sleep(2)

            logger.info(f"拍照station是:  {station}")
            if station == "default":
                if camera_id == 0:
                    self.send_broadcast("com.example.vb_testtool.setDngFile",
                                        [["dng_file", remote_path + ".dng"], ["jpg_file", remote_path + ".jpg"]])
                else:
                    self.send_broadcast("com.example.vb_testtool.setDngFile",
                                        [["dng_file", remote_path + ".raw"], ["jpg_file", remote_path + ".jpg"]])
                self.send_broadcast(f"com.example.vb_testtool.startCamera{camera_id}")
            else:
                self.send_broadcast(f"com.example.vb_testtool.setOption", [["AE_MODE", "ON"]])
                self.send_broadcast(f"com.example.vb_testtool.startCamera{camera_id}JPG")
            time.sleep(6)
        self.d.keyevent(19)
        time.sleep(1)
        self.d.keyevent(19)
        logger.info("该回去了")
        time.sleep(2)
        return True
    def init_app_socket_con(self):
        self.cam_info = self.get_device_info()

        return self.cam_info

    def init_test_app(self):
        self.stop_test_app()
        time.sleep(1)
        self.start_test_app()
        time.sleep(2)

    def push_scripy(self):
        self.send_command("mkdir /sdcard/test_data")
        data_name = ["LED1_TEST.sh", "LED2_TEST.sh", "test.mp3"]
        try:
            for name in data_name:
                local_path = f"./test_data/{name}"
                remote_path = f"/sdcard/test_data/{name}"
                self.push_file(local_path, remote_path)
            return True

        except Exception as e:
            logger.info(e)
            return False

    def check_old_test_data(self):
        check_cmd = "cd sdcard/ ; ls"
        for i in range(3):
            res = self.send_command(check_cmd)
            if "test_data" not in res:
                self.send_command("cd sdcard/ ; mkdir test_data")
                res2 = self.push_scripy()
                if res2:
                    return res2
            else:
                return True
        return False
    def init_camera(self):
        # self.send_command("setenforce 0")
        self.send_command("setprop vendor.select.mulicamera 0")
        # self.send_command("setprop insta.debug.st_force_dual false")
        self.send_command("setprop vendor.multicamera.tracking.visualize false")

    def start_test_app(self):
        activity = "com.example.vb_testtool/.MainActivity"
        self.start_app(activity)
    def restart_test_app(self):
        activity = "com.example.vb_testtool/.MainActivity"
        self.close_app(activity)
        time.sleep(2)
        self.start_test_app()
        time.sleep(2)
    def stop_test_app(self):
        activity = "com.example.vb_testtool"
        self.close_app(activity)
        # self.send_command("setenforce 0")
        # self.send_command("setprop vendor.select.mulicamera 0")
        # self.send_command("setprop insta.debug.st_force_dual false")
        # self.send_command("setprop vendor.multicamera.tracking.visualize false")

    def start_old_test(self, test_time):
        self.stop_test_app()
        time.sleep(2)
        # self.send_command("setenforce 0")
        # self.send_command("setprop vendor.select.mulicamera 1")
        # self.send_command("setprop insta.debug.st_force_dual true")
        # self.send_command("setprop vendor.multicamera.tracking.visualize true")

        res = self.check_old_test_data()
        time.sleep(2)
        if res:

            self.start_test_app()
            time.sleep(2)
            action = "com.example.vb_testtool.startOldTest"
            arg = ["test_time", f"{test_time}"]
            res = self.send_broadcast(action, [arg])
            self.send_command("getprop")
            return res
        else:
            logger.info("未能连接设备")

    def close_old_test(self):
        action = "com.example.vb_testtool.closeOldTest"
        res = self.send_broadcast(action)
        return res
if __name__ == '__main__':
    import wave
    import numpy as np

    with wave.open(r'D:\code\gfpt_android\测试结果\半成品测试\音频\20230626\ZTS30S1100GT\test.wav', 'rb') as wf:
        # 获取声道数和采样宽度
        num_channels = wf.getnchannels()
        sample_width = wf.getsampwidth()
        # 检查各个声道状态
        for i in range(num_channels):
            wf.setpos(0)
            channel_samples = np.frombuffer(wf.readframes(
                wf.getnframes()), dtype=np.int16)[i::num_channels]
            if channel_samples.max() == 0 and channel_samples.min() == 0:
                print('第{}个声道损坏'.format(i + 1))
            else:
                print('第{}个声道正常'.format(i + 1))