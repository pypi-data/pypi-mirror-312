from .android import Android
from .camera import Camera


from PySide6.QtCore import QObject, Signal, Slot, Property, QMetaObject
from PySide6.QtQml import  QmlElement

from ..utils.adb_util import Adb
from ..utils.logger import logger
from ..utils.zs_mes import zsMes

QML_IMPORT_NAME = "InsFactory"
QML_IMPORT_MAJOR_VERSION = 1
QML_IMPORT_MINOR_VERSION = 0

@QmlElement
class Device(QObject):
    """docstring for Device"""
    def __init__(self, sn="default", usb_device="default", ghost=False, project_name="default", config=None):
        super(Device, self).__init__()
        if sn == "default":
            sn = None
        if usb_device == "default":
            usb_device = None
        if project_name == "VB":
            usb_device = usb_device
        self._zsMesConfig = {}
        self._zsMesEnable = False
        self.project_name = project_name
        self.sn = sn
        self.usb_device = usb_device
        self._uuid = None
        self._infos = []
        self._selected = False
        self._name = None
        self.sensor_id1 = None
        self.sensor_id2 = None
        self.ptz_uuid = "0"
        self._product = None
        self._groups = []
        self._ngCount = 0
        self._modules = []
        self.__factory_sn = None
        self._connecting = False
        self._ghost = ghost  # 是否虚拟设备，用于没有设备时也加载测试项
        self._config = config
        self._is_binding_sensor = False
        self._is_binding_ptz_uuid = False
        self._is_sn_binding = False
        self._write_flag = False
        logger.info(usb_device)
        # if self.project_name=="VB":
        self.camera = Android(sn=sn, usb_device=usb_device, config=self._config)
        if self.camera:
            sn = self.camera.api.getDeviceAddress()
            if sn and "IAB" in sn:
                self._device_address = self.camera.query_uuid_from_sn()
            else:
                self._device_address = sn
        else:
            self._device_address = None
        
    selectedChanged = Signal()
    moduleChanged = Signal()
    groupChanged = Signal()
    infoChanged = Signal()
    nonNotify = Signal()

    @Property(str, notify=nonNotify)
    def uuid(self):
        return self._uuid

    @Property(list, notify=infoChanged)
    def infos(self):
        return self._infos

    def update_infos(self):
        self._write_flag = False
        self.update_binding()
        self.sn = self.camera.api.getDeviceAddress()
        self.camera.get_camera_info()
        rrr = self.camera.query_sensor_binding()
        if rrr:
            self.sensor_id1 = rrr[0]
            self.sensor_id2 = rrr[1]
        self._infos = self.camera.device_info
        self.ptz_uuid = self.camera.api.cam_info['device_info']['ptz_uuid']


        logger.info(f"info ::: {self._infos}")
        # self.update_binding()
        self.infoChanged.emit()

    @Property(list, notify=nonNotify)
    def modules(self):
        return self._modules

    @Property(list, notify=groupChanged)
    def groups(self):
        return self._groups

    @Property(str, notify=nonNotify)
    def product(self):
        return self._product

    @Property(bool, notify=selectedChanged)
    def selected(self):
        return self._selected

    @Property(str, notify=nonNotify)
    def name(self):
        return self._name

    def update_device_info(self):
        self.camera.api.cam_info = {}
        self.camera.api.init_app_socket_con()
        self.camera.get_camera_info()
        self.ptz_uuid = self.camera.api.cam_info['device_info']['ptz_uuid']
        rrr = self.camera.query_sensor_binding()
        if rrr:
            self.sensor_id1 = rrr[0]
            self.sensor_id2 = rrr[1]
        self.infoChanged.emit()

    def update_binding(self):
        self.camera.is_sensor_binder = self._is_binding_sensor
        self.camera.is_sn_binding = self._is_sn_binding
        self.update_device_info()

    def connect_camera(self):

        self.camera.connect()
        self.camera.get_camera_info()
        self._infos = self.camera.device_info
        self._uuid = self.camera.uuid
        self._zsMes.UUID = self.camera.uuid
        self.ptz_uuid = self.camera.api.cam_info['device_info']['ptz_uuid']
        rrr = self.camera.query_sensor_binding()
        if rrr:
            self.sensor_id1 = rrr[0]
            self.sensor_id2 = rrr[1]
        self._product = self.camera.product
        self._connecting = True
        logger.info(f"xxxxx {self._infos}")

    def disconnect_camera(self):
        if not self._ghost and self.project_name!="VB":
            self.camera.disconnect()
            self._connecting = False
        elif not self._ghost:
            self._connecting = False
    
    @Slot(bool)
    def set_selected(self, selected: bool):
        self._selected = selected
        self.selectedChanged.emit()

    def set_name(self, name):
        self._name = name
        return self._name

    def set_groups(self, _groups):
        self._groups = _groups
        self.groupChanged.emit()

    def set_modules(self, _modules):
        self._modules = _modules
        self.moduleChanged.emit()

    def init_zsMes(self, zsMesConfig, zsErrorcode):
        self._zsMesConfig = zsMesConfig
        self._zsMes = zsMes(zsMesConfig, zsErrorcode)
        return self._zsMes


    