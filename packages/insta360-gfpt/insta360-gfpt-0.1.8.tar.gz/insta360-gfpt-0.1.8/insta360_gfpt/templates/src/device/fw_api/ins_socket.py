#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :ins_socket.py
# @Time      :2022/7/11 16:24
# @Author    :lilinhong
"""
https://gitlab.insta360.com/sd/mobile/ins_camera_proto
"""
import os
import sys
import time
import socket
import traceback
import threading
import cv2 as cv
from loguru import logger
from src.fw_api.packet import *
from proto.message_code_pb2 import MessageCode


class Proto_Socket:
    # TODO:还需要解决设备返回的通知问题，做一个监听者的设计模式？返回自动序列化成notifications

    def __init__(self, host='192.168.42.1', port=6666):
        self.host = host
        self.port = port
        self.address = (self.host, self.port)
        self.socket: socket.socket = socket.socket()
        # self.socket.settimeout(10)
        self.stream_id = 1
        self.connection_closed = True
        self.message_map = {}
        self.beat_list = []
        self.read_thread = None
        self.heartbeat_thread = None
        self.lock = threading.Lock()

    def init_socket(self):
        # 连接socket
        try:
            self.socket.connect(self.address)
        except TimeoutError as e:
            logger.error(e)
            time.sleep(1)
            logger.info("retry connect socket")
            self.socket.connect(self.address)

        logger.info("init socket okay")
        # 开启读response的线程
        self.read_thread = threading.Thread(target=self._read_packet, name='reader', daemon=True)
        self.read_thread.start()
        # 发送sync
        logger.info("sender sync")
        msg = self.send_sync_message()
        # 开启心跳线程
        self.heartbeat_thread = threading.Thread(target=self._heartbeat, name='heartbeat', daemon=True)
        self.heartbeat_thread.start()

    def send_command_message(self, msg_code: MessageCode,
                             content_obj):
        if not self.connection_closed:
            raise RuntimeError("端口已经被关掉了，请重新new一个对象")
        method = msg_code
        if content_obj is None:
            content = b''
        else:
            content = content_obj.SerializeToString()
        msg = Message_Packet(method=method, content=content, stream_id=self.stream_id)
        self._send_package(msg)
        req_str = str(content_obj).replace("\n", "|")
        logger.info(f'stream_id:{msg.stream_id}，{MessageCode.Name(method)}, {req_str}')
        return msg

    def get_msg_response(self, msg: Message_Packet, timeout: float = 15) ->Message_Packet:
        start = cv.getTickCount()
        now = start
        while (now - start) < (timeout * cv.getTickFrequency()):
            if msg.stream_id in self.message_map:
                # 收到msg之后等待200ms，以获取多个response
                time.sleep(0.2)
                resp = self.message_map[msg.stream_id][0]
                return resp
            now = cv.getTickCount()
        logger.error(f'等待response超时, stream_id:{msg.stream_id}')
        return None

    def send_msg_get_resp(self, msg_code: MessageCode,
                          content_obj,
                          resp_type,
                          timeout: float = 30):
        msg = self.send_command_message(msg_code=msg_code,
                                        content_obj=content_obj,)
        resp_msg = self.get_msg_response(msg=msg, timeout=timeout)
        if resp_msg is None:
            # 获取不到设备返回的包
            # 有可能相机死机，或丢失相机的回复包，看心跳情况判断
            return None
        if resp_type is None:
            resp = None
            code = resp_msg.error_code
            logger.info(f'stream_id:{resp_msg.stream_id}  '
                        f'MessageCode:{MessageCode.Name(msg_code)}  '
                        f'response:{resp_msg} ')
            return code, resp
        else:
            resp = resp_type()
            code = resp_msg.error_code
            resp.ParseFromString(resp_msg.content)

        # 统一打印response
        temp_resp_list = []
        for temp_msg in self.message_map[msg.stream_id]:
            temp = resp_type()
            code = resp_msg.error_code
            temp.ParseFromString(temp_msg.content)
            temp_resp_list.append(temp)
        temp_str = str(temp_resp_list).replace('\n', '|')
        str_con = str(content_obj).replace('\n', '|')
        logger.info(f'stream_id:{resp_msg.stream_id} '
                    f'MessageCode:{MessageCode.Name(msg_code)} '
                    f'response:{temp_str} '
                    f'req:{str_con}')

        return code, resp

    def send_sync_message(self, timeout: float = 15):
        msg = Sync_Packet()
        self._send_package(msg=msg)
        start = cv.getTickCount()
        now = start
        while (now - start) < (timeout * cv.getTickFrequency()):
            if len(self.beat_list) > 0:
                return msg
        raise RuntimeWarning('没有收到sync包回复')

    def _send_package(self, msg: Packet):
        self.lock.acquire()
        try:
            if type(msg) is Message_Packet:
                msg.set_steam_id(self.stream_id)
            data = msg.build()
            try:
                resp = self.socket.sendall(data)
                logger.info(f'pkt send：{self.stream_id}，{str(type(msg))}，resp：{resp}')
                return resp
            except BrokenPipeError as e:
                self.close()
                traceback.print_exc()
                msg = traceback.format_exc()
                logger.error(msg)
                raise e
            except ConnectionResetError as e:
                self.close()
                traceback.print_exc()
                msg = traceback.format_exc()
                logger.error(msg)
                raise e
            except Exception as e:
                self.close()
                traceback.print_exc()
                msg = traceback.format_exc()
                logger.error(msg)
                raise e
        finally:
            self.stream_id = self.stream_id + 1
            self.lock.release()

    def _read_packet(self):
        while True and self.connection_closed:
            # 读取整个packet的长度
            length_byte = self.socket.recv(4)
            length = int.from_bytes(length_byte, byteorder="little")
            if length == 0:
                # logger.info("空包，跳过")
                continue
            # TODO:处理MemoryError
            # 读取整个packet的内容
            try:
                packet_byte = self.socket.recv(length - 4)
            except MemoryError as e:
                logger.error(str(e))
                continue
            while len(packet_byte) < (length - 4):
                packet_byte += self.socket.recv(length - 4 - len(packet_byte))
            packet = Packet.parse_packet(length, packet_byte)
            if packet.packet_type == Packet.TYPE_ENUM.MESSAGE:
                message: Message_Packet = packet
                key = message.stream_id
                if not (key in self.message_map):
                    self.message_map.update({
                        key: [message]
                    })
                else:
                    self.message_map.get(key).append(message)
                if message.error_code in MessageCode.values():
                    msg_name = MessageCode.Name(message.error_code)
                    logger.info(f"收到了固件的通知包:stream_id:{message.stream_id} {msg_name}")
                    if 'CAMERA_NOTIFICATION_SHUTDOWN' in msg_name:
                        self.close()
                        raise RuntimeError('收到相机关机的通知，请注意相机是否发生了异常')
                else:
                    logger.info(f"收到了非通知的消息:stream_id:{message.stream_id} error code:{message.error_code}")
                logger.info(f"message package:"
                            f"stream_id:{message.stream_id}，"
                            f"error code:{message.error_code}，"
                            f"message.method:{message.method}，"
                            # f"message.content_type:{message.content_type}，"
                            f"message.content:{message.content}")
            elif packet.packet_type == Packet.TYPE_ENUM.SYNCHRONIZE:
                logger.info("收到了sync包回复")
                self.beat_list.append(cv.getTickCount())
            elif packet.packet_type == Packet.TYPE_ENUM.HEART_BEAT:
                logger.info("收到了心跳包")
                self.beat_list.append(cv.getTickCount())
                if len(self.beat_list) > 10:
                    self.beat_list.pop(0)
            else:
                # logger.info(f"收到了其他包 {packet.packet_type}")
                pass

    def _heartbeat(self, interval=2):
        logger.info("Heartbeat Thread Started")
        while True and self.connection_closed:
            msg = HEART_BEAT_Packet()
            self._send_package(msg)
            logger.info(f"发送心跳包")
            time.sleep(interval)

    def close(self):
        self.connection_closed = False
        time.sleep(3)
        self.socket.close()

    def check_heartbeat(self, timeout=10):
        a = self.beat_list.copy()
        a.sort()
        if len(a) == 0:
            return False
        last_time = a[-1]
        return (cv.getTickCount() - last_time)/cv.getTickFrequency() < timeout


if __name__ == "__main__":
    run_code = 0

