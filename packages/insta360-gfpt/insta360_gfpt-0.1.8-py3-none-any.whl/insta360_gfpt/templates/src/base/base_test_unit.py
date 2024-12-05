import os
import json
import datetime
import threading
import time
from enum import Enum
from PySide6.QtGui import QDesktopServices
from PySide6.QtCore import QObject, Signal, Slot, Property, QMetaObject, QEnum, QUrl
from PySide6.QtQml import QmlElement
from loguru import logger

from src.utils.network import ResultHandle
from src.utils.revolving_table import Calibration


QML_IMPORT_NAME = "InsFactory"
QML_IMPORT_MAJOR_VERSION = 1
QML_IMPORT_MINOR_VERSION = 0

#
# def len(_units):
#     pass


@QmlElement
class Unit(QObject):
    """docstring for Unit"""

    @QEnum
    class TestStatus(Enum):
        NotTested = -1
        Failed = 0
        Passed = 1
        Testing = 2

    statusChanged = Signal()
    showDecideBtnChanged = Signal()
    enableDecideBtnChanged = Signal()
    infoChanged = Signal()
    unitLogChanged = Signal()
    uploadedChanged = Signal()
    errorInfoChanged = Signal()
    nonNotify = Signal()

    def __init__(self, _id, _name, _test_auto, _qml, _url, _parent=None, _config=None):
        super(Unit, self).__init__()
        self._id = _id
        self._name = _name
        self._qml = _qml
        self._url = _url
        self._config = _config
        self._status = self.TestStatus.NotTested.value
        self._test_auto = _test_auto
        self._show_decide_btn = None
        self._hide_start_btn = False
        self._enable_decide_btn = None
        self._has_test_file = False
        self._test_file = ""
        self._unit_dir = None
        self._info = ""
        self._unit_log = ""
        self._parent = _parent  # Module
        self._error_reason = ""  # 上报error_reason
        self._test_data = ""  # 上报test_data
        self.isreport = False # mes 报工是否完成
        self._uploaded = None
        self._error_info = []

    def test_done(self):
        u""""""
        self.teardown()
        logger.info("测试Unit上报测试完成，继续上报给proj")
        self._parent.test_done()
        # self.set_info("测试完成")

    def update_local_status(self):
        self._parent.update_final_status()

    @Property(int, notify=statusChanged)
    def status(self):
        return self._status

    @Slot(int)
    def set_status(self, status):
        self._status = status
        # if status != self.TestStatus.Failed.value:
        self.statusChanged.emit()

    @Property(str, notify=nonNotify)
    def name(self):
        return self._name

    @Property(bool, notify=nonNotify)
    def uploaded(self):
        return self._uploaded

    @Slot(bool)
    def set_uploaded(self, status):
        if self._uploaded != status:
            self._uploaded = status
            self.uploadedChanged.emit()

    @Property(bool, notify=nonNotify)
    def has_test_file(self):
        return self._has_test_file

    @Property(bool, notify=nonNotify)
    def hide_start_btn(self):
        if hasattr(self, "_hide_start_btn"):
            return self._hide_start_btn
        else:
            return False

    @Property(str, notify=infoChanged)
    def info(self):
        return self._info

    @Slot(str)
    def set_info(self, msg):
        self._info = msg
        self.infoChanged.emit()

    @Property(str, notify=unitLogChanged)
    def unit_log(self):
        return self._unit_log

    @Slot(str)
    def set_unit_log(self, msg):
        self._unit_log = msg
        self.unitLogChanged.emit()

    @Property(bool, notify=nonNotify)
    def test_auto(self):
        return self._test_auto

    @Property(str, notify=nonNotify)
    def qmlfile(self):
        return self._qml

    @Property(bool, notify=showDecideBtnChanged)
    def show_decide_btn(self):
        return self._show_decide_btn

    def set_show_decide_btn(self, status: bool):
        self._show_decide_btn = status
        self.showDecideBtnChanged.emit()
        if status:
            self.set_info("请判定结果")

    @Property(bool, notify=enableDecideBtnChanged)
    def enable_decide_btn(self):
        return self._enable_decide_btn

    def set_enable_decide_btn(self, status: bool):
        self._enable_decide_btn = status
        self.enableDecideBtnChanged.emit()
        if status:
            self.set_info("请判定结果")

    @Slot()
    def test_ok(self, dev=None, is_upload=True):
        self.set_show_decide_btn(False)
        self.set_status(self.TestStatus.Passed.value)
        if is_upload:
            self.set_info("上报测试结果到服务器中...")
            t = threading.Thread(target=self.upload_result, args=[dev, ], daemon=True)
            t.start()
        else:
            self.test_done()

    @Slot()
    def test_ng(self, dev=None, is_upload=True):
        self.set_show_decide_btn(False)
        self.set_status(self.TestStatus.Failed.value)
        if is_upload:
            # self.set_info("上报测试结果到服务器中...")
            t = threading.Thread(target=self.upload_result, args=[dev, ], daemon=True)
            t.start()
        else:
            self.test_done()
        # self.upload_result(dev)
        # self.test_done()
        # if self._parent._parent._parent._config['config']['need_log']:
        #     logger.debug('测试ng了，需要下载日志。。。。')
        #     self.download_log()

    def handle_test_result(self, flag):
        if flag is True:
            self.test_ok()
        elif flag is False:
            self.test_ng()
        # elif flag == "":
        #     return ""
        else:
            self.set_status(self.TestStatus.NotTested.value)
            self._parent._parent._parent.set_testing(False)

    @Property(str, notify=errorInfoChanged)
    def error_info(self):
        return "\n".join(self._error_info)

    @Slot(str)
    def set_error_info(self, info):
        self._error_info.append(info)
        self.errorInfoChanged.emit()

    @Slot()
    def reset_error_info(self):
        self._error_info = []
        self.errorInfoChanged.emit()

    # 相机标定转台复位
    @Slot()
    def reset_revolving(self):
        self.set_info("复位中...")
        host_ip = self._config["host_ip"]
        logger.info(f"复位按钮按下，复位中")
        try:
            master = Calibration(host_ip).start()
            turn_result, error = Calibration(host_ip).run(master, "Reset")
            if not turn_result:
                logger.error(f"转台未旋转到位，{str(error)}")
                self.set_info(f"转台未旋转到位，{str(error)}")
            else:
                logger.info(f"转台复位成功")
                self.set_info(f"转台复位成功")
        except Exception as e:
            logger.error(f"复位发生错误：{e}")
            self.set_info(f"复位发生错误：{e}")

    @Slot()
    def open_module_dir(self):
        open_dir = self._unit_dir
        try:
            self.download_camera_log()
            cur_dev_uuid = self._parent._parent._parent.cur_dev._uuid
            cur_dev_ptz_uuid = self._parent._parent._parent.cur_dev.ptz_uuid
        except Exception as e:
            cur_dev_uuid = ""
            cur_dev_ptz_uuid = ""
        if not self._unit_dir:
            root = os.getcwd()
            now = datetime.datetime.now().strftime("%Y%m%d")
            if os.path.exists(f"{root}\\result\\{self._parent._parent._id}\\{self._id}\\{now}\\{cur_dev_uuid}\\{cur_dev_ptz_uuid}"):
                open_dir = f"{root}\\result\\{self._parent._parent._id}\\{self._id}\\{now}\\{cur_dev_uuid}\\{cur_dev_ptz_uuid}"
            elif os.path.exists(f"{root}\\result\\{self._parent._parent._id}\\{self._id}\\{now}\\{cur_dev_uuid}"):
                open_dir = f"{root}\\result\\{self._parent._parent._id}\\{self._id}\\{now}\\{cur_dev_uuid}"
            elif os.path.exists(f"{root}\\result\\{self._parent._parent._id}\\{self._id}\\{now}"):
                open_dir = f"{root}\\result\\{self._parent._parent._id}\\{self._id}\\{now}"
            elif os.path.exists(f"{root}\\result\\{self._parent._parent._id}\\{self._id}"):
                open_dir = f"{root}\\result\\{self._parent._parent._id}\\{self._id}"
            elif os.path.exists(f"{root}\\result\\{self._parent._parent._id}"):
                open_dir = f"{root}\\result\\{self._parent._parent._id}"
            elif os.path.exists(f"{root}\\vb_test_data\\{now}"):
                open_dir = f"{root}\\vb_test_data\\{now}"
            else:
                open_dir = f"{root}\\result"
        else:
            try:
                cur_dev_uuid = self._parent._parent._parent.cur_dev._uuid
                open_dir = self._unit_dir + f"\\{cur_dev_uuid}"
            except Exception as e:
                open_dir = self._unit_dir
        logger.info(open_dir)
        QDesktopServices.openUrl(QUrl.fromLocalFile(open_dir))

    def download_camera_log(self):
        """获取老化异常日志，并上传服务器"""
        cur_dev = self._parent._parent._parent.cur_dev
        resp = cur_dev.camera.api.get_log_file()
        if resp['result'] != 'success':
            self.log_error(f"获取日志失败: {resp}")
            return
        # 创建测试文件夹
        run_threads = []
        self.create_result_dir(cur_dev._uuid, cur_dev.ptz_uuid)
        tar_path = os.path.join(self._unit_dir, cur_dev._uuid)

        if self._parent._parent._parent._project == 'PC100':
            files_path = resp['file_path'].split('|')
            for name in files_path:
                file_path, file_name = os.path.split(name)
                t = threading.Thread(target=self.download, args=[
                    cur_dev, name, os.path.join(tar_path, file_name)])
                t.setDaemon(True)
                run_threads.append(t)
            for t in run_threads:
                t.start()
                time.sleep(0.1)

        else:
            file_path, file_name = os.path.split(resp['file_name'])
            log_info = os.path.join(tar_path, file_name)

            if not cur_dev.camera.download_file(resp['file_name'], log_info):
                self.log_error(f'日志{file_name}下载失败')
            with open(log_info, 'r', encoding='utf-8') as f:
                text = f.read()

            logger.info(f'log日志文件：{file_name}内容：{text}')
            log_names = self.parse_log_info(text)
            if not log_names:
                self.log_error(f'解析{file_name}文件内容失败，无法下载相机日志')
                return

            for name in log_names:
                origin_path = file_path + '/' + name
                t = threading.Thread(target=self.download, args=[
                    cur_dev, origin_path, os.path.join(tar_path, name)])
                t.setDaemon(True)
                run_threads.append(t)
            for t in run_threads:
                t.start()
                time.sleep(0.1)

        self.log_error('日志下载完成')

    def read_white_balance_correct_config(self):
        """获取白平衡校正的参数"""
        wbc_config_file = f"{os.getcwd()}\\project\\{self._parent._parent._parent._project}\\white_balance_correct_config.json"
        if not os.path.exists(wbc_config_file):
            logger.error(f"读取项目文件{wbc_config_file}失败")
        with open(wbc_config_file, "r", encoding="utf-8") as f:
            wbc_config = json.load(f)
        for (key, value) in wbc_config.items():
            wbc_config[key] = str(value)
        logger.info(f"文件读取到白平衡测试设置参数为：{wbc_config}")
        return wbc_config

    def parse_log_info(self, content):
        """解析获取log文件名"""
        if not content:
            return []
        try:
            log_files = content.split('\x00\n')[1:-1]
            logger.debug(f'解析获取到的日志文件名列表：{log_files}')
            return log_files
        except Exception as e:
            logger.error(e)
            return []

    def download(self, dev, origin, target):
        # self.log_error(f'正在下载{origin}文件'.center(50, '*'))
        return dev.camera.download_file(origin, target)

    def add_error_reason(self, reason):
        logger.info(f"添加错误原因： {reason}")
        if self._error_reason:
            self._error_reason += "\n"
        self._error_reason += f"{reason}"

    def add_test_data(self, data):
        logger.info(f"添加错误原因： {data}")
        self._test_data += f"{data}\n"
        logger.info(f"_test_data: {self._test_data}")

    def log_error(self, error):
        logger.error(error)
        self.set_info(error)
        # self.add_error_reason(error)

    def upload_result(self, dev):
        if self._id == "":
            self.set_info("")
            self.test_done()
            return
        if self._status != self.TestStatus.NotTested.value:
            proj = self._parent._parent._parent  # unit->module->group->proj
            result_handler = ResultHandle(proj._config["config"])
            if dev is None:
                dev = proj.cur_dev
            uri = self._parent._parent._upload_url
            model = self._parent._parent._id
            # self.set_info("上报测试结果到服务器中...")
            if self._test_file:
                logger.info("有测试文件要上传到OSS系统")
                # proj_cfg = self._parent._parent._parent._config
                # logger.info(proj_cfg)
                insta_callback_uri = proj._config["config"].get("upload_callback")
                if model == "waike":
                    oss_req_data = {
                        "product": proj._config["config"].get("id"),
                        "type": self._parent._parent._id,
                        "tag_id": dev.sn,
                        "item": self._id,
                        "file_name": os.path.basename(self._test_file)
                    }
                elif model == "sensor":
                    oss_req_data = {
                        "product": proj._config["config"].get("id"),
                        "type": self._parent._parent._id,
                        "tag_id": dev.ptz_uuid,
                        "item": self._id,
                        "file_name": os.path.basename(self._test_file)
                    }
                else:
                    oss_req_data = {
                        "product": proj._config["config"].get("id"),
                        "type": self._parent._parent._id,
                        "tag_id": dev._uuid,
                        "item": self._id,
                        "file_name": os.path.basename(self._test_file)
                    }
                self.add_test_data(result_handler.upload_file_to_oss(oss_req_data, self._test_file, insta_callback_uri))
                logger.info(f"_test_data: {self._test_data}")
            # 上报测试项结果
            station = self._parent._id
            if self._id in ["wifi_bluetooth", "wifi_audio", "wifi_wifi", "wifi_key", "wifi_led"]:
                # 服务器奇怪的工站逻辑
                station = "half_wifi"
            # 为了合并工站，产生的神奇逻辑
            if self._id in ["gyro_correct"]:
                station = "product_function_station5"
            if self._id in ["white_balance_correct"]:
                station = "product_function_station10"
            if model == "waike":
                data = {
                    "serial": dev.sn, "item": self._id,
                    "ok": self._status == self.TestStatus.Passed.value,
                    f"{self._id}": self._status == self.TestStatus.Passed.value,
                    "test_data": self._test_data}
            elif model == "sensor":
                data = {
                    "yt_uuid": dev.ptz_uuid, "item": self._id,
                    "ok": self._status == self.TestStatus.Passed.value,
                    f"{self._id}": self._status == self.TestStatus.Passed.value,
                    "test_data": self._test_data}
            else:
                data = {
                    "uuid": dev._uuid, "item": self._id,
                    "ok": self._status == self.TestStatus.Passed.value,
                    f"{self._id}": self._status == self.TestStatus.Passed.value,
                    "test_data": self._test_data}

            logger.info("上传结果到产测服务器")
            work_sever_result = result_handler.upload_result(uri, data)

            if self._parent._units:
                name = self._name
            else:
                name = self._parent._name
            number = self._parent._mes_id

            vb_999_mes_update = False
            if number == "VB_999工站":
                logger.info("开始进行报工第一个工站")
                response, upmess = dev._zsMes.report_uuid(dev.ptz_uuid, number)
                if response:
                    self.set_info("VB第0个工站报工成功，可以进行后面测试")
                    self.isreport = True
                    vb_999_mes_update = response
                else:
                    self.set_info(f"VB第0个工站报工失败，需要重新过这个工站,错误消息{upmess}")
                    self.isreport = False
                    vb_999_mes_update = response


            if number == "VB_002工站":
                # 先进行查询关系 ，看看是否绑定的有
                response, bind_resp = dev._zsMes.query_sn_relation(dev.ptz_uuid)
                if response:
                    logger.info(f"使用产品Sn = {dev.ptz_uuid}查询成功")
                else:
                    # 虚拟云台UUID
                    # ptz_uuid = dev.ptz_uuid
                    # if ptz_uuid.endswith("-6"):
                    #     ptz_uuid = ptz_uuid[:-4]  # 去掉最后4个字符
                    #     ptz_uuid = ptz_uuid+"XP"  # 去掉最后两个字符


                    # 虚拟sensor_id1   "SY9E37G9999" 改为 “SY9E37G9966”
                    # sensor_id1 = dev.sensor_id1
                    # if sensor_id1.endswith("BL"):
                    #     sensor_id1 = sensor_id1[:-2]  # 去掉最后两个字符
                    #     sensor_id1 = sensor_id1+"XQ"
                    """
                    虚拟的数据
                    """
                    # dev.sensor_id1 = "SY9E43R00AC"
                    # sensor_id1 = dev.sensor_id1
                    #
                    # dev.sensor_id2 = "TSTSNP406801240426001324"
                    # sensor_id2 = dev.sensor_id2
                    #
                    # if sensor_id2.endswith("24"):
                    #     sensor_id2 = sensor_id2[:-2]  # 去掉最后两个字符
                    #     sensor_id2 = sensor_id2+"11"
                    #
                    # bind_info = [
                    #     {"key": "sensor_id1", "value": sensor_id1},
                    #     {"key": "sensor_id2", "value": sensor_id2},
                    #     #{"key": "yt_uuid", "value":ptz_uuid}
                    #
                    # ]

                    """
                    正式的数据
                    """
                    #正式环境需要修改
                    bind_info = [
                        {"key": "sensor_id1", "value": dev.sensor_id1},
                        {"key": "sensor_id2", "value": dev.sensor_id2}
                        # 后面正式环境这个耗料应该不需要再002工站绑定
                        # {"key": "yt_uuid", "value": dev.ptz_uuid}
                    ]
                    # 打印发送的数据
                    logger.info(f"Sending data: {json.dumps(bind_info, indent=2, ensure_ascii=False)}")

                    # 回来补充self.serial_number
                    # 拿替换SN

                    # 进行绑定
                    try:
                        logger.info(f"procedure_code: {number}")
                        logger.info(f"data: {bind_info}")
                        bind_result, message = dev._zsMes.bind_info(dev.ptz_uuid, bind_info, number)
                        if bind_result:
                            logger.info("绑定成功")
                            self.set_info("已经有绑定结果了")
                        else:
                            logger.info(f"绑定失败,{message}")
                    except TypeError as e:
                        logger.error(f"绑定失败，TypeError: {e}")
            vb_008_mes_update = False
            if number == "VB_008工站":
                if self._status == self.TestStatus.Passed.value:
                    test_result = 1
                else:
                    test_result = 0
                names = ["48c白平衡确认", "jn1白平衡确认", "48c脏污检测", "jn1脏污检测"]
                dev._zsMes.ptz_uuid = dev.ptz_uuid
                vb_008_mes_update = False
                if  test_result == 1 and dev.ptz_uuid != "":
                    count = 1
                    test_result1 = 1
                    test_data = "testData:1"
                    for name1  in names:
                        logger.info(f"VB_008工站 开始保存结果，第{count}次，这次保存质量特性是{name1}")
                        update_mes_zs_result, message = dev._zsMes.update_mes(number, name1, test_result1,test_data)
                        count+=1
                        time.sleep(1)
                        vb_008_mes_update = update_mes_zs_result
                    logger.info(f"VB_008工站 成功结果，全部保存完毕")
                elif test_result == 0 and dev.ptz_uuid != "":
                    count = 1
                    test_result2 = 0
                    test_data = "testData:1"
                    for name1 in names:
                        logger.info(f"VB_008工站 开始保存结果，第{count}次，这次保存质量特性是{name1}")
                        update_mes_zs_result, message = dev._zsMes.update_mes(number, name1, test_result2, test_data)
                        count += 1
                        time.sleep(1)
                        vb_008_mes_update = update_mes_zs_result
                    logger.info(f"VB_008工站 失败结果，全部保存完毕")

            vb002isbind = False
            vb010isbind = False
            # 如果是VB_000工站 不上报结果
            if number == "VB_000工站":


                update_mes_zs_result = True
                # 上传错误码到mes
                if name == "上传错误码":
                    # 获取当前脚本的目录
                    current_dir = os.path.dirname(__file__)

                    # 构建目标文件的相对路径
                    target_file_path = os.path.join(current_dir, '../../project/vb/errcode.json')

                    # 规范化路径（将相对路径转换为绝对路径）
                    target_file_path = os.path.abspath(target_file_path)
                    self.set_info("上传错误码中...")
                    workOrderCode = dev._zsMes.workOrderCode
                    if workOrderCode == "":
                        logger.info("生产单号没有填写", True)
                        return
                    with open(target_file_path, "r", encoding="utf-8") as f:
                        test_errcode = json.load(f)
                        for data in test_errcode["组装后工序"]:
                            for key in data:
                                for key2 in data[key]:
                                    if "工站编码" == key2:
                                        continue
                                    print(key, workOrderCode, data[key][key2], key2)
                                    dev._zsMes.update_mes_errcode(key, workOrderCode, data[key][key2], key2)
            else:
                if self._status == self.TestStatus.Passed.value:
                    test_result = 1
                else:
                    test_result = 0
                # 为了如果test_data里面没有值，mes会报返回结果不能为空
                if self._test_data == "":
                    self._test_data="testData"

                module_value = self._parent.status
                logger.info(f"获得的当前工站的测试值是 ======{module_value}")
                dev._zsMes.ptz_uuid = dev.ptz_uuid
                dev._zsMes.serial = dev.sn
                update_mes_zs_result = False  # 初始化变量并赋默认值
                if name != "白平衡确认及脏污检测" and name != "获取UUID":
                    if number == "VB_002工站":
                        response, bind_resp = dev._zsMes.query_sn_relation(dev.ptz_uuid)
                        if response:
                            if self._status == self.TestStatus.Passed.value:
                                test_result = 1
                            else:
                                test_result = 0
                            # 为了如果test_data里面没有值，mes会报返回结果不能为空
                            if self._test_data == "":
                                self._test_data = "testData"
                            logger.info(f"使用产品Sn = {dev.ptz_uuid}查询成功")
                            logger.info("vb002工站已完成绑定可以去保存结果！")
                            vb002isbind = True
                            update_mes_zs_result, message = dev._zsMes.update_mes(number, name, test_result, self._test_data)
                            if not update_mes_zs_result:
                                logger.info(f"vb002工站,Mes保存检验结果出现问题，原因是{message}")
                                vb002isbind = False
                        else:
                            logger.info("vb002工站没有完成绑定，不让保存结果!")
                            vb002isbind = False

                    if number == "VB_010工站":
                        response, bind_resp = dev._zsMes.query_sn_relation(dev.ptz_uuid)
                        if response:
                            if self._status == self.TestStatus.Passed.value:
                                test_result = 1
                            else:
                                test_result = 0
                            # 为了如果test_data里面没有值，mes会报返回结果不能为空
                            if self._test_data == "":
                                self._test_data = "testData"
                            logger.info(f"使用产品Sn = {dev.ptz_uuid}查询成功")
                            logger.info("vb010工站已完成绑定可以去保存结果！")
                            vb010isbind = True
                            # 保存结果
                            update_mes_zs_result, message = dev._zsMes.update_mes(number, name, test_result,self._test_data)
                            if not update_mes_zs_result:
                                logger.info(f"vb010工站,Mes保存检验结果出现问题，原因是{message}")
                                vb010isbind = False
                        else:
                            logger.info("vb010工站没有完成绑定，不让保存结果!")
                            vb010isbind = False
                    if number != "VB_002工站" and  number != "VB_010工站":
                        update_mes_zs_result, message = dev._zsMes.update_mes(number, name, test_result, self._test_data)
                    if not update_mes_zs_result:
                        logger.info(f"{number},Mes保存检验结果出现问题，原因是{message}")
                elif vb_008_mes_update or vb_999_mes_update:
                    update_mes_zs_result = True
            # 上报mes
            if work_sever_result and update_mes_zs_result and self._status == self.TestStatus.Passed.value:
                # 上传测试结果到产测服务器了 ，mes也保存结果了，测试结果也是OK了，
                # 获取工站的每一个unit的测试结果，判断是否都完成了
                Notest_res = []
                Notest_res_name = []
                module_s = self._parent
                for module_s_units in module_s.units:
                    # 如果有测试项 还没有测试的话，保存这个测试项的名
                    if module_s_units.status == -1:
                        Notest_res_name.append(module_s_units.name)
                if Notest_res_name:
                    # 根据缺少的工站个数去上传结果
                    for checkpoint in Notest_res_name:
                        logger.info(f"有{len(Notest_res_name)}个还没有保存结果")
                        count = 1
                        count += 1
                    logger.info(f"测试结果是通过了，但是还有其他测试项：{checkpoint}，没有完成先不报工")
                    self.set_info(f"测试结果是通过了，但是还有其他测试项：{checkpoint}，没有完成先不报工")
                    self.isreport = False
                    time.sleep(1)

                else:
                    test_fail = []
                    # 判断测试项都测完了，且所有的测试项都是pass 可以直接报工
                    for module_s_units in module_s.units:
                        # 如果测试项都通过了，但是 测试项是有测试结果没有通过的，没有通过的值为0
                        if module_s_units.status == 0:
                            # 把测试未通过的保存下来
                            test_fail.append(module_s_units.name)

                    test_fail_num = len(test_fail)
                    # 如果全部测试项的测试结果都是 通过的话，那么这里不会有数量
                    if test_fail_num == 0:
                        logger.info("恭喜所有的测试项都测试通过了，可以去报工了！！")
                        #进行报工
                        # 结果值
                        if number != "VB_999工站" and number!="VB_000工站":
                            if self._status == self.TestStatus.Passed.value:
                                test_result = 1
                            else:
                                test_result = 0
                            if vb010isbind:
                                reporting_work_result, message = dev._zsMes.reporting_work(test_result, number)
                                if reporting_work_result:
                                    logger.info(f"VB010工站报工成功")
                                    self.set_info(f"报工成功")
                                    self.isreport=True
                                    time.sleep(1)
                                else:
                                    logger.info(f"VB010工站报工失败，原因: {message}")
                                    self.isreport=False
                                    self.set_info(f"报工失败")
                                    time.sleep(1)
                            if vb002isbind:
                                reporting_work_result, message = dev._zsMes.reporting_work(test_result, number)
                                if reporting_work_result:
                                    logger.info(f"VB002工站报工成功")
                                    self.set_info(f"报工成功")
                                    self.isreport = True
                                    time.sleep(1)
                                else:
                                    logger.info(f"VB002工站报工失败，原因: {message}")
                                    self.isreport = False
                                    self.set_info(f"报工失败")
                                    time.sleep(1)
                            # 除了特殊工站和VB002 和 VB 010，其他工站可以报工
                            if number!="VB_002工站" and number!="VB_010工站":
                                reporting_work_result, message = dev._zsMes.reporting_work(test_result, number)
                                logger.info(f"报工的参数是：{test_result},{number}")
                                if reporting_work_result:
                                    logger.info(f"报工成功")
                                    self.set_info(f"报工成功")
                                    self.isreport = True
                                    time.sleep(1)
                                else:
                                    logger.info(f"报工失败，原因: {message}")
                                    self.set_info(f"报工失败")
                                    self.isreport = False
                                    time.sleep(1)
                        else:
                            if number =="VB_999工站":
                                logger.info("vb999工站不需要报工了")
                                logger.info("vb999工站报工完成")
                                self.set_info("VB_999工站 报工成功")
                                self.isreport = True
                            if number =="VB_000工站":
                                logger.info("VB_000工站不需要报工了")
                            time.sleep(3)
                    else:
                        logger.info("测试结果是测试完了，但是还有测试项的测试结果是false，不能报工")
                        self.set_info(f"测试结果是测试完了，但是还有测试项的测试结果是false，不能报工")
                        self.isreport = False
                        time.sleep(2)

                logger.info("上报结果完成")
                self.set_uploaded(True)
                if self.isreport:
                    if proj._config["zsMes"].get("enable") is not False:
                        self.set_info("上报测试结果和报工都完成")
                    else:
                        self.set_info("上报测试结果完成，mes系统已关闭")
                else:
                    if proj._config["zsMes"].get("enable") is not False:
                        self.set_info("上报测试结果完成,但是报工失败了")
                    else:
                        self.set_info("上报测试结果完成，mes系统已关闭")
            else:
                # 如果未上传结果，或者上传检验结果失败的 或者测试结果为NG的 ,那就来下面
                Notest_res = []
                Notest_res_name = []
                module_s = self._parent
                for module_s_units in module_s.units:
                        # 如果有测试项 还没有测试的话，保存这个测试项的名
                        if module_s_units.status == -1:
                            Notest_res_name.append(module_s_units.name)
                # 如果NG次数等于指定次数的话，需要判断测试项是否都通过
                if dev._ngCount >= dev._zsMes.ngCount:
                    if Notest_res_name is not None:
                        number1 = number
                        flagup = False
                        test_result1 = 0
                        # 根据缺少的工站个数去上传结果
                        for checkpoint in Notest_res_name:
                            logger.info(f"有{len(Notest_res_name)}个还没有保存结果")
                            count = 1
                            logger.info(f"第{count}个保存结果")
                            update_mes_zs_result, message = dev._zsMes.update_mes(number1, checkpoint, test_result1,self._test_data)
                            count += 1
                            if update_mes_zs_result:
                                logger.info(f"未测试的未测试的checkpoint为{checkpoint},已经上传成功了")
                                flagup = True
                            else:
                                logger.info(f"未测试的未测试的checkpoint为{checkpoint},没有上传成功，原因{message}")
                                flagup = False
                        # 上报结果
                        if flagup:
                            logger.info(f"NG次数大于等于{dev._zsMes.ngCount}，直接上报")
                            # 结果值
                            if self._status == self.TestStatus.Passed.value:
                                test_result = 1
                            else:
                                test_result = 0
                            reporting_work_result, message = dev._zsMes.reporting_work(test_result, number)
                            logger.info(f"报工的参数是：{test_result},{number}")
                            if reporting_work_result:
                                logger.info(f"报工成功")
                                self.set_info(f"报工成功")
                                self.isreport = True
                                time.sleep(1)
                            else:
                                logger.info(f"报工失败，原因: {message}")
                                self.set_info(f"报工失败")
                                self.isreport = False
                                time.sleep(1)
                        else:
                            logger.info(f"未测试的未测试的checkpoint为{checkpoint},没有上传成功，原因{message}")
                    else:
                        # 测试项都通过了 可以直接报工
                        # 结果值
                        if self._status == self.TestStatus.Passed.value:
                            test_result = 1
                        else:
                            test_result = 0
                        reporting_work_result, message = dev._zsMes.reporting_work(test_result, number)
                        logger.info(f"报工的参数是：{test_result},{number}")
                        if reporting_work_result:
                            logger.info(f"报工成功")
                        else:
                            logger.info(f"报工失败，原因: {message}")
                            self.set_info(f"报工失败")
                            self.isreport = False
                self.set_uploaded(True)
                if self.isreport:
                    if proj._config["zsMes"].get("enable") is not False:
                        self.set_info("上报测试结果和报工都完成")
                    else:
                        self.set_info("上报测试结果完成，mes系统已关闭")
                else:
                    if proj._config["zsMes"].get("enable") is not False:
                        self.set_info("上报测试结果完成,但是报工失败了")
                    else:
                        self.set_info("上报测试结果完成，mes系统已关闭")

        else:
            logger.info("该测试单元还未开始测试")
            self.set_uploaded(False)
            self.set_info("该测试单元还未开始测试")
        self.test_done()

    def get_download_progress(self, progress):
        """固件下载文件进度回调函数"""
        self.set_info(f"下载进度: {progress}")

    def create_result_dir(self, uuid, ptz_uuid):
        root = os.getcwd()
        now = datetime.datetime.now().strftime("%Y%m%d")
        self._unit_dir = f"{root}\\result\\{self._parent._parent._id}\\{self._id}\\{now}"
        if not os.path.exists(self._unit_dir + f"\\{uuid}"):
            os.makedirs(self._unit_dir + f"\\{uuid}")
        if not os.path.exists(self._unit_dir + f"\\{uuid}\\{ptz_uuid}"):
            os.makedirs(self._unit_dir + f"\\{uuid}\\{ptz_uuid}")
        return self._unit_dir

    def get_project_dir(self):
        proj = self._parent._parent._parent._project
        return f"{os.getcwd()}\\project\\{proj}"

    def teardown(self):
        pass
