import os
import time
from enum import Enum
from src.device.fw_api.api_factory_cv5 import API_Libusb
from src.device.fw_api.util_libusb import list_usb_device
from src.utils.logger import logger
from tools.JN1SFR.sfr_test import get_dll_ret


class Camera(object):
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

    def __init__(self, sn=None, usb_device=None, product=None):
        self.sn = sn
        self.usb_device = usb_device
        self.uuid = None
        self.api = None
        self.product = product
        self.device_info = []
        self.battery = None
        self.white_balance_error_code = {0: "标定完成", 10: "文件出错打开文件失败", 11: "内存申请失败", 20: "曝光亮度错误",
                                        21: "边角超出阈值", 22: "找中心失败，请检查是否有光源中心", 30: "曝光错误",
                                        31: "计算结果超出阈值", 32: "计算失败", 33: "OTP写入失败，请重新校正",
                                        34: "OTP已写入，已校正", 40: "坏点超出阈值", 41: "漏光", 129: "拍照失败",
                                        130: "白平衡校正数据写到文件失败"}

    def connect(self):
        usb_devices = list_usb_device()
        if usb_devices:
            self.sn = list(usb_devices.keys())[0]
        else:
            if self.product == 'PC100':
                self.sn = '123456789ABC'
            elif self.product == 'IAC2':
                self.sn = 'INSWWYYNXXXXXX'
        self.api = API_Libusb(self.sn)
        self.api.init_socket()
        # # 0:产测模式 1：老化模式 2：正常模式
        # resp = self.get_factory_mode()
        # if resp['code'] == 'success' and resp['data']['value'] == '1':
        #     logger.info(f"当前模式是老化模式")
        #     return

        self.api.init_app_socket_con()
        # self.device_address = self.api.info_usb_device.get("DeviceAddress")
        self.connecting = True
        if self.api.cam_info['device_info'] and self.api.cam_info['device_info']['result'] == self.ApiCode.SUCCESS.value:
            self.uuid = self.api.cam_info['device_info']['uuid']

            # self.uuid = "123456789123"
            self.set_sync_time()
            logger.info(f"连接设备: {self.uuid} 成功")
        else:
            logger.info(f"连接设备失败")

    def disconnect(self):
        # time.sleep(2)
        self.api.close()
        self.connecting = False
        logger.info(f"断开 {self.uuid} 连接成功")

    def get_camera_info(self):
        # UUID Sensor 固件版本 硬件版本 
        # 序列号 镜头类型 音频码 相机电量
        # 相机类型
        logger.debug(f"相机设备信息：{self.api.cam_info}")
        if not self.api.cam_info or not self.api.cam_info.get('device_info', {}) or \
                self.api.cam_info.get('device_info', {}).get('result') != self.ApiCode.SUCCESS.value:
            logger.error(f"相机信息获取失败")
            return []
        self.api.get_vb_info()
        self.device_info = [
            {"name": "UUID:", "info": self.api.cam_info['device_info']['uuid']},
            # {"name": "UUID:", "info": "123456789123"},
            {"name": "固件版本:", "info": self.api.cam_info['device_info']['software']},
            {"name": "硬件版本:", "info": self.api.cam_info['device_info']['hardware']},
            {"name": "序列号:", "info": self.api.cam_info['device_info']['serial']},
            {"name": "电量:", "info": self.api.cam_info['device_info']['battery']},
            {"name": "Sensor:", "info": self.api.cam_info['device_info']['sensor_id']},
            {"name": "MCU:", "info": self.api.cam_info['device_info']['mcu_version']},
            {"name": "ptz_uuid:", "info": self.api.cam_info['device_info']['ptz_uuid']}
        ]

        logger.info(f"222设备信息: {self.device_info}")
        return self.device_info

    def set_sync_time(self, product=None):
        if product == "PC100":
            struct_time = time.localtime(time.time())
            str_time = time.strftime("%Y-%m-%d %H:%M:%S")
            wday = str(struct_time.tm_wday)
            cur_str_time = str_time + ' ' + wday
            logger.info('设置本地的同步时间到相机里面')
            self.api.set_sync_time(cur_str_time)
        else:
            self.api.set_sync_time(str(int(time.time())))

    def start_button_test(self):
        resp = self.api.button_test_start()
        if not resp:
            return self.pack_result(code=self.ApiCode.FAIL.value, msg=self.ErrorMsg.TIMEOUT.value, data={})

        if resp['result'] != self.ApiCode.SUCCESS.value:
            logger.error(f"开始进行按键测试指令失败：{resp}")
            return self.pack_result(code=self.ApiCode.FAIL.value, msg=self.ErrorMsg.START_BUTTON_FAIL.value, data={})

        return self.pack_result(code=self.ApiCode.SUCCESS.value, msg='', data={})

    def stop_button_test(self):
        resp = self.api.button_test_stop()
        if not resp:
            return self.pack_result(code=self.ApiCode.FAIL.value, msg=self.ErrorMsg.TIMEOUT.value, data={})
        if resp['result'] != self.ApiCode.SUCCESS.value:
            logger.error(f"停止按键测试指令失败：{resp}")
            return self.pack_result(code=self.ApiCode.FAIL.value, msg=self.ErrorMsg.STOP_BUTTON_FAIL.value, data={})

        return self.pack_result(code=self.ApiCode.SUCCESS.value, msg='', data={})

    def listen_button_status(self):
        last_index = list(self.api._pkt_map.keys())[-1]
        last_resp = self.api._pkt_map[last_index][-1].jsobj
        if not last_resp or last_resp['result'] != self.ApiCode.SUCCESS.value:
            logger.error(f"最新的指令异常：{last_resp}")
            return self.pack_result(code=self.ApiCode.FAIL.value, msg=self.ErrorMsg.EXCEPTION.value, data={})

        if not last_resp.get('key'):
            return self.pack_result(
                code=self.ApiCode.FAIL.value, msg=self.ErrorMsg.WAIT_BUTTON_RESPONSE.value, data={}
            )
        button = last_resp['key']
        logger.info(f"当前按的按钮是：{button}")
        return self.pack_result(
            code=self.ApiCode.SUCCESS.value, msg='', data={'button': button}
        )

    def start_lcd_test(self):
        resp = self.api.lcd_test_start()
        if not resp:
            return self.pack_result(code=self.ApiCode.FAIL.value, msg=self.ErrorMsg.TIMEOUT.value, data={})

        if resp['result'] != self.ApiCode.SUCCESS.value:
            logger.error(f"开始lcd指令失败：{resp}")
            return self.pack_result(code=self.ApiCode.FAIL.value, msg=self.ErrorMsg.START_LCD_FAIL.value, data={})

        return self.pack_result(code=self.ApiCode.SUCCESS.value, msg='', data={})

    def stop_lcd_test(self):
        resp = self.api.lcd_test_stop()
        if not resp:
            return self.pack_result(code=self.ApiCode.FAIL.value, msg=self.ErrorMsg.TIMEOUT.value, data={})

        if resp['result'] != self.ApiCode.SUCCESS.value:
            logger.error(f"停止lcd指令失败：{resp}")
            return self.pack_result(code=self.ApiCode.FAIL.value, msg=self.ErrorMsg.STOP_LCD_FAIL.value, data={})

        return self.pack_result(code=self.ApiCode.SUCCESS.value, msg='', data={})

    def start_tp_test(self):
        resp = self.api.tp_test_start()
        if not resp:
            return self.pack_result(code=self.ApiCode.FAIL.value, msg=self.ErrorMsg.TIMEOUT.value, data={})

        if resp['result'] != self.ApiCode.SUCCESS.value:
            logger.error(f"开启tp指令失败：{resp}")
            return self.pack_result(code=self.ApiCode.FAIL.value, msg=self.ErrorMsg.START_TP_FAIL.value, data={})

        return self.pack_result(code=self.ApiCode.SUCCESS.value, msg='', data={})

    def stop_tp_test(self):
        resp = self.api.tp_test_stop()
        if not resp:
            return self.pack_result(code=self.ApiCode.FAIL.value, msg=self.ErrorMsg.TIMEOUT.value, data={})

        if resp['result'] != self.ApiCode.SUCCESS.value:
            logger.error(f"停止tp指令失败：{resp}")
            return self.pack_result(code=self.ApiCode.FAIL.value, msg=self.ErrorMsg.STOP_TP_FAIL.value, data={})

        return self.pack_result(code=self.ApiCode.SUCCESS.value, msg='', data={})

    def start_led_test(self):
        resp = self.api.led_test_start()
        if not resp:
            return self.pack_result(code=self.ApiCode.FAIL.value, msg=self.ErrorMsg.TIMEOUT.value, data={})

        if resp['result'] != self.ApiCode.SUCCESS.value:
            logger.error(f"开启led指令失败：{resp}")
            return self.pack_result(code=self.ApiCode.FAIL.value, msg=self.ErrorMsg.START_LED_FAIL.value, data={})

        return self.pack_result(code=self.ApiCode.SUCCESS.value, msg='', data={})

    def stop_led_test(self):
        resp = self.api.led_test_stop()
        if not resp:
            return self.pack_result(code=self.ApiCode.FAIL.value, msg=self.ErrorMsg.TIMEOUT.value, data={})

        if resp['result'] != self.ApiCode.SUCCESS.value:
            logger.error(f"停止led指令失败：{resp}")
            return self.pack_result(code=self.ApiCode.FAIL.value, msg=self.ErrorMsg.STOP_LED_FAIL.value, data={})

        return self.pack_result(code=self.ApiCode.SUCCESS.value, msg='', data={})

    def start_oled_test(self):
        resp = self.api.oled_test_start()
        if not resp:
            return self.pack_result(code=self.ApiCode.FAIL.value, msg=self.ErrorMsg.TIMEOUT.value, data={})

        if resp['result'] != self.ApiCode.SUCCESS.value:
            logger.error(f"开启oled指令失败：{resp}")
            return self.pack_result(code=self.ApiCode.FAIL.value, msg=self.ErrorMsg.START_OLED_FAIL.value, data={})

        return self.pack_result(code=self.ApiCode.SUCCESS.value, msg='', data={})

    def stop_oled_test(self):
        resp = self.api.oled_test_stop()
        if not resp:
            return self.pack_result(code=self.ApiCode.FAIL.value, msg=self.ErrorMsg.TIMEOUT.value, data={})

        if resp['result'] != self.ApiCode.SUCCESS.value:
            logger.error(f"停止oled指令失败：{resp}")
            return self.pack_result(code=self.ApiCode.FAIL.value, msg=self.ErrorMsg.STOP_OLED_FAIL.value, data={})

        return self.pack_result(code=self.ApiCode.SUCCESS.value, msg='', data={})

    def start_g_sensor_test(self):
        resp = self.api.gsensor_test_start()
        if not resp:
            return self.pack_result(code=self.ApiCode.FAIL.value, msg=self.ErrorMsg.TIMEOUT.value, data={})

        if resp['result'] != self.ApiCode.SUCCESS.value:
            logger.error(f"开启g-sensor指令失败：{resp}")
            return self.pack_result(code=self.ApiCode.FAIL.value, msg=self.ErrorMsg.START_G_SENSOR_FAIL.value, data={})

        return self.pack_result(code=self.ApiCode.SUCCESS.value, msg='', data={})

    def stop_g_sensor_test(self):
        resp = self.api.gsensor_test_stop()
        if not resp:
            return self.pack_result(code=self.ApiCode.FAIL.value, msg=self.ErrorMsg.TIMEOUT.value, data={})

        if resp['result'] != self.ApiCode.SUCCESS.value:
            logger.error(f"停止g-sensor指令失败：{resp}")
            return self.pack_result(code=self.ApiCode.FAIL.value, msg=self.ErrorMsg.STOP_G_SENSOR_FAIL.value, data={})

        return self.pack_result(code=self.ApiCode.SUCCESS.value, msg='', data={})

    def open_camera_wifi(self):
        resp = self.api.wifi_open()
        if not resp:
            return self.pack_result(code=self.ApiCode.FAIL.value, msg=self.ErrorMsg.TIMEOUT.value, data={})

        if resp['result'] != self.ApiCode.SUCCESS.value:
            logger.error(f"打开相机wifi指令失败：{resp}")
            return self.pack_result(code=self.ApiCode.FAIL.value, msg=self.ErrorMsg.START_WIFI_FAIL.value, data={})

        return self.pack_result(code=self.ApiCode.SUCCESS.value, msg='', data={})

    def close_camera_wifi(self):
        resp = self.api.wifi_close()
        if not resp:
            return self.pack_result(code=self.ApiCode.FAIL.value, msg=self.ErrorMsg.TIMEOUT.value, data={})

        if resp['result'] != self.ApiCode.SUCCESS.value:
            logger.error(f"关闭相机wifi指令失败：{resp}")
            return self.pack_result(code=self.ApiCode.FAIL.value, msg=self.ErrorMsg.STOP_WIFI_FAIL.value, data={})

        return self.pack_result(code=self.ApiCode.SUCCESS.value, msg='', data={})

    def set_camera_wifi_freq(self, value='5g'):
        resp = self.api.set_wifi_freq(value=value)
        if not resp:
            return self.pack_result(code=self.ApiCode.FAIL.value, msg=self.ErrorMsg.TIMEOUT.value, data={})

        if resp['result'] != self.ApiCode.SUCCESS.value:
            logger.error(f"设置相机wifi频段指令失败：{resp}")
            return self.pack_result(code=self.ApiCode.FAIL.value, msg=self.ErrorMsg.SET_WIFI_FREQ_FAIL.value, data={})

        return self.pack_result(code=self.ApiCode.SUCCESS.value, msg='', data={})

    def start_camera_iperf_tx(self, config):
        resp = self.api.iperf_tx_start(config)
        if not resp:
            return self.pack_result(code=self.ApiCode.FAIL.value, msg=self.ErrorMsg.TIMEOUT.value, data={})

        if resp['result'] != self.ApiCode.SUCCESS.value:
            logger.error(f"开启相机的iperf性能工具指令失败：{resp}")
            return self.pack_result(code=self.ApiCode.FAIL.value, msg=self.ErrorMsg.START_IPERFTX_FAIL.value, data={})

        return self.pack_result(code=self.ApiCode.SUCCESS.value, msg='', data={})

    def stop_camera_iperf_tx(self):
        resp = self.api.iperf_tx_stop()
        if not resp:
            return self.pack_result(code=self.ApiCode.FAIL.value, msg=self.ErrorMsg.TIMEOUT.value, data={})

        if resp['result'] != self.ApiCode.SUCCESS.value:
            logger.error(f"停止相机的iperf性能工具指令失败：{resp}")
            return self.pack_result(code=self.ApiCode.FAIL.value, msg=self.ErrorMsg.STOP_IPERFTX_FAIL.value, data={})

        return self.pack_result(code=self.ApiCode.SUCCESS.value, msg='', data={})

    def bt_wakeup(self):
        resp = self.api.bt_wakeup()
        if not resp:
            return self.pack_result(code=self.ApiCode.FAIL.value, msg=self.ErrorMsg.TIMEOUT.value, data={})

        if resp['result'] != self.ApiCode.SUCCESS.value:
            logger.error(f"开启蓝牙唤醒测试请求失败：{resp}")
            return self.pack_result(code=self.ApiCode.FAIL.value, msg=self.ErrorMsg.BT_WAKEUP_FAIL.value, data={})

        return self.pack_result(code=self.ApiCode.SUCCESS.value, msg='', data={})

    def get_ble_wakeup_flag(self):
        resp = self.api.get_ble_wakeup_flag()
        logger.debug(f'蓝牙唤醒的标记：{resp}')
        if not resp:
            return self.pack_result(code=self.ApiCode.FAIL.value, msg=self.ErrorMsg.TIMEOUT.value, data={})

        if resp['result'] != self.ApiCode.SUCCESS.value:
            logger.error(f"设备不是通过蓝牙唤醒的：{resp}")
            return self.pack_result(code=self.ApiCode.FAIL.value, msg=self.ErrorMsg.NOT_BLE_WAKEUP_FAIL.value, data={})

        return self.pack_result(code=self.ApiCode.SUCCESS.value, msg='', data={})

    def get_factory_mode(self):
        resp = self.api.get_factory_mode()
        logger.debug(f'获取设备模式：{resp}')
        if self.product == "VB":
            return resp
        if not resp:
            return self.pack_result(code=self.ApiCode.FAIL.value, msg=self.ErrorMsg.TIMEOUT.value, data={})

        if resp['result'] != self.ApiCode.SUCCESS.value:
            logger.error(f"获取设备模式失败：{resp}")
            return self.pack_result(code=self.ApiCode.FAIL.value, msg=self.ErrorMsg.GET_FACTORY_MODE_FAIL.value, data={})

        return self.pack_result(code=self.ApiCode.SUCCESS.value, msg='', data={'value': resp['value']})

    def set_factory_mode(self, mode=None):
        resp = self.api.set_factory_mode(mode)
        logger.debug(f'设置设备模式：{resp}')
        if not resp:
            return self.pack_result(code=self.ApiCode.FAIL.value, msg=self.ErrorMsg.TIMEOUT.value, data={})

        if resp['result'] != self.ApiCode.SUCCESS.value:
            logger.error(f"设置设备模式失败：{resp}")
            return self.pack_result(code=self.ApiCode.FAIL.value, msg=self.ErrorMsg.SET_FACTORY_MODE_FAIL.value, data={})

        return self.pack_result(code=self.ApiCode.SUCCESS.value, msg='', data={})

    def set_age_config(self, config1=None, config2=None, config3=None, interval="3600"):
        resp = self.api.set_config(config1=config1, config2=config2, config3=config3, interval=interval)
        logger.debug(f'设置老化参数：{resp}')
        if not resp:
            return self.pack_result(code=self.ApiCode.FAIL.value, msg=self.ErrorMsg.TIMEOUT.value, data={})

        if resp['result'] != self.ApiCode.SUCCESS.value:
            logger.error(f"设置老化参数失败：{resp}")
            return self.pack_result(code=self.ApiCode.FAIL.value, msg=self.ErrorMsg.SET_AGE_CONFIG_FAIL.value, data={})

        return self.pack_result(code=self.ApiCode.SUCCESS.value, msg='', data={})

    def power_off(self):
        resp = self.api.power_off()
        logger.debug(f'老化关机：{resp}')
        if not resp:
            return self.pack_result(code=self.ApiCode.FAIL.value, msg=self.ErrorMsg.TIMEOUT.value, data={})

        if resp['result'] != self.ApiCode.SUCCESS.value:
            logger.error(f"老化关机数失败：{resp}")
            return self.pack_result(code=self.ApiCode.FAIL.value, msg=self.ErrorMsg.AGE_POWER_OFF_FAIL.value, data={})

        return self.pack_result(code=self.ApiCode.SUCCESS.value, msg='', data={})

    def get_age_result(self):
        resp = self.api.get_age_result()
        logger.debug(f'老化结果：{resp}')
        if not resp:
            return self.pack_result(code=self.ApiCode.FAIL.value, msg=self.ErrorMsg.TIMEOUT.value, data={})

        if resp['result'] != self.ApiCode.SUCCESS.value:
            logger.error(f"老化结果获取失败：{resp}")
            return self.pack_result(code=self.ApiCode.FAIL.value, msg=self.ErrorMsg.AGE_RESULT_FAIL.value, data={})

        return self.pack_result(code=self.ApiCode.SUCCESS.value, msg='', data={'value': resp['aging_result']})

    def reset_age_result(self):
        resp = self.api.reset_result()
        logger.debug(f'清除老化结果：{resp}')
        if not resp:
            return self.pack_result(code=self.ApiCode.FAIL.value, msg=self.ErrorMsg.TIMEOUT.value, data={})

        if resp['result'] != self.ApiCode.SUCCESS.value:
            logger.error(f"清除老化结果失败：{resp}")
            return self.pack_result(code=self.ApiCode.FAIL.value, msg=self.ErrorMsg.RESET_AGE_RESULT_FAIL.value, data={})

        return self.pack_result(code=self.ApiCode.SUCCESS.value, msg='', data={})

    def take_photo(self, config):
        cmd = {
            "cmd": "CAPTURE", "action": "start",
            "config": config
        }
        resp = self.api.send_json_pkt_get_resp(cmd)
        if not resp:
            logger.error('相机返回异常')
            return self.pack_result(code=self.ApiCode.FAIL.value, msg=self.ErrorMsg.EXCEPTION.value, data={})

        if resp['result'] != self.ApiCode.SUCCESS.value:
            logger.error('开启拍照失败')
            return self.pack_result(code=self.ApiCode.FAIL.value, msg=self.ErrorMsg.START_CAPTURE_FAIL.value, data={})
        resp = self.api.capture_stop()
        if resp['result'] != self.ApiCode.SUCCESS.value:
            logger.error('停止拍照失败')
            return self.pack_result(code=self.ApiCode.FAIL.value, msg=self.ErrorMsg.STOP_CAPTURE_FAIL.value, data={})
        logger.info('拍照成功')
        return self.pack_result(code=self.ApiCode.SUCCESS.value, msg='', data={'file_path': resp['file_path']})

    def set_param_photo(self, width="3040", height="3040", type="jpeg", iso="100", shutter="1/12.5"):
        cmd = {"cmd": "CAPTURE", "action": "start",
               "config": {"width": width, "height": height, "type": type, "iso": iso, "shutter": shutter}}
        resp = self.api.send_json_pkt_get_resp(cmd)
        if not resp:
            logger.error('相机返回异常')
            return self.pack_result(code=self.ApiCode.FAIL.value, msg=self.ErrorMsg.EXCEPTION.value, data={})
        if resp['result'] != self.ApiCode.SUCCESS.value:
            logger.error('开启拍照失败')
            return self.pack_result(code=self.ApiCode.FAIL.value, msg=self.ErrorMsg.START_CAPTURE_FAIL.value, data={})
        resp = self.api.capture_stop()
        if resp['result'] != self.ApiCode.SUCCESS.value:
            logger.error('停止拍照失败')
            return self.pack_result(code=self.ApiCode.FAIL.value, msg=self.ErrorMsg.STOP_CAPTURE_FAIL.value, data={})
        logger.info('拍照成功')
        return self.pack_result(code=self.ApiCode.SUCCESS.value, msg='', data={'file_path': resp['file_path']})

    def take_record(self, config, interval=5):
        cmd = {"cmd": "RECORD", "action": "start", "config": config}
        resp = self.api.send_json_pkt_get_resp(cmd)
        if not resp:
            logger.error('相机返回异常')
            return self.pack_result(code=self.ApiCode.FAIL.value, msg=self.ErrorMsg.EXCEPTION.value, data={})

        if resp['result'] != self.ApiCode.SUCCESS.value:
            logger.error('开启录像失败')
            return self.pack_result(code=self.ApiCode.FAIL.value, msg=self.ErrorMsg.START_RECORD_FAIL.value, data={})

        time.sleep(interval)
        resp = self.api.record_stop()
        if resp['result'] != self.ApiCode.SUCCESS.value:
            logger.error('停止录像失败')
            return self.pack_result(code=self.ApiCode.FAIL.value, msg=self.ErrorMsg.STOP_RECORD_FAIL.value, data={})
        logger.info('录像成功')
        return self.pack_result(code=self.ApiCode.SUCCESS.value, msg='', data={'record_file': resp['record_file']})

    def capture_start_pc100_gyroa_pict(self):
        """拍照开始pc100标定"""
        return self.api.send_json_pkt_get_resp({
            "cmd": "CAPTURE", "action": "start",
            "config": {"width": "3040", "height": "3040", "type": "raw/jpeg/yuv", "iso": "100", "shutter": "10"}
        })

    def capture_start_pc100_gyroa_pano(self):
        """拍照开始pc100全景标定"""
        return self.api.send_json_pkt_get_resp({
            "cmd": "CAPTURE", "action": "start",
            "config": {"width": "5760", "height": "2880", "type": "raw/jpeg/yuv", "iso": "100", "shutter": "1/10"}
        })

    def download_file(self, ori_path, tar_path):
        """
        下载文件
        :param path_dcim: 传参/DCIM/xxxx
        :param p_out: 下载文件全路径
        :param callbcak: 回调函数,回传进度, callback(progress)
        :return:
        """
        try:
            return self.api.download_file(ori_path, tar_path)
        except Exception as e:
            logger.error(e)
            return False

    def pack_result(self, code, msg, data):
        return {'code': code, 'msg': msg, 'data': data}

    def correct_gyro(self):
        # 陀螺仪校准
        cmd = {"cmd": "IMU", "action": "start_calibration", "count": "200"}
        resp = self.api.send_json_pkt_get_resp(cmd)
        if not resp:
            logger.error('相机返回异常')
            return {"result": "fail"}
        if resp['result'] != self.ApiCode.SUCCESS.value:
            logger.error('陀螺仪校准失败')
            return resp
        logger.info('陀螺仪校准成功')
        return resp

    def gyro_set_offset(self, select, value):
        # 陀螺仪标定参数设置
        cmd = {"cmd": "IMU", "action": "set_offset", "select":select, "value":value}
        resp = self.api.send_json_pkt_get_resp(cmd)
        if not resp:
            logger.error('相机返回异常')
            return {"result": "fail"}
        if resp['result'] != self.ApiCode.SUCCESS.value:
            logger.error('陀螺仪写入标定参数失败')
            return resp
        logger.info('陀螺仪写入标定参数成功')
        return resp

    def gyro_get_offset(self):
        # 获取陀螺仪标定参数
        cmd = {"cmd": "IMU", "action": "get_offset"}
        resp = self.api.send_json_pkt_get_resp(cmd)
        if not resp:
            logger.error('相机返回异常')
            return {"result": "fail"}
        if resp['result'] != self.ApiCode.SUCCESS.value:
            logger.error('陀螺仪获取标定参数失败')
            return resp
        logger.info('陀螺仪获取标定参数成功')
        return resp
    def get_gyro_confirm(self):
        # 获取IMU标定参数
        cmd = {"cmd": "IMU", "action": "get_offset"}
        resp = self.api.send_json_pkt_get_resp(cmd)
        if not resp:
            logger.error('相机返回异常')
            return {"result": "fail"}
        if resp['result'] != self.ApiCode.SUCCESS.value:
            logger.error('获取陀螺仪标定参数失败')
            return resp
        logger.info(f'获取陀螺仪标定参数成功，V1:{resp["V1"]},V2:{resp["V2"]},V3:{resp["V3"]}')
        return resp

    def gsensor_calibration(self):
        # g-sensor校准
        cmd = {"cmd": "GSENSOR", "action": "gsensor_calibration"}
        resp = self.api.send_json_pkt_get_resp(cmd)
        if not resp:
            logger.error('相机返回异常')
            return {"result": "fail"}
        if resp['result'] != self.ApiCode.SUCCESS.value:
            logger.error('g-sensor校准失败')
            return resp
        logger.info('g-sensor校准成功')
        return resp

    def white_balance_correct(self, capture_param):
        # 白平衡校正
        cmd = {"cmd": "IMAGE", "action": "wb_start",
               "config": capture_param}
        resp = self.api.send_json_pkt_get_resp(cmd)
        if not resp:
            logger.error('相机返回异常')
            return self.pack_result(code=self.ApiCode.FAIL.value, msg=self.ErrorMsg.EXCEPTION.value, data={})
        if resp['result'] != self.ApiCode.SUCCESS.value:
            logger.error(f'白平衡校正失败，返回结果为：{resp}')
            error_code = int(list(resp.values())[3])
            if error_code in self.white_balance_error_code:
                error_msg = self.white_balance_error_code[error_code]
            else:
                error_msg = f"错误代码为：{error_code}"
            return self.pack_result(code=self.ApiCode.FAIL.value, msg=error_msg, data={})
        logger.info(f'白平衡校正成功，返回结果为：{resp}')
        return self.pack_result(code=self.ApiCode.SUCCESS.value, msg='', data=resp)


def handle_picture():
    # camera = Camera(sn='123456789ABC')
    camera = Camera(sn='INSWWYYNXXXXXX')
    camera.connect()
    camera.get_camera_info()
    result = camera.take_photo()
    file_path = result['data']['file_path']
    if '|' in file_path:
        files = file_path.split('|')
        logger.info(files)
        file = camera.download_file(files[0], files[0].split('/')[-1])
        logger.info(file)
        time.sleep(2)
        file = camera.download_file(files[1], files[1].split('/')[-1])
        logger.info(file)
    else:
        file = camera.download_file(file_path, file_path.split('/')[-1])
        logger.info(file)

    logger.info(f'收到的所有的结果：{camera.api._pkt_map}')


if __name__ == '__main__':
    dll_path = "D:\\code\\gfpt_android\\tools\\JN1SFR"
    os.environ['PATH'] = dll_path + ';' + os.environ['PATH']
    path = r"D:\code\gfpt_android\tools\JN1SFR\VBJN1SFRTEST.dll"

    get_dll_ret(path)