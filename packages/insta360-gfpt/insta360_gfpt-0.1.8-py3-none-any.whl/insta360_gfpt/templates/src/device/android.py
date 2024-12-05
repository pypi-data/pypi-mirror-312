import datetime
import os
import time
from enum import Enum
from src.device.fw_api.api_vbTestTool import api_vbTestTool
import rawpy
import imageio
import numpy as np
from src.utils.logger import logger
from src.utils.mipiraw2raw import mipiraw2raw
from src.utils.network import ResultHandle


class Android(object):
    """docstring for Camera"""

    class ApiCode(Enum):
        SUCCESS = 'success'
        FAIL = 'fail'

    class ErrorMsg(Enum):
        EXCEPTION = '相机返回异常'
        TIMEOUT = '相机响应超时'
        START_CAPTURE_FAIL = '开启拍照指令失败'
        STOP_CAPTURE_FAIL = '停止拍摄指令失败'
        START_RECORD_FAIL = '开始录像指令失败'
        STOP_RECORD_FAIL = '停止拍摄指令失败'
        START_BUTTON_FAIL = '开启按键测试指令失败'
        WAIT_BUTTON_RESPONSE = '等待按键的反馈'
        STOP_BUTTON_FAIL = '停止按键测试指令失败'
        START_LCD_FAIL = '开启屏幕颜色测试指令失败'
        STOP_LCD_FAIL = '停止屏幕颜色测试指令失败'
        START_TP_FAIL = '开启屏幕触摸测试指令失败'
        STOP_TP_FAIL = '停止屏幕触摸测试指令失败'
        START_LED_FAIL = '开启led测试指令失败'
        STOP_LED_FAIL = '停止led测试指令失败'
        START_OLED_FAIL = '开启oled测试指令失败'
        STOP_OLED_FAIL = '停止oled测试指令失败'
        START_G_SENSOR_FAIL = '开启g-sensor测试指令失败'
        STOP_G_SENSOR_FAIL = '停止g-sensor测试指令失败'
        START_WIFI_FAIL = '打开wifi指令失败'
        STOP_WIFI_FAIL = '关闭wifi指令失败'
        SET_WIFI_FREQ_FAIL = '设置wifi频段指令失败'
        START_IPERFTX_FAIL = '开启相机的iperf性能工具指令失败'
        STOP_IPERFTX_FAIL = '停止相机的iperf性能工具指令失败'
        BT_WAKEUP_FAIL = '开启蓝牙唤醒测试请求失败'
        NOT_BLE_WAKEUP_FAIL = '设备不是通过蓝牙唤醒的'
        GET_FACTORY_MODE_FAIL = '获取设备模式失败'
        SET_FACTORY_MODE_FAIL = '设置设备模式失败'
        SET_AGE_CONFIG_FAIL = '设置老化参数失败'
        AGE_POWER_OFF_FAIL = '老化关机失败'
        AGE_RESULT_FAIL = '老化关机失败'
        RESET_AGE_RESULT_FAIL = '清除老化结果失败'

    def __init__(self, sn=None, usb_device=None, product=None, config=None):
        self.sn = sn
        self.uuid = usb_device
        self.api: api_vbTestTool = api_vbTestTool(self.sn)
        self.product = product
        self.device_info = []
        self._config = config
        self.battery = None
        self.is_sensor_binder = False
        self.is_sn_binding = False
        self.white_balance_error_code = {0: "标定完成", 10: "文件出错打开文件失败", 11: "内存申请失败", 20: "曝光亮度错误",
                                        21: "边角超出阈值", 22: "找中心失败，请检查是否有光源中心", 30: "曝光错误",
                                        31: "计算结果超出阈值", 32: "计算失败", 33: "OTP写入失败，请重新校正",
                                        34: "OTP已写入，已校正", 40: "坏点超出阈值", 41: "漏光", 129: "拍照失败",
                                        130: "白平衡校正数据写到文件失败"}

    def connect(self):
        self.api.init_socket()
        self.api.init_app_socket_con()
        self.connecting = True
        if self.api.cam_info:
            self.uuid = self.query_uuid_from_sn()
            self.api.cam_info['device_info']['uuid'] = self.uuid
            self.set_sync_time()
            logger.info(f"连接设备: {self.uuid} 成功")
        else:
            logger.info(f"连接设备失败")

    def is_boot_completed(self):
        return self.api.is_boot_completed()

    def get_len_pos(self):
        return self.api.get_len_pos()
    def wait_boot_completed(self, time_out):
        s_time = datetime.datetime.now()
        while (datetime.datetime.now() - s_time).seconds <= time_out:
            res = self.is_boot_completed()
            if res:
                return res
        return False

    def led_test(self):
        self.api.led_test()

    def disconnect(self):

        self.connecting = False
        logger.info(f"断开 {self.uuid} 连接成功")

    def push_device_armeabi(self):
        self.api.push_device_armeabi()

    def close_bt_protect(self):
        return self.api.close_bt_protect()
    def disconnect_bt(self):
        return self.api.disconnect_bt()
    def get_camera_info(self):
        # UUID Sensor 固件版本 硬件版本
        # 序列号 镜头类型 音频码 相机电量
        # 相机类型
        logger.debug(f"相机设备信息：{self.api.cam_info}")
        if not self.api.cam_info or not self.api.cam_info.get('device_info', {}):
            logger.error(f"相机信息获取失败")
            return []
        self.api.get_vb_info()
        # self.sn = self.api.cam_info['device_info']['serial']
        self.uuid = self.query_uuid_from_sn()
        self.api.cam_info['device_info']['uuid'] = self.uuid
        self.device_info = [
            {"name": "UUID:", "info": self.api.cam_info['device_info']['uuid']},
            # {"name": "UUID:", "info": "123456789123"},
            {"name": "固件版本:", "info": self.api.cam_info['device_info']['software']},
            {"name": "硬件版本:", "info": self.api.cam_info['device_info']['hardware']},
            {"name": "序列号:", "info": self.api.cam_info['device_info']['serial']},
            {"name": "内存:", "info": self.api.cam_info['device_info']['memory']},
            {"name": "ptz_version:", "info": self.api.cam_info['device_info']['ptz_version']},
            {"name": "ptz_uuid:", "info": self.api.cam_info['device_info']['ptz_uuid']}
        ]

        rrr = self.query_sensor_binding()
        if rrr:
            sensor_id1 = {"name": "sensor_id1:", "info": rrr[0]}
            sensor_id2 = {"name": "sensor_id2:", "info": rrr[1]}
            sensor_flag1 = False
            sensor_flag2 = False
            for i in range(len(self.device_info)):
                if self.device_info[i].get("sensor_id1"):
                    self.device_info[i] = sensor_id1
                    sensor_flag1 = True
                if self.device_info[i].get("sensor_id2"):
                    self.device_info[i] = sensor_id2
                    sensor_flag2 = True
            if not sensor_flag1:
                self.device_info.append(sensor_id1)
            if not sensor_flag2:
                self.device_info.append(sensor_id2)
        else:
            logger.info("没有查询到绑定信息")
        logger.info(f"111设备信息: {self.device_info}")
        return self.device_info


    def connect_wifi(self, ssid, pwd):
        self.api.restart_test_app()
        return self.api.connect_wifi(ssid, pwd)

    def connect_bt(self, addr):
        return self.api.connect_bt(addr)

    def scran_bt(self, addr, bt_device, count=1):
        return self.api.scran_bt(addr, bt_device, count)

    def set_sync_time(self, product=None):
        #  需要用到时注意修改

        pass
    def mic_test(self, test_time=5):
        return self.api.mic_test(test_time)

    def usb_test(self):
        return self.api.usb_test()
    def auth_device(self):
        self.api.send_command("sync")
        return self.api.auth_device()

    def binding_ble(self, ble_mac):
        return self.api.binding_ble(ble_mac)
    def dng2jpg(self, input_path, output_path, bright):
         # 打开DNG文件
        with rawpy.imread(input_path) as raw:
            # 转换为RGB图像
            if bright == 1:
                postprocess_params = {
                    "no_auto_bright": True,  # 手动控制亮度
                    "bright": 12,  # 增加亮度
                    "output_bps": 16,
                    "use_camera_wb": True,
                    "half_size": False,
                    "dcb_enhance": True,
                    "output_color": rawpy.ColorSpace.sRGB,
                }
            elif bright == 0:
                postprocess_params = {
                    "no_auto_bright": True,  # 手动控制亮度
                    "bright": 4,  # 增加亮度
                    "output_bps": 16,
                    "use_camera_wb": True,
                    "half_size": False,
                    "dcb_enhance": True,
                    "output_color": rawpy.ColorSpace.sRGB,
                }
            else:
                postprocess_params = {
                    "no_auto_bright": True,  # 手动控制亮度
                    "output_bps": 16,
                    "use_camera_wb": True,
                    "half_size": False,
                    "dcb_enhance": True,
                    "output_color": rawpy.ColorSpace.sRGB,
                }
            # 转换为RGB图像
            rgb_output = raw.postprocess(**postprocess_params)
            if rgb_output.dtype == np.uint16:
                # Scale the 16-bit image to 8-bit
                rgb_output = ((rgb_output / 65535) * 255).round().astype(np.uint8)

              # 保存为JPG文件
        imageio.imwrite(output_path, rgb_output)

    def query_sensor_binding(self):
        ptz_uuid = self.api.ptz_info["uuid"] if self.api.get_ptz_info() else ""
        if ptz_uuid.endswith("-3"):
            ptz_uuid = ptz_uuid[:-2]  # 去掉最后两个字符
        logger.info(f"查询云台UUID: {ptz_uuid}")
        handler = ResultHandle(self._config["config"])
        res = handler.query_uuid_sensor_id_binding(uuid=ptz_uuid)
        # if res:
        #     if ptz_uuid and ptz_uuid != "":
        #         if res["yt_uuid"] and res["yt_uuid"] != ptz_uuid:
        #             res = handler.unbinding_ptz_uuid(ptz_uuid=res["yt_uuid"], uuid=self.uuid)
        #             if res is not False:
        #                 res = handler.binding_ptz_uuid(ptz_uuid=ptz_uuid, uuid=self.uuid)
        #                 logger.info(res)
        #                 if res is not False:
        #                     logger.info("云台uuid已绑定")
        #                 else:
        #                     logger.info("云台uuid绑定失败")
        #             else:
        #                 logger.info(f"服务器云台uuid: {res['yt_uuid']}, 本机云台uuid: {ptz_uuid}")
        #                 logger.info("云台uuid解绑失败")
        #         elif not res["yt_uuid"]:
        #             res = handler.binding_ptz_uuid(ptz_uuid=ptz_uuid, uuid=self.uuid)
        #             logger.info(res)
        #             if res is not False:
        #                 logger.info("云台uuid已绑定")
        #             else:
        #                 logger.info("云台uuid绑定失败")
        #
        #         logger.info("云台uuid已绑定")
        #     else:
        #         logger.info("未获取到ptz_uuid")
        # else:
        #
        #     if ptz_uuid and ptz_uuid != "":
        #         res = handler.binding_ptz_uuid(ptz_uuid=ptz_uuid, uuid=self.uuid)
        #         logger.info(res)
        #         if res is not False:
        #             logger.info("ptz_uuid已绑定")
        #         else:
        #             logger.info("ptz_uuid未绑定")
        #     else:
        #         logger.info("未获取到ptz_uuid")
        # if ptz_uuid and ptz_uuid != "":
        #     res = handler.query_uuid_sensor_id_binding(uuid=ptz_uuid)
        # else:
        #     return None
        if res:
            # logger.info("sss"+res)
            return [res.get("major_sensor"), res.get("minor_sensor"), res.get("machine_uuid")]
        else:
            return res

    def query_uuid_from_sn(self):
        handler = ResultHandle(self._config["config"])
        res = handler.query_uuid_binding(sn=self.sn)
        if res:
            if res.get("uuid"):
                return res.get("uuid")
            else:
                return self.sn
        else:
            return self.sn
    def open_camera(self):

        self.api.stop_test_app()
        time.sleep(1)
        self.api.start_test_app()
        time.sleep(3)
        self.api.send_command("setprop vendor.multicamera.tracking.visualize true")

        # self.api.send_command("setenforce 0")
        self.api.send_command("setprop vendor.select.mulicamera 1")
        # self.api.send_command("setprop insta.debug.st_force_dual true")
        self.api.send_broadcast("com.example.vb_testtool.startCamera0")
    def start_speck_test(self):
        self.api.send_command("media volume --show --stream 3 --set 70", False)
        self.api.send_broadcast("com.example.vb_testtool.startSpeckTest")

    def lan_test(self):
        return self.api.lan_test()
    def stop_speck_test(self):
        self.api.send_broadcast("com.example.vb_testtool.stopSpeckTest")
        self.api.send_command("media volume --show --stream 3 --set 7", False)

    def dual_take_photo(self, remote_path="/storage/emulated/0/near_1", local_path=""):
        self.api.send_command(f"rm -rf /storage/emulated/0/*.jpg", False)
        self.api.send_command(f"rm -rf /storage/emulated/0/*.jpg", False)
        self.api.send_command(f"rm -rf /storage/emulated/0/*.dng", False)
        logger.info("进入android take_photo")
        res = self.api.dual_take_photo(remote_path)
        time.sleep(2)
        logger.info(f"android: {res}")
        if res:
            file_path = local_path + "_maincam.jpg"
            # if os.path.exists(file_path):
            #     os.remove(file_path)
            ress = self.api.pull_file(local_path + "_maincam.jpg", remote_path + "_maincam.jpg")
            if type(ress) is not int:
                return False
            file_path = local_path + "_subcam.jpg"
            # if os.path.exists(file_path):
            #     os.remove(file_path)
            ress = self.api.pull_file(local_path + "_subcam.jpg", remote_path + "_subcam.jpg")
            if type(ress) is not int:
                return False
    def mipiRaw2Raw(self, file_path):
        xx = mipiraw2raw()
        rawPath = None
        img_width = 4080
        img_height = 2296
        rawDepth = 16
        bayer = "bayer_gr"
        bayer_order = 49
        result = xx.ProcSingleFile(file_path, img_width, img_height, rawDepth, bayer_order)
        return result

    def save_device_log(self, local_path):
        return self.api.save_device_log(local_path)

    def take_photo(self, camera_id=0, remote_path="/storage/emulated/0/near_1.dng", local_path="", bright=-1, station="default", is_reopen=True):

        self.api.send_command(f"rm -rf /storage/emulated/0/*.jpg", False)
        self.api.send_command(f"rm -rf /storage/emulated/0/*.dng", False)
        self.api.send_command(f"rm -rf /storage/emulated/0/*.raw", False)
        logger.info("进入android take_photo")

        res = self.api.take_photo(camera_id, remote_path, station=station, is_reopen=is_reopen)
        time.sleep(2)
        logger.info(f"android: {res}")
        if res:
            if station == "default":
                if camera_id==1:
                    ress = self.api.pull_file(local_path + ".raw", remote_path + ".raw")
                else:
                    ress = self.api.pull_file(local_path+".dng", remote_path+".dng")
                if type(ress) is not int:
                    return False
            ress = self.api.pull_file(local_path+".jpg", remote_path+".jpg")
            if camera_id==0 and type(ress) is not int:
                return False
            # dir_path = os.path.dirname(local_path)
            # input_path = os.path.join(dir_path, f"{os.path.splitext(os.path.basename(local_path))[0]}.dng")
            # output_path = os.path.join(dir_path, f"{os.path.splitext(os.path.basename(local_path))[0]}.jpg")
            # logger.info(input_path)
            # logger.info(output_path)
            time.sleep(1)
            if station == "default":
                if camera_id==0:
                    logger.info(f"local_path: {local_path}")
                    self.dng2jpg(local_path+".dng", local_path+".jpg", bright)
                else:
                    result = self.mipiRaw2Raw(local_path+".raw")
                    return result
            return ress
        else:
            return False
    def start_test_app(self):
        return self.api.start_test_app()

    def check_auth_result(self):
        return self.api.check_auth_result()

    def start_camera_iperf_tx(self, duration):

        resp = self.api.iperf_tx_start(duration)
        return resp

    def stop_camera_iperf_tx(self):
        resp = self.api.iperf_tx_stop()
        return resp


    def get_factory_mode(self):
        resp = self.api.get_factory_mode()
        # if not resp:
        #     self.push_scripy()
        return resp
    def get_wav_info(self, path):
        return self.api.get_wav_info(path)

    def is_wav_hassound(self, path):
        return self.api.is_wav_hassound(path)
    def get_audio_file(self, local_path):
        file_name = self.api.send_command("ls /storage/emulated/0/record_test")
        if file_name:
            file_name = file_name.split(" ")
            logger.info(file_name)
        else:
            return False
        for name in file_name:
            remote_path = f"/storage/emulated/0/record_test/{name}"
            path = local_path + f"\\{name}"
            logger.info(remote_path)
            logger.info(path)
            self.api.pull_file(path, remote_path)
    def get_old_test_file(self, local_path):
        # root = os.getcwd()
        # now = datetime.datetime.now().strftime("%Y%m%d")
        # if not os.path.exists(f"{root}\\vb_test_data\\"):
        #     os.mkdir(f"{root}\\vb_test_data\\")
        # if not os.path.exists(f"{root}\\vb_test_data\\{now}"):
        #     os.mkdir(f"{root}\\vb_test_data\\{now}")

        # local_path = f"{root}\\vb_test_data\\{now}\\test_result.json"
        remote_path = f"/storage/emulated/0/test_result.json"
        logger.info(remote_path)
        logger.info(local_path)
        self.api.pull_file(local_path, remote_path)

    def get_old_test_result(self):

        return self.api.get_old_test_result()
    def get_mic_test_result(self):
        return self.api.get_mic_test_result()
    def check_old_test_data(self):

        return self.api.check_old_test_data()

    def push_scripy(self):

        self.api.send_command("mkdir /sdcard/test_data")
        data_name = ["LED1_TEST.sh", "LED2_TEST.sh", "test.mp3"]
        try:
            for name in data_name:
                local_path = f"./test_data/{name}"
                remote_path = f"/sdcard/test_data/{name}"
                self.api.push_file(local_path, remote_path)
            return True

        except Exception as e:
            logger.info(e)
            return False

    def start_old_test(self, test_time=100, vol_value=20):
        self.api.send_command(f"media volume --show --stream 3 --set {vol_value}", False)
        self.api.start_old_test(test_time)
    def init_test_app(self):
        self.api.init_test_app()
    def close_old_test(self):
        self.api.send_command("media volume --show --stream 3 --set 7", False)
        self.api.close_old_test()








if __name__ == '__main__':
    def dng2jpg(input_path, output_path):
         # 打开DNG文件
        with rawpy.imread(input_path+".dng") as raw:
            postprocess_params = {
                "no_auto_bright": True,  # 手动控制亮度
                "output_bps": 16,
                "use_camera_wb": True,
                "half_size": False,
                "dcb_enhance": True,
                "output_color": rawpy.ColorSpace.sRGB,
            }
            rgb_output = raw.postprocess(**postprocess_params)
            if rgb_output.dtype == np.uint16:
                # Scale the 16-bit image to 8-bit
                rgb_output = ((rgb_output / 65535) * 255).round().astype(np.uint8)

            # 保存为JPG文件
            imageio.imwrite(output_path, rgb_output)


    import numpy as np
    from PIL import Image


    def raw10_to_rgb(raw10_path, width, height):
        with open(raw10_path, 'rb') as f:
            raw_data = np.frombuffer(f.read(), dtype=np.uint8)

        # 创建一个空的16位数组来存储解码后的像素值
        raw16 = np.zeros((height, width), dtype=np.uint16)

        for i in range(height):
            for j in range(width // 4):
                pixel_index = i * (width // 4) * 5 + j * 5
                raw16[i, j * 4 + 0] = (raw_data[pixel_index + 0] << 2) + ((raw_data[pixel_index + 4] & 0xC0) >> 6)
                raw16[i, j * 4 + 1] = (raw_data[pixel_index + 1] << 2) + ((raw_data[pixel_index + 4] & 0x30) >> 4)
                raw16[i, j * 4 + 2] = (raw_data[pixel_index + 2] << 2) + ((raw_data[pixel_index + 4] & 0x0C) >> 2)
                raw16[i, j * 4 + 3] = (raw_data[pixel_index + 3] << 2) + (raw_data[pixel_index + 4] & 0x03)

        # 将16位图像转换为8位图像
        rgb_image = ((raw16 / 1023.0) * 255).astype(np.uint8)

        return rgb_image


    def raw2jpg(input_path, output_path, width=1920, height=1056):
        # 调用转换函数
        rgb_output = raw10_to_rgb(input_path, width, height)

        # 将numpy数组转换为PIL图像
        image = Image.fromarray(rgb_output)

        # 保存为JPEG格式
        image.save(output_path, 'JPEG')
    def testRaw2jpg(ImgPath, outPath):
        # ImgPath = "D:\DATA\test_0.raw"
        # outPath = "D:\DATA\\test_0_out.jpg"
        img = np.fromfile(ImgPath, dtype=np.uint16).reshape((1056, 1920))

        with open(outPath, "wb") as f:
            f.write(img)
            f.close()


    def convert_raw10_to_image(raw10_data, width=1920, height=1056):
        # RAW10 每个像素点10位，需要转换成8位
        raw10_image = np.frombuffer(raw10_data, dtype=np.uint16).reshape((height, width))
        # 将数据转换为8位
        raw10_image = (raw10_image >> 2).astype(np.uint8)
        return raw10_image


    # 读取 RAW10 数据
    # with open('input.raw10', 'rb') as f:
    #     raw10_data = f.read()
    #
    # # 假设图像的宽度和高度已知
    # width = 1920
    # height = 1080
    #
    # # 转换 RAW10 数据为图像
    # image_data = convert_raw10_to_image(raw10_data, width, height)
    # image = Image.fromarray(image_data)
    #
    # # 保存为 JPG
    # image.save('output.jpg')

    # 调用raw2jpg函数进行转换
    # raw2jpg(r"C:\Users\Insta360\Downloads\test_0.raw", r"C:\Users\Insta360\Downloads\48C\test4.jpg")

    raw_file_path = r"C:\Users\Insta360\Downloads\test_0.raw"
    jpg_file_path = r"C:\Users\Insta360\Downloads\48C\test4.jpg"

    # 图像尺寸
    width, height = 1920, 1056

    # 读取 raw 文件内容
    with open(raw_file_path, 'rb') as raw_file:
        raw_data = raw_file.read()

    # 检查数据长度是否与预期匹配
    expected_length = width * height * 2
    if len(raw_data) != expected_length:
        raise ValueError(f"Raw data length mismatch: expected {expected_length}, got {len(raw_data)}")

    # 将 raw 数据转换为 numpy 数组
    image_array = np.frombuffer(raw_data, dtype=np.uint16).reshape((height, width))

    # 将 numpy 数组转换为 Pillow 图像对象
    image = Image.fromarray(image_array, mode='I;16')

    # 将图像对象转换并保存为 JPG 格式
    image.convert('L').save(jpg_file_path)

    print(f'Successfully converted raw to JPG and saved as {jpg_file_path}')
