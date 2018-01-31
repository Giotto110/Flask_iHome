# -*- coding:utf-8 -*-

from qiniu import Auth, put_data

access_key = "yV4GmNBLOgQK-1Sn3o4jktGLFdFSrlywR2C-hvsW"
secret_key = "bixMURPL6tHjrb8QKVg2tm7n9k8C7vaOeQ4MEoeW"

bucket_name = "ihome"


def upload_image(data):
    q = Auth(access_key, secret_key)
    token = q.upload_token(bucket_name)
    ret, info = put_data(token, None, data)

    if info.status_code == 200:
        # 代表上传成功
        return ret.get("key")
    else:
        # 代表上传失败
        raise Exception("七牛上传文件失败")


if __name__ == '__main__':
    file_name = raw_input("请输入文件名：")
    with open(file_name, "rb") as f:
        print upload_image(f.read())
