import datetime
import os

import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_tcp as modbus_tcp
import time
from func_timeout import func_set_timeout
import func_timeout
import serial
import binascii
from loguru import logger
from ctypes import *
# PC100近景解析转台
class NearTurntable(object):
    def __init__(self):
        self.bps = 9600
        self.timeout = 5

    def direction0(self, port="COM2"):
        # 控制继电器断开,默认状态（假设接线是常开）
        #打开串口
        try:
            ser = serial.Serial(port, self.bps, timeout=self.timeout)
            time.sleep(0.5)
            send_data = [0xA0, 0x01, 0x02, 0xA3]
            retry = 3
            while retry > 0:
                retry -= 1
                ser.write(send_data)
                read_data = str(binascii.b2a_hex(ser.read(4)))[2:-1]
                if read_data == "a00100a1":
                    ser.close()
                    return True
                else:
                    time.sleep(0.2)
            else:
                ser.close()
                return False
        except Exception as e:
            logger.error(f"控制继电器断开时发生错误：{e}")

    def direction1(self, port="COM2"):
        # 控制继电器闭合
        # 打开串口
        try:
            ser = serial.Serial(port, self.bps, timeout=self.timeout)
            time.sleep(0.5)
            send_data = [0xA0, 0x01, 0x03, 0xA4]
            retry = 3
            while retry > 0:
                retry -= 1
                ser.write(send_data)
                read_data = str(binascii.b2a_hex(ser.read(4)))[2:-1]
                if read_data == "a00101a2":
                    ser.close()
                    return True
                else:
                    time.sleep(0.2)
            else:
                ser.close()
                return False
        except Exception as e:
            logger.error(f"控制继电器闭合时发生错误：{e}")

    def read_direction(self, port, expect_data):
        # 读取继电器状态
        # 打开串口
        try:
            ser = serial.Serial(port, self.bps, timeout=self.timeout)
            time.sleep(0.5)
            send_data = [0xA0, 0x01, 0x05, 0xA6]
            ser.write(send_data)
            retry = 3
            while retry > 0:
                retry -= 1
                read_data = str(binascii.b2a_hex(ser.read(4)))[2:-1]
                return read_data
                if read_data == expect_data:
                    ser.close()
                    return True
                else:
                    time.sleep(0.5)
            else:
                ser.close()
                return False
        except Exception as e:
            logger.error(f"读取继电器状态时发生错误：{e}")


# PC1002.5m远景解析转台
class Turntable(object):
    def __init__(self, host_ip="192.168.1.5"):
        self.master = None
        self.host = host_ip
        self.registers_write = {"Middle": 4097, "UP": 4098, "Left": 4099, "Down": 4100, "Right": 4101,
                                "Middle2": 4102, "UP2": 4103, "Left2": 4104, "Down2": 4105, "Right2": 4106, "Reset": 4096}
        self.registers_read = {"Middle": 4107, "UP": 4108, "Left": 4109, "Down": 4110, "Right": 4111,
                               "Middle2": 4112, "UP2": 4113, "Left2": 4114, "Down2": 4115, "Right2": 4116, "Reset": 4117}
        self.direction = "Middle"

    def run(self, direct):
        try:
            # 仿真调试可以使用本机地址: 127.0.0.1
            # 实际使用PLC地址,将 client 的地址设置在于 server 同一频段下,host填写 server 的地址
            self.direction = direct
            self.master = modbus_tcp.TcpMaster(host=self.host)
            self.master.set_timeout(5.0)
            register = self.registers_write.get(self.direction)
            self.master.execute(1, cst.WRITE_SINGLE_REGISTER, register, output_value=1)
            logger.info(f'{self.direction}：保持寄存器{str(register)}写入1')
            res = self.read_register()
            return res

        except func_timeout.exceptions.FunctionTimedOut as e:
            logger.error(f"发生超时错误，{str(e)}")
            return False
        except modbus_tk.modbus.ModbusError as e:
            logger.error("%s- Code=%d" % (e, e.get_exception_code()))
            return False
        except Exception as e:
            logger.error(str(e))
            return False

    @func_set_timeout(30)
    def read_register(self):
        # 循环读取寄存器，判断旋转是否到位;到位后把该寄存器写入0
        register = self.registers_read.get(self.direction)
        result_int = 0
        res = False
        logger.info(f'{self.direction}：循环读取保持寄存器{str(register)}中...')
        while result_int != 1:
            time.sleep(0.5)
            result_int = self.master.execute(1, cst.READ_HOLDING_REGISTERS, register, 1)[0]
        else:
            self.master.execute(1, cst.WRITE_SINGLE_REGISTER, register, output_value=0)
            logger.info(f'{self.direction}：旋转到位，保持寄存器{str(register)}写入0')
            res = True
        logger.info(str(res))
        return res

# PC100相机标定转台
# 相机标定转台顺序必须是：Down-Up-Right-Front-Left-Back；中间可以加Reset，Reset后需要从Down再开始。
# 输入”Down“表示启动转台，转台会转动到”Down“位置，到位信号的保持寄存器更新为1，等待拍照；
# 拍照完成后，输入”Up“，会把”Down“的到位保持器更新为3，然后转台旋转到”Up“位置，”Up“的到位信号寄存器更新为1；以此类推.
class Calibration(object):
    def __init__(self, host_ip="192.168.1.5"):
        # "127.0.0.1"，"192.168.1.5"
        self.host = host_ip
        self.registers_write = {"Down": 4097, "Reset": 4096}
        self.registers_rw = {
            "Down": 4098, "Up": 4099, "Right": 4100, "Back": 4101, "Left": 4102, "Front": 4103, "Reset": 4116
        }
        self.registers_exception = {
            "Flip_cylinder_origin": 4136, "Flip_cylinder_point": 4137, "Jacking_cylinder_origin": 4138,
            "Jacking_cylinder_point": 4139, "Stepper_motor_exceeds_limit": 4140
        }

    def start(self):
        try:
            master = modbus_tcp.TcpMaster(host=self.host)
            master.set_timeout(5.0)
            self.read_exception(master)
            time.sleep(0.2)
            return master
        except Exception as e:
            logger.error(e)
            return e

    def run(self, master, direction):
        try:
            self.direction = direction
            if self.direction == "Reset":
                result = self.Reset(master)
            elif self.direction == "Down":
                master.execute(1, cst.WRITE_SINGLE_REGISTER, self.registers_write.get("Down"), output_value=1)
                logger.info(f'{direction}：设备启动，{str(self.registers_write.get("Down"))}写入1')
                result = self.read_register(master, self.registers_rw.get("Down"))
            else:
                # 将上一个位置的到位信号置3，才能进行下一步运转
                w_register = self.registers_rw.get(self.direction) - 1
                master.execute(1, cst.WRITE_SINGLE_REGISTER, w_register, output_value=3)
                logger.info(f"{direction}:上一位置到位信号寄存器{w_register}更新为3")
                logger.info(f"{direction}:设备旋转中...")
                result = self.read_register(master, self.registers_rw.get(direction))
            return result, "no error"

        except func_timeout.exceptions.FunctionTimedOut as e:
            logger.error(f"发生超时错误，{str(e)}")
            return False, e
        except modbus_tk.modbus.ModbusError as e:
            logger.error("%s- Code=%d" % (e, e.get_exception_code()))
            return False, e
        except Exception as e:
            logger.error(e)
            return False, e

    @func_set_timeout(30)
    def read_register(self, master, register):
        # 循环读取寄存器，判断旋转是否到位
        result_int = 0
        result = False
        logger.info(f'{self.direction}：循环读取保持寄存器{str(register)}中...')
        while result_int != 1:
                time.sleep(0.5)
                result_int = master.execute(1, cst.READ_HOLDING_REGISTERS, register, 1)[0]
        else:
            logger.info(f'{self.direction}：旋转到位')
            result = True
        return result

    def Reset(self, master):
        # 写入Reset信号，并等待Reset结束;结束后将到位信号更新为0
        register = self.registers_write.get("Reset")
        r_register = self.registers_rw.get("Reset")
        logger.info(f"{self.direction}:Reset中...")
        master.execute(1, cst.WRITE_SINGLE_REGISTER, register, output_value=1)
        result = self.read_register(master, r_register)
        master.execute(1, cst.WRITE_SINGLE_REGISTER, r_register, output_value=0)
        if result:
            logger.info(f"{self.direction}:Reset完成，到位信号寄存器{r_register}更新为0")
        else:
            logger.info(f"{self.direction}:复位不成功")
        return result

    def read_exception(self, master):
        # 读取几个异常信号的寄存器
        results_int = master.execute(1, cst.READ_HOLDING_REGISTERS, self.registers_exception.get("Flip_cylinder_origin"), 5)
        error_list = []
        for i in range(0,5):
            if results_int[i] == 1:
                error_list.append(list(self.registers_exception.keys())[i])
        if sum(results_int) != 0:
            raise Exception(f"{','.join(str(i) for i in error_list)}")


class IAC2Turntable(Turntable):
    # IAC2的远景解析转台
    def __init__(self, host_ip="192.168.250.111"):
        super(IAC2Turntable, self).__init__()
        # self.host = "192.168.250.111"
        self.host = host_ip
        self.registers_write = {"Location1": 1, "Location2": 2, "Location3": 3, "Location4": 4,
                                "Location5": 5, "Reset": 0}
        self.register = 20
        self.registers_read = {"Location1": 2, "Location2": 4, "Location3": 8, "Location4": 10,
                                "Location5": 20, "Reset": 1}
        self.direction = "Location1"
        self.master = None

    @func_set_timeout(30)
    def read_register(self):
        register = self.registers_read.get(self.direction)
        # 循环读取寄存器，判断旋转是否到位;到位后把控制指令清零
        result_int = 0
        res = False
        logger.info(f'{self.direction}：循环读取保持寄存器{self.register}中...')
        while result_int != register:
            time.sleep(0.5)
            result_int = self.master.execute(1, cst.READ_HOLDING_REGISTERS, self.register, 1)[0]
        else:
            #写入的寄存器清0，这个需要跟供应商确认是否需要这一步
            self.master.execute(1, cst.WRITE_SINGLE_REGISTER, self.registers_write.get(self.direction), output_value=0)
            logger.info(f'{self.direction}：旋转到位，保持寄存器{self.registers_write.get(self.direction)}写入0')
            res = True
        return res
class VBJN1TurnTable():
    def __init__(self, JN1port="COM6"):
        self.now_time = datetime.datetime.now()
        root = os.getcwd()
        dll_path = f"{root}\\tools\\mc_cotrol"
        os.environ['PATH'] = dll_path + ';' + os.environ['PATH']
        root = os.getcwd()
        txt = f"{root}\\tools\\mc_cotrol\\CommonLib.dll"
        logger.info("dll地址: "+txt)
        self.dll = WinDLL(txt)
        logger.info("dll已打开")
        logger.info(f"端口: {JN1port}")
        pCom = c_char_p(bytes(JN1port, "gbk"))
        ret = self.dll.mc_init(pCom)
        logger.info(f"连接端口: {ret}")
        self.is_open = False
        if ret == 0:
            self.dll.mc_getState.restype = c_int
            self.dll.mc_getState.argtypes = [POINTER(c_int), ]
            res = self.dll.mc_reset()
            logger.info(f"初始化: {res}")
            ress = self.dll.mc_home_move()
            if ress ==1:
                ress = self.dll.mc_home_move()
            logger.info(f"回原点: {ress}")
            self.is_open = True


        else:
            logger.info("连接端口失败")

    def get_status(self):
        state = c_int()

        repp = self.dll.mc_getState(byref(state))
        if repp == 0:
            return state.value
        else:
            return -1

    def wait_sleep(self, time_out=10):
        now_time = datetime.datetime.now()
        status_flag = False
        while (datetime.datetime.now() - now_time).total_seconds() <= time_out:
            resp = self.get_status()
            if resp == 2:
                status_flag = True
                break
            time.sleep(0.5)
        return status_flag
    def move(self, light_Dis:int, glass_Dis:int, table_dis:int):
        logger.info("开始移动")

        if self.wait_sleep(120):
            logger.info(f"参数：light_Dis:{light_Dis},  glass_Dis: {glass_Dis}, table_dis: {table_dis}")
            self.dll.mc_absolute_move.argtypes = [c_float, c_float, c_float, c_int]
            ret = self.dll.mc_absolute_move(light_Dis, glass_Dis, table_dis, 1500)
            logger.info(f"移动ret: {ret}")
            if ret == 0:

                return self.wait_sleep(120)
            else:
                return False
        else:
            logger.info("设备状态不对！")
            return
    def close_mc(self):
        ret = self.dll.mc_close()
        return ret

class VBTurntable():
    def __init__(self, port="COM3"):
        self.com = serial.Serial(port=port, baudrate=9600, timeout=0.8, bytesize=7, parity='E', stopbits=1)
        self.set_reset = ":010610000001"
        self.reset_reset = ":010610150000"
        self.read_reset = ":010310150001"

        self.set_local = {
            "中间": ":010610010001",
            "左上": ":010610020001",
            "左下": ":010610030001",
            "右上": ":010610040001",
            "右下": ":010610050001"
        }
        self.read_local = {
            "中间": ":0103100B0001",
            "左上": ":0103100C0001",
            "左下": ":0103100D0001",
            "右上": ":0103100E0001",
            "右下": ":0103100F0001"
        }
        self.reset_local = {
            "中间": ":0106100B0000",
            "左上": ":0106100C0000",
            "左下": ":0106100D0000",
            "右上": ":0106100E0000",
            "右下": ":0106100F0000"
        }

    def is_reset_complete(self, time_out=20):
        import datetime
        now_time = datetime.datetime.now()
        while ((datetime.datetime.now() - now_time).total_seconds() <= time_out):
            sendbytes = self.write_data(self.read_reset)
            # 将hexstr导入bytes对象  报文需要是字节格式
            sendbytes = bytes.fromhex(sendbytes)
            logger.info(sendbytes)
            # 发送报文
            self.com.write(sendbytes)
            xx = self.com.readall()
            logger.info(f'原始回复：{xx}')
            if xx:
                logger.info('转义后')
                mm = str(xx, encoding="utf-8")
                if ":0106100B0000DE" in mm:
                    logger.info("重置完成")
                    return True
        return False

    def is_set_completed(self, data):
        import datetime
        now_time = datetime.datetime.now()
        while ((datetime.datetime.now() - now_time).total_seconds() <= 30):
            time.sleep(1)
            sendbytes = self.write_data(data)
            # 将hexstr导入bytes对象  报文需要是字节格式
            sendbytes = bytes.fromhex(sendbytes)
            logger.info(sendbytes)
            # 发送报文
            self.com.write(sendbytes)
            xx = self.com.readall()
            logger.info(f'原始回复：{xx}')
            if xx:
                logger.info('转义后')
                mm = str(xx, encoding="utf-8")
                if ":0103020001" in mm:
                    logger.info("转动完成")
                    return True
        return False
    def calculate_lrc(self, ascii_str):
        lrc = 0
        data = bytearray.fromhex(ascii_str)
        for c in data:
            lrc += c
        xx = (256 - (lrc % 256)) % 256
        return hex(xx)[2:].zfill(2).upper()
    def write_data(self, xx):
        mm = self.calculate_lrc(xx[1:])
        xx = xx + mm
        sendbytes = ''
        for i in xx:
            if sendbytes == '':
                sendbytes += f"{hex(ord(i))[2:].upper()}"
            else:
                sendbytes += f" {hex(ord(i))[2:].upper()}"
        sendbytes = sendbytes + " " + "0D" + " " + "0A"
        # 生成完整报文"
        # print("-----------------")
        # print("将发送的报文:")
        # print(sendbytes)
        return sendbytes

    def is_reset_complete(self, data):
        import datetime
        now_time = datetime.datetime.now()
        flag = False
        while ((datetime.datetime.now() - now_time).total_seconds() < 10):
            time.sleep(1)
            sendbytes = self.write_data(data)
            # 将hexstr导入bytes对象  报文需要是字节格式
            sendbytes = bytes.fromhex(sendbytes)
            self.com.write(sendbytes)
            xx = self.com.readall()
            logger.info(f'原始回复：{xx}')
            if xx:

                mm = str(xx, encoding="utf-8")
                if data in mm:
                    logger.info("标志位重置完成")
                    flag = True
                    break
                else:
                    logger.info("标志位未重置完成")
        if flag:
            return True
        else:
            return False
    def reset_table(self):
        time.sleep(1)
        logger.info("开始复位相机")
        sendbytes = self.write_data(self.reset_reset)
        # 将hexstr导入bytes对象  报文需要是字节格式
        sendbytes = bytes.fromhex(sendbytes)
        logger.info(sendbytes)
        # 发送报文
        self.com.write(sendbytes)
        time.sleep(1)
        sendbytes = self.write_data(self.set_reset)
        # 将hexstr导入bytes对象  报文需要是字节格式
        sendbytes = bytes.fromhex(sendbytes)
        logger.info(sendbytes)
        # 发送报文
        self.com.write(sendbytes)
        time.sleep(1)
        logger.info("读是否复位完成")
        result = self.is_set_completed(self.read_reset)
        if result:
            logger.info("复位完成")
            return True
        else:
            logger.info("复位未完成")
            return False
    def turn_table(self, location="中间"):

        logger.info(f"开始移动到{location}位置")
        sendbytes = self.write_data(self.set_local[location])
        # 将hexstr导入bytes对象  报文需要是字节格式
        sendbytes = bytes.fromhex(sendbytes)
        logger.info(sendbytes)
        # 发送报文
        self.com.write(sendbytes)
        time.sleep(1)
        result = self.is_set_completed(self.read_local[location])
        if result:
            logger.info(f"设置{location}完成")
            return True
        else:
            logger.error(f"设置{location}未完成")
            return False


    def reset_flag(self, location="中间"):
        logger.info(f"开始重置{location}标志位")
        return self.is_reset_complete(self.reset_local[location])



if __name__ == "__main__":

    try:
        ser = serial.Serial("COM19", 9600, timeout=10)
        time.sleep(0.5)
        send_data = [0x88, 0xAE, 0x00, 0x11]
        retry = 3
        ser.write(send_data)
        while retry > 0:
            retry -= 1

            read_data = str(binascii.b2a_hex(ser.read(4)))[2:-1]
            logger.info(read_data)
            if read_data == "a00100a1":
                ser.close()

            else:
                time.sleep(0.2)
        else:
            ser.close()

    except Exception as e:
        logger.error(f"控制继电器断开时发生错误：{e}")
    # def is_reset_complete(self, data):
    #     import datetime
    #     now_time = datetime.datetime.now()
    #     flag = False
    #     while ((datetime.datetime.now() - now_time).total_seconds() < 10):
    #         time.sleep(1)
    #         self.com.write(data)
    #         xx = self.com.readall()
    #         logger.info(f'原始回复：{xx}')
    #         if xx:
    #
    #             mm = str(xx, encoding="utf-8")
    #             if data in mm:
    #                 logger.info("标志位重置完成")
    #                 flag = True
    #                 break
    #             else:
    #                 logger.info("标志位未重置完成")
    #     if flag:
    #         return True
    #     else:
    #         return False
    #
    #
    #
    #
    # # def reset_table(self):
    # #     time.sleep(1)
    # #     logger.info("开始复位相机")
    # #     self.com.write(reset_reset)
    # #     time.sleep(1)
    # #     self.com.write(set_reset)
    # #     time.sleep(1)
    # #     logger.info("读是否复位完成")
    # #     result = is_set_completed(read_reset)
    # #     if result:
    # #         logger.info("复位完成")
    # #         return True
    # #     else:
    # #         logger.info("复位未完成")
    # #         return False
    #
    #
    #
    # def calculate_lrc(ascii_str):
    #     lrc = 0
    #     data = bytearray.fromhex(ascii_str)
    #     for c in data:
    #         lrc += c
    #     xx = (256 - (lrc % 256)) % 256
    #     return hex(xx)[2:].zfill(2).upper()
    # def write_data(xx):
    #     mm = calculate_lrc(xx[1:])
    #     xx = xx + mm
    #     sendbytes = ''
    #     for i in xx:
    #         if sendbytes == '':
    #             sendbytes += f"{hex(ord(i))[2:].upper()}"
    #         else:
    #             sendbytes += f" {hex(ord(i))[2:].upper()}"
    #     sendbytes = sendbytes + " " + "0D" + " " + "0A"
    #     # 生成完整报文"
    #     # print("-----------------")
    #     # print("将发送的报文:")
    #     # print(sendbytes)
    #     return sendbytes
    #
    # def reset_table(self):
    #     time.sleep(1)
    #     logger.info("开始复位相机")
    #     sendbytes = self.write_data(self.reset_reset)
    #     sendbytes = bytes.fromhex(sendbytes)
    #     logger.info(sendbytes)
    #     # 发送报文
    #     self.com.write(sendbytes)
    #     time.sleep(1)
    #     sendbytes = self.write_data(self.set_reset)
    #     # 将hexstr导入bytes对象  报文需要是字节格式
    #     sendbytes = bytes.fromhex(sendbytes)
    #     logger.info(sendbytes)
    #     # 发送报文
    #     self.com.write(sendbytes)
    #     time.sleep(1)
    #     logger.info("读是否复位完成")
    #     result = self.is_set_completed(self.read_reset)
    #     if result:
    #         logger.info("复位完成")
    #         return True
    #     else:
    #         logger.info("复位未完成")
    #         return False
    #
    #
    # set_reset = ":010610000001"
    # reset_reset = ":010610150000"
    # read_reset = ":010310150001"
    #
    # set_local = {
    #     "中间": ":010610010001",
    #     "左上": ":010610020001",
    #     "左下": ":010610030001",
    #     "右上": ":010610040001",
    #     "右下": ":010610050001"
    # }
    # read_local = {
    #     "中间": ":0103100B0001",
    #     "左上": ":0103100C0001",
    #     "左下": ":0103100D0001",
    #     "右上": ":0103100E0001",
    #     "右下": ":0103100F0001"
    # }
    # reset_local = {
    #     "中间": ":0106100B0000",
    #     "左上": ":0106100C0000",
    #     "左下": ":0106100D0000",
    #     "右上": ":0106100E0000",
    #     "右下": ":0106100F0000"
    # }
    #
    # sendbytes = write_data(read_reset)
    #
    # sendbytes = bytes.fromhex(sendbytes)
    # logger.info(f"{sendbytes}")


    # 相机标定转台自动调试
    # while True:
    #     try:
    #         start_now = input("是否准备启动Y/N：")
    #         if start_now == "Y" or start_now == "y":
    #             cal = Calibration("127.0.0.1")
    #             master = cal.start()
    #             direction = ["Down", "Up", "Right", "Back", "Left", "Front", "Reset"]
    #             for i in range(0,7):
    #                 result = cal.run(master, direction[i])
    #                 time.sleep(0.2)
    #                 if result[0] and i<6:
    #                     print("转动到位，等待3s后，自动转动到下一位置")
    #                     time.sleep(3)
    #                     continue
    #                 elif result[0] and i==6:
    #                     print("已经全部旋转到位，并复位")
    #                 else:
    #                     print("未转动到位，请重新开始")
    #                     break
    #             continue
    #         else:
    #             continue
    #     except Exception as e:
    #         print("发生错误：" + str(e))
    #         continue
    #     2.5m解析转台手动调试
    # while True:
    #     try:
    #         turn = Turntable("127.0.0.1")
    #         direction = input("请输入方向（Middle,UP,Left,Down,Right,Middle2,UP2,Left2,Down2,Right2,Reset）：")
    #         if direction in ["Middle","UP","Left","Down","Right","Middle2","UP2","Left2","Down2","Right2","Reset"]:
    #             result = turn.run(direction)
    #             time.sleep(0.2)
    #             continue
    #         else:
    #             print("输入有误")
    #             continue
    #     except Exception as e:
    #         print("发生错误："+str(e))
    #         continue
    # 2.5m解析转台自动调试
    # while True:
    #     try:
    #         start_now = input("是否准备启动Y/N：")
    #         if start_now == "Y" or start_now == "y":
    #             turn = Turntable("127.0.0.1")
    #             direction = ["Middle", "UP", "Left", "Down", "Right", "Middle2", "UP2", "Left2", "Down2", "Right2",
    #                              "Middle"]
    #             for i in range(0,11):
    #                 result = turn.run(direction[i])
    #                 time.sleep(0.2)
    #                 if result[0] and i<10:
    #                     print("转动到位，等待3s后，自动转动到下一位置")
    #                     time.sleep(3)
    #                     continue
    #                 elif result[0] and i==10:
    #                     print("已经全部旋转到位，并复位")
    #                 else:
    #                     print("未转动到位，请重新开始")
    #                     break
    #             continue
    #         else:
    #             continue
    #     except Exception as e:
    #         print("发生错误：" + str(e))
    #         continue
    # IAC2的转台自动测试
    # while True:
    #     try:
    #         start_now = input("是否准备启动Y/N：")
    #         if start_now == "Y" or start_now == "y":
    #             turn = IAC2Turntable("127.0.0.1)
    #             direction = ["Location1", "Location2", "Location3", "Location4", "Location5", "Location1"]
    #             for i in range(0,6):
    #                 result = turn.run(direction[i])
    #                 time.sleep(0.2)
    #                 if result[0] and i<5:
    #                     print("转动到位，等待3s后，自动转动到下一位置")
    #                     time.sleep(3)
    #                     continue
    #                 elif result[0] and i==5:
    #                     print("已经全部旋转到位，并回到位置1")
    #                 else:
    #                     print("未转动到位，请重新开始")
    #                     break
    #             continue
    #         else:
    #             continue
    #     except Exception as e:
    #         print("发生错误：" + str(e))
    #         continue

    # IAC2转台手动调试
    # while True:
    #     try:
    #         turn = IAC2Turntable("127.0.0.1")
    #         direction = input("请输入方向（Location1,Location2,Location3,Location4,Location5,Reset）：")
    #         if direction in ["Location1","Location2","Location3","Location4","Location5","Reset"]:
    #             result = turn.run(direction)
    #             time.sleep(0.2)
    #             continue
    #         else:
    #             print("输入有误")
    #             continue
    #     except Exception as e:
    #         print("发生错误："+str(e))
    #         continue
