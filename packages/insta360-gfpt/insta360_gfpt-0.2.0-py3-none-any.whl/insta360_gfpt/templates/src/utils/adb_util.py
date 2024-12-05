# _*_ coding:utf-8 _*_
import json
import os
import re
import time
import logging
import datetime
import traceback
import shutil
from loguru import logger
from adbutils import adb
import adbutils

lib_logging = logging.getLogger(os.path.basename(__file__))


def get_time():
    return datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S.%f')


def ref_time(time_str):
    return datetime.datetime.strptime(time_str, '%Y_%m_%d_%H_%M_%S.%f')


class Adb:

    def __init__(self, serial=None):
        '''
                登录adb
                :param serial:
                :return:
                '''
        self.cam_info = None
        self.d = None
        self.ptz_info = None
        self.sn = serial
        if serial:
            self.serial = serial
            self.d = adb.device(serial=serial)
            self.cam_info = self.get_vb_info()
        else:
            self.devices = self.get_devices()
            if len(self.devices) == 1:

                self.d = adb.device()
                self.sn = self.d.get_serialno()

            elif len(self.devices) == 0:
                logger.info("未发现连接设备！！")

            else:
                logger.info(f'有多个设备连接，请选择你的设备！ 设备有：{self.devices}')
        # logger.info(self.d)

    def is_boot_completed(self, tout=-1):
        if tout<0:
            boot_result = self.send_command("getprop sys.boot_completed")
            #boot_result = "1"
            if boot_result == "1":
                logger.info("启动完成")
                return True
            else:
                logger.debug("设备还没启动完成")
                return False
        else:
            now_time = datetime.datetime.now()
            while (datetime.datetime.now() - now_time).total_seconds() <= tout:
                boot_result = self.send_command("getprop sys.boot_completed")
                #boot_result = "1"
                if boot_result == "1":
                    logger.info("启动完成")
                    return True
                else:
                    logger.debug("设备还没启动完成")
                    time.sleep(1)
            return False
    def get_devices(self):
        '''
        获取设备列表
        :return:
        '''
        devices = []
        try:
            for d in adb.device_list():
                devices.append(d.serial)
            # logger.info(devices)
            return devices
        except:
            return devices

    def check_device(self, sn):
        """
        检测指定设备是否在线
        :param sn:
        :return:
        """
        try:
            devices = self.get_devices()
            if sn in devices:
                return True
            else:
                return False
        except:
            traceback.print_exc()
            return False

    def touch_reset_file(self):

        for i in range(3):
            self.send_command('touch /sdcard/reset.txt')
            self.send_command('echo "vb_reset test" > /sdcard/reset.txt')
            if not self.is_reset():
                return True
        return False

    def is_reset(self):
        res = self.send_command("cat /sdcard/reset.txt")
        if res and "vb_reset" in res:
            return False
        else:
            return True
    def wait_device_online(self, sn, time_out):

        s_time = datetime.datetime.now()
        while (datetime.datetime.now() - s_time).seconds <= time_out:
            res = self.check_device(sn)
            if res:
                logger.info(f"重连sn{sn}")
                self.login_adb(sn)
                return res
        return False

    def getDeviceAddress(self):
        if self.d:

            return self.d.get_serialno()
        else:
            self.login_adb()
            if self.d:
                return self.d.get_serialno()
            else:
                return None

    def format_mac(self, mac: str) -> str:
        mac = re.sub('[.:-]', '', mac).upper()  # remove delimiters and convert to lower case
        mac = ''.join(mac.split())  # remove whitespaces
        assert len(mac) == 12  # length should be now exactly 12 (eg. 008041aefd7e)
        assert mac.isalnum()  # should only contain letters and numbers
        # convert mac in canonical form (eg. 00:80:41:ae:fd:7e)
        mac = ":".join(["%s" % (mac[i:i + 2]) for i in range(0, 12, 2)])
        return mac

    def get_vb_info(self):
        vb_info = {"device_info": {}}
        try:
            ptz_info = self.get_ptz_info()
            vb_info["device_info"]["serial"] = self.send_command("rw_reservepartition r serialno", False)
            vb_info["device_info"]["uuid"] = vb_info["device_info"]["serial"] if "IAB" not in vb_info["device_info"]["serial"] else None
            vb_info["device_info"]["software"] = self.send_command('getprop ro.build.insta.version', False)
            vb_info["device_info"]["hardware"] = self.send_command('getprop vendor.insta360.hardware.version', False)
            vb_info["device_info"]["memory"] = self.get_memory()
            vb_info["device_info"]["bt_mac"] = self.format_mac(self.send_command("rw_reservepartition r btmac", False))
            vb_info["device_info"]["ptz_version"] = self.ptz_info["firmware_version"] if ptz_info else ""
            vb_info["device_info"]["ptz_uuid"] = self.ptz_info["uuid"] if ptz_info else ""
            logger.info(vb_info)
            return vb_info

        except:

            return None
    def get_ptz_info(self):
        ptz_info = {}
        # data = "ptz sn: INSWWYYNPTZXXX uuid: 3635345433500EFF0C76FFFF firmware version: v1.0.8 hardware version: v1.0"
        res = self.send_command("ptz -V", False)
        logger.info(res)
        if res:
            result = re.search(r"ptz sn: (.*) uuid: (.*) firmware version: (.*) hardware version: (.*)", res)
            if result:
                ptz_info["sn"] = result[1]
                ptz_info["uuid"] = result[2]

                # 虚拟的数据
                # original_uuid = result[2]
                #
                # # 在这里直接修改 UUID 的后两位（可以手动设置新的后缀）
                # new_uuid_suffix = "AC"  # 这里直接修改为你想要的后两位
                # ptz_info["uuid"] = original_uuid[:-2] + new_uuid_suffix
                # logger.info(f"UUID 已修改为: {ptz_info['uuid']}")

                ptz_info["firmware_version"] = result[3]
                ptz_info["hardware_version"] = result[4]
                self.ptz_info = ptz_info
        self.send_command("ptz -S 0 0", False)
        return ptz_info



    def get_memory(self):
        for i in range(3):
            res = self.send_command("dumpsys mount", False)
            if res:
                result = re.search(r"total size: (\d+) ", res)
                if result:
                    return f"{int(result[1])/1000000000}GB"
            time.sleep(3)
        return "0GB"

    def get_ble_mac(self):
        return self.format_mac(self.send_command("rw_reservepartition r blemac", False))

    def login_adb(self, serial=None):

        '''
        登录adb
        :param serial:
        :return:
        '''
        if serial:
            self.d = adb.device(serial=serial)
            self.cam_info = self.get_vb_info()
            self.sn = serial

        else:
            devices = self.get_devices()
            if len(devices)==1:

                self.d = adb.device()
                # self.get_root()
                self.sn = self.d.get_serialno()
                self.cam_info = self.get_vb_info()

            elif len(devices) ==0:
                logger.info("未发现连接设备！！")
                return None

            else:
                logger.info(f'有多个设备连接，请选择你的设备！ 设备有：{devices}')
                return None
        logger.info(self.d)

        return self.d

    def get_log_for_tag(self, tag):
        self.send_command("logcat -c")
        cmd = f"logcat -s {tag}"
    def install_app(self, path):
        if self.d:

            res = self.d.install(path)
            return res
        else:
            logger.info("发送失败，未成功连接设备！")
            return False
    def send_broadcast(self, action, data:list=None, send_type=None):
        # 发送广播

        cmd = f"am broadcast -a {action}"
        logger.info(action)
        logger.info(data)
        if data and send_type is None:
            for d in data:
                cmd = f"{cmd} -e {d[0]} {d[1]}"
        elif data:
            for d in data:
                cmd = f"{cmd} -es {d[0]} {d[1]}"
        logger.info(f"cmd : {cmd}")
        if self.d:
            try:
                output = self.d.shell(cmd, timeout=120)
                logger.info(output)
                return output
            except adbutils.errors.AdbError as e:
                traceback.print_exc()
                logger.info(e)
                return False
        else:
            logger.info("发送失败，未成功连接设备！")
            return False
    def get_debug(self):

        debugger_result = self.send_command("getprop ro.debuggable")
        if debugger_result == "1":
            logger.info("debug 版本")
            return True
        else:
            logger.debug("user 版本")
            return False

    def get_root(self):
        # 获取vb root （手机不适应，慎用）
        if self.d and self.get_debug():

            logger.info("获取最高权限")
            udid = self.sn

            try:
                for i in range(2):
                    self.d.root()
                    time.sleep(0.1)
            except:
                pass
            logger.info(udid)
            res = self.wait_device_online(udid, 60)
            # os.system(f"adb -s {udid} remount")
            # self.send_command("setenforce 0")
            return res
        elif self.d and not self.get_debug():
            return True
        return False

        # logger.info(f"sn：{udid}，回连5s失败，root失败")

    def start_check_app(self, cmd):
        # 发送长时间回复的指令，最长300s

        if self.d:
            try:
                output = self.d.shell(cmd, timeout=300)

                logger.info(output)
                return output
            except adbutils.errors.AdbError as e:
                logger.info(e)
                return False
        else:
            logger.info("发送失败，未成功连接设备！")
            return False

    def send_command(self, cmd, output_print=True, timeout=5):
        '''
        adb 发指令
        :param cmd:
        :param serial:
        :return:
        '''


        if self.d:
            try:
                output = False
                for i in range(3):
                    output = self.d.shell(cmd, timeout=timeout)

                    if output_print :
                        logger.info(output)
                    if output != "closed":
                        return output
                    time.sleep(1)
                return output
            except adbutils.errors.AdbError as e:
                logger.info(e)
                return False
        else:
            logger.info("发送失败，未成功连接设备！")
            return False

    def start_app(self, activity):
        cmd = f"am start {activity}"
        self.send_command(cmd)

    def close_app(self, activity):
        cmd = f"am force-stop {activity}"
        self.send_command(cmd)

    def push_file(self, local_path, rempte_path):

        '''
        adb 推送文件
        :param local_path:
        :param rempte_path:
        :param serial:
        :return:
        '''


        if self.d:
            try:
                output = self.d.sync.push(local_path, rempte_path)
                logger.info(output)
                return output
            except adbutils.errors.AdbError as e:
                logger.info(e)
                return False
        else:
            logger.info("推送失败，未成功连接设备！")
            return False

    def pull_file(self, local_path, remote_path):

        '''
        adb拉取文件
        :param local_path:
        :param rempte_path:
        :param serial:
        :return:
        '''


        if self.d:
            try:
                if os.path.isdir(local_path):
                    # 删除文件夹
                    shutil.rmtree(local_path)

                output = self.d.sync.pull(remote_path, local_path)
                logger.info(output)
                if output == 0:
                    if os.path.isdir(local_path):
                        # 删除文件夹
                        shutil.rmtree(local_path)
                    # return False
                return output
            except adbutils.errors.AdbError as e:
                logger.info(e)
                return False
        else:
            logger.info("拉取失败，未成功连接设备！")
            return False

if __name__ == '__main__':
    adb = Adb()
    adb.d.keyevent(19)
    # adb.is_boot_completed()
    # dd = {"uuid": "uuid",
    #       "sensor_id1": "sensor_id1",
    #       "sensor_id2": "sensor_id2"}
    #
    # dd = json.dumps(dd)
    # logger.info(dd)
    # local_path = r"D:\code\test_data\LED1_TEST.sh"
    # remote_path = "/sdcard/LED1_TEST.sh"
    # adb.send_command("ls /mnt/vendor/persist")
    # udid = adb.d.get_serialno()

    # logger.info(udid)
    # adb.get_root()
    # s_time = datetime.datetime.now()
    # while((datetime.datetime.now() - s_time).seconds<=5):
    #     isOnline = adb.check_device(udid)
    #     if isOnline:
    #         adb.login_adb(udid)
    #         break
    # flag = False
    # res = adb.send_command("ls /mnt/media_rw", False)
    # if res != "":
    #     result = res.split(" ")
    #     logger.info(result)
    #     if len(result) >=2:
    #         for usb in result:
    #             adb.send_command(f"rm -rf /mnt/media_rw/{usb}/test.txt", False)
    #             res = adb.send_command(f"cat /mnt/media_rw/{usb}/test.txt", False)
    #
    #             adb.send_command(f'echo vb_test > /mnt/media_rw/{usb}/test.txt',False)
    #             rest = adb.send_command(f"cat /mnt/media_rw/{usb}/test.txt", False)
    #             if "vb_test" == rest:
    #                 flag = True
    #             else:
    #                 flag = False
    #                 logger.info("确认错误")
    # logger.info(flag)

    # res = adb.send_command("dumpsys mount")
    # logger.info(res)
    # if res:
    #     result = re.search(r"total size: (\d+) ", res)
    #     if result:
    #         logger.info(f"{int(result[1]) / 1000000000}MB")
    #     else:
    #         logger.info("0MB")
    # else:
    #     logger.info("xxx 0MB")
