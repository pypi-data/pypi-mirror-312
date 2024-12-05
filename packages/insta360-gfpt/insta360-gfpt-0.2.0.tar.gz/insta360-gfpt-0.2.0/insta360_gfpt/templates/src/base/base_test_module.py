import time
from enum import Enum
from .base_test_unit import Unit
from PySide6.QtCore import QObject, Signal, Slot, Property, QEnum
from PySide6.QtQml import QmlElement

from loguru import logger

QML_IMPORT_NAME = "InsFactory"
QML_IMPORT_MAJOR_VERSION = 1
QML_IMPORT_MINOR_VERSION = 0


@QmlElement
class Module(QObject):
    """docstring for Module"""

    @QEnum
    class TestStatus(Enum):
        NotTested = -1
        Failed = 0
        Passed = 1
        Testing = 2

    def __init__(self, _id, _name, _units, _mes_id, _parent=None):
        super(Module, self).__init__()
        self._id = _id
        self._mes_id = _mes_id
        self._name = _name
        self._status = self.TestStatus.NotTested.value
        self._units = []
        self._cur_unit = None
        self._parent = _parent  # Group
        self.init_units(_units)
        if self._units:
            self.set_index(0)
        # self.index = 0

    statusChanged = Signal()
    curUnitChanged = Signal()
    nonNotify = Signal()

    @Property(str, notify=nonNotify)
    def name(self):
        return self._name

    @Property(str, notify=nonNotify)
    def id(self):
        return self._id

    @Property(int, notify=statusChanged)
    def status(self):
        return self._status

    @Property(list, notify=nonNotify)
    def units(self):
        return self._units

    @Property(Unit, notify=curUnitChanged)
    def cur_unit(self):
        # return self._units[0]
        return self._cur_unit

    @Slot(int)
    def set_index(self, index):
        if index >= len(self._units):
            index = len(self._units) - 1
        self._cur_unit = self._units[index]
        self.curUnitChanged.emit()

    def create_unit_by_type(self, unit_cfg):
        product = self._parent._parent._project
        if product == 'IAC2':
            import src.test_unit.IAC2 as test_unit
        if product == 'PC100':
            import src.test_unit.PC100 as test_unit
        if product == 'VB':
            import src.test_unit.VB as test_unit
        unit_route = unit_cfg["route"].split(".")  # unit的qml和py路由
        unit_class = getattr(getattr(test_unit, f"{unit_route[0]}"), unit_route[1])
        unit = unit_class(
            _id=unit_cfg["id"],
            _name=unit_cfg["name"],
            _test_auto=unit_cfg.get("auto", False),
            _qml=f"{unit_route[0]}.qml",
            _url=unit_cfg.get("url"),
            _parent=self,
            _config=unit_cfg)
        return unit

    @Slot()
    def update_local_status(self):
        test_status = self.TestStatus.NotTested.value
        for unit in self._units:
            if unit._status == unit.TestStatus.NotTested.value:
                test_status = self.TestStatus.NotTested.value
                break
            elif unit._status == unit.TestStatus.Failed.value:
                test_status = self.TestStatus.Failed.value
                break
            elif unit._status == unit.TestStatus.Testing.value:
                test_status = self.TestStatus.Testing.value
                break
            elif unit._status == unit.TestStatus.Passed.value:
                test_status = self.TestStatus.Passed.value
                continue
            else:
                test_status = self.TestStatus.NotTested.value
        else:
            test_status = self.TestStatus.Passed.value
        self._status = test_status
        self.statusChanged.emit()

    def test_done(self):
        u"""回调函数，用于下级上报测试完成"""
        logger.info("测试Unit上报测试完成,更新module状态并继续上报给Group")
        self.update_local_status()
        self._parent.test_done()

    def update_final_status(self):
        self.update_local_status()

    def init_units(self, units: list):
        for ut in units:
            unit = self.create_unit_by_type(ut)
            # unit = Unit(i["id"], i["name"], i["type"], i["qml"], url)
            self._units.append(unit)

        return True

    @Property(bool, notify=nonNotify)
    def has_test_all_btn(self):
        auto_unit_num = 0
        for u in self._units:
            if u._test_auto:
                auto_unit_num += 1
        if auto_unit_num > 1:
            return True
        else:
            return False

    def start_auto_test(self, dev):
        """自动项一键测试"""
        for i in range(0, len(self._units)):
            if self.units[i]._test_auto:
                self.set_index(i)
                time.sleep(0.5)
                self.units[i].start_test(dev)

    def start_factory_comfirm(self, dev):
        for i in range(0, len(self._units)):
            self.set_index(i)
            time.sleep(0.5)
            self.units[i].start_test(dev)
            if self.units[i]._status is not True:
                break
