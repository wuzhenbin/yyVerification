#!/usr/bin/env python
# coding:utf-8

import requests
from hashlib import md5


# 超级鹰用户名、密码、软件 ID、验证码类型 
CHAOJIYING_USERNAME = '' 
CHAOJIYING_PASSWORD = ''
# 验证码类型 # 用户中心>>软件ID 
CHAOJIYING_SOFT_ID =  
CHAOJIYING_KIND = 9102


class Chaojiying:
    def __init__(self):
        self.username = CHAOJIYING_USERNAME
        self.password =  md5(CHAOJIYING_PASSWORD.encode('utf8')).hexdigest()
        self.soft_id = CHAOJIYING_SOFT_ID
        self.base_params = {
            'user': self.username,
            'pass2': self.password,
            'softid': self.soft_id,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        }

    def PostPic(self, im, codetype):
        """
        im: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        params = {
            'codetype': codetype,
        }
        params.update(self.base_params)
        files = {'userfile': ('ccc.jpg', im)}
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, files=files, headers=self.headers)
        return r.json()

    def ReportError(self, im_id):
        """
        im_id:报错题目的图片ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://upload.chaojiying.net/Upload/ReportError.php', data=params, headers=self.headers)
        return r.json()


if __name__ == '__main__':
    chaojiying = Chaojiying()  
    # 本地图片文件路径 来替换 a.jpg
    with open('a.jpg', 'rb') as f:
        im = f.read() 

    #1902 验证码类型  官方网站>>价格体系 3.4+版 print 后要加()
    res = chaojiying.PostPic(im, 1902)                                            
    if res['pic_str']:
        data = res['pic_str']

    