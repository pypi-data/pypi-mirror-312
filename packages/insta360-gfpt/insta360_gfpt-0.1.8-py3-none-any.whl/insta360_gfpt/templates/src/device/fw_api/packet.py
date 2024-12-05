#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :packet.py
# @Time      :2022/7/11 16:22
# @Author    :lilinhong
"""

"""
import json
from enum import Enum
from loguru import logger
from src.device.fw_api.proto.message_code_pb2 import MessageCode


class Packet:
    length: int = 32

    class TYPE_ENUM(Enum):
        UNKNOW = 0x00
        STREAM = 0x01
        # PROTOBUF = 0x02
        NANO1_DICT = 0x03
        MESSAGE = 0x04
        HEART_BEAT = 0x05
        SYNCHRONIZE = 0x06
        SOCKET_TUNNEL = 0x07
        SYNC_MEDIA_TIME = 0x08
        LINUX_CMD = 0x09
        JSON_MESSAGE = 0xFE

    packet_type: TYPE_ENUM = None

    def __str__(self):
        return f'Packet：{self.packet_type if self.packet_type is None else self.TYPE_ENUM(self.packet_type)}'

    @classmethod
    def parse_packet(cls, length: int, packet_bytes: bytes):
        pkt_type_value = int.from_bytes(packet_bytes[:1], byteorder="little")
        pkt_type = cls.TYPE_ENUM(pkt_type_value)

        if pkt_type == cls.TYPE_ENUM.JSON_MESSAGE:
            # JSON_Message(Packet)
            json_msg = JSON_Packet.parse_packet(length, packet_bytes)
            return json_msg
        else:
            # Packet_Proto(Packet)
            padding_length = int.from_bytes(packet_bytes[1:3], byteorder="little")
            assert padding_length <= length
            payload = packet_bytes[3:]
            if pkt_type == cls.TYPE_ENUM.MESSAGE:
                msg = Message_Packet.parse_packet(length, packet_bytes)
                return msg
            if pkt_type == cls.TYPE_ENUM.SOCKET_TUNNEL:
                st_pkt = Socket_Tunnel_Packet.parse_packet(length, packet_bytes)
                return st_pkt
            elif pkt_type == cls.TYPE_ENUM.SYNCHRONIZE:
                sync = Sync_Packet()
                sync.length = length
                sync.padding_length = padding_length
                sync.payload = payload
                return sync
            elif pkt_type == cls.TYPE_ENUM.HEART_BEAT:
                beat = HEART_BEAT_Packet()
                beat.length = length
                beat.padding_length = padding_length
                beat.payload = payload
                return beat
            else:
                packet = Packet_Proto(pkt_type, payload)
                packet.length = length
                packet.padding_length = padding_length
                packet.payload = payload
                return packet

    def build(self):
        pass


class Packet_Proto(Packet):
    """
    +--------+------+----------------+-----------+---------+
    | Length | Type | padding-length |  payload  | padding |
    +--------+------+----------------+-----------+---------+
    |   32   |  8   |       16       |           |         |
    +--------+------+----------------+-----------+---------+
    """
    padding_length: int = 0
    payload: bytes = None
    padding = b''

    def __init__(self, pkt_type: Packet.TYPE_ENUM, payload: bytes):
        self.packet_type = pkt_type
        self.payload = payload

    def build(self):
        type_padding_length_payload = (
                self.packet_type.value.to_bytes(1, byteorder="little")
                + self.padding_length.to_bytes(2, byteorder="little")
                + self.payload
        )
        self.length = len(type_padding_length_payload) + 4
        data = self.length.to_bytes(4, byteorder="little") + type_padding_length_payload
        return data

    def __str__(self):
        packet_type = f'{self.packet_type if self.packet_type is None else self.TYPE_ENUM(self.packet_type)}'
        return f'Packet_Proto：pkt_type_{packet_type}, padding_length_{self.padding_length}, payload_len_{len(self.payload)}， payload_{self.payload}, padding_{self.padding}'


class Message_Packet(Packet_Proto):
    """
    message消息包，libusb的里面暂时留空
    """
    method: MessageCode = None
    #   如果是请求，应该为消息类型
    #   如果是回复，应该为error code. Error code 尽量保持与HTTP 的error code 相近，便于理解。
    error_code: int = None

    class CONTENT_TYPE_ENUM(Enum):
        application_octet_stream = 0x0001
        application_protobuf = 0x0002
        application_nano1_dict = 0x0003
        application_raw = 0x0005
    content_type: CONTENT_TYPE_ENUM = CONTENT_TYPE_ENUM.application_protobuf

    end: int = 1
    direction: int = 0
    stream_id: int = 0
    rsv: int = 0
    content: bytes = None

    def __str__(self):
        if self.method is None:
            msg_method_name = None
        elif self.method in MessageCode.values():
            msg_method_name = MessageCode.Name(self.method)
        else:
            msg_method_name = self.method

        if self.error_code is None:
            error_code_msg = f'未知包：{None}'
        elif self.error_code in MessageCode.values():
            error_code_msg = f'通知包：{MessageCode.Name(self.error_code)}'
        else:
            error_code_msg = f'未知包：{self.error_code}'

        rets = 'Message_Packet: '
        rets += f'stream_id_{self.stream_id}, '
        rets += f'direction_{"发给相机" if self.direction == 0 else "收到信息"}, '
        rets += f'Message_method_{msg_method_name}, '
        rets += f'error_code_{self.error_code}, '
        rets += f'error_code_msg_{error_code_msg}, '
        rets += f'Message_content_{self.content}'
        return rets

    def _build_message_payload(self):
        """
        构建message的payload，主要protobuf协议
        :return:
        """
        self.payload = (
            self.method.to_bytes(2, byteorder="little")
            + self.content_type.value.to_bytes(1, byteorder="little")
            + self.end.to_bytes(1, byteorder="little")
            + self.direction.to_bytes(1, byteorder="little")
            + self.stream_id.to_bytes(2, byteorder="little")
            + self.rsv.to_bytes(2, byteorder="little")
            + self.content
        )
        return self.payload

    def __init__(self, method: MessageCode, content: bytes, stream_id: int, error_code=None):
        pkg_type = self.TYPE_ENUM.MESSAGE
        self.method = method
        self.content = content
        self.stream_id = stream_id
        self.error_code = error_code
        if error_code is None:
            payload = self._build_message_payload()
        else:
            payload = None
        super(Message_Packet, self).__init__(pkg_type, payload)

    def set_steam_id(self, stream_id):
        self.stream_id = stream_id
        self.payload = self._build_message_payload()

    @classmethod
    def parse_packet(cls, length: int, packet_bytes: bytes):
        # packet
        pkt_type_value = int.from_bytes(packet_bytes[:1], byteorder="little")
        pkt_type = cls.TYPE_ENUM(pkt_type_value)
        # packet_proto
        padding_length = int.from_bytes(packet_bytes[1:3], byteorder="little")
        assert padding_length <= length
        # Message_Packet，解析payload
        payload = packet_bytes[3:]
        method_value = int.from_bytes(payload[:2], byteorder="little")
        content_type = int.from_bytes(payload[2:3], byteorder="little")
        end = int.from_bytes(payload[3:4], byteorder="little")
        direction = int.from_bytes(payload[4:5], byteorder="little")
        stream_id: int = int.from_bytes(payload[5:7], byteorder="little")
        rsv = int.from_bytes(payload[7:9], byteorder="little")
        content = payload[9:]

        try:
            method = MessageCode(method_value)
            logger.info(str(method))
            error_code = None
            message = Message_Packet(method=method, content=content, stream_id=stream_id, error_code=error_code)
        except TypeError as e:
            method = None
            error_code = method_value
            message = Message_Packet(method=method, content=content, stream_id=stream_id, error_code=error_code)

        message.padding_length = padding_length
        message.direction = direction
        message.rsv = rsv
        message.payload = payload
        message.content_type = Message_Packet.CONTENT_TYPE_ENUM(content_type)
        message.end = end
        return message


class Sync_Packet(Packet_Proto):
    """
    sync包
    """
    def __init__(self):
        pkg_type = Packet.TYPE_ENUM.SYNCHRONIZE
        payload = bytes([0xAF, 0xFA, 0xAF, 0xFA, 0xAF, 0xFA, 0xAF, 0xFA, 0xAF, 0xFA])
        super(Sync_Packet, self).__init__(pkg_type, payload)

    def __str__(self):
        return 'Sync_Packet：同步包'


class HEART_BEAT_Packet(Packet_Proto):
    """
    心跳包
    """
    def __init__(self):
        pkg_type = Packet.TYPE_ENUM.HEART_BEAT
        payload = b""
        super(HEART_BEAT_Packet, self).__init__(pkg_type, payload)

    def __str__(self):
        return 'HEART_BEAT_Packet：心跳包'


class JSON_Packet(Packet):
    """
HEAD
typedef struct INS_PACKET_COMM_HEAD_ {
    uint32_t packet_length;  // 消息长度     json实际长度+20字节
    uint8_t packet_type;     // 设备类型     254 : factory产测协议类型
    uint8_t version;         // 通信协议版本
    uint8_t factory_dev_id;  // 当前产测设备编号ID，PC临时生产便于设备与PC对应显示
    uint8_t is_response;     // 正常固件应答报文is_response = 1, 按键主动上报 is_response  = 0
    uint32_t packet_id;      // 包序号
    uint16_t crc16_check;    // crc16_check 报文合法性校验
    uint16_t device_type;    // 设备类型
    int16_t response_code;   // 返回错误code
    int16_t reserved;        // 保留扩展字段
} INS_PACKET_COMM_HEAD;

JSON Content
    https://arashivision.feishu.cn/wiki/wikcn3HqkmUpwqdikDiJ2H3hJrb
    """
    version: int = 0
    factory_dev_id: int = 0
    is_response: int = 0
    packet_id = None
    crc16_check = 0
    device_type = 0
    response_code = 0
    reserved = 0

    jsobj: dict = None

    @classmethod
    def parse_packet(cls, length: int, packet_bytes: bytes):
        json_pkt = cls()
        json_pkt.length = length
        pkt_type_value = int.from_bytes(packet_bytes[:1], byteorder="little")
        json_pkt.packet_type = cls.TYPE_ENUM(pkt_type_value)
        json_pkt.version = int.from_bytes(packet_bytes[1: 2], byteorder="little")
        json_pkt.factory_dev_id = int.from_bytes(packet_bytes[2: 3], byteorder="little")
        json_pkt.is_response = int.from_bytes(packet_bytes[3: 4], byteorder="little")
        json_pkt.packet_id = int.from_bytes(packet_bytes[4: 8], byteorder="little")
        json_pkt.crc16_check = int.from_bytes(packet_bytes[8: 10], byteorder="little")
        json_pkt.device_type = int.from_bytes(packet_bytes[10: 12], byteorder="little")
        json_pkt.response_code = int.from_bytes(packet_bytes[12: 14], byteorder="little")
        json_pkt.reserved = int.from_bytes(packet_bytes[14: 16], byteorder="little")
        jsobj_str = str(packet_bytes[16:], encoding='utf-8')
        if jsobj_str and '\\' in jsobj_str:
            jsobj_str = jsobj_str.replace('\\', '/')
        try:
            json_pkt.jsobj = json.loads(jsobj_str, strict = False)
        except json.decoder.JSONDecodeError as e:
            logger.error(f'json解析失败，{jsobj_str}')
            json_pkt.jsobj = {'error': jsobj_str}
            raise e
        return json_pkt

    def build(self):
        data_head = (
            # self.length.to_bytes(4, byteorder="little")
            self.packet_type.value.to_bytes(1, byteorder="little")
            + self.version.to_bytes(1, byteorder="little")
            + self.factory_dev_id.to_bytes(1, byteorder="little")
            + self.is_response.to_bytes(1, byteorder="little")
            + self.packet_id.to_bytes(4, byteorder="little")
            + self.crc16_check.to_bytes(2, byteorder="little")
            + self.device_type.to_bytes(2, byteorder="little")
            + self.response_code.to_bytes(2, byteorder="little")
            + self.reserved.to_bytes(2, byteorder="little")
        )
        data_json = json.dumps(self.jsobj).encode('utf-8')
        self.length = 4 + len(data_head) + len(data_json)
        data_length = self.length.to_bytes(4, byteorder="little")
        return data_length + data_head + data_json

    def __str__(self):
        return f'JSON_Message_Packet: ' \
               f'packet_id_{self.packet_id}, ' \
               f'jsobj_{json.dumps(self.jsobj)}'

    def __init__(self):
        self.packet_type = self.TYPE_ENUM.JSON_MESSAGE


class Socket_Tunnel_Packet(Packet_Proto):
    """
        payload放这些：
        uint32_t identifier_;
        uint16_t flags_;
        int64_t window_size_;
        content
    """
    identifier: int = 0

    class Flag(Enum):
        NEW_CONNECTION = 1
        CLOSE_CONNECTION = 1 << 1
        DATA = 1 << 2
        WINDOW_SIZE = 1 << 3
        ERROR = 1 << 4
        RELEASE_ALL_CONNECTIONS = 1 << 5

    flags: int = 0

    window_size = 1 * 1024 * 1024

    content: bytes = b''

    def __init__(self):
        self.packet_type = Packet.TYPE_ENUM.SOCKET_TUNNEL

    def set_flags(self, flag: Flag):
        self.flags = self.flags | flag.value

    @classmethod
    def parse_packet(cls, length: int, packet_bytes: bytes):
        st_pkt = cls()
        # packet
        st_pkt.length = length
        pkt_type_value = int.from_bytes(packet_bytes[:1], byteorder="little")
        st_pkt.packet_type = Packet.TYPE_ENUM(pkt_type_value)
        # packet_proto
        st_pkt.padding_length = int.from_bytes(packet_bytes[1:3], byteorder="little")
        assert 0 == st_pkt.padding_length
        st_pkt.payload = packet_bytes[3:]
        st_pkt.padding = b''
        # Socket_Tunnel_Packet，解析payload
        payload = st_pkt.payload
        st_pkt.identifier = int.from_bytes(payload[: 4], byteorder="little")
        st_pkt.flags = int.from_bytes(payload[4: 6], byteorder="little")
        st_pkt.window_size = int.from_bytes(payload[6: 14], byteorder="little")
        st_pkt.content = payload[14:]
        return st_pkt

    def build(self):
        # Socket_Tunnel_Packet
        self.payload = (self.identifier.to_bytes(4, byteorder="little")
                        + self.flags.to_bytes(2, byteorder="little")
                        + self.window_size.to_bytes(8, byteorder="little")
                        + self.content)
        # packet_proto、packet
        type_padding_length_payload = (self.packet_type.value.to_bytes(1, byteorder="little")
                                       + self.padding_length.to_bytes(2, byteorder="little")
                                       + self.payload)
        self.length = 4 + len(type_padding_length_payload)
        return self.length.to_bytes(4, byteorder="little") + type_padding_length_payload

    def get_flags(self):
        objs = [self.Flag.NEW_CONNECTION, self.Flag.CLOSE_CONNECTION, self.Flag.DATA,
                self.Flag.WINDOW_SIZE, self.Flag.ERROR, self.Flag.RELEASE_ALL_CONNECTIONS]
        f_names = []
        for obj in objs:
            if not(self.flags & obj.value == 0):
                f_names.append(obj.name)
        return f_names

    def __str__(self):
        return f'Socket_Tunnel_Packet：' \
               f'length_{self.length}, ' \
               f'identifier_{self.identifier}, ' \
               f'flags_{self.flags}, ' \
               f'{self.get_flags()}, ' \
               f'window_size_{self.window_size}, ' \
               f'content_len_{len(self.content)}'#, content_  {self.content}'


if __name__ == "__main__":
    run_code = 0
