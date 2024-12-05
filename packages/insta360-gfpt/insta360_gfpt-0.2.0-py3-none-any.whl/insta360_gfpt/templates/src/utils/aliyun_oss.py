from loguru import logger
import oss2
from itertools import islice

class OssSystem(object):
    """docstring for OssSystem"""
    def __init__(self, config):
        self.config = config
        self.access_key_id = config.get("access_key_id")
        self.access_key_secret = config.get("access_key_secret")
        self.security_token = config.get("security_token")
        self.bucket_name = config.get("bucket")
        self.endpoint = config.get("endpoint")
        self.key = config.get("key")
        self.auth = oss2.StsAuth(self.access_key_id, self.access_key_secret, self.security_token)
        self.bucket = oss2.Bucket(self.auth, self.endpoint, bucket_name=self.bucket_name)

    def check_info(self):
        cks = ["access_key_id", "access_key_secret", "security_token", "bucket", "endpoint", "key"]
        flag = True
        for ck in cks:
            if self.config.get(ck) is None:
                logger.error(f"服务器返回OSS信息异常,缺少: {ck}")
                flag = False
        return flag

    def get_bucket_list(self):
        """列举当前endpoint下所有的bucket_name"""
        service = oss2.Service(self.auth, self.endpoint)
        bucket_list = [b.name for b in oss2.BucketIterator(service)]
        return bucket_list

    def get_all_file(self, prefix):
        """获取指定前缀下所有文件"""
        for b in islice(oss2.ObjectIterator(self.bucket, prefix=prefix), 10):
            yield b.key

    def read_file(self, path):
        try:
            file_info = self.bucket.get_object(path).read()
            return file_info
        except Exception as e:
            print(e, '文件不存在')

    def download_file(self, path, save_path):
        result = self.bucket.get_object_to_file(path, save_path)
        if result.status == 200:
            print('下载完成')

    def upload_file(self, local_path):
        try:
            result = self.bucket.put_object_from_file(self.key, local_path)
            logger.info(result)
            if result.status == 200:
                logger.info(f"文件{local_path}上传到服务器成功")
                return True
            else:
                logger.error(f"文件{local_path}上传到服务器失败:[{result.status}]")
                return False
        except Exception as e:
            logger.error(f"文件{local_path}上传到服务器失败:[{str(e)}]")