import requests
import json

"""
flask 转发请求
"""



def forward(method, url, data=None):
    resp = requests.request(
        method=method,
        url=url,
        headers={'Content-Type': 'application/json'},
        data=json.dumps(data),  
        allow_redirects=True
    )

    return resp

def forward_img(method, url, files):
    resp = requests.request(
        method=method,
        url=url,
        # headers={'Content-Type': 'multipart/form-data'},
        files=files,
        allow_redirects=True
    )
    return resp
    