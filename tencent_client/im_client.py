import json
import random

import TLSSigAPIv2
import requests

from tencent_client.constants import ApiList


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
        return "{base_url}/{version}/{path}?sdkappid={app_id}&identifier={identifier}&usersig={user_sig}&random={random}&contenttype=json".format(
            base_url=self.base_url,
            version=self.version,
            path=path,
            app_id=self.app_id,
            identifier=self.identifier,
            user_sig=user_sig,
            random=random.randint(1, 4294967294)
        )

    # ------------------------------- 账号管理 -------------------------------

    def _request(self, path, params):
        header = {"Content-Type": "application/json; charset=utf-8"}
        url = self._format_url(path=path)
        resp = requests.post(url=url, data=json.dumps(params), headers=header)

        if resp.status_code != 200:
            return None, "http error status code is %d" % resp.status_code

        result = json.loads(resp.text)
        if result["ErrorCode"] != 0:
            return None, "操作失败, 错误码: %d, 错误信息: %s " % (result["ErrorCode"], result["ErrorInfo"])

        return result, None

    def account_import(self, identifier, nick="", face_url=""):
        """
        导入单个账号
        :param identifier:必填	用户名，长度不超过32字节
        :param nick:选填	用户昵称 非必填
        :param face_url:选填	用户头像 URL
        :return:
        """
        params = {
            "Identifier": identifier,
            "Nick": nick,
            "FaceUrl": face_url
        }
        return self._request(path=ApiList.ACCOUNT_IMPORT, params=params)

    def multi_account_import(self, accounts):
        """
        导入多个账号
        :param accounts:必填	用户名，单个用户名长度不超过32字节，单次最多导入100个用户名 例:["test1","test2","test3"]
        :return:"FailAccounts": ["test3","test4"]
        """
        params = {
            "Accounts": accounts
        }
        return self._request(path=ApiList.MULTI_ACCOUNT_IMPORT, params=params)

    def account_delete(self, delete_item):
        """
        删除帐号
        :param delete_item:必填	请求删除的帐号对象数组，单次请求最多支持100个帐号 例:[{"UserID":"UserID_1"}, {"UserID":"UserID_2"}]
        :return:"ResultItem": [{"ResultInfo": "", "ResultCode": 0, "UserID": "UserID_1"}]
        """
        params = {
            "DeleteItem": delete_item
        }
        return self._request(path=ApiList.ACCOUNT_DELETE, params=params)

    def account_check(self, check_item):
        """
        查询帐号
        :param check_item:必填	请求检查的帐号对象数组，单次请求最多支持100个帐号 例:[{"UserID":"UserID_1"}, {"UserID":"UserID_2"}]
        :return:"ResultItem": [{"ResultInfo": "", "ResultCode": 0, "UserID": "UserID_1", "AccountStatus": "Imported"}]
        """
        params = {
            "CheckItem": check_item
        }
        return self._request(path=ApiList.ACCOUNT_CHECK, params=params)

    def kick(self, identifier):
        """
        失效帐号登录状态
        :param identifier:必填	用户名
        :return:
        """
        params = {
            "Identifier": identifier
        }
        return self._request(path=ApiList.KICK, params=params)

    def query_state(self, to_account, is_need_detail=1):
        """
        查询帐号在线状态
        :param to_account:必填	需要查询这些 UserID 的登录状态，一次最多查询500个 UserID 的状态 例:["id1", "id2", "id3"]
        :param is_need_detail:选填	是否需要返回详细的登录平台信息。0表示不需要，1表示需要
        :return:"QueryResult": [{"Status": "Offline", "To_Account": "id1", "Detail": [{"Status": "PushOnline", "Platform": "iPhone"}]}], "ErrorList": [{"ErrorCode": 70107, "To_Account": "id4"}]
        """
        params = {
            "To_Account": to_account,
            "IsNeedDetail": is_need_detail
        }
        return self._request(path=ApiList.QUERY_STATE, params=params)

    # ------------------------------- 单聊消息 -------------------------------

    def send_msg(self):
        params = {
          "SyncOtherMachine": 2,
          "To_Account": "test",
          "MsgLifeTime": 60,
          "MsgRandom": 1287657,
          "MsgTimeStamp": 1557387418,
          "ForbidCallbackControl": [
              "ForbidBeforeSendMsgCallback",
              "ForbidAfterSendMsgCallback"],
          "MsgBody": [
              {
                  "MsgType": "TIMTextElem",
                  "MsgContent": {
                      "Text": "hi, beauty"
                  }
              }
          ]
        }
        return self._request(path=ApiList.SEND_MSG, params=params)

    # ------------------------------- 全员推送 -------------------------------

    # ------------------------------- 资料管理 -------------------------------

    # -------------------------------关系链管理-------------------------------

    # ------------------------------- 群组管理 -------------------------------

    # ------------------------------全局禁言管理------------------------------

    # ------------------------------- 运营管理 -------------------------------
