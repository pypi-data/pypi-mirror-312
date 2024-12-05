"""
from requests_toolbelt import  *
import requests

f = r"D:\desktop-dev\go3se-host\测试结果\主机半成品 性能测试\陀螺仪标定\20220830\0a40d37e-e0f7-4de5-b111-0c0e56968aff\PRO_LRV_20220825_040950_01_024.mp4"
m = MultipartEncoder(fields={'video': open(f, 'rb'), 'uuid': '0a40d37e-e0f7-4de5-b111-0c0e56968aff'},
                     boundary='---------------------------7de1ae242c06ca'
                    )

import time
url = "http://api-produce-test.insta360.cn/go3/se/calibrate/gyro"
def my_callback(monitor):
    # Your callback function
    print(monitor.bytes_read)

m = MultipartEncoderMonitor(m, my_callback)

# req_headers = {'Content-Type': m.content_type,
#                'path':'2016/07/09/5ASD5SDFASDFASDF/{}.zip'.format(time.time()),}
headers = {"app": "all", "app_version": "v1", "token": "123", "Content-Type": "application/octet-stream"}
response = requests.post(url, data=m, headers=headers)
print(response.status_code)
resp = response.content
print(resp)
"""
import os
from requests_toolbelt import *
import requests
 
file_path = r"D:\desktop-dev\go3se-host\测试结果\主机半成品 性能测试\陀螺仪标定\20220830\0a40d37e-e0f7-4de5-b111-0c0e56968aff\PRO_LRV_20220825_040950_01_024.mp4"
file_name = "PRO_LRV_20220825_040950_01_024.mp4"        # 这里为了简化就直接给出文件名了，也可以从文件路径中获取
file_stats = os.stat(file_path)
file_size = file_stats.st_size
 
with open(file_path, mode='rb') as f:
    file_rb = f.read()
 
def upload_file():
 
    url = "http://api-produce-test.insta360.cn/go3/se/calibrate/gyro" 
 
    item = {
        "name": file_name,
        "chunkNumber": "1",
        "chunkSize": "204800000",
        "fileSize": str(file_size),
        # "file": (file_name, file_rb, "application/x-zip-compressed")    # 这里application/x-zip-compressed是从请求接口的header是中看到的
        "video": (file_name, file_rb, "application/octet-stream")
    }
    
    temp = MultipartEncoder(item)
    data = MultipartEncoderMonitor(temp)
 
    headers = {
        "Content-Type": temp.content_type
    }
 
    response = requests.post(url=url, data=data, headers=headers)
    print(response.content)


upload_file()