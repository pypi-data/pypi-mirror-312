#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :ins_libusb.py
# @Time      :2022/7/11 16:25
# @Author    :lilinhong
"""
https://github.com/Insta360Develop/CameraSDK-Cpp
https://gitlab.insta360.com/desktop-dev/factorycamerasdk
"""
import os
import sys
import time

import usb1
import socket
import random
import requests
import traceback
import threading
# import cv2 as cv
from src.device.fw_api.packet import *
from src.device.fw_api.util_libusb import *
from src.device.fw_api.proto.message_code_pb2 import MessageCode
from src.utils.logger import logger


class Ins_Libusb:

    # http://www.usbzh.com/article/detail-244.html
    # Arashi Vision Inc.厂商编号 11802
    VENDOR_ID_insta360 = 0x2E1A
    PRODUCT_ID = 0x0002
    INTERFACE_POINT = 0x0
    WRITE_END_POINT = 0x01
    READ_END_POINT = 0x81
    ss_pkt_timeout = 90

    class TYPE_CONNECT(Enum):
        LIBUSB = 'libusb'
        SOCKET = 'socket'
        SERIAL = 'serial'

    def __init__(self, cam_usb_sn: str):

        self.cam_usb_sn: str = cam_usb_sn

        # packet包的ID
        self.pkt_id: int = 1
        # 记录连接状态
        self.is_con: bool = False
        self._beat_list: list = []
        self._read_thread: threading.Thread = None
        self._heartbeat_thread: threading.Thread = None
        self._lock: threading.Lock = threading.Lock()

        self._pkt_map: dict = {}
        self._pkt_map_st: dict = {}

        self.type_connect: Enum = None
        if not (cam_usb_sn is None):
            self.type_connect = self.TYPE_CONNECT.LIBUSB
        else:
            assert False

        if self.type_connect == self.TYPE_CONNECT.LIBUSB:
            # 走libusb
            self.usb_vendor_id = self.VENDOR_ID_insta360
            self._usb_context: usb1.USBContext = None
            self._usb_device: usb1.USBDevice = None
            self.info_usb_device = None
            self._usb_dh: usb1.USBDeviceHandle = None
            self.info_usb_device_handle: dict = None
            self.Product = None
            self.SerialNumber = None
        self.factory_dev_id = None
        self.log_tag_dev_id = ''

    def init_socket(self, usb_device=None, usb_context=None):
        """
        通过Socket、Libusb连接设备
        """
        try:
            if (usb_device is None) and (usb_context is None):
                usb_device, usb_context = get_usb_device_sn(cam_sn=self.cam_usb_sn, vendor_id=self.usb_vendor_id)
            self._usb_device: usb1.USBDevice = usb_device
            self._usb_context: usb1.USBContext = usb_context
            self.info_usb_device = get_device_info(self._usb_device)
            logger.info(f'device 信息 {self.info_usb_device}')
            self._usb_dh = self._usb_device.open()
            self._usb_dh.claimInterface(self.INTERFACE_POINT)
            self.info_usb_device_handle = get_device_handle_info(self._usb_dh)
            self.Product = self.info_usb_device_handle['Product']
            self.SerialNumber = self.info_usb_device_handle['SerialNumber']
            logger.info(f'device handle信息 {self.info_usb_device_handle}')
            self.factory_dev_id = self.info_usb_device["DeviceAddress"]
            self.log_tag_dev_id = f'{self.SerialNumber}_{self.factory_dev_id}:'
            logger.info(f'{self.log_tag_dev_id}打开设备完成：{self.info_usb_device["usb_id"]}')
            self.is_con = True

            # 开启读response线程
            self._read_thread = threading.Thread(target=self._read_packet, name='reader', daemon=True)
            self._read_thread.start()
            # 发送sync
            # self._send_sync_packet()
            self.pkt_id += 1
            # 开启心跳线程
            # self._heartbeat_thread = threading.Thread(target=self._heartbeat, name='heartbeat', daemon=True)
            # self._heartbeat_thread.start()
        except Exception as e:
            logger.error('检查下是否有libusbk的驱动')
            logger.error(e)

    def _send_sync_packet(self, timeout: float = 10):
        """连接成功后发送sync包"""
        pkt_sync = Sync_Packet()
        self._send_packet(pkt=pkt_sync)
        t_s = time.time()
        while (time.time() - t_s) < timeout:
            if len(self._beat_list) > 0:
                return pkt_sync
        raise RuntimeWarning('没有收到sync包回复')

    def _send_packet(self, pkt: Packet):
        """发送packet"""
        if self._usb_dh is None:
            self.init_socket()

        self._lock.acquire()
        try:
            # self.pkt_id += 1
            if pkt.packet_type == Packet.TYPE_ENUM.MESSAGE:
                pkt_msg: Message_Packet = pkt
                pkt_msg.stream_id = self.pkt_id
            elif pkt.packet_type == Packet.TYPE_ENUM.JSON_MESSAGE:
                pkt_json: JSON_Packet = pkt
                pkt_json.packet_id = self.pkt_id
                pkt_json.factory_dev_id = self.factory_dev_id
            else:
                pass
            # if not pkt.packet_type == Packet.TYPE_ENUM.SOCKET_TUNNEL:
            logger.info(f'{self.log_tag_dev_id}pkt send：{self.pkt_id}，{pkt}')
            if self.type_connect == self.TYPE_CONNECT.LIBUSB:
                if not self._usb_dh:
                    return None
                send_ret = self._usb_dh.bulkWrite(self.WRITE_END_POINT, pkt.build(), timeout=0)
                # logger.info(f'debug_send_ret, {send_ret}, pkt length, {pkt.length}')
            return pkt
        except BaseException as e:
            emsg = traceback.format_exc()
            logger.error(f'{self.log_tag_dev_id} _send_packet BaseException {emsg}')
            self.close()
            raise e
        except Exception as e:
            emsg = traceback.format_exc()
            logger.error(f'{self.log_tag_dev_id} _send_packet Exception {emsg}')
            self.close()
            raise e
        finally:
            self.pkt_id += 1
            self._lock.release()

    def _heartbeat(self, interval=2):
        """心跳线程"""
        logger.info(f"{self.log_tag_dev_id}Heartbeat Thread Started")
        while True and self.is_con:
            pkt_beat = HEART_BEAT_Packet()
            self._send_packet(pkt_beat)
            logger.info(f"{self.log_tag_dev_id}发送心跳包")
            time.sleep(interval)

    def close(self):
        """关闭接口"""
        logger.info(f"{self.log_tag_dev_id}api.close(), 打印close函数调用堆栈：")
        traceback.print_stack()
        self.is_con = False
        time.sleep(0.2)
        if not(self._usb_dh is None):
            self._usb_dh.close()
        self._usb_dh = None

        # packet包的ID
        self.pkt_id: int = 1
        # 记录连接状态
        self.is_con: bool = False
        self._beat_list: list = []
        self._read_thread: threading.Thread = None
        self._heartbeat_thread: threading.Thread = None
        self._lock: threading.Lock = threading.Lock()

        self._pkt_map: dict = {}
        self._pkt_map_st: dict = {}

        # 多机连接时，调用会出问题
        # if not(self._usb_context is None):
        #     self._usb_context.close()

    def check_is_connect(self):
        return self._read_thread.is_alive() and self.is_con

    def check_heartbeat(self, timeout=10):
        """检查心跳"""
        a = self._beat_list.copy()
        a.sort()
        if len(a) == 0:
            return False
        last_time = a[-1]
        return (time.time() - last_time) < timeout

    def _read_packet(self):
        """读response线程"""
        while True and self.is_con:
            if self.type_connect == self.TYPE_CONNECT.LIBUSB:
                try:
                    data = self._usb_dh.bulkRead(self.READ_END_POINT, 2046, timeout=0)
                    length = int.from_bytes(data[:4], byteorder="little")
                    while len(data) < length:
                        data += self._usb_dh.bulkRead(self.READ_END_POINT, length - len(data), timeout=0)
                except OSError as e:
                    # 关闭连接的话这里会报错
                    emsg = traceback.format_exc()
                    logger.error(f'{self.log_tag_dev_id} _read_packet OSError {emsg}')
                    self.close()
                    if self.is_con:
                        self.is_con = False
                        raise e
                    self.is_con = False
                except usb1.USBErrorPipe as e:
                    # 断开usb连接的报错
                    emsg = traceback.format_exc()
                    logger.error(f'{self.log_tag_dev_id} _read_packet usb1.USBErrorPipe {emsg}')
                    self.close()
                    if self.is_con:
                        self.is_con = False
                        raise e
                    self.is_con = False
            # 解析通讯包
            pkt = Packet.parse_packet(length, data[4:])
            # if not pkt.packet_type == Packet.TYPE_ENUM.SOCKET_TUNNEL:
            logger.info(f"{self.log_tag_dev_id}收到了pkt包：{pkt}")
            if pkt.packet_type == Packet.TYPE_ENUM.HEART_BEAT:
                self._beat_list.append(time.time())
                if len(self._beat_list) > 10:
                    self._beat_list.pop(0)
            elif pkt.packet_type == Packet.TYPE_ENUM.MESSAGE:
                pkt_msg: Message_Packet = pkt
                key = pkt_msg.stream_id
                if not (key in self._pkt_map):
                    self._pkt_map.update({key: [pkt_msg]})
                else:
                    self._pkt_map.get(key).append(pkt_msg)

                if pkt_msg.error_code in MessageCode.values():
                    msg_name = MessageCode.Name(pkt_msg.error_code)
                    if 'CAMERA_NOTIFICATION_SHUTDOWN' in msg_name:
                        self.close()
                        raise RuntimeError(f'{self.log_tag_dev_id}收到相机关机的通知，请注意相机是否发生了异常')
            elif pkt.packet_type == Packet.TYPE_ENUM.JSON_MESSAGE:
                pkt_json: JSON_Packet = pkt
                key = pkt_json.packet_id
                if not (key in self._pkt_map):
                    self._pkt_map.update({key: [pkt_json]})
                else:
                    self._pkt_map.get(key).append(pkt_json)

            elif pkt.packet_type == Packet.TYPE_ENUM.SYNCHRONIZE:
                self._beat_list.append(time.time())
            elif pkt.packet_type == Packet.TYPE_ENUM.SOCKET_TUNNEL:
                pkt_st: Socket_Tunnel_Packet = pkt
                key = pkt_st.identifier

                if not (key in self._pkt_map_st):
                    self._pkt_map_st.update({key: [pkt_st]})
                else:
                    self._pkt_map_st.get(key).append(pkt_st)

            else:
                logger.info(f"{self.log_tag_dev_id}收到了未处理的packet：{pkt.packet_type}, {pkt}")
                logger.info(f"{self.log_tag_dev_id}收到了未处理的packet：{length}, {data}")
                pass

    def send_command_message(self, msg_method: MessageCode, content_obj):
        """发送command的message packet"""
        if not self.is_con:
            raise RuntimeError(f"{self.log_tag_dev_id}端口已经被关掉了，请重新new一个对象")
        if content_obj is None:
            content_byte = b''
        else:
            content_byte = content_obj.SerializeToString()
        pkt_msg = Message_Packet(method=msg_method, content=content_byte, stream_id=self.pkt_id)
        self._send_packet(pkt_msg)
        logger.info(f'{self.log_tag_dev_id}{pkt_msg}')
        return pkt_msg

    def get_recv_packet(self, pkt_id: int, timeout: float = 10) -> Packet:
        """获取收到的packet的包"""
        t_s = time.time()
        while (time.time() - t_s) < timeout:
            if pkt_id in self._pkt_map:
                # 收到msg之后等待200ms，以获取多个response
                time.sleep(0.2)
                resp = self._pkt_map[pkt_id][0]
                return resp
        logger.error(f'{self.log_tag_dev_id}等待response超时, 包ID:{pkt_id}')
        return None

    def send_msg_get_resp(self, msg_method: MessageCode, content_obj, resp_type, timeout: float = 30):
        """发送command的message packet
        并获取message packet的回复包"""
        pkt_msg = self.send_command_message(msg_method=msg_method, content_obj=content_obj)
        resp_msg = self.get_recv_packet(pkt_id=pkt_msg.stream_id, timeout=timeout)
        if resp_msg is None:
            # 获取不到设备返回的包，有可能相机死机，或丢失相机的回复包，看心跳情况判断
            return None
        if resp_type is None:
            resp = None
            code = resp_msg.error_code
            logger.info(f'{self.log_tag_dev_id}{resp_msg}')
            return code, resp
        else:
            resp = resp_type()
            code = resp_msg.error_code
            resp.ParseFromString(resp_msg.content)
            for recv_msg in self._pkt_map[pkt_msg.stream_id]:
                logger.info(f'{self.log_tag_dev_id}{recv_msg}')
            return code, resp

    def send_json_packet(self, jsobj: dict) -> JSON_Packet:
        json_pkt = JSON_Packet()
        json_pkt.jsobj = jsobj
        self._send_packet(json_pkt)
        return json_pkt

    def send_json_pkt_get_resp(self, jsobj: dict, timeout: float = 30):
        json_pkt = self.send_json_packet(jsobj)
        logger.info(f'{self.log_tag_dev_id}send_json_message json_pkt：{json_pkt}')
        resp_pkt: JSON_Packet = self.get_recv_packet(pkt_id=json_pkt.packet_id, timeout=timeout)
        if not resp_pkt:
            return None
        return resp_pkt.jsobj

    th_ss_server: threading.Thread = None
    ss_server_port: int = random.randint(8000, 9000)
    ss: socket.socket = None
    ss_base_url: str = None
    ss_buf_len: int = 1 * 1024 * 1024

    def start_service(self):
        if not (self.th_ss_server is None):
            if self.th_ss_server.is_alive():
                # raise RuntimeError('请不要重复调用')
                logger.info(f'{self.log_tag_dev_id}请不要重复打开服务器')
                # return self.ss_base_url

        def _start_service(info: dict):
            self.ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            while True:
                try:
                    p_id = random.randint(8000, 9000)
                    host = '127.0.0.1'
                    self.ss.bind((host, p_id))
                    self.ss.listen(1)
                    self.ss_server_port = p_id
                    info['ss_base_url'] = f'http://{host}:{p_id}/'
                    logger.info(f'{self.log_tag_dev_id}socket server的信息：{info}')
                    break
                except OSError as e:
                    self.ss_server_port = random.randint(p_id, p_id + 1000)
                    logger.info(f'{self.log_tag_dev_id}端口号冲突，随机到: {self.ss_server_port}')
            client, addr = self.ss.accept()

            def _close_ss():
                st_pkt = Socket_Tunnel_Packet()
                st_pkt.identifier = identifier
                st_pkt.set_flags(Socket_Tunnel_Packet.Flag.CLOSE_CONNECTION)
                self._send_packet(st_pkt)
                logger.info(f'{self.log_tag_dev_id}发送CLOSE_CONNECTION的包')

                client.close()
                if self.ss:
                    self.ss.close()
                self.ss = None
                self.th_ss_server = None
            now_rec_data_len = 0
            buf_data = b''
            while not (b'\r\n\r\n' in buf_data):
                data = client.recv(self.ss_buf_len)
                logger.info(f'{self.log_tag_dev_id}recv data')
                buf_data += data
                now_rec_data_len += len(data)
            idx_line_h = buf_data.index(b'\r\n\r\n') + len(b'\r\n\r\n')
            data_head = buf_data[:idx_line_h]
            logger.info(f'{self.log_tag_dev_id}请求头为：{data_head}')
            data_content_temp = buf_data[idx_line_h:]
            logger.info(f'{self.log_tag_dev_id}请求内容前1000: {data_content_temp[:1000]}')
            content_length = 0
            if b'Content-Length: ' in data_head:
                content_length = int(data_head[data_head.index(b'Content-Length: '):].split(b'\r\n')[0].split(b' ')[1])
            req_data_len = len(data_head) + content_length

            # 封装usb透传
            identifier = self.pkt_id + 1

            def _send_ss_req_pkt(pkt_data, pkt_order):
                """pkt_data 传包的数据、pkt_order 第x个包"""
                if len(pkt_data) == 0:
                    raise RuntimeError(f'{self.log_tag_dev_id}透传数据错误')
                st_pkt = Socket_Tunnel_Packet()
                st_pkt.window_size = self.ss_buf_len
                st_pkt.identifier = identifier
                if pkt_order == 0:
                    st_pkt.set_flags(st_pkt.Flag.NEW_CONNECTION)
                st_pkt.set_flags(st_pkt.Flag.DATA)
                st_pkt.set_flags(st_pkt.Flag.WINDOW_SIZE)
                st_pkt.content = pkt_data
                self._send_packet(st_pkt)
                time.sleep(1)
            # 转发包逻辑
            now_pkt_od = 0
            num_data_pkt = req_data_len//self.ss_buf_len + 1
            while now_rec_data_len < req_data_len:
                data = client.recv(self.ss_buf_len)
                buf_data += data
                now_rec_data_len += len(data)
                if len(buf_data) >= self.ss_buf_len:
                    _send_ss_req_pkt(buf_data[:self.ss_buf_len], now_pkt_od)
                    now_pkt_od += 1
                    buf_data = buf_data[self.ss_buf_len:]
            while len(buf_data) > 0:
                _send_ss_req_pkt(buf_data[:self.ss_buf_len], now_pkt_od)
                now_pkt_od += 1
                buf_data = buf_data[self.ss_buf_len:]
            assert num_data_pkt == now_pkt_od
            logger.info(f'{self.log_tag_dev_id}转发请求包结束')
            # 解析固件返回包，转发response逻辑
            recv_window_size = 0
            t_s = time.time()
            while time.time() - t_s < self.ss_pkt_timeout:
                if not(identifier in self._pkt_map_st.keys()):
                    continue
                else:
                    logger.info(f'{self.log_tag_dev_id}收到相机的包')
                    pkt = self._pkt_map_st[identifier][0]
                    if Socket_Tunnel_Packet.Flag.WINDOW_SIZE.name in pkt.get_flags():
                        recv_window_size = pkt.window_size
                    break
            if not(identifier in self._pkt_map_st.keys()):
                logger.error(f'{self.log_tag_dev_id}没有收到相机的response')
                raise RuntimeError(f'{self.log_tag_dev_id}没有收到相机的response')
            resp_head = None
            buf_data = b''
            data_temp = b''
            now_send_data_len = 0
            resp_data_len = None
            conn_client_window_size = self.ss_buf_len
            t_s = time.time()
            while resp_data_len is None or now_send_data_len < resp_data_len:
                pkts = self._pkt_map_st.get(identifier)
                if len(pkts) <= 0 and time.time() - t_s > self.ss_pkt_timeout:
                    logger.error(f'{self.log_tag_dev_id}等待响应包超时, 当前接收数据进度：{now_send_data_len}/{resp_data_len}--{"%.2f"%(now_send_data_len/1024/1024)}MB/{"%.2f"%(resp_data_len/1024/1024)}MB')
                    logger.error(f'当前发送给固件的window_size值_{conn_client_window_size} 超时：{self.ss_pkt_timeout}')
                    logger.error(f'{self.log_tag_dev_id}可能需要重启相机')
                    break
                while len(pkts) > 0:
                    pkt: Socket_Tunnel_Packet = pkts.pop(0)
                    if Socket_Tunnel_Packet.Flag.ERROR.name in pkt.get_flags():
                        logger.error(f'{self.log_tag_dev_id}固件端返回异常 {pkt}，停止从固件读包的逻辑')
                        _close_ss()
                        raise RuntimeError(f'{self.log_tag_dev_id}固件端返回异常')
                    elif Socket_Tunnel_Packet.Flag.CLOSE_CONNECTION.name in pkt.get_flags():
                        logger.info(f'{self.log_tag_dev_id}固件端请求关闭连接')
                        if len(buf_data) > 0:
                            client.sendall(buf_data)
                            buf_data = b''
                        _close_ss()
                        raise RuntimeError(f'固件端请求关闭连接')
                    buf_data += pkt.content
                    if resp_head is None:
                        data_temp += buf_data
                        if b'\r\n\r\n' in data_temp:
                            idx_line_h = data_temp.index(b'\r\n\r\n') + len(b'\r\n\r\n')
                            resp_head = data_temp[:idx_line_h]
                            content_length = 0
                            if b'Content-Length: ' in resp_head:
                                content_length = int(resp_head[resp_head.index(b'Content-Length: '):].split(b'\r\n')[0].split(b' ')[1])
                            if content_length == 0:
                                resp_data_len = len(buf_data)
                            else:
                                resp_data_len = len(resp_head) + content_length
                            logger.info(f'{self.log_tag_dev_id}响应头为：{resp_head}')
                            logger.info(f'{self.log_tag_dev_id}响应内容前1000为：{data_temp[idx_line_h:][:1000]}')
                if len(buf_data) > 0:
                    now_send_data_len += len(buf_data)
                    client.sendall(buf_data)
                    buf_data = b''
                    # logger.info(f'{self.log_tag_dev_id}转发包进度：{now_send_data_len}/{resp_data_len}')
                notify_size = self.ss_buf_len / 5 + recv_window_size
                len_cos = conn_client_window_size - now_send_data_len
                if (time.time() - t_s > 3) and (len_cos > notify_size) and (len_cos < notify_size * 3):
                    notify_size = notify_size * 3
                    logger.error(f'当前已经卡3秒了，尝试容错 ：{len_cos} < {notify_size} recv_window_size：{recv_window_size}')
                if len_cos < notify_size:
                    if conn_client_window_size == self.ss_buf_len:
                        conn_client_window_size += now_send_data_len
                    else:
                        conn_client_window_size += self.ss_buf_len
                    st_wz = Socket_Tunnel_Packet()
                    st_wz.identifier = identifier
                    # st_wz.set_flags(Socket_Tunnel_Packet.Flag.DATA)
                    st_wz.set_flags(Socket_Tunnel_Packet.Flag.WINDOW_SIZE)
                    st_wz.window_size = conn_client_window_size
                    self._send_packet(st_wz)
                    t_s = time.time()

            _close_ss()

        info_obj = {'ss_base_url': None, }
        self.th_ss_server = threading.Thread(target=_start_service, daemon=True, args=(info_obj,))
        self.th_ss_server.start()
        time.sleep(1)
        while info_obj['ss_base_url'] is None:
            time.sleep(1)
            if not self.th_ss_server.is_alive():
                raise RuntimeError(f'{self.log_tag_dev_id}启动socket server失败')
        self.ss_base_url = info_obj['ss_base_url']
        return self.ss_base_url

    def send_get_http_tunnel(self, action, method="POST", **kwargs) -> requests.Response:
        """
        发送http透传请求
        :param action:拼接url，传osc/info等
        :param method:请求方法
        :param kwargs:带其他参数 json、timeout、files等
        :return:
        """
        self.start_service()
        url = self.ss_base_url + action
        logger.info(f'{self.log_tag_dev_id}url {url}')
        return requests.request(method=method, url=url, **kwargs)

    def upload_file(self, fpath):
        """上传文件接口"""
        resp_get = self.send_get_http_tunnel('upload_file', method='GET')
        logger.info(f'{self.log_tag_dev_id}上传文件先线get一次，{resp_get}')
        files = {"file": open(fpath, "rb")}
        return self.send_get_http_tunnel('upload_file', method='POST', files=files, timeout=1000)

    def upload_fw(self, fpath):
        """OTA接口"""
        resp_get = self.send_get_http_tunnel('upload_fw', method='GET')
        logger.info(f'{self.log_tag_dev_id}上传文件前先get一次，{resp_get}')
        files = {"file": open(fpath, "rb")}
        return self.send_get_http_tunnel('upload_fw', method='POST', files=files, timeout=1000)

    def download_file(self, path_dcim, p_out):
        """
        下载文件
        :param path_dcim: 传参/DCIM/xxxx
        :param p_out: 下载文件全路径
        :return:
        """
        if path_dcim.startswith('/'):
            path_dcim = path_dcim[1:]
        resp_down = self.send_get_http_tunnel(path_dcim, method='GET', stream=True)
        ct_out = 0
        logger.info(f'{self.log_tag_dev_id}客户端接收到的response：{resp_down.headers}')
        with open(p_out, 'wb+') as f:
            for file_size in resp_down.iter_content(self.ss_buf_len//1024):
                if file_size:
                    ct_out += f.write(file_size)
        logger.info(f'实际下载的文件长度：{ct_out}，目标：{resp_down.headers["Content-Length"]}')
        return resp_down.status_code == 200 and int(resp_down.headers['Content-Length']) == ct_out

