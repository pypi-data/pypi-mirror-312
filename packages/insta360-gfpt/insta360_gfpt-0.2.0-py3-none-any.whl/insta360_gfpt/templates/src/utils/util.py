import os
import json
import socket

import qrcode as qrcode
from loguru import logger
import time
import zipfile


def project_setting(setting=None, project=None):
    u"""get or set project setting form setting.json"""
    if not project:
        setting_path = f"{os.getcwd()}\\project\\VB\\setting.json"
    else:
        setting_path = f"{os.getcwd()}\\project\\{project}\\setting.json"
    if setting is None:
        with open(setting_path, "r", encoding="utf-8") as f:
            setting_all = json.load(f)
        setting_path = f"{os.getcwd()}\\project\\{setting_all.get('测试项目')}\\setting.json"
        with open(setting_path, "r", encoding="utf-8") as f:
            setting_pro = json.load(f)
        return setting_pro
    elif type(setting) is dict:
        with open(setting_path, "r", encoding="utf-8") as f:
            setting_all = json.load(f)
        setting_path = f"{os.getcwd()}\\project\\{setting_all.get('测试项目')}\\setting.json"
        with open(setting_path, "w", encoding="utf-8") as f:
            json.dump(setting, f, indent=4, ensure_ascii=False)
        return True
    else:
        return {}


def zipFiles(files: list, output):
    """
    压缩指定文件
    :param files: 目标文件路径列表
    :param output: 压缩文件保存路径+xxxx.zip
    :return: 无
    """
    error_msg = ""
    try:
        file_not_esixt = []
        zip = zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED)
        for file in files:
            if os.path.exists(file):
                zip.write(file, arcname=os.path.basename(file))
    except Exception as e:
        logger.error(e)
    finally:
        zip.close()


# zipFiles([r"D:\desktop-dev\go3se-host\测试结果\主机成品测试\白平衡校正\20220901\0a40d37e-e0f7-4de5-b111-0c0e56968aff\VIG_EXPOSURE.txt",
#     r"D:\desktop-dev\go3se-host\测试结果\主机成品测试\白平衡校正\20220901\0a40d37e-e0f7-4de5-b111-0c0e56968aff\vignette.txt"], 
#     r"D:\\vignette_and_VIG_EXPOSURE_20220901152100.zip")


def generate_qrcode(content, save_path):
    """生成二维码"""
    for retry in range(0, 3):
        try:
            img = qrcode.make(content)
            img.save(save_path)  # 保存二维码
            time.sleep(0.5)
            if not os.path.exists(save_path):
                logger.error("生成二维码失败,找不到文件")
            return True
        except Exception as e:
            logger.error(f"生成二维码失败: {e}")
    else:
        return True


def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


def get_host_ip_by_prefix(prefix):
    local_ip = ""
    for ip in socket.gethostbyname_ex(socket.gethostname())[2]:
        if prefix in ip:
            local_ip = ip
            break
    return local_ip


def cmp_file(f1, f2):
    st1 = os.stat(f1)
    st2 = os.stat(f2)

    # TODO
    # 可以考虑加入md5
    # 比较文件大小
    if st1.st_size != st2.st_size:
        return False

    buf_size = 8*1024
    with open(f1, 'rb') as fp1, open(f2, 'rb') as fp2:
        while True:
            b1 = fp1.read(buf_size)  # 读取指定大小的数据进行比较
            b2 = fp2.read(buf_size)
            if b1 != b2:
                return False
            if not b1:
                return True


if __name__ == '__main__':
    ip = get_host_ip_by_prefix('192.168.')
    print(ip)