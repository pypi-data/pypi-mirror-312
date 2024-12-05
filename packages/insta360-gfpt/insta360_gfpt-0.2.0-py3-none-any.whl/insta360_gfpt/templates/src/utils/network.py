import json
import os,time
import traceback

import requests
from loguru import logger
from .aliyun_oss import OssSystem
from requests_toolbelt.multipart import encoder

class ResultHandle(object):
    def __init__(self, config: object) -> object:
        self.config = config
        if config.get("test_env") is True:
            self.host = "http://api-produce-test.insta360.cn"
            self.token = "123"
            self.app = "all"
            self.app_version = "v1"
        else:
            self.host = "http://api-produce.insta360.cn"
            self.token = config.get("token")
            self.app = config.get("app")
            self.app_version = config.get("app_version")
        self.headers = {"app": self.app, "app_version": self.app_version,
                        "token": self.token}

    def send_request(self, method, url, data=None, log=True):
        for retry in range(0, 3):
            try:
                if method in ["post", "POST"]:
                    response = requests.post(url=url, json=data, headers=self.headers, timeout=3)
                    logger.info(f"{url},{data},{self.headers}")
                elif method in ["get", "GET"]:
                    response = requests.get(url=url, headers=self.headers, timeout=3)
                else:
                    logger.info(f"未支持的请求类型: {method}")
                    return False

                if response.status_code != 200 or response.json().get("code") != 0:
                    # code:1003是数据库不存在这条数据
                    if response.json().get("code") == 1003:
                        return response.json()

                    logger.error(response.json())
                    logger.error(url)
                    logger.error(self.headers)
                    continue
                resp = response.json()
                if log:
                    logger.debug(resp)
                return resp
            except Exception as e:
                logger.error(e)
                continue
        else:
            return False

    def upload_result(self, uri, data):
        """上报测试项结果"""
        url = self.host + uri
        return self.send_request("post", url, data)

    def get_result(self, uri, quere_text):
        # if quere_text.endswith("AD"):
        #     quere_text = quere_text[:-2]  # 去掉最后两个字符
        #     quere_text = quere_text+"FF"  # 去掉最后两个字符
        """根据uuid获取结果"""
        url = self.host + uri + quere_text
        logger.info(url)
        resp = self.send_request("get", url)
        logger.info(resp)
        if not resp:
            return False
        else:
            return resp.get("data")

    def clear_test_record(self, uri, data):
        url = self.host + uri
        logger.info(url)
        return self.send_request("post", url, data)

    def bind_sn_and_uuid(self, uri, data):
        url = self.host + uri
        logger.info(url)
        return self.send_request("post", url, data)

    def unbind_sn_and_uuid(self, uri, data):
        url = self.host + uri
        logger.info(url)
        return self.send_request("post", url, data)

    def get_sn_and_uuid_binding(self, uri):
        url = self.host + uri
        logger.info(url)
        resp = self.send_request("get", url)
        if not resp:
            return False
        else:
            return resp.get("data", False)

    def check_version_info(self, uri):
        url = self.host + uri
        logger.info(url)
        resp = self.send_request("get", url)
        if not resp or resp['code'] != 0:
            logger.error(f'检测版本信息错误：{resp}')
            return False
        else:
            return resp['data']

    def get_oss_info(self, data):
        url = self.host + self.config.get("oss", "/common/upload/uploadInfo")
        resp = self.send_request("post", url, data)
        if not resp:
            return False
        else:
            return resp.get("data")

    def update_info_to_insta(self, uri, data):
        """将上传后的文件链接回调给产测服务器保存链接"""
        url = self.host + uri
        result = self.send_request("post", url, data)
        if result is False:
            return False
        elif result.get("code") == 0:
            return True
        else:
            return False

    def upload_file_to_oss(self, oss_req_data: list, file, insta_callback_uri):
        """
        上传测试文件到OSS流程:
        1. 产测项测试执行完成，PASS or NG
        2. 将测试产生的文件上传到阿里云OSS系统，调用本方法
            2.1 调用insta服务器的<oss上传>接口,获取OSS相关信息和文件url
            2.2 通过获取到的OSS信息连接OSS系统
            2.3 上传文件到OSS系统
            2.4 上传成功，调用insta服务器对应项目的<上传结果回调>接口，传入文件url
            2.5 就可以在浏览器直接用这个文件url查看文件了
        """
        # 从服务器获取oss鉴权信息
        info = self.get_oss_info(oss_req_data)
        if not info:
            return False
        else:
            info = info.get("result")
        oss_url = info.get("url")
        if not oss_url:
            logger.error(f"获取oss url异常  url:{oss_url}")
            return False
        # 上传文件到OSS
        oss = OssSystem(info)
        if not oss.check_info():
            logger.error("获取OSS信息异常")
            return False
        result = oss.upload_file(file)
        if not result:
            logger.error("上传文件到OSS系统失败!")
            return False
        else:
            logger.info(f"上传成功,文件链接: {oss_url}")
        # 上传成功，将链接返回给服务器
        uuid = oss_req_data.get("tag_id")
        test_item = oss_req_data.get("item")
        data = {"uuid": uuid, "item": test_item, "url": oss_url}
        result = self.update_info_to_insta(insta_callback_uri, data)
        if result:
            return oss_url
        else:
            return False
    def query_ptzUuid_binding(self, uuid):
        url = self.host + self.config.get("query_ptz_uuid_binding") + f"?machine_uuid={uuid}"
        resp = self.send_request("get", url)
        if not resp:
            return False
        else:
            return resp.get("data")

    def query_uuid_sensor_id_binding(self, uuid):
        # if uuid.endswith("AD"):
        #     uuid = uuid[:-2]  # 去掉最后两个字符
        #     uuid = uuid+"FF"
        url = self.host + self.config.get("query_sensor_binding") + f"?yt_uuid={uuid}"
        logger.info(url)
        resp = self.send_request("get", url)
        if not resp:
            return False
        else:
            return resp.get("data")

    def query_uuid_binding(self, sn):
        # logger.info(self.config)
        if "IAB" in sn:
            url = self.host + self.config.get("query_uuid_binding") + f"?serial={sn}"

        else:
            url = self.host + self.config.get("query_uuid_binding") + f"?uuid={sn}"
        # logger.info(url)
        resp = self.send_request("get", url, log=False)
        if not resp:
            return False
        else:
            return resp.get("data")

    def unbinding_ptz_uuid(self, ptz_uuid, uuid):
        dd = {
            "machine_uuid": uuid,
            "yt_uuid": ptz_uuid,
        }
        url = self.host + self.config.get("ptz_unbinding")
        resp = self.send_request("post", url, dd)
        if not resp:
            return False
        else:
            return resp.get("data")
    def binding_ptz_uuid(self, ptz_uuid, uuid):
        dd = {
            "machine_uuid": uuid,
            "yt_uuid": ptz_uuid,
        }
        url = self.host + self.config.get("ptz_binding")
        resp = self.send_request("post", url, dd)
        if not resp:
            return False
        else:
            return resp.get("data")

    def binding_sensor_id(self, uuid, sensor_id1, sensor_id2):
        dd = {
            "uuid": uuid,
            "sensor_id1": sensor_id1,
            "sensor_id2": sensor_id2
        }
        # dd = json.dumps(dd)
        url = self.host + self.config.get("sensor_binding")
        resp = self.send_request("post", url, dd)
        if not resp:
            return False
        else:
            return resp.get("data")

    def unbinding_sensor_id(self, uri, data):
        url = self.host + uri
        logger.info(url)
        resp = self.send_request("post", url, data)
        if not resp:
            return False
        else:
            return resp.get("data")
    def get_factory_server_ip(self, uri):
        """获取工厂标定服务器IP"""
        url = self.host + uri
        # url = self.host + uri + "?network=zhongshan&service_name=integrated"
        logger.info(url)
        resp = self.send_request("get", url)
        logger.info(f"获取标定服务器返回{resp}")
        if not resp:
            return False
        else:
            return resp.get("data")

    def upload_calibrate_photo(self, url, files, uuid, callback):
        # 上传标定图片
        self._progress = 0
        def my_monitor(monitor):
            progress = int((monitor.bytes_read / monitor.len) * 100)
            # # callback(f"{progress}% ({monitor.bytes_read}/{monitor.len})")
            # callback(progress)
            # # print("\r 文件上传进度：%d%%(%d/%d)" % (progress, monitor.bytes_read, monitor.len), end=" ")
            if self._progress != progress:
                self._progress = progress
                callback(progress)
        for retry in range(0, 3):
            try:
                files_open = {}
                for i in range(len(files)):
                    files_open[f"f{i+1}"] = open(files[i], 'rb')

                fields = [('uuid', uuid)]
                for i in range(len(files)):
                    image_data = ('images', (os.path.basename(files[i]), files_open[f"f{i+1}"], 'multipart/form-data'))
                    fields.append(image_data)

                e = encoder.MultipartEncoder(fields)
                m = encoder.MultipartEncoderMonitor(e, my_monitor)
                response = requests.post(url, data=m,
                                         headers={'Content-Type': m.content_type}, timeout=1)
                for key in files_open:
                    files_open[key].close()
                logger.debug(response)
                if response.status_code != 200:
                    logger.error(f"{uuid}上传图片失败")
                    continue
                resp = response.json()
                logger.info(resp)
                logger.info("-------------------上传图片到标定服务器完成-------------------")

            except Exception as e:
                traceback.print_exc()
                logger.error(f"上传标定图片异常: {e}")
                time.sleep(1)
                continue
            else:
                return resp
        else:
            return False

    def upload_gyro_video(self, url, files, uuid, callback, LensNum):
        #上传陀螺仪标定视频，双镜头上传两个视频;单镜头上传一个；
        self._progress = 0
        def my_monitor(monitor):
            progress = int((monitor.bytes_read / monitor.len) * 100)
            if self._progress != progress:
                self._progress = progress
                callback(progress)
        for retry in range(0, 3):
            try:
                if LensNum == 2:
                    files_open = {"f1": open(files[0], 'rb'), "f2": open(files[1], 'rb')}
                    e = encoder.MultipartEncoder(
                        fields=[('uuid', uuid),
                                ('video', (os.path.basename(files[0]), files_open["f1"], 'multipart/form-data')),
                                ('video', (os.path.basename(files[1]), files_open["f2"], 'multipart/form-data'))
                                ]
                    )
                else:
                    files_open = {"f1": open(files, 'rb')}
                    e = encoder.MultipartEncoder(
                        fields={'uuid': uuid,
                                'video': (os.path.basename(files), files_open["f1"], 'multipart/form-data')})
                m = encoder.MultipartEncoderMonitor(e, my_monitor)
                response = requests.post(url, data=m,
                                         headers={'Content-Type': m.content_type}, timeout=30)
                for key in files_open:
                    files_open[key].close()
                resp = response.json()
                logger.info(resp)
                if response.status_code != 200:
                    logger.error(f"{uuid}上传视频失败")
                    continue
                logger.info("-------------------上传视频到陀螺仪标定服务器完成-------------------")

            except Exception as e:
                logger.error(f"上传标定陀螺仪标定视频异常: {e}")
                time.sleep(1)
                continue
            else:
                return resp
        else:
            return False


    def upload_monitor(self, monitor):
        print(round(monitor.bytes_read/monitor.len*100,2))
     
        url = 'http://127.0.0.1:18019/upload-file'
         
        headers={}
         
        path=r'C:\file.txt'
        filename=path.split('\\')[-1]
        multipart_encoder = encoder.MultipartEncoder(
            fields={
                filename: (filename, open(path, 'rb'), 'text/plain')#根据上传文件类型的不同而不同
            },
        )
        monitor = encoder.MultipartEncoderMonitor(multipart_encoder, self.upload_monitor)
         
         
        boundary=multipart_encoder.content_type.split('=')[-1]
        headers['Content-Type']=multipart_encoder.content_type
        r = requests.post(url, data=monitor, headers=headers)
        print(r.text)
        

def get_audio_lincese(sn):
    url = "https://license-center.mobvoi.com/v2/license"
    if sn[0:3] == "IBK":      # GO3 SE
        auth = "Basic aW5zdGEzNjAtZ28zc2U6MTZkNWFmOTViZWQ0ZDM2MTJhYmM3NThiZGNmMjkzY2Q="
    elif sn[0:3] == "IAT":   # GO3
        auth = "Basic aW5zdGEzNjAtZ28zOmVkZjg0YmFhOGU3NDgzZDBhNjU2YjNmNmM4ZDQyZDE4"
    else:
        logger.error("产品错误")
        return False
    headers = {"Content-Type": "application/json", "Authorization": auth}
    data = {"public_id": sn}
    for retry in range(0, 3):
        response = requests.post(url=url, json=data, headers=headers)
        if response.status_code != 200:
            logger.error(response.json())
            continue
        resp = response.json()
        # logger.debug(resp)
        return resp
"""
file = r"D:\desktop-dev\go3se-host\测试结果\近景冷解析\20220826\c3770a73-9586-405e-b03a-7d1fe7720742\IMG_20220819_124719_00_032.jpg"
_data = {
            "product": "go3_dvt2",
            "type": "half_product",
            "tag_id": "c3770a73-9586-405e-b03a-7d1fe7720742",
            "item": "near_sight_cold_analysis",
            "file_name": os.path.basename(file)
        }
config = {"test_token": "123", "test_env": True}
res = ResultHandle(config)
res.upload_file_to_oss(_data, file, "")
"""