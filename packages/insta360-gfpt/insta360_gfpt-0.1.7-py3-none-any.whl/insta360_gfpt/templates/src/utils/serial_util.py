# _*_ coding:utf-8 _*_
import os
import re
import time
import serial
import logging
import datetime
import threading
import serial.tools.list_ports
import sys

from src.utils.logger import logger


def get_time():
    return datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S.%f')


def get_ser_ports():
    """可用端口"""
    plist = list(serial.tools.list_ports.comports())
    if len(plist) <= 0:
        logger.error("The Serial port not find! Please check serial driver or serial_line.")
        return []
    else:
        for port in plist:
            logger.info('端口：{}, 端口描述：{}'.format(port.device, port.description))
        return plist


class Serial:
    def __init__(self, port=None, baud_rate=115200):
        self.ser = serial.Serial()
        self.ser.port = port
        logger.info('open ser port: {}'.format(port))
        self.baud_rate = baud_rate
        self.log_file = None
        self.check_strs = []
        self.check_sign = False
        self.check_log = None
        self.all_log = []  # 存储当前打印的所有日志
        self.cur_res = ''

    def open_port(self, log_name=None):
        self.ser.baudrate = self.baud_rate  # 波特率
        if self.ser.is_open:
            logger.error("serial is alerady open, please check and close already user_app")
            return False
        else:
            self.ser.open()
            if not log_name:
                logger.info('不需记录日志')
                return True

            out_log_path = os.path.join(log_name)
            self.log_file = open(out_log_path, 'a+', encoding='utf-8')  # 创建接收文件
            return out_log_path

    def write(self, cmd):
        logger.info('serial send one cmd: {}'.format(cmd))
        self.ser.write(cmd.encode('utf-8'))
        # self.ser.write('\r'.encode('utf-8'))
        time.sleep(1)

    def write_AT(self, cmd):
        if isinstance(cmd, str):
            self.ser.write(cmd.encode('utf-8'))
            logger.info('serial send one cmd: {}'.format(cmd))
        else:
            self.ser.write(cmd)
            logger.debug('xxxxxxxxxxxxxxxxxxxxxxxxxxxx')
            logger.info(f'{cmd}')
            logger.debug('xxxxxxxxxxxxxxxxxxxxxxxxxxxx')
        time.sleep(2)
        return self.cur_res


    # 查找关键字是否存在串口日志中
    def from_serial_find_text(self, text, cmd, wait_time):
        self.write(cmd)
        time.sleep(wait_time)
        result = False
        for item in self.all_log:
            if text in item:
                print("找到需要的字符", item)
                result = True
        return result

    def register_check_str(self, c_str):
        if c_str not in self.check_strs:
            self.check_strs.append(c_str)
        return self.check_strs.index(c_str)

    def del_register_str(self, r_str):
        if r_str in self.check_strs:
            self.check_strs.remove(r_str)

    def clear_checks(self):
        self.check_strs = []

    def start_read(self):
        self.waitEnd = threading.Event()  # 将线程事件赋值给变量
        self.alive = True  # 改变条件变量值

        self.read_thread = threading.Thread(target=self.reader)  # 创建一个读取串口数据的线程
        self.read_thread.setDaemon(True)  # 调用线程同时结束的函数

        self.read_thread.start()  # 启动读数据线程

    def reader(self):
        while self.alive:  # 当条件变量为True时执行
            # data = self.ser.readline().decode("latin1", "ignore").strip()
            # data = self.ser.readline().decode('utf-8').strip()
            # logger.debug(data)
            # liblogging.info(data)
            # t_date = get_time()
            # r_data = f'{t_date}: {data}\n'
            # self.log_file.write(r_data)
            # self.log_file.flush()
            # for check_index, check_s in enumerate(self.check_strs):
            #     res = re.search(check_s, data)  # 支持正则
            #     if res is not None and res.group():
            #         self.check_sign = check_index
            #         self.check_log = data
            #         break
            #     elif data.find(check_s) != -1:
            #         self.check_sign = check_index
            #         self.check_log = data
            #         break
            # # 用正则表达式过滤一下
            # if "[" in data:
            #     pattern = re.compile(r'20.*]')
            #     s_result = pattern.search(data)
            #     if s_result is not None:
            #         new_data = (data.replace(s_result.group(), "")).strip()  # 过滤掉时间部分，获得真正的日志
            #         self.all_log.append(new_data)  # 将所有日志存起来
            try:
                data = self.ser.readline().decode("latin1", "ignore").strip()
                self.cur_res = ''
                logger.debug(f'-------------------{data}')
                self.cur_res = data

                # data = self.ser.readline().decode('utf-8').strip()
                # logger.debug(data)
                # lib_logging.info(data)
                t_date = get_time()
                r_data = f'{t_date}: {data}\n'
                # self.log_file.write(r_data)
                r_data = r_data.replace('\x00', ' ')
                r_data = r_data.replace('\x1b[0m', ' ')
                r_data = r_data.replace('\x1b[0;32m', ' ')
                r_data = r_data.replace('\x1b[31;22m', ' ')
                r_data = r_data.replace('\x1b[32;22m', ' ')
                r_data = r_data.replace('\x1b[34;22m', ' ')
                self.log_file.write(r_data)
            except BaseException as e:
                import traceback
                traceback.print_exc()
                info = traceback.format_exc()
                logger.error(info)
                raise e
            finally:
                # self.log_file.flush()
                self.log_file.flush()

    def waiting(self):
        # 等待event停止标志
        if self.waitEnd is not None:
            # logger.info('exit thread')
            self.waitEnd.wait()  # 改变线程事件状态为False，使线程阻止后续程序执行

    # 关闭串口、保存文件
    def stop(self):
        self.alive = False
        if self.ser.isOpen():
            self.ser.close()
        self.log_file.close()

    def check_str(self, c_str, cmd=None, time_out=1, cmd_step_time=0.5):
        register_id = self.register_check_str(c_str)
        if cmd is not None:
            cmd_step = cmd.split(',')
            for c in cmd_step:
                time.sleep(cmd_step_time)
                self.write(c)
        for i in range(time_out * 2):
            logger.info('register_id {} check: {}, {}'.format(register_id, c_str, self.check_sign))
            if self.check_sign is not False and register_id == self.check_sign:
                self.check_sign = False
                logger.info('yes, check out **{}** from: {}'.format(c_str, self.check_log))
                self.del_register_str(c_str)
                return self.check_log
            else:
                self.check_sign = False

            time.sleep(0.5)
        self.del_register_str(c_str)
        return None


def pack_str():
    pack_val = "AT+ADVDAT=" + chr(int("0x00", 16)) + chr(int("0x5D", 16)) + "XXXXXX" + chr(int("0x01", 16))
    print(pack_val)
    res = str2hex(pack_val)
    # pack_val = bytearray(pack_val, 'utf-8')
    return res

def new_func():
    data = []
    for x in 'AT+ADVDAT=':
        # 字符 -> 10进制整形 -> 16进制字符
        data.append((ord(x)))
        # data.append(hex(ord(x)))

    data.append(int(0x5D))
    data.append(int(0x00))

    for x in 'XXXXXX':
        data.append(ord(x))

    data.append(int(0x01))

    print(data)
    print(bytearray(data))
    return data

def str2hex(str_val):
    by = bytes(str_val, 'utf-8')
    hex_str = by.hex()
    a = int(hex_str, 16)
    result = hex(a)
    print(result)
    return result

def test1():
    bytearray("AT+ADVDAT=")


if __name__ == '__main__':
    port = None
    ports = get_ser_ports()
    for p in ports:
        if p.pid == 60000 and p.vid == 4292:
            port = p.name
            break
    ser = Serial(port)
    ser.open_port("xxxxxxxx.log")
    ser.start_read()
    time.sleep(3)
    SET_CLOSE_BROADCAST = "AT+ADV=0"
    SET_BROADCAST_INTEL_VAL = "AT+ADVINTV=32"
    SET_BROADCAST_POWER = "AT+IPWR=0"
    SET_BROADCAST_DATA = "AT+ADVDAT="
    SET_OPEN_BROADCAST = "AT+ADV=1"

    result1 = ser.write_AT(SET_CLOSE_BROADCAST)
    time.sleep(2)

    result2 = ser.write_AT(SET_BROADCAST_INTEL_VAL)
    time.sleep(2)
    result3 = ser.write_AT(SET_BROADCAST_POWER)
    time.sleep(2)
    result4 = ser.write_AT(new_func())
    time.sleep(2)
    result5 = ser.write_AT(SET_OPEN_BROADCAST)
    # ser.open_port(sys.argv[2])
    # ser.start_read()
    time.sleep(99999)
