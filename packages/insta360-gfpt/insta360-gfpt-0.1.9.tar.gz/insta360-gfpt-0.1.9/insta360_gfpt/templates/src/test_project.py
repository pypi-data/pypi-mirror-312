import datetime
import os, json, time, sys
import threading
import traceback

from loguru import logger

from .device.device import Device
from .base.base_test_group import Group
from .base.base_test_module import Module
from .utils.adb_util import Adb
from .utils.network import ResultHandle
from .utils.util import project_setting
from PySide6.QtCore import QObject, Signal, Slot, Property, QMetaObject
from PySide6.QtQml import QmlElement


class TestProject(QObject):
    """docstring for TestProject"""

    def __init__(self, version=None, logical_lock=None, project=None):
        super(TestProject, self).__init__()
        self._app_version = version    # app版本
        self._logical_lock = logical_lock  # 不知道啥锁
        self._project = project   # 项目名字
        self._testing = False  # 是否正在测试
        self._test_env = None
        self._updating_devs = False  # 更新设备
        self._config = {}
        self._zsMes_config = {}
        self._mes_errcode = {}
        self._devs = []
        self._cur_dev_index = None
        self._cur_group_index = 0
        self._groups = []
        self._modules = []
        self._cur_module_index = 0
        self._cur_module = None
        self.retest = False
        self._cur_unit_index = 0
        self._stop_worker = False
        self.connect_num = 0
        self.ngCount = 0  # 初始化 ngCount 变量
        # 加载工站描述字典
        # 获取当前文件所在的目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # 拼接 JSON 文件的路径（相对路径）
        # file_path = os.path.join(current_dir, '../project/VB/errcode.json')
        # self.station_descriptions = self.extract_station_info(file_path)
        logger.info(f"PC版本: {self._app_version}")

    updatingDevChanged = Signal()
    testingChanged = Signal()
    curDevChanged = Signal()
    needUpdateDevs = Signal()
    devicesChanged = Signal()
    curModuleChanged = Signal()
    groupIndexChanged = Signal()
    moduleIndexChanged = Signal()
    curDevDisconnected = Signal()
    projectChanged = Signal()
    selectedCountChanged = Signal()
    nonNotify = Signal()
    openFactorySnDialog = Signal()

    def device_monitor(self):
        def worker(self):
            while True:


                # logger.info(devs)
                if self._updating_devs:
                    continue
                if self._cur_dev_index is not None:
                    cur_dev = self._devs[self._cur_dev_index]
                else:
                    cur_dev = None
                if cur_dev._ghost is True:
                    logger.info("检测到新USB设备,更新")
                    self.set_updating_devs(True)
                    self.needUpdateDevs.emit()
                    continue


        t = threading.Thread(target=worker, args=[self, ], daemon=True)
        t.start()

    @Property(bool, notify=nonNotify)
    def test_env(self):
        return self._test_env

    @Property(dict, notify=nonNotify)
    def logical_lock(self):
        return self._logical_lock

    @Property(str, notify=nonNotify)
    def password(self):
        return self._logical_lock.get("pwd")

    @Property(list, notify=devicesChanged)
    def devices(self):
        return self._devs

    @Property(str, notify=projectChanged)
    def project_name(self):
        return self._project


    @Property(int, notify=selectedCountChanged)
    def selected_count(self):
        count = 0
        for d in self._devs:
            if not d._ghost and d._selected:
                count += 1
        return count

    @Property(str, notify=nonNotify)
    def app_version(self):
        return self._app_version

    @Property(bool, notify=testingChanged)
    def testing(self):
        return self._testing

    @Slot(bool)
    def set_testing(self, status):
        self._testing = status
        self.testingChanged.emit()

    @Property(bool, notify=updatingDevChanged)
    def updating_devs(self):
        return self._updating_devs

    @Slot(bool)
    def set_updating_devs(self, status):
        self._updating_devs = status
        self.updatingDevChanged.emit()

    @Property(int, notify=groupIndexChanged)
    def group_index(self):
        return self._cur_group_index

    @Property(int, notify=moduleIndexChanged)
    def module_index(self):
        return self._cur_module_index

    @Property(list, notify=nonNotify)
    def modules(self):
        return self._modules


    @Property(int, notify=nonNotify)
    def unit_index(self):
        # return self._moduleIndex
        return 0

    @Slot(str)
    def set_project(self, name):
        if self._project != name:
            logger.info(f"项目变更[{self._project}] -> [{name}]")

            self._project = name
            self.projectChanged.emit()
            self.proj_init()

    @Slot(int, int)
    def set_module_index(self, group_index, module_index):
        if group_index != self._cur_group_index:
            self._cur_group_index = group_index
            self.groupIndexChanged.emit()
        self._cur_module_index = module_index
        self._cur_module = self._groups[group_index]._modules[module_index]
        self.curModuleChanged.emit()
        self.moduleIndexChanged.emit()
        self._cur_module.set_index(0)
        # if self.cur_dev and self.cur_dev._uuid != "ghost" and self._cur_module.id == "base_hardware_check":
        #     # if not self.cur_dev.check_factory_sn_binded():
        #     logger.info(f"uuid {self.cur_dev._uuid}")
        #     if self.query_sensor_binding() is None:
        #         self.cur_dev.sensor_id1 = None
        #         self.cur_dev.sensor_id2 = None
        #         self.openFactorySnDialog.emit()

        # self._cur_module.set_index(self._cur_unit_index)


    @Slot(int)
    def select_device(self, new_index):
        if self._cur_dev_index is not None and new_index != self._cur_dev_index:
            logger.info(f"切换设备至: {self._devs[new_index]}")
            # logger.info(f"断开旧设备: {self._devs[self._cur_dev_index]} 连接")
            # self._devs[self._cur_dev_index].disconnect_camera()
            self._devs[self._cur_dev_index].set_selected(False)
            self._cur_dev_index = new_index
            # self._devs[self._cur_dev_index].connect_camera()
            self._devs[self._cur_dev_index].set_selected(True)
            self._groups = self._devs[self._cur_dev_index]._groups
            self.set_module_index(self._cur_group_index, self._cur_module_index)
            self.curDevChanged.emit()

            self.update_local_status()

    def extract_station_info(self,file_path):
        """
        从指定的 JSON 文件中提取工站信息并返回工站描述字典。

        参数:
        file_path (str): JSON 文件的路径。

        返回:
        station_descriptions (dict): 包含所有工站信息的字典，格式为 { "工站编码": "测试项名称" }。
        """
        # 读取 JSON 文件
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # 创建一个存储工站描述的字典
        station_descriptions = {}

        # 遍历 "组装后工序" 列表
        for station in data.get("组装后工序", []):
            for station_code, details in station.items():
                # 遍历该工站的所有测试项（排除 "工站编码" 键）
                for key, value in details.items():
                    if key != "工站编码":
                        # 将工站编码映射到测试项名称
                        station_descriptions[details["工站编码"]] = key

        return station_descriptions

    @Slot()
    def start_test(self):
        # 触发工站单元变化信号
        self._cur_module.curUnitChanged.emit()
        cur_unit = self._cur_module._cur_unit
        cur_unit.set_status(cur_unit.TestStatus.Testing.value)
        cur_unit.update_local_status()

        # 设置测试状态
        self.set_testing(True)


    @Slot()
    def single_retest(self):
        """单项重测"""
        self._cur_module.curUnitChanged.emit()
        self.start_test()
        self.retest = True

    @Slot()
    def start_auto_test(self):
        """一键测试"""


        self.set_testing(True)

    @Slot()
    def start_factory_comfirm(self):
        dev = self._devs[self._cur_dev_index]
        t = threading.Thread(target=self._cur_module.start_factory_comfirm, args=[dev, ], daemon=True)
        t.start()
        self.set_testing(True)



    def teardown(self):
        logger.info("关闭QT,做环境恢复")
        # if self._testing:
        #     self._cur_module._cur_unit.teardown()
        for dev in self._devs:
            if dev._connecting:
                dev.disconnect_camera()
        # 记录当前的测试组|测试模块|测试项

    def test_done(self):
        u"""回调函数，用于下级上报测试完成"""
        logger.info("收到group上报测试完成，修改测试状态")
        # if self.check_upload_result():
        #     logger.info(f'测试模块【{self.cur_module.name}】，已测试完，上报测试结果')
        #     self.upload_result_to_server()
        self.set_testing(False)



    def proj_init(self):
        u"""init project info from test_project.json"""

        # 获取上一次的测试工站记忆



        proj_cfg_path = f"{os.getcwd()}\\project\\{self._project}\\test_project.json"
        errcode_path = f"{os.getcwd()}\\project\\{self._project}\\errcode.json"
        self._config = None
        # if not os.path.exists(proj_cfg_path):
        #     logger.error(f"读取项目文件{proj_cfg_path}失败")
        #     sys.exit(-1)

        # with open(proj_cfg_path, "r", encoding="utf-8") as f:
        #     self._config = json.load(f)
        #     self._test_env = self._config['config']['test_env']
        #     self._zsMes_config = self._config["zsMes"]
        #     logger.debug(f'当前的测试环境的状态：{self._test_env}'.center(50, '*'))
        # if not os.path.exists(errcode_path) and self._zsMes_config["enable"]:
        #     logger.error(f"读取项目文件{errcode_path}失败")
        #     sys.exit(-1)
        # with open(errcode_path, "r", encoding="utf-8") as f:
        #     self._mes_errcode = json.load(f)
        # logger.info(f"zsMes: {self._zsMes_config}")
        # if not self._config.get("config"):
        #     logger.error("加载项目配置文件config失败!")
        #     return False
        flag = True
        checks = ["name", "app", "app_version", "token", "test_token", "test_env", "refresh_flag"]

        return flag

    def get_last_group_index(self, name):
        for index, group in enumerate(self._groups):
            if group.name == name:
                self._cur_group_index = index
                break
        return self._cur_group_index

    def get_last_module_index(self, name):
        for index, module in enumerate(self._groups[self._cur_group_index].modules):
            if module.name == name:
                self._cur_module_index = index
                break
        return self._cur_module_index


    def update_ghost_local_status(self):
        logger.info("恢复初始化的结果状态")
        self.set_testing(False)
        groups = self._devs[self._cur_dev_index]._groups
        for gp in groups[:-1]:
            modules = gp._modules
            for mod in modules:
                units = mod._units
                for unit in units:
                    unit.set_status(unit.TestStatus.NotTested.value)
                    unit.set_info("")

                mod.update_local_status()
            gp.update_local_status()

    def update_local_status(self):
        logger.info("更新本地结果")
        groups = self._devs[self._cur_dev_index]._groups
        for gp in groups:
            res = self.get_cur_dev_result(gp._result_url)
            if not res:
                break

            modules = gp._modules
            for mod in modules:
                if res['result'] is None:
                    continue
                if res['result'][mod._id] is None:
                    continue
                units = mod._units
                for unit in units:
                    if res['result'][unit._id] is True:
                        unit.set_status(unit.TestStatus.Passed.value)
                    elif res['result'][unit._id] is False:
                        unit.set_status(unit.TestStatus.Failed.value)
                mod.update_local_status()
            gp.update_local_status()

        for g in groups:
            for m in g._modules:
                for u in m._units:
                    logger.info(f"{g._name}: {g._status} -> {m._name}: {m._status} -> {u._name}: {u._status}")
