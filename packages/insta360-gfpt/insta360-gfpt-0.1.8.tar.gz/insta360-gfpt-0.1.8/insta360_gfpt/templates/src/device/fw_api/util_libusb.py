#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :util_libusb.py
# @Time      :2022/8/5 15:43
# @Author    :lilinhong
import usb1
from loguru import logger
from src.utils.adb_util import Adb as adb
from src.utils.network import ResultHandle


def get_device_info(usb_device: usb1.USBDevice):
    info = {
        'bcdUSB': usb_device.getbcdUSB(),
        'bcdDevice': usb_device.getbcdDevice(),
        'BusNumber': usb_device.getBusNumber(),

        'DeviceAddress': usb_device.getDeviceAddress(),
        'DeviceClass': usb_device.getDeviceClass(),
        'DeviceSpeed': usb_device.getDeviceSpeed(),
        'DeviceProtocol': usb_device.getDeviceProtocol(),
        'DeviceSubClass': usb_device.getDeviceSubClass(),
        # 'device_descriptor': usb_device.device_descriptor,

        # 'Manufacturer': usb_device.getManufacturer(),
        'ManufacturerDescriptor': usb_device.getManufacturerDescriptor(),
        'MaxPacketSize0': usb_device.getMaxPacketSize0(),
        'NumConfigurations': usb_device.getNumConfigurations(),

        # 'Product': usb_device.getProduct(),
        'ProductID': usb_device.getProductID(),
        'ProductDescriptor': usb_device.getProductDescriptor(),
        'PortNumber': usb_device.getPortNumber(),
        'PortNumberList': usb_device.getPortNumberList(),

        # 'SerialNumber': usb_device.getSerialNumber(),
        'SerialNumberDescriptor': usb_device.getSerialNumberDescriptor(),
        # 'SupportedLanguageList': usb_device.getSupportedLanguageList(),

        'VendorID': usb_device.getVendorID(),
    }
    usb_id = ''
    for port in info['PortNumberList']:
        usb_id = usb_id + f'{port}->'
    usb_id = usb_id + f'{info["DeviceAddress"]}'
    info['usb_id'] = usb_id
    return info


def get_device_handle_info(usb_device_handle: usb1.USBDeviceHandle):
    info = {
        'Configuration': usb_device_handle.getConfiguration(),
        'Manufacturer': usb_device_handle.getManufacturer(),
        'SerialNumber': usb_device_handle.getSerialNumber(),
        'Product': usb_device_handle.getProduct(),
        'SupportedLanguageList': usb_device_handle.getSupportedLanguageList(),
        # 'StringDescriptor': [usb_device_handle.getStringDescriptor(i, 1) for i in [1, 2, 3, 4]],
    }
    return info


def get_usb_devs(vendor_id=0x2E1A, project_name="default") -> list:
    """
    返回符合条件的设备列表
    厂商ID、设备SN
    """
    devs = []
    # adb
    # logger.info(project_name)
    if project_name=="VB":
        # logger.info("要用adb")
        mAdb = adb()
        devs = mAdb.get_devices()

    else:
    # with usb1.USBContext() as context:
        context = usb1.USBContext()
        for usb_device in context.getDeviceIterator(skip_on_error=True):
            if usb_device.getVendorID() == vendor_id:
                devs.append(usb_device)
    return devs


def list_usb_device(dev_sn: str = None, vendor_id=0x2E1A):
    """
    返回符合条件的设备列表
    厂商ID、设备SN
    """
    dev_map = {}
    # with usb1.USBContext() as context:
    context = usb1.USBContext()
    for usb_device in context.getDeviceIterator(skip_on_error=True):
        if usb_device.getVendorID() == vendor_id:
            usb_ser_num = usb_device.getSerialNumber()
            if dev_sn is None:
                dev_map.update({usb_ser_num: usb_device})
            elif usb_ser_num == dev_sn:
                dev_map.update({usb_ser_num: usb_device})
    return dev_map


def list_usb_device_info():
    dev_map = {}
    with usb1.USBContext() as context:
        for usb_device in context.getDeviceIterator(skip_on_error=True):
            vendor_id = usb_device.getVendorID()
            dev_map[vendor_id] = get_device_info(usb_device)
    return dev_map


def get_all_usb_device(vendor_id=0x2E1A):
    dev_list = []
    context = usb1.USBContext()
    for usb_device in context.getDeviceIterator(skip_on_error=True):
        if vendor_id == usb_device.getVendorID():
            dev_list.append(usb_device)
    return dev_list, context

def get_device_num(vendor_id=0x05C6):
    i = 0
    context = usb1.USBContext()
    devices = context.getDeviceList(skip_on_access_error=True)
    for device in devices:
        if device.getVendorID() == vendor_id:
            i += 1

    return i

def list_usb_device_sn(vendor_id=0x2E1A):
    dev_map = {}
    with usb1.USBContext() as context:
        for usb_device in context.getDeviceIterator(skip_on_error=True):
            if vendor_id == usb_device.getVendorID():
                try:
                    usb_device_sn = usb_device.getSerialNumber()
                    dev_map[usb_device_sn] = get_device_info(usb_device)
                    logger.info(f'PC挂载的设备：{dev_map[usb_device_sn]}')
                except usb1.USBErrorAccess as e:
                    logger.error(f'遍历到了已经打开的设备：{get_device_info(usb_device)}')
    return dev_map


def get_usb_device_sn(cam_sn, vendor_id=0x2E1A):
    context = usb1.USBContext()
    for usb_device in context.getDeviceIterator(skip_on_error=True):
        if usb_device.getVendorID() == vendor_id:
            try:
                usb_ser_num = usb_device.getSerialNumber()
                if usb_ser_num == cam_sn:
                    return usb_device, context
            except usb1.USBErrorAccess as e:
                logger.error(f'遍历到了已经打开的设备：{get_device_info(usb_device)}')
    context.close()
    return None


def get_usb_device_address(address, vendor_id=0x2E1A):
    context = usb1.USBContext()
    for usb_device in context.getDeviceIterator(skip_on_error=True):
        if usb_device.getVendorID() == vendor_id:
            if usb_device.getDeviceAddress() == address:
                return usb_device, context
    context.close()
    return None


def get_usb_devs_by_type(vendor_id=0x2E1A, by="list", config=None) -> list:
    """
    返回符合条件的设备列表
    厂商ID、设备SN
    """
    # logger.info("要用adb")
    usb_device = adb()
    addrs = usb_device.get_devices()
    sn = addrs
    handler = ResultHandle(config.get("config"))
    if addrs:
        for i in range(len(addrs)):
            if "IAB" in addrs[i]:

                res = handler.query_uuid_binding(addrs[i])
                if res:
                    if res.get("uuid"):
                        addrs[i] = res.get("uuid")
    if by == "list":
        devs = addrs
    elif by == "addrMap":
        devs = {}
        if sn:
            for i in range(len(sn)):
                # addr = usb_device.getDeviceAddress()
                devs.update({addrs[i]: addrs[i]})
    else:
        devs = None
    # with usb1.USBContext() as context:

    return devs


if __name__ == "__main__":
    devs = list_usb_device()
    print(devs)

