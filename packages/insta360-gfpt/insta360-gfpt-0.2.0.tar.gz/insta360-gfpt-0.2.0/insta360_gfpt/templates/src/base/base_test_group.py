from enum import Enum
from .base_test_module import Module
from loguru import logger
from PySide6.QtCore import QObject, Signal, Slot, Property, QMetaObject, QEnum
from PySide6.QtQml import QmlElement

QML_IMPORT_NAME = "InsFactory"
QML_IMPORT_MAJOR_VERSION = 1
QML_IMPORT_MINOR_VERSION = 0


@QmlElement
class Group(QObject):
    """docstring for Group"""

    @QEnum
    class TestStatus(Enum):
        NotTested = -1
        Failed = 0
        Passed = 1
        Testing = 2

    def __init__(self, _id, _name, _modules, upload_url, result_url, _parent=None):
        super(Group, self).__init__()
        self._id = _id
        self._name = _name
        self._upload_url = upload_url
        self._result_url = result_url
        self._status = self.TestStatus.NotTested.value
        self._modules = []

        self._parent = _parent  # TestProject
        self.init_modules(_modules)

    statusChanged = Signal()
    nonNotify = Signal()

    def test_done(self):
        u"""回调函数，用于下级上报测试完成"""
        logger.info("测试Module上报测试完成,更新group状态并继续上报给Proj")
        self.update_local_status()
        self._parent.test_done()

    def init_modules(self, modules: list):
        self._modules = []
        for m in modules:
            # logger.info(m)
            module = Module(m["id"], m["name"], m["units"], m["procedureCode"], self)
            self._modules.append(module)

    def get_modules(self, cfg):
        if not cfg.get("content"):
            return
        module_idx = 1
        while cfg["content"].get(f"module{module_idx}"):
            m_cfg = cfg["content"].get(f"module{module_idx}")
            module = Module(module_idx, m_cfg["name"])
            module.get_units(m_cfg)
            self._modules.append(module)
            module_idx += 1

    @Property(bool, notify=statusChanged)
    def status(self):
        return self._status

    @Property(str, notify=nonNotify)
    def name(self):
        return self._name

    @Property(list, notify=nonNotify)
    def modules(self):
        return self._modules

    @Slot()
    def update_local_status(self):
        test_status = self.TestStatus.NotTested.value
        for module in self._modules:
            if module._status == module.TestStatus.NotTested.value:
                test_status = self.TestStatus.NotTested.value
                break
            elif module._status == module.TestStatus.Failed.value:
                test_status = self.TestStatus.Failed.value
                break
            elif module._status == module.TestStatus.Testing.value:
                test_status = self.TestStatus.Testing.value
                break
            elif module._status == module.TestStatus.Passed.value:
                test_status = self.TestStatus.Passed.value
                continue
            else:
                test_status = self.TestStatus.NotTested.value
        else:
            test_status = self.TestStatus.Passed.value
        self._status = test_status
        self.statusChanged.emit()
