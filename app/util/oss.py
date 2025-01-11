from minio import Minio
import io
from datetime import timedelta
from .b64 import decode_base64


class MinioClient:
    def __init__(self):
        client = Minio("127.0.0.1:9000",
            access_key="ZEbXcfZ0tWomxNr4OHpf",
            secret_key="VxCKxki5FkHy9frSsVjNl7uQbl3eSjuAkEKRZAbv",
            secure=False,
        )
        self.cli = client

    # 递归遍历一个buk
    def ls_buk(self, buk_name):
        if self.cli.bucket_exists(buk_name):
            objs = self.cli.list_objects(bucket_name=buk_name, recursive=True) # obj: bucket_name, object_name
            object_links = []
            for obj in objs:
                # 生成预签名的GET URL，设置过期时间（这里设置为1小时，单位是秒）
                presigned_url = self.cli.presigned_get_object(buk_name, obj.object_name, expires=timedelta(hours=2))
                object_links.append(presigned_url)
            return True, object_links
        else:
            # print(f'bucket: {buk_name} not exist')
            return False, None 

    def ls_one_buk(self, buk_name, user_dir):
        if self.cli.bucket_exists(buk_name):
            objs = self.cli.list_objects(bucket_name=buk_name, prefix=user_dir, recursive=True)
            object_links = []
            for obj in objs:
                print(obj.object_name)
                # 生成预签名的GET URL，设置过期时间（这里设置为1小时，单位是秒）
                presigned_url = self.cli.presigned_get_object(buk_name, obj.object_name, expires=timedelta(hours=2))
                object_links.append(presigned_url)
            return True, object_links
        else:
            # print(f'bucket: {buk_name} not exist')
            return False, None

    # 上传文件，并返回在线url
    def upload_file(self, buk_name, dst, base64_data):
        if not self.cli.bucket_exists(buk_name):
            # print(f"create bucket: {buk_name}")
            self.cli.make_bucket(buk_name)
        
        decoded_data = decode_base64(base64_data)
        data_stream = io.BytesIO(decoded_data)
        self.cli.put_object(
            buk_name, dst, data_stream, len(decoded_data)
        )
        presigned_url = self.cli.presigned_get_object(buk_name, dst, expires=timedelta(days=1))
        return presigned_url


MINIO_CLI = MinioClient()


if __name__ == '__main__':
    cli = MinioClient()
    base64_data = ""
    print(cli.upload_file("stable-diffusion", 
                    "user-1/taro.jpg",
                    base64_data))
    # print(cli.ls_buk("stable-diffusion"))
    # print(cli.ls_one_buk("stable-diffusion", "user-1"))