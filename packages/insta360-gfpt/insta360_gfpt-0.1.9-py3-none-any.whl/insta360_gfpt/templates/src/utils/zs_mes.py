import traceback

import requests
import json
from loguru import logger




class zsMes:
    def __init__(self, zsMesConfig, zsErrorcode):
        self.token = ""
        self.is_open = zsMesConfig["enable"]
        self.host = zsMesConfig["host"]
        self.appKey = zsMesConfig["appKey"]
        self.appSecret = zsMesConfig["appSecret"]
        self.workOrderCode = zsMesConfig["workOrderCode"]
        self.projectName = zsMesConfig["projectName"]
        self.staffCode = zsMesConfig["staffCode"]  #员工编号
        self.staffName = zsMesConfig["staffName"]  #员工名字
        self.ngCount = zsMesConfig["failCount"]  #ng count
        self.errcodes = zsErrorcode
        self.UUID = ""
        self.ptz_uuid = ""
        self.sensor_id1 = ""
        self.sensor_id2 = ""
        self.replace_Sn = ""
        self.serial = None

    def do_post(self, url, data):
        self.token = self.get_token()
        logger.info(f"post data: {data}")
        if self.token:
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + self.token
            }
            res = requests.post(url, headers=headers, data=json.dumps(data))
            logger.info(f"post result: {res.text}")
            if res.status_code == 200:
                try:
                    return res.json()
                except json.JSONDecodeError:
                    traceback.print_exc()
                    return {"code": -1, "message": "JSON 解析失败"}
            else:
                logger.info(f"res code: {res.status_code}")
                return {"code": res.status_code, "message": "请求失败"}
        else:
            logger.error("无法获取 mes token")
            return {"code": -1, "message": "无法获取 token"}

    def get_token(self):
        url = self.host + '/api/open/v2/token'
        headers = {
            'Content-Type': 'application/json'
        }
        data = {
            "body": {
                "appKey": self.appKey,
                "appSecret": self.appSecret
            }
        }
        res = requests.post(url, headers=headers, data=json.dumps(data))
        if res.status_code == 200:
            try:
                self.token = res.json()['data']['accessToken']
                logger.info(res.json())
                return self.token
            except:
                traceback.print_exc()
                return None
        else:
            logger.info(f"res code: {res.status_code}")
            return None

    def reporting_work(self, ok, procedureCode, replaceSn=None):
        logger.info("开始报工")
        url = self.host + '/api/open/v2/customize/insta360/jobBooking'
        if not self.is_open:
            logger.error("mes系统已经关闭,报工失败")
            return True,"mes系统已经关闭"

        if self.serial is None and self.ptz_uuid is None:
            return False, "sn 和 云台uuid 都为空"

        # 优先处理 VB_011工站 并且序列号是 IAB 的情况
        if procedureCode == "VB_011工站" and self.serial and "IAB" in self.serial:
            data = {
                "ok": ok,
                "procedureCode": procedureCode,
                "sn": self.ptz_uuid,
                "replaceSn": self.serial
            }
        else:
            # 其他工站的逻辑
            specific_stations = ["VB_000工站", "VB_001工站", "VB_999工站", "VB_002工站", "VB_005工站",
                                 "VB_006工站", "VB_007工站", "VB_008工站", "VB_009工站", "VB_010工站"]

            if procedureCode in specific_stations:
                data = {
                    "ok": ok,
                    "procedureCode": procedureCode,
                    "sn": self.ptz_uuid,
                }
            elif self.serial and "IAB" in self.serial:
                data = {
                    "ok": ok,
                    "procedureCode": procedureCode,
                    "sn": self.serial,
                }
            elif self.serial is None:
                data = {
                    "ok": ok,
                    "procedureCode": procedureCode,
                    "sn": self.ptz_uuid,
                }
            elif self.ptz_uuid is None:
                data = {
                    "ok": ok,
                    "procedureCode": procedureCode,
                    "replaceSn": self.serial
                }
            else:
                data = {
                    "ok": ok,
                    "procedureCode": procedureCode,
                    "sn": self.ptz_uuid,
                    "replaceSn": self.serial
                }

        # 发送请求
        result = self.do_post(url, data)
        # 检查 data 是否为字典并包含 'code' 键
        if isinstance(data, dict) and data.get("code") == 200:
            return True, data["message"]
        else:
            return False, data["message"] if data is not None else {"error": "请求失败，未返回有效数据"}

    def init_station(self, procedureCode, replaceSn=None):
        logger.info("开始过站")
        if not self.is_open:
            logger.error("mes系统已经关闭,过站失败")
            return True, 0,False,procedureCode, "mes系统已关闭"

        url = self.host + '/api/open/v2/customize/insta360/sn/query'

        if self.serial is None and self.ptz_uuid is None:
            return  False ,  0 , False,procedureCode, "sn 和 云台uuid 都为空"

        # 这四个工站优先使用 ptz_uuid
        specific_stations = ["VB_000工站","VB_001工站","VB_999工站","0VB_002工站", "VB_005工站", "VB_006工站", "VB_007工站","VB_008工站","VB_009工站","VB_010工站","VB_011工站"]

        if procedureCode in specific_stations:
            data = {
                "procedure": procedureCode,
                "sn": self.ptz_uuid,
            }
        # 如果 serial 包含 "IAB"，则优先使用 serial
        elif self.serial and "IAB" in self.serial:
            data = {
                "procedure": procedureCode,
                "sn": self.serial,
            }
        elif self.serial is None:
            data = {
                "procedure": procedureCode,
                "sn": self.ptz_uuid,
            }
        elif self.ptz_uuid is None:
            data = {
                "procedure": procedureCode,
                "replaceSn": self.serial
            }
        else:
            data = {
                "procedure": procedureCode,
                "sn": self.ptz_uuid,
                "replaceSn": self.serial
            }

        result = self.do_post(url, data)

        if result:
            try:
                if result.get("code") == 403:
                    return False,0,False,procedureCode,result.get("message")

                entity = result.get("data", {}).get("entity", {})
                ok = entity.get("ok", False)
                current_procedure = entity.get("currentProcedure", "")
                ng_count = entity.get("ngCount", 0)

                if result.get("code") == 200:
                    return True, ng_count, ok, current_procedure,result
                else:
                    return False, ng_count, ok, current_procedure,result
            except:
                traceback.print_exc()
                return False,0,False,procedureCode,"解析失败",
        else:
            return False,0,False,procedureCode,"没有获取到结果",

    def bind_info(self, sn, data, procedureCode):
        logger.info("开始绑定")
        if not self.is_open:
            logger.error("mes系统已经关闭,绑定失败")
            return True,"mes系统已关闭"
        url = self.host + '/api/open/v2/customize/insta360/sn/bind'
        # 根据不同工站进行不同的逻辑处理
        if procedureCode == "VB_010工站":
            # 对于 VB_010工站，使用 data[1].get("value") 设置 uuIdAndReplaceSN
            uuIdAndReplaceSN = data[1].get("value")
        else:
            # 否则 uuIdAndReplaceSN 传空字符串
            uuIdAndReplaceSN = ""

        # 针对 VB_011工站，传 uuIdAndReplaceSN 为空字符串
        if procedureCode == "VB_011工站":
            post_data = {
                "sn": sn,
                "projectName": self.projectName,
                "procedureCode": procedureCode,
                "bindInfo": data,
                "uuIdAndReplaceSN": "",  # 对于 VB_011工站，传空字符串
                "otherKey": ""
            }
        else:
            # 对于其他工站，传 bindInfo 字段
            post_data = {
                "sn": sn,
                "projectName": self.projectName,
                "procedureCode": procedureCode,
                "bindInfo": data,
                "uuIdAndReplaceSN": uuIdAndReplaceSN,
                "otherKey": ""
            }

        # 发起 POST 请求
        result = self.do_post(url, post_data)
        # 根据结果返回
        # 检查 data 是否为字典并包含 'code' 键
        if isinstance(data, dict) and data.get("code") == 200:
            return True, data["message"]
        else:
            return False, data["message"] if data is not None else {"error": "请求失败，未返回有效数据"}

    # def save_info(self, procedureCode, sn, staffCode, staffName, checkpoint, result, testData, errorCodes=[]):
    def save_info1(self, procedureCode, sn, result,checkpoint):
        if not self.is_open:
            return True
        url = self.host + '/api/open/v2/customize/insta360/testingResult/save'

        post_data = {
            "procedureCode": procedureCode,
            "workOrderCode": self.workOrderCode,
            "sn": sn,
            "staffCode": "",
            "staffName": "",
            "testResults": [
                {
                    "checkpoint": checkpoint,
                    "errorCodes": [200],
                    "result": 0 if result else 1,
                    "testData": 0
                }
            ]
        }
        data = self.do_post(url, post_data)
        if 200 == data["code"]:
            return True
        else:
            return False

    def update_mes(self, procedureCode, checkpoint, result, testData, errorCodes=None):
        logger.info("开始保存检验结果")
        if errorCodes is None:
            errorCodes = []

        if not self.is_open:
            logger.error("mes系统已经关闭,开始保存mes检验结果失败")
            return True,"mes系统已经关闭"

        url = self.host + '/api/open/v2/customize/insta360/testingResult/save'

        # 特定工站列表
        specific_stations = ["VB_000工站", "VB_001工站","VB_999工站","VB_002工站", "VB_005工站", "VB_006工站", "VB_007工站",
                             "VB_008工站","VB_009工站","VB_010工站","VB_011工站"]

        # 根据条件选择 sn
        if procedureCode in specific_stations:
            sn = self.ptz_uuid
        elif self.serial and "IAB" in self.serial:
            sn = self.serial
        else:
            sn = self.ptz_uuid

        if result:
            errorCodes = []
        else:
            logger.info(self.errcodes)
            for keys in self.errcodes["组装后工序"]:
                for key in keys.keys():
                    if keys[key]["工站编码"] == procedureCode:
                        errorCodes.append(keys[key][checkpoint])

        post_data = {
            "procedureCode": procedureCode,
            "workOrderCode": self.workOrderCode,
            "sn": sn,
            "staffCode": self.staffCode,
            "staffName": self.staffName,
            "testResults": [
                {
                    "checkpoint": checkpoint,
                    "errorCodes": errorCodes,
                    "result": result,
                    "testData": testData
                }
            ]
        }
        logger.info(f"保存结果的data值是：{post_data}")
        data = self.do_post(url, post_data)
        # 检查 data 是否为字典并包含 'code' 键
        if isinstance(data, dict) and data.get("code") == 200:
            return True, data["message"]
        else:
            return False, data["message"] if data is not None else {"error": "请求失败，未返回有效数据"}

    def update_mes_errcode(self, procedureCode, errCode, errMsg):
        if not self.is_open:
            logger.error("mes系统已经关闭,上传错误码失败")
            return True
        url = self.host + '/api/metadata-flow/trigger/webhook/978599d6-9978-4703-8aa6-56389e73e4e3'
        post_data = {"body":[{
            "procedureCode": procedureCode,  # 工序编码
            "workOrderCode": self.workOrderCode,  # 工单编码
            "errCode": errCode,  # 错误码
            "errMsg": errMsg # 错误信息
        }]}
        data = self.do_post(url, post_data)
        # print(data)
        if 200 == data["code"]:
            return True
        else:
            return False

    def query_sn_relation(self, productSn=None, factorySn=None):
        """
        查询产品SN和组件SN关系
        :param partSn: 组件SN
        :param productSn: 产品SN
        :param start: 起始页
        :param length: 页容量
        :return: 查询结果
        """
        if not self.is_open:
            logger.error("mes系统已经关闭,查询组件关系失败")
            return True,"查询组件关系失败"

        url = self.host + '/api/open/v2/customize/insta360/partSn/query'

        if not productSn and not factorySn:
            raise ValueError("查询绑定的2个SN 都是空的")

        data = {
            "start": 0,
            "length": 10
        }

        if factorySn:
            data["factorySn"] = factorySn
        if productSn:
            data["productSn"] = productSn
        if self.projectName:
            data["projectName"] = self.projectName

        logger.info(f"Sending data: {json.dumps(data, indent=2, ensure_ascii=False)}")

        result = self.do_post(url, data)
        # 检查 data 是否为字典并包含 'code' 键
        if isinstance(data, dict) and data.get("code") == 200:
            return True, data["message"]
        else:
            return False, data["message"] if data is not None else {"error": "请求失败，未返回有效数据"}

    def report_uuid(self,ptz_uuid,procedureCode):
        if not self.is_open:
            logger.error("mes系统已经关闭,获取云台uuid报工失败")
            return True,"获取云台uuid报工失败"

        url = self.host + '/api/public/manufacture/workOrderProcedureTask/jobBookingRecord/create'
        post_data = {
            "workOrderCode": self.workOrderCode,  # 生产单号
            "procedureCode": procedureCode,  # 工序编号
            "jobBookingQty": 1,  # 报工数量，默认值为1
            "containerCode": ptz_uuid,  # 云台UUID
            "inspectParams": [],  # 默认值为空列表
            "assignees": [
                {
                    "assigneeCode": "产测小组（勿删）",  # 默认报工人/小组
                    "assigneeType": "GROUP"  # 默认负责人类型
                }
            ],
            "consumeMaterialType": 1,  # 默认耗料类型
            "planMaterialConsumeParams": [],  # 默认值为空列表
            "allocateMaterialConsumeParams": []  # 默认值为空列表
        }

        result = self.do_post(url, post_data)
        if result.get("code") == 200:
            return True, result["message"]
        else:
            return False, result["message"]

    def update_mes_errcode(self, procedureCode, workOrderCode, errCode, errMsg):
        if not self.is_open:
            logger.error("mes系统已经关闭,上传错误码失败")
            return True
        url = self.host + '/api/metadata-flow/trigger/webhook/978599d6-9978-4703-8aa6-56389e73e4e3'
        post_data = {"body":[{
            "procedureCode": procedureCode,  # 工序编码
            "workOrderCode": workOrderCode,  # 工单编码
            "errCode": errCode,  # 错误码
            "errMsg": errMsg # 错误信息
        }]}
        data = self.do_post(url, post_data)
        # print(data)
        if 200 == data["code"]:
            logger.info(f"上传成功错误码成功,单号是：{workOrderCode},工站编码是：{procedureCode},错误码是：{errCode},错误信息是：{errMsg}",True)
            return True
        else:
            logger.info(f"上传错误信息失败")
            return False


if __name__ == '__main__':
    setting={}
    setting["is_open"] = True
    rain_test = zsMes(setting)
    result = False
    procedureCode = "VB_001工站"
    workOrderCode = "MO006951"
    sn = "MVT2401N012"
    replaceSn = "IABZ7777777777"
    staffCode = ""
    staffName = ""
    checkpoint = "组装"
    errorCodes = ["FT004"]
    check_result = 0
    testData = "0"

    test_errcode = {"组装后工序": [{
    "yt_calibrate": {
    "云台标定": "FT001"
  }},
  {"near_normal_analysis48c": {
    "主摄近景解析": "FT002"
  }},
  {"near_normal_analysis_jn1": {
    "副摄近景解析": "FT003"
  }},
  {"package_test": {
    "组装": "FT004"
  }}
  ]
}
    data = [
    {
      "key": "yt_uuid",
      "value": "12345678901234567890FFFF"
    }
  ]



    # token = rain_test.get_token()
    # logger.info(token)
    with open("/Users/chenrunming/Downloads/procedure/errcode.json", "r", encoding="utf-8") as f:
        test_errcode = json.load(f)

        for data in test_errcode["组装后工序"]:
            for key in data:
                for key2 in data[key]:
                    if "工站编码" == key2:
                        continue
                    print(key, data[key][key2])
                    rain_test.update_mes_errcode(key, workOrderCode,data[key][key2], key2)
    # rain_test.init_station(procedureCode, sn)
    # {'code': 200, 'message': 'success', 'data': {'entity': {'sn': 'sntest20231225-002', 'currentProcedure': 'yt_calibrate', 'ngCount': 0, 'ok': False}}}
    # rain_test.bind_info(sn,data)
    data = [
        {
            "key": "sensor_id1",
            "value": "SY9E7777777"
        }
    ]
    data = [
        {
            "key": "sensor_id2",
            "value": "Y0907777777777"
        }
    ]

    data = [
        {
            "key": "serial",
            "value": "IABZ7777777777"
        }
    ]

    # rain_test.bind_info(sn, data)
    # rain_test.update_mes(procedureCode, workOrderCode, sn, staffCode, staffName, checkpoint, check_result, testData, errorCodes)
    # rain_test.reporting_work(result, procedureCode, sn, replaceSn)

