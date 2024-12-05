"""
https://github.com/Insta360Develop/Insta360_OSC
"""
import os
import sys
import time
import requests
from loguru import logger

# logger = logging.getLogger(os.path.basename(__file__))


def http(url, method="POST", json=None, timeout=None, **kwargs):
    try:
        name = None if json is None else json.get("name")
        resp = requests.request(
            method=method, url=url, json=json, timeout=timeout, **kwargs
        )
    except Exception:
        logger.error(f"Exception")
        return None
    else:
        if resp.status_code != 200 or resp.status_code != 201:
            # pass
            logger.info(f"Exception: resp error with  json {json} {resp.text}")
        elif name is None:
            # pass
            logger.info(f"{url} request success with json {json} resp {resp.text}")
        else:
            # pass
            logger.info(f"{name} request success with json {json} resp {resp.text}")
        return resp


class API_OSC:

    def __init__(self):
        self.baseurl = 'http://192.168.42.1:80/'
        self.osc_info = f'{self.baseurl}osc/info'
        self.osc_state = f'{self.baseurl}osc/state'
        self.osc_takepicture = f'{self.baseurl}osc/takepicture'

    def get_info(self):
        resp = http(self.osc_info, "GET")
        return resp

    def post_state(self):
        pass

    def takepicture(self):
        pass

# {"manufacturer":"Arashi Vision","model":"Insta360 OneR","serialNumber":"IAEAH28BVGE3UD",
# "firmwareVersion":"v1.2.64","supportUrl":"https://www.insta360.com/product/insta360-oner/",
# "endpoints":{"httpPort":80,"httpUpdatesPort":10080},"gps":true,"gyro":true,"uptime":15,
# "api":["/osc/info","/osc/state","/osc/checkForUpdates","/osc/commands/execute","/osc/commands/status"],
# "apiLevel":[2],"_sensorModuleType":"Dual_Fisheye","_vendorVersion":"v1.1_build1"}

    def upgrade_firmware(self, firmware_path: str):
        logger.info(f"start to upgrade to {firmware_path}")
        files = {"file": open(firmware_path, "rb")}
        url = f"{self.baseurl}upload_fw"
        resp = http(url, files=files, timeout=1000)
        logger.info(f"upgrade_firmware resp：{resp} {str(resp.content)}")


if __name__ == '__main__':
    resp = API_OSC().get_info()
    print(resp, str(resp.content))
    resp = API_OSC().upgrade_firmware('Insta360OneRFW.bin')
    print(resp)

