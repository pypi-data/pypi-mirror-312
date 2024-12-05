import time, os
import pywifi
import subprocess
from pywifi import const

from src.utils.logger import logger


class WifiConnecter(object):
    """docstring for WifiConnecter"""

    def __init__(self, ssid, pwd, ifacename=None):
        super(WifiConnecter, self).__init__()
        self.ssid = ssid
        self.pwd = pwd
        self.ifacename = ifacename
        self.wifi = pywifi.PyWiFi()
        self.iface = None

    def get_iface(self):
        if not self.wifi.interfaces():
            logger.error("没有WIFI网卡")
            return None
        if not self.ifacename:
            self.iface = self.wifi.interfaces()[-1]
            return True
        for iface in self.wifi.interfaces():
            if iface.name() == self.ifacename:
                self.iface = iface
                break
        else:
            self.iface = self.wifi.interfaces()[-1]
        return True

    def wifi_connect_status(self):
        wifi = pywifi.PyWiFi()
        if self.iface.status() in [const.IFACE_CONNECTED, const.IFACE_INACTIVE]:
            logger.info("wifi connected!")
            return 1
        else:
            logger.info("wifi not connected!")
            return 0

    def scan_wifi(self):
        # wifi = pywifi.PyWiFi()
        self.iface.scan()
        time.sleep(1)
        basewifi = self.iface.scan_results()

        for i in basewifi:
            logger.info("wifi scan result:{}".format(i.ssid))
            logger.info("wifi device MAC address:{}".format(i.bssid))
        return basewifi

    def connect_wifi(self):
        try:
            self.iface.disconnect()
            time.sleep(3)
            self.scan_wifi()
            profile = pywifi.Profile()  # 配置文件
            profile.ssid = self.ssid  # wifi名称
            profile.auth = const.AUTH_ALG_OPEN  # 需要密码
            profile.akm.append(const.AKM_TYPE_WPA2PSK)  # 加密类型
            profile.cipher = const.CIPHER_TYPE_CCMP  # 加密单元
            profile.key = self.pwd  # wifi密码

            self.iface.remove_all_network_profiles()  # 删除其它配置文件
            tmp_profile = self.iface.add_network_profile(profile)  # 加载配置文件
            self.iface.connect(tmp_profile)
            time.sleep(5)
            isok = True

            if self.iface.status() == const.IFACE_CONNECTED:
                logger.info(f"=================={self.ssid} connect successfully!==================")
            else:
                logger.error("connect failed!")
                isok = False
            return isok
        except Exception as e:
            logger.error(e)
            return False

    def connect(self):
        if self.get_iface() is None:
            return None
        # self.wifi_connect_status()
        return self.connect_wifi()


class IperfController(object):
    def __init__(self):
        super(IperfController, self).__init__()
        self.server_ip = "10.0.50.247"
        self.iperf_path = f"{os.getcwd()}\\tools\\iperf\\iperf.exe"
        # self.iperf_path = "D:\\code\\gfpt_android\\tools\\iperf\\iperf.exe"
        logger.info(self.iperf_path)
        self.iperf = None
        self.iperf_data = []

    def kill_perf(self):
        if self.iperf:
            self.iperf.terminate()
            self.iperf = None
        os.system("TASKKILL /F /IM iperf.exe")

    def run_perf(self, duration=10):
        self.kill_perf()
        cmd = [self.iperf_path, "-c", self.server_ip, "-t", str(duration), "-i", "1", "-f", "Mbytes"]
        # cmd = f"{self.iperf_path} -s -i 1 -w 1m f Mbytes"
        print(cmd)
        self.iperf = subprocess.Popen(cmd, shell=False,
                                      stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = self.iperf.stdout.readlines()
        logger.info(f'iperf输出：{output}')
        self.iperf.terminate()
        self.iperf = None
        if "Connection refused" in str(output):
            logger.error("iperf连接失败")
            return False
        datas = self.calc_perf_bw(output)
        self.kill_perf()
        return datas

    def run_server_iperf(self):
        self.kill_perf()
        cmd = f"{self.iperf_path} -s"
        logger.info(cmd)
        self.iperf = subprocess.Popen(cmd, shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logger.info(self.iperf)

    def get_iperf_data(self):
        output = self.iperf.stdout.readlines()
        logger.info(f'iperf输出：{output}')
        self.iperf.terminate()
        self.iperf = None
        if "Connection refused" in str(output):
            logger.error("iperf连接失败")
            return False
        datas = self.calc_perf_bw(output)
        return datas

    def calc_perf_bw(self, datas):
        try:
            begin = 0
            datas = [str(i) for i in datas]
            logger.info("iperf data: ")
            for d in datas:
                logger.info(d)
            for i in range(0, len(datas)):
                if "Interval       Transfer     Bandwidth" in datas[i]:
                    begin = i + 1
                    break
            bw_datas = datas[begin:]
            bw_list = [i[i.find("MBytes  ") + len("MBytes  "):i.rfind(" MBytes/sec")] for i in bw_datas]
            iperf_data = {"datas": bw_datas, "max": max(bw_list), "min": min(bw_list), "avg": bw_list[-1]}
            return iperf_data
        except Exception as e:
            logger.error(e)
            return False


if __name__ == "__main__":
    # wifi_connnecter = WifiConnecter("GO3SE XXXXXX.OSC", "88888888", "802.11ac Wireless LAN Card")
    # wifi_connnecter.connect()
    i = IperfController()
    i.run_perf()
