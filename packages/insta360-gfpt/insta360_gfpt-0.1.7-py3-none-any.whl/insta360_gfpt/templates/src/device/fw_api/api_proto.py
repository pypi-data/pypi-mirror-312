import logging
import os
import sys
import time
import json
import socket
import ffmpeg
from loguru import logger

from src.device.fw_api.ins_libusb import Ins_Libusb
from src.device.fw_api.proto.capture_state_pb2 import CameraCaptureState
from src.device.fw_api.proto.commands.get_options_pb2 import GetOptionsResp, GetOptions
from src.device.fw_api.proto.commands.set_options_pb2 import SetOptions, SetOptionsResp
from src.device.fw_api.proto.message_code_pb2 import MessageCode
from src.device.fw_api.proto.options_pb2 import Options, OptionType
from src.device.fw_api.proto.photo_pb2 import PhotoSubMode
from src.device.fw_api.proto.sensor_pb2 import Sensor, SensorDevice
from src.device.fw_api.proto.video_pb2 import VideoSubMode
from src.device.fw_api.util_libusb import list_usb_device


class API_Proto(Ins_Libusb):

    def __init__(self, cam_sn):
        super(API_Proto, self).__init__(cam_sn)

    def init_socket(self):
        super(API_Proto, self).init_socket()

    def init_app_socket_con(self):
        info = {}
        # 1. 在链路连接成功后（iOS App状态为Found）get一些信息
        code, resp = self.get_options([
            # 是否正插反插，# 固件版本，
            'IS_SELFIE', 'FIRMWAREREVISION',
            # 设备序列号, readwrite，# 相机名 readOnly
            'SERIAL_NUMBER', 'CAMERA_TYPE',
            # 镜头信息，自己加的
            'SENSOR_ID', 'SENSOR_INFO',
            # 视频编码格式
            'VIDEO_ENCODE_TYPE',
        ])
        logger.info(str(resp))
        info['is_selfie'] = resp.value.is_selfie
        info['firmwareRevision'] = resp.value.firmwareRevision
        info['serial_number'] = resp.value.serial_number
        info['camera_type'] = resp.value.camera_type
        info['sensor_id'] = resp.value.sensor_id
        info['sensor_str'] = str(resp.value.sensor).replace('\n', '|')
        info['sensor_type_name'] = Sensor.Type.Name(resp.value.sensor.type)
        info['video_encode_type'] = Options.VideoEncodeType.Name(resp.value.video_encode_type)

        # 2. 在获取到sync包后 set一些信息
        logger.info('等待设备的beat包')
        while not self.check_heartbeat(3):
            # logger.info('no beat')
            pass
        # options = Options()
        # options.local_time = int(time.time())
        # TODO:连接设备成功后，同步时间戳等信息
        # # options.time_zone_seconds_from_GMT = int()
        # # options.authorization_id = str()
        # resp = self.set_options([
        #     # 本地时间，# 本地时区，# 手机验证ID
        #     'LOCAL_TIME', 'TIME_ZONE', 'AUTHORIZATION_ID',
        # ], options)
        # 3.在set成功后，get一些信息
        code, resp = self.get_options([
            # 相机OFFSET，# 3d: 相机OFFSET，相机的预览流的时间戳
                'MEDIA_OFFSET', 'MEDIA_OFFSET_3D', 'MEDIA_TIME',
        ])
        info['media_offset'] = resp.value.media_offset
        info['media_offset_3d'] = resp.value.media_offset_3d
        info['media_time'] = resp.value.media_time

        # 2/3任意一步失败，iOSApp状态切换为failed
        # 3成功后，iOSApp状态切换为connected
        self.cam_info = info
        return info

    def set_options(self, options_option_type_names: list, option: Options):
        """
        设置相机参数
        """
        msg_code = MessageCode.PHONE_COMMAND_SET_OPTIONS
        req = SetOptions()
        req.option_types.extend([OptionType.Value(name) for name in options_option_type_names])
        req.value.CopyFrom(option)
        return self.send_msg_get_resp(msg_code, req, SetOptionsResp)

    def get_options(self, options_option_type_names: list) -> GetOptionsResp:
        """
        获取相机设置，需要是options.proto->OptionType中的字段
        """
        msg_code = MessageCode.PHONE_COMMAND_GET_OPTIONS
        req = GetOptions()
        listiv = [OptionType.Value(name) for name in options_option_type_names]
        req.option_types.extend(listiv)
        return self.send_msg_get_resp(msg_code, req, GetOptionsResp)

    def get_current_capture_status(self):
        from proto.commands.get_current_capture_status_pb2 import GetCurrentCaptureStatusResp
        code, resp = self.send_msg_get_resp(MessageCode.PHONE_COMMAND_GET_CURRENT_CAPTURE_STATUS, None,
                                            GetCurrentCaptureStatusResp)
        status = {
            'state_name': CameraCaptureState.Name(resp.status.state),
            'capture_nums': resp.status.capture_nums,
            'capture_time': resp.status.capture_time,
        }
        return status

    def set_curren_sub_mode_options(self, *sub_mode_name_list):
        """
        切换拍摄的子模式（拍照、录像）
        photo.proto.photo_sub_mode
        video.proto.video_sub_mode
        """
        options_option_type_names = []
        options = Options()
        for sub_mode_name in sub_mode_name_list:
            if sub_mode_name in PhotoSubMode.keys():
                options_option_type_names.append('PHOTO_SUB_MODE')
                options.photo_sub_mode = PhotoSubMode.Value(sub_mode_name)
            if sub_mode_name in VideoSubMode.keys():
                options_option_type_names.append('VIDEO_SUB_MODE')
                options.video_sub_mode = VideoSubMode.Value(sub_mode_name)
        code, resp = self.set_options(options_option_type_names, options)
        return resp

    def set_focus_sensor_options(self, *focus_sensor_name_list):
        options_option_type_names = []
        options = Options()
        for focus_sensor_name in focus_sensor_name_list:
            if focus_sensor_name in SensorDevice.keys():
                options_option_type_names.append('INSTAPANO_FOCUS_SENSOR')
                options.focusSensor = SensorDevice.Value(focus_sensor_name)
        code, resp = self.set_options(options_option_type_names, options)
        return resp

    def get_curren_sub_mode_options(self):
        """
        获取当前拍摄的子模式（拍照、录像）
        拍照图片大小，录像视频分辨率 帧率
        """
        options_option_type_names = [
            # 拍照子模式，录像子模式
            'PHOTO_SUB_MODE', 'VIDEO_SUB_MODE',
            # 照片分辨率，视频分辨率
            # 'PHOTO_SIZE', 'VIDEO_RESOLUTION',
        ]
        code, resp = self.get_options(options_option_type_names)
        value: Options = resp.value
        sub_mode = {}
        resp_names = [OptionType.Name(option_type) for option_type in resp.option_types]
        if 'PHOTO_SUB_MODE' in resp_names:
            photo_sub_mode_name = PhotoSubMode.Name(value.photo_sub_mode)
            sub_mode['photo_sub_mode'] = photo_sub_mode_name
            # sub_mode['photo_size'] = PhotoSize.Name(value.photo_size)
        if 'VIDEO_SUB_MODE' in resp_names:
            video_sub_mode = VideoSubMode.Name(value.video_sub_mode)
            sub_mode['video_sub_mode'] = video_sub_mode
            # sub_mode['video_resolution'] = VideoResolution.Name(value.video_resolution)
        photography_options = self.page_CaptureActivity.get_photography_options(video_sub_mode)
        sub_mode['video_resolution'] = photography_options['RECORD_RESOLUTION']
        logger.info(sub_mode)
        return sub_mode

    def get_media_id(self, media_uri):
        """应对文件名命名规则，计算视频文件名的id"""
        if media_uri in [None, '']:
            return ''
        basename = os.path.basename(media_uri)
        temp_name = basename.replace('LRV_', '').replace('VID_', '').replace('PRO_', '').replace('IMG_', '').split('_')
        media_id = f'{temp_name[0]}_{temp_name[1]}'
        return media_id

    def set_focusSensor_video_capture(self, config):
        assert 'sub_mode_name' in config
        sub_mode_name = config['sub_mode_name']
        self.set_curren_sub_mode_options(sub_mode_name)

        # time.sleep(3)
        # self.page_CaptureActivity.stop_live_stream()
        assert 'focus_sensor' in config
        focus_sensor_name = config['focus_sensor']
        self.set_focus_sensor_options(focus_sensor_name)
        self.page_CaptureActivity.set_active_sensor(focus_sensor_name)

        # time.sleep(3)
        # self.page_CaptureActivity.start_live_stream()
        if 'fov_type' in config:
            fov_type_name = config['fov_type']
            self.page_CaptureActivity.set_fov_type(sub_mode_name, fov_type_name)
        if 'video_resolution' in config:
            video_resolution_name = config['video_resolution']
            if focus_sensor_name == 'SENSOR_DEVICE_ALL':
                self.page_CaptureActivity.set_sub_mode_video_resolution(sub_mode_name, video_resolution_name)
            else:
                self.page_CaptureActivity.set_focus_sensor(sub_mode_name, video_resolution_name)
        if 'record_duration' in config:
            record_duration = config['record_duration']
            self.page_CaptureActivity.set_record_duration(sub_mode_name, record_duration)
        if sub_mode_name == 'VIDEO_TIMESHIFT':
            if 'accelerate_frequency' in config:
                accelerate_frequency = config['accelerate_frequency']
                self.page_CaptureActivity.set_timeshift_options(sub_mode_name, accelerate_frequency)
        if '' in config:
            # 设置曝光等参数
            pass
        if 'flowstate_base_enable' in config:
            pass
            # flowstate_base_enable = config['flowstate_base_enable']
            # self.page_CaptureActivity.set_flowstate_base_enable(flowstate_base_enable)

    def set_sub_mode_video_capture(self, config):
        """设置录像子模式相关参数"""
        assert 'sub_mode_name' in config
        sub_mode_name = config['sub_mode_name']
        self.set_curren_sub_mode_options(sub_mode_name)
        if 'video_resolution' in config:
            video_resolution_name = config['video_resolution']
            self.page_CaptureActivity.set_sub_mode_video_resolution(sub_mode_name, video_resolution_name)
        if 'record_duration' in config:
            record_duration = config['record_duration']
            self.page_CaptureActivity.set_record_duration(sub_mode_name, record_duration)
        if sub_mode_name == 'VIDEO_TIMESHIFT':
            if 'accelerate_frequency' in config:
                accelerate_frequency = config['accelerate_frequency']
                self.page_CaptureActivity.set_timeshift_options(sub_mode_name, accelerate_frequency)
        if 'gamma_mode_name' in config:
            """色彩模式"""
            gamma_mode_name = config['gamma_mode_name']
            self.page_CaptureActivity.set_gamma_mode(sub_mode_name, gamma_mode_name)
        if 'fov_type' in config:
            fov_type_name = config['fov_type']
            self.page_CaptureActivity.set_fov_type(sub_mode_name, fov_type_name)
        if 'focal_length_value' in config:
            """手动调节fov"""
            focal_length_value = config['focal_length_value']
            self.page_CaptureActivity.set_focal_length_value(sub_mode_name, focal_length_value)
        if 'exposure_bias' in config:
            exposure_bias = config['exposure_bias']
            self.page_CaptureActivity.set_exposure_bias(sub_mode_name, exposure_bias)
        if 'white_balance_value' in config:
            white_balance_value = config['white_balance_value']
            self.page_CaptureActivity.set_white_balance_value(sub_mode_name, white_balance_value)
        if 'exposure_options' in config:
            # 设置曝光等参数
            exposure_options = config['exposure_options']
            program_name = exposure_options['program_name']
            iso = exposure_options['iso']
            shutter_speed = exposure_options['shutter_speed']
            self.page_CaptureActivity.set_exposure_options(sub_mode_name, program_name, iso, shutter_speed)
        if 'flowstate_base_enable' in config:
            """设置防抖，实际不生效"""
            flowstate_base_enable = config['flowstate_base_enable']
            self.page_CaptureActivity.set_flowstate_base_enable(flowstate_base_enable)

    def test_focusSensor_video_capture(self, config):
        logger.info(config)
        # self.page_CaptureActivity.start_live_stream()
        # time.sleep(3)
        self.set_focusSensor_video_capture(config)
        # time.sleep(3)
        # self.page_CaptureActivity.stop_live_stream()

        sub_mode_name = config['sub_mode_name']

        file_list_start = self.page_MainActivity_PhotoAlbum.get_all_file_list()
        file_info_start = self.page_MainActivity_PhotoAlbum.get_file_info_group_map()
        time.sleep(1)
        time_start = time.time_ns()
        self.page_CaptureActivity.start_capture(sub_mode_name)
        if 'cap_time' in config:
            cap_time = config['cap_time']
            time.sleep(cap_time)
        else:
            time.sleep(10)
        info = self.page_CaptureActivity.stop_capture(sub_mode_name)
        time_end = time.time_ns()
        logger.info(f'停止拍摄的response：{info}')
        file_list_end = self.page_MainActivity_PhotoAlbum.get_all_file_list()
        file_info_end = self.page_MainActivity_PhotoAlbum.get_file_info_group_map()
        self.check_video_photo_test_result(config, file_list_start, file_info_start, file_list_end, file_info_end,
                                           time_end - time_start)

    def test_sub_mode_video_capture(self, config):
        logger.info(config)
        # 复杂度：机型 X 镜头 X 拍摄模式 X 拍摄分辨率、拍摄时长、其他参数、文件检查参数
        # self.page_CaptureActivity.start_live_stream()
        # time.sleep(3)
        self.set_sub_mode_video_capture(config)
        # time.sleep(3)
        # self.page_CaptureActivity.stop_live_stream()
        sub_mode_name = config['sub_mode_name']

        file_list_start = self.page_MainActivity_PhotoAlbum.get_all_file_list()
        file_info_start = self.page_MainActivity_PhotoAlbum.get_file_info_group_map()
        time.sleep(1)
        time_start = time.time_ns()
        self.page_CaptureActivity.start_capture(sub_mode_name)
        if 'cap_time' in config:
            cap_time = config['cap_time']
            time.sleep(cap_time)
        else:
            time.sleep(10)
        info = self.page_CaptureActivity.stop_capture(sub_mode_name)
        time_end = time.time_ns()
        logger.info(f'停止拍摄的response：{info}')
        file_list_end = self.page_MainActivity_PhotoAlbum.get_all_file_list()
        file_info_end = self.page_MainActivity_PhotoAlbum.get_file_info_group_map()
        self.check_video_photo_test_result(config, file_list_start, file_info_start, file_list_end, file_info_end,
                                           time_end-time_start)

    def set_sub_mode_video_photo_timelapse(self, config):
        logger.info(config)
        assert 'sub_mode_name' in config
        # sub_mode_name：MOBILE_TIMELAPSE_VIDEO、TIMELAPSE_INTERVAL_SHOOTING
        sub_mode_name = config['sub_mode_name']
        self.set_curren_sub_mode_options(sub_mode_name)
        if "VIDEO_TIMELAPSE" == sub_mode_name:
            timelapse_mode_name = "MOBILE_TIMELAPSE_VIDEO"
        elif "PHOTO_INTERVAL" == sub_mode_name:
            timelapse_mode_name = "TIMELAPSE_INTERVAL_SHOOTING"
        else:
            assert False

        if 'focus_sensor' in config:
            focus_sensor_name = config['focus_sensor']
            self.set_focus_sensor_options(focus_sensor_name)
            self.page_CaptureActivity.set_active_sensor(focus_sensor_name)
            assert 'video_resolution' in config
            video_resolution_name = config['video_resolution']
            self.page_CaptureActivity.set_focus_sensor(sub_mode_name, video_resolution_name)
        else:
            if 'video_resolution' in config:
                video_resolution_name = config['video_resolution']
                self.page_CaptureActivity.set_sub_mode_video_resolution(sub_mode_name, video_resolution_name)
        if 'lapse_time' in config:
            lapse_time = config['lapse_time']
            self.page_CaptureActivity.set_timelapse_options(timelapse_mode_name, lapse_time)
            time.sleep(1)
        if 'fov_type' in config:
            fov_type_name = config['fov_type']
            self.page_CaptureActivity.set_fov_type(sub_mode_name, fov_type_name)
        return {
            'timelapse_mode_name': timelapse_mode_name
        }

    def test_sub_mode_video_photo_timelapse(self, config):
        logger.info(config)
        # self.page_CaptureActivity.start_live_stream()
        # time.sleep(3)
        resp = self.set_sub_mode_video_photo_timelapse(config)
        # self.page_CaptureActivity.stop_live_stream()
        timelapse_mode_name = resp['timelapse_mode_name']
        file_list_start = self.page_MainActivity_PhotoAlbum.get_all_file_list()
        file_info_start = self.page_MainActivity_PhotoAlbum.get_file_info_group_map()
        time.sleep(1)
        time_start = time.time_ns()
        self.page_CaptureActivity.start_timelapse(timelapse_mode_name)
        if 'cap_time' in config:
            cap_time = config['cap_time']
            time.sleep(cap_time)
        else:
            time.sleep(10)
        info = self.page_CaptureActivity.stop_timelapse(timelapse_mode_name)
        time_end = time.time_ns()
        logger.info(f'停止拍摄的response：{info}')
        file_list_end = self.page_MainActivity_PhotoAlbum.get_all_file_list()
        file_info_end = self.page_MainActivity_PhotoAlbum.get_file_info_group_map()
        time.sleep(1)
        self.check_video_photo_test_result(config, file_list_start, file_info_start, file_list_end, file_info_end,
                                           time_end-time_start)

    def set_sub_mode_photo_take_picture(self, config):
        sub_mode_name = config['sub_mode_name']
        self.set_curren_sub_mode_options(sub_mode_name)

        if 'photo_resolution' in config:
            photo_resolution_name = config['photo_resolution']
            self.page_CaptureActivity.set_sub_mode_photo_resolution(sub_mode_name, photo_resolution_name)
        if 'photography_self_timer' in config:
            photography_self_timer = config['photography_self_timer']
            self.page_CaptureActivity.set_photography_self_timer(sub_mode_name, photography_self_timer)
        if 'fov_type_name' in config:
            fov_type_name = config['fov_type_name']
            self.page_CaptureActivity.set_fov_type(sub_mode_name, fov_type_name)
        if 'photo_size_id' in config:
            photo_size_id = config['photo_size_id']
            self.page_CaptureActivity.set_photo_size_id(sub_mode_name, photo_size_id)
        if 'raw_capture_type_name' in config:
            raw_capture_type_name = config['raw_capture_type_name']
            self.page_CaptureActivity.set_raw_capture_type(sub_mode_name, raw_capture_type_name)
        pass

    def test_sub_mode_photo_take_picture(self, config):
        logger.info(config)
        sub_mode_name = config['sub_mode_name']
        self.set_sub_mode_photo_take_picture(config)
        aeb_ev_bias = None
        if 'aeb_ev_bias' in config:
            aeb_ev_bias = config['aeb_ev_bias']
        file_list_start = self.page_MainActivity_PhotoAlbum.get_all_file_list()
        file_info_start = self.page_MainActivity_PhotoAlbum.get_file_info_group_map()
        time.sleep(1)
        time_start = time.time_ns()
        info = self.page_CaptureActivity.take_picture(sub_mode_name, aeb_ev_bias=aeb_ev_bias)
        time_end = time.time_ns()
        logger.info(f'拍照的response：{info}')
        file_list_end = self.page_MainActivity_PhotoAlbum.get_all_file_list()
        file_info_end = self.page_MainActivity_PhotoAlbum.get_file_info_group_map()
        self.check_video_photo_test_result(config, file_list_start, file_info_start, file_list_end, file_info_end,
                                           time_end-time_start)

    def _get_collection_name(self):
        collection_name = f"{self.cam_info['camera_type']}_" \
                          f"{self.cam_info['firmwareRevision']}_" \
                          f"{self.cam_info['sensor_type_name']}_" \
                          f"{'selfie' if self.cam_info['is_selfie'] else 'no_selfie'}".replace(' ', '_')
        # return {'db_name': db_name, 'collection_name': collection_name}
        return collection_name

    def check_video_photo_test_result(self, config,
                                      file_list_start, file_info_start,
                                      file_list_end, file_info_end,
                                      time_cos, db_name='firmware_shooting_traversal',
                                      photography_options=None):
        """
        检查拍摄生成的视频和图片，并存储
        """
        if 'dont_check' in config:
            sub_mode_name = config['sub_mode_name']
            file_list = list(set(file_list_end) - set(file_list_start))
            logger.info(f'{sub_mode_name} 拍摄生成的视频列表：{file_list}')
            self.page_MainActivity_PhotoAlbum.delete_files(file_list)
            return None

        sub_mode_name = config['sub_mode_name']
        file_list = list(set(file_list_end)-set(file_list_start))
        logger.info(f'{sub_mode_name} 拍摄生成的视频列表：{file_list}')
        file_info_key = list(file_info_end.keys()-file_info_start.keys())
        logger.info(f'{sub_mode_name} 拍摄生成的视频info_key列表：{file_info_key}')
        # 可能时录像编码掉帧、相机高温、sd卡存储不够 无法拍摄，也可能是控制流出错 或其他原因导致的拍摄失败
        assert not len(file_info_key) == 0
        logger.info(f'{sub_mode_name} 拍摄生成的视频info数量')
        assert len(file_info_key) == 1
        file_info_list = file_info_end[file_info_key[0]]
        logger.info(f'{sub_mode_name} 拍摄生成的fileinfo：{file_info_list}')
        if photography_options is None:
            photography_options = self.page_CaptureActivity.get_photography_options(sub_mode_name)

        def save_data(data):
            collection_name = self._get_collection_name()
            logger.info(f'up data:{data}')
            collection = get_db_collection(db_name, collection_name)
            collection.delete_one({'tick_time': data['tick_time'], 'pc_hostname': data['pc_hostname']})
            ret = collection.insert_one(data)
            logger.info(f'up data done')
            return ret
        # 记录测试数据
        data_record = {
            'cam_info': self.cam_info,
            'config': config,
            # 测试时间
            'now_time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            # 当前时间 ns、主机名，作为查询的标志
            'tick_time': time.time_ns(),
            'pc_hostname': socket.gethostname(),
            # 录像拍照的耗时，单位ns
            'time_cos': time_cos,
            # 录像拍照新生成的文件数量
            'file_num': len(file_list),
            # file info接口从固件拿到的metadata数据
            'file_info_metadata_str': str(file_info_list).replace('\n', '|'),
            'photography_options': photography_options,
            'test_result': False,
            # 临时增加，为了生成测试报告增加的容错
            'fw_version': file_info_list[0]['metadata'].fw_version,
            'sub_mode_name': config['sub_mode_name'],
            'video_resolution': '' if not('video_resolution' in config.keys()) else config['video_resolution'],
        }
        save_data(data_record)

        res_app_total_time = 0
        from proto.extra_info_pb2 import ExtraMetadata
        metadata_first: ExtraMetadata = file_info_list[0]['metadata']
        for file_info in file_info_list:
            file_path = file_info['file_path']
            metadata: ExtraMetadata = file_info['metadata']
            if not (self.cam_info is None):
                # assert self.cam_info['is_selfie'] == metadata.is_selfie
                assert self.cam_info['serial_number'] == metadata.serial_number
                assert self.cam_info['camera_type'] == metadata.camera_type
                assert self.cam_info['firmwareRevision'] in metadata.fw_version
            assert metadata_first.resolution_size.x == metadata.resolution_size.x
            assert metadata_first.resolution_size.y == metadata.resolution_size.y
            assert metadata_first.frame_rate == metadata.frame_rate
            assert metadata_first.gamma_mode == metadata.gamma_mode
            assert metadata_first.dimension.x == metadata.dimension.x
            assert metadata_first.dimension.y == metadata.dimension.y
            assert metadata_first.fov_type == metadata.fov_type
            assert metadata_first.fw_version == metadata.fw_version
            assert metadata_first.file_group_info.type == metadata.file_group_info.type
            res_app_total_time += metadata.total_time

        if 'video_resolution' in config:
            video_resolution = config['video_resolution']
            # res_x = int(video_resolution.split('_')[1])
            # res_y = int(video_resolution.split('_')[2].split('P')[0])
            # rate = int(video_resolution.split('P')[1])
            # assert res_x == metadata_first.resolution_size.x
            # assert res_y == metadata_first.resolution_size.y
            # assert rate == metadata_first.frame_rate
            data_record.update({
                'video_resolution': video_resolution,
            })
            # TODO: 增加防抖、陀螺仪等校验
        if 'sub_mode_name' in config:
            data_record.update({'sub_mode_name': config['sub_mode_name']})
        data_record.update({
            'file_info_metadata': {
                'total_time': res_app_total_time,
                'resolution_size.x': metadata_first.resolution_size.x,
                'resolution_size.y': metadata_first.resolution_size.y,
                'frame_rate': metadata_first.frame_rate,
                'gamma_mode': metadata_first.gamma_mode,
                # 'gamma_mode_name': GammaMode.Name(metadata_first.gamma_mode),
                'dimension.x': metadata_first.dimension.x,
                'dimension.y': metadata_first.dimension.y,
                'fov_type': metadata_first.fov_type,
                # 'fov_type_name': FovType.Name(metadata_first.fov_type),
                'fw_version': metadata_first.fw_version,
                'sub_media_type': metadata_first.file_group_info.type,
                'sub_media_type_name': ExtraMetadata.SubMediaType.Name(metadata_first.file_group_info.type),
            },
            'fw_version': metadata_first.fw_version,
        })

        # -------------------以下是FFProbe的解析--------------------------
        res_file_size = 0
        probe_file_list = []
        list_vid_probe = []
        list_lrv_probe = []
        list_img_probe = []
        for file_uri in file_list:
            file_url = f'http://{self.host}:80{file_uri}'
            logger.info(f'开始解析：{file_url}')
            c_retry = 0
            probe = None
            while c_retry < 5:
                try:
                    probe = ffmpeg.probe(file_url)
                except ffmpeg._run.Error as e:
                    print(e)
                    time.sleep(1)
                except BaseException as e_base:
                    print(e_base)
                    time.sleep(1)

                c_retry +=1
            probe_file_list.append(probe)
            logger.info(f'解析结果：{file_url} {probe}')

            res_file_size += int(probe['format']['size'])
            basename = os.path.basename(probe['format']['filename'])
            if "VID_" in basename:
                list_vid_probe.append(probe)
            elif "LRV_" in basename:
                list_lrv_probe.append(probe)
            elif "IMG_" in basename:
                list_img_probe.append(probe)

        data_record.update({
            'probe_file_list': probe_file_list,
            'file_size': res_file_size,
        })
        save_data(data_record)
        if sub_mode_name in VideoSubMode.keys():
            logger.info(f'子模式是录像模式 {sub_mode_name}')
            assert len(list_vid_probe) > 0
            assert len(list_img_probe) == 0
            probe_vid_first = list_vid_probe[0]['streams'][0]
            for probe in list_vid_probe:
                probe_stream = probe['streams'][0]
                assert probe_stream['width'] == metadata_first.dimension.x
                assert probe_stream['height'] == metadata_first.dimension.y
                # assert probe_stream['width'] == probe_stream['coded_width']
                # assert probe_stream['height'] == probe_stream['coded_height']
                assert probe_stream['r_frame_rate'] == probe_stream['avg_frame_rate']
                # 只有相同media id相同时才要比对这个时长（好像多余）
                # assert probe_first_stream['duration'] == probe_stream['duration']
                # assert probe_first_stream['duration_ts'] == probe_stream['duration_ts']
                assert probe_stream['sample_aspect_ratio'] == probe_vid_first['sample_aspect_ratio']
                assert probe_stream['display_aspect_ratio'] == probe_vid_first['display_aspect_ratio']
            data_record.update({
                'VID': {
                    'width': probe_vid_first['width'],
                    'height': probe_vid_first['height'],
                    'r_frame_rate': probe_vid_first['r_frame_rate'],
                    'r_frame_rate': probe_vid_first['r_frame_rate'],
                    'codec_type': probe_vid_first['codec_type'],
                    'codec_name': probe_vid_first['codec_name'],
                    'codec_long_name': probe_vid_first['codec_long_name'],
                    'avg_frame_rate': probe_vid_first['avg_frame_rate'],
                    'sample_aspect_ratio': probe_vid_first['sample_aspect_ratio'],
                    'display_aspect_ratio': probe_vid_first['display_aspect_ratio'],
                    'count': len(list_vid_probe),
                    'bit_rate': list_vid_probe[0]['format']['bit_rate'],
                }
            })
            for probe in list_lrv_probe:
                probe_stream = probe['streams'][0]
                data_record.update({
                    'LRV': {
                        'width': probe_stream['width'],
                        'height': probe_stream['height'],
                        'r_frame_rate': probe_stream['r_frame_rate'],
                        'count': len(list_lrv_probe),
                    }
                })
        elif sub_mode_name in PhotoSubMode.keys():
            logger.info(f'子模式是拍照模式 {sub_mode_name}')
            assert len(list_vid_probe) == 0
            assert len(list_img_probe) > 0
            probe_img_first = list_img_probe[0]['streams'][0]
            for probe in list_img_probe:
                probe_stream = probe['streams'][0]
                # 不知道为什么有时候x y会反过来，先用这样的方式容错~
                dim_xy = [metadata_first.dimension.x, metadata_first.dimension.y]
                assert probe_stream['width'] in dim_xy
                assert probe_stream['height'] in dim_xy
                assert probe_stream['width'] == probe_stream['coded_width']
                assert probe_stream['height'] == probe_stream['coded_height']
            # TODO: 区分处理insp和dnp的图片
            # TODO: 增加exif校验
            data_record.update({
                'IMG': {
                    'width': probe_img_first['width'],
                    'height': probe_img_first['height'],
                    'codec_type': probe_img_first['codec_type'],
                    'codec_name': probe_img_first['codec_name'],
                    'codec_long_name': probe_img_first['codec_long_name'],
                    # insp和dnq 会表现不一样，暂时跳过
                    # 'sample_aspect_ratio': probe_img_first['sample_aspect_ratio'],
                    # 'display_aspect_ratio': probe_img_first['display_aspect_ratio'],
                    'count': len(list_img_probe),
                }
            })
        else:
            logger.info(f'不知道是什么模式 {sub_mode_name}')
            assert False
        data_record.update({'test_result': True, })
        # 保存：reco_data 到mongoDB
        save_data(data_record)
        # 保持到本地：
        logger.info(f'data_record：{data_record}')
        # 下载视频？删除视频？

    def reconnect(self):
        """
        TODO:重启、升级之后重连设备socket
        :return:
        """
        pass


if __name__ == '__main__':
    print('list_usb_device()', list_usb_device())
    # sys.exit(0)


    api = API_Proto('123456789ABC')
    api.init_socket()
    res = api.init_app_socket_con()
    logger.info(str(api.cam_info))
    for i in range(10):
        time.sleep(0.2)
        code, resp = api.get_options([
            # 是否正插反插，# 固件版本，
            'IS_SELFIE', 'FIRMWAREREVISION',
            # 设备序列号, readwrite，# 相机名 readOnly
            'SERIAL_NUMBER', 'CAMERA_TYPE',
            # 镜头信息，自己加的
            'SENSOR_ID', 'SENSOR_INFO',
            # 视频编码格式
            'VIDEO_ENCODE_TYPE',
        ])
        logger.info(str(resp))
    logger.info('for end')
    time.sleep(10)
    logger.info('api_close')
    api.close()
    logger.info('api_close')
    time.sleep(10)
    logger.info('end')

