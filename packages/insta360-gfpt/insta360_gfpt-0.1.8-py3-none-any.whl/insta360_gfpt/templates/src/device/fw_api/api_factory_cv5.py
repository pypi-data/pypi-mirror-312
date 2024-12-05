#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :api_factory_cv5.py
# @Time      :2022/7/12 20:17
# @Author    :lilinhong
"""
https://arashivision.feishu.cn/wiki/wikcn3HqkmUpwqdikDiJ2H3hJrb
产测命令接口列表
"""
import os
import sys
import time

from src.device.fw_api.ins_libusb import Ins_Libusb
from src.device.fw_api.util_libusb import list_usb_device
from src.utils.logger import logger


class API_Libusb(Ins_Libusb):

    def __init__(self, cam_sn):
        super(API_Libusb, self).__init__(cam_sn)
        self.cam_info: dict = {}

    def init_app_socket_con(self):
        self.cam_info = {
            # 'product_uuid': self.get_product_uuid(),
            'device_info': self.get_device_info(),
        }

    def get_device_info(self):
        """读取设备信息"""
        return self.send_json_pkt_get_resp({
            'cmd': 'DEVICEINFO', 'action': 'get_device_info'
        })

    def get_mcu_version(self):
        """读取MCU版本号"""
        return self.send_json_pkt_get_resp({
            'cmd': 'DEVICEINFO', 'action': 'get_mcu_version'
        })

    def set_factory_mode(self, value: str):
        """设置设备模式"""
        return self.send_json_pkt_get_resp({
            'cmd': 'DEVICEINFO', 'action': 'set_factory_mode', 'value': value
        })

    def get_factory_mode(self):
        """获取设备模式"""
        return self.send_json_pkt_get_resp({
            'cmd': 'DEVICEINFO', 'action': 'get_factory_mode'
        })

    def get_product_uuid(self):
        """获取设备UUID"""
        return self.send_json_pkt_get_resp({
            'cmd': 'DEVICEINFO', 'action': 'get_product_uuid'
        })

    def set_product_serial(self, value: str):
        """设置Serial号"""
        return self.send_json_pkt_get_resp({
            'cmd': 'DEVICEINFO', 'action': 'set_product_serial', "value": value
        })

    def get_product_serial(self):
        """读取Serial号"""
        return self.send_json_pkt_get_resp({
            'cmd': 'DEVICEINFO', 'action': 'get_product_serial'
        })

    def set_sync_time(self, value):
        """设置设备同步时间"""
        return self.send_json_pkt_get_resp({
            'cmd': 'DEVICEINFO', 'action': 'set_sync_time', "value": value
        })

    def reset_info(self):
        """恢复出厂设置"""
        return self.send_json_pkt_get_resp({"cmd": "DEVICEINFO", "action": "reset_info"})

    def reboot(self):
        """重启设备"""
        return self.send_json_pkt_get_resp({"cmd": "SYS", "action": "reboot"})

    def link_test_start(self):
        """Link测试开始"""
        return self.send_json_pkt_get_resp({
            'cmd': 'LINK', 'action': 'start'
        })

    def led_test_start(self):
        """LED测试开始"""
        return self.send_json_pkt_get_resp({
            'cmd': 'LED', 'action': 'start'
        })

    def led_test_stop(self):
        """LED测试结束"""
        return self.send_json_pkt_get_resp({
            'cmd': 'LED', 'action': 'stop'
        })

    def oled_test_start(self):
        """OLED测试开始"""
        return self.send_json_pkt_get_resp({
            'cmd': 'OLED', 'action': 'start'
        })

    def oled_test_stop(self):
        """OLED测试结束"""
        return self.send_json_pkt_get_resp({
            'cmd': 'OLED', 'action': 'stop'
        })

    def lcd_test_start(self):
        """LCD测试开始"""
        return self.send_json_pkt_get_resp({
            'cmd': 'LCD', 'action': 'start'
        })

    def lcd_test_stop(self):
        """LCD测试结束"""
        return self.send_json_pkt_get_resp({
            'cmd': 'LCD', 'action': 'stop'
        })

    def tp_test_start(self):
        """TP测试开始"""
        return self.send_json_pkt_get_resp({
            'cmd': 'TP', 'action': 'start'
        })

    def tp_test_stop(self):
        """TP测试结束"""
        return self.send_json_pkt_get_resp({
            'cmd': 'TP', 'action': 'stop'
        })

    def motor_test_start(self):
        """Motor测试开始"""
        return self.send_json_pkt_get_resp({
            'cmd': 'MOTOR', 'action': 'start'
        })

    def motor_test_stop(self):
        """Motor测试结束"""
        return self.send_json_pkt_get_resp({
            'cmd': 'MOTOR', 'action': 'stop'
        })

    def gsensor_test_start(self):
        """G-sensor测试开始"""
        return self.send_json_pkt_get_resp({
            'cmd': 'GSENSOR', 'action': 'start'
        })

    def gsensor_test_stop(self):
        """G-sensor测试结束"""
        return self.send_json_pkt_get_resp({
            'cmd': 'GSENSOR', 'action': 'stop'
        })

    def wifi_open(self):
        """打开wifi"""
        return self.send_json_pkt_get_resp({
            'cmd': 'WIFI', 'action': 'start'
        })

    def wifi_close(self):
        """关闭wifi"""
        return self.send_json_pkt_get_resp({
            'cmd': 'WIFI', 'action': 'stop'
        })

    def set_wifi_freq(self, value=None):
        """设置wifi频段
            支持：2g|5g
        """
        return self.send_json_pkt_get_resp({
            'cmd': 'WIFI', 'action': 'set_wifi_freq', 'value': value
        })

    def iperf_tx_start(self, config):
        return self.send_json_pkt_get_resp({
            'cmd': 'WIFI', 'action': 'iperf_tx_start', 'config': config
        })

    def iperf_tx_stop(self):
        return self.send_json_pkt_get_resp({
            'cmd': 'WIFI', 'action': 'iperf_tx_stop'
        })

    def bt_wakeup(self):
        return self.send_json_pkt_get_resp({
            'cmd': 'BT', 'action': 'bt_wakeup'
        })

    def get_ble_wakeup_flag(self):
        return self.send_json_pkt_get_resp({
            'cmd': 'BT', 'action': 'get_ble_wakeup_flag'
        })

    def record_start(self, config: dict):
        """录像开始
        config: {"width": "3840", "height": "2160", "fps": "60",
        "codec": "H.264", "enable": "0", "bitrate": "100", "filetail": "0", "eis": "1"}
        """
        return self.send_json_pkt_get_resp({
            'cmd': 'RECORD', 'action': 'start', 'config': config
        })

    def record_stop(self):
        """停止录像"""
        return self.send_json_pkt_get_resp({
            'cmd': 'RECORD', 'action': 'stop'
        })

    def capture_start(self):
        """拍照开始"""
        return self.send_json_pkt_get_resp({
            'cmd': 'CAPTURE', 'action': 'start'
        })

    def capture_stop(self):
        """拍照结束"""
        return self.send_json_pkt_get_resp({
            'cmd': 'CAPTURE', 'action': 'stop'
        })

    def audio_start_record(self):
        """录音开始"""
        return self.send_json_pkt_get_resp({
            'cmd': 'AUDIO', 'action': 'start_record'
        })

    def audio_stop_record(self):
        """录音结束"""
        return self.send_json_pkt_get_resp({
            'cmd': 'AUDIO', 'action': 'stop_record'
        })

    def audio_start_start_play(self, file_path=None):
        """开始播放录音"""
        return self.send_json_pkt_get_resp({
            'cmd': 'AUDIO', 'action': 'start_play', 'file_path': file_path
        })

    def audio_stop_start_play(self):
        """停止播放录音"""
        return self.send_json_pkt_get_resp({
            'cmd': 'AUDIO', 'action': 'stop_play'
        })

    def button_test_start(self):
        """按键测试开始"""
        return self.send_json_pkt_get_resp({
            'cmd': 'BUTTON', 'action': 'start'
        })

    def button_test_stop(self):
        """按键测试结束"""
        return self.send_json_pkt_get_resp({
            'cmd': 'BUTTON', 'action': 'stop'
        })

    def set_config(self, config1=None, config2=None, config3=None, interval="3600"):
        """设置老化参数"""
        return self.send_json_pkt_get_resp({
            'cmd': 'AGING', 'action': 'set_config', 'period': interval, "config1": config1, "config2": config2,
            "config3": config3,
        })

    def get_age_result(self):
        """获取老化结果"""
        return self.send_json_pkt_get_resp({
            'cmd': 'AGING', 'action': 'get_result'
        })

    def power_off(self):
        """老化关机"""
        return self.send_json_pkt_get_resp({"cmd": "AGING", "action": "poweroff"})

    def reset_result(self):
        """reset老化结果"""
        return self.send_json_pkt_get_resp({"cmd": "AGING", "action": "reset_result"})

    def get_status_info(self):
        """获取老化状态信息"""
        return self.send_json_pkt_get_resp({"cmd":"AGING","action":"get_status_info"})

    def get_log_file(self):
        """获取日志文件"""
        return self.send_json_pkt_get_resp({
            'cmd': 'LOG', 'action': 'get'
        })

    # TODO: IMU的开始录像、结束录像

    def imu_start_calibration(self, count: str):
        """IMU校准"""
        return self.send_json_pkt_get_resp({
            'cmd': 'IMU', 'action': 'start_calibration', 'count': str(count)
        })

    def imu_set_offset(self, select: str = 'V1/V2/V3', value: str = '***'):
        return self.send_json_pkt_get_resp({
            'cmd': 'IMU', 'action': 'set_offset', 'select': select, 'value': value
        })

    def get_offset(self):
        """IMU标定参数获取"""
        return self.send_json_pkt_get_resp({"cmd": "IMU", "action": "get_offset"})

    # TODO: 近解析的拍照、远解析的拍照

    def image_wb_start(self):
        """设置白平衡参数"""
        pass

    def command(self, cmd):
        """相机执行命令行"""
        return self.send_json_pkt_get_resp({
            'cmd': 'COMMAND', 'action': cmd
        })

    def switch_burn_mode(self):
        return self.command('aip mmc debug send_event 11 1')

    def image_data_get(self):
        """获取flash中的图像校正数据在包装前检查时使用"""
        return self.send_json_pkt_get_resp({
            'cmd': 'COMMAND', 'action': "image_data_get"
        })


if __name__ == "__main__":
    api = API_Libusb('INSWWYYNXXXXXX')
    api.init_socket()
    api.init_app_socket_con()
    resp = api.send_json_pkt_get_resp({"action": "get_product_uuid", "cmd": "DEVICEINFO"})
    logger.info(f'resp {resp}')

    # logger.info(f'cam_info {api.cam_info}')
    # config = {"width": "3840", "height": "2160", "fps": "60",
    #          "codec": "H.264", "enable": "0", "bitrate": "100", "filetail": "0", "eis": "1"}
    # api.record_start(config)
    # time.sleep(3)
    # api.record_stop()

    # logger.info('结果录像。。。。。')
    # api.capture_start()
    # time.sleep(10)
    # stop_result = api.capture_stop()
    # file_path = stop_result.get('file_path')
    # file_path = '/DCIM/IMG.jpg'
    # if file_path:
    #     api.download_file(file_path, 'IMG.jpg')
    #
    # time.sleep(30)
    #
    logger.info('end')
