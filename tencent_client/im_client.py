import json
import random

import TLSSigAPIv2
import requests


class IMClient(object):

    def __init__(self):
        self.base_url = "https://console.tim.qq.com"
        self.version = "v4"
        self.identifier = "administrator"
        self.app_id = 1400512134
        self.secret = "150427f3d9e7f25c69d24f79538432aa51eb4ed2b8cc990dee23340b4a2d64a2"

    def _get_user_sign(self):
        # TODO 存入redis
        api = TLSSigAPIv2.TLSSigAPIv2(self.app_id, self.secret)
        user_sig = api.gen_sig(self.identifier, expire=180*86400)
        return user_sig

    def _format_url(self, path):
        user_sig = self._get_user_sign()
        return f"{self.base_url}/{self.version}/{path}?sdkappid={self.app_id}&identifier={self.identifier}" \
               f"&usersig={user_sig}&random={random.randint(1, 4294967294)}&contenttype=json"

    # ------------------------------- 账号管理 -------------------------------

    def request(self, path, params):
        header = {"Content-Type": "application/json; charset=utf-8"}
        url = self._format_url(path=path)
        resp = requests.post(url=url, data=json.dumps(params), headers=header)

        if resp.status_code != 200:
            return None, "http error status code is %d" % resp.status_code

        result = json.loads(resp.text)
        if result["ErrorCode"] != 0:
            return None, "操作失败, 错误码: %d, 错误信息: %s " % (result["ErrorCode"], result["ErrorInfo"])

        return result, None
