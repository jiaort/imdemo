import json
import random
import time

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

    def send_msg(self, to_account, msg_body, sync_other_machine=1, from_account=None):
        """
        单发单聊消息
        :param to_account:必填  消息接收方 UserID
        :param msg_body:必填  消息内容
        :param sync_other_machine:选填 1：把消息同步到 From_Account 在线终端和漫游上；2：消息不同步至 From_Account；若不填写默认情况下会将消息存 From_Account 漫游
        :param from_account:选填 消息发送方 UserID
        :return:
        """
        params = {
            "SyncOtherMachine": sync_other_machine,
            "From_Account": from_account,
            "To_Account": to_account,
            "MsgRandom": random.randint(1, 4294967294),
            "MsgTimeStamp": int(time.time()),
            "MsgBody": msg_body
        }
        if from_account:
            params["From_Account"] = from_account
        return self._request(path=ApiList.SEND_MSG, params=params)

    def batch_send_msg(self, to_account, msg_body, sync_other_machine=1, from_account=None):
        """
        批量发单聊消息
        :param to_account:必填 消息接收方用户 UserID ["id1", "id2", "id3"]
        :param msg_body:必填	 TIM 消息
        :param sync_other_machine:选填 把消息同步到 From_Account 在线终端和漫游上；2：消息不同步至 From_Account；若不填写默认情况下会将消息存 From_Account 漫游
        :param from_account:管理员指定消息发送方帐号
        :return:
        """
        params = {
            "SyncOtherMachine": sync_other_machine,
            "To_Account": to_account,
            "MsgRandom": random.randint(1, 4294967294),
            "MsgBody": msg_body
        }
        if from_account:
            params["From_Account"] = from_account
        return self._request(path=ApiList.BATCH_SEND_MSG, params=params)

    def import_msg(self, to_account, msg_body, sync_from_old_system=1, from_account=None):
        """
        导入单聊信息
        :param to_account:必填	消息接收方 UserID
        :param msg_body:必填	消息内容
        :param sync_from_old_system:必填 该字段只能填1或2，其他值是非法值 1表示实时消息导入，消息加入未读计数 2表示历史消息导入，消息不计入未读
        :param from_account:必填	消息发送方 UserID，用于指定发送消息方
        :return:
        """
        params = {
            "SyncFromOldSystem": sync_from_old_system,
            "From_Account": from_account,
            "To_Account": to_account,
            "MsgRandom": random.randint(1, 4294967294),
            "MsgTimeStamp": int(time.time()),
            "MsgBody": msg_body
        }
        return self._request(path=ApiList.IMPORT_MSG, params=params)

    def admin_get_roam_msg(self, from_account, to_account, max_cnt, min_time, max_time, last_msg_key=None):
        """
        查询单聊消息
        :param from_account:必填	会话其中一方的 UserID，若已指定发送消息方帐号，则为消息发送方
        :param to_account:必填	会话其中一方的 UserID
        :param max_cnt:必填	请求的消息条数
        :param min_time:必填	请求的消息时间范围的最小值
        :param max_time:必填	请求的消息时间范围的最大值
        :param last_msg_key:选填	上一次拉取到的最后一条消息的 MsgKey，续拉时需要填该字段
        :return:
        """
        params = {
           "From_Account": from_account,
           "To_Account": to_account,
           "MaxCnt": max_cnt,
           "MinTime": min_time,
           "MaxTime": max_time
        }
        if last_msg_key:
            params["LastMsgKey"] = last_msg_key
        return self._request(path=ApiList.ADMIN_GET_ROAM_MSG, params=params)

    def admin_msg_withdraw(self, from_account, to_account, msg_key):
        """
        撤回单聊消息
        :param from_account:必填	消息发送方 UserID
        :param to_account:必填	消息接收方 UserID
        :param msg_key:必填	待撤回消息的唯一标识。该字段由 REST API 接口 单发单聊消息 和 批量发单聊消息 返回
        :return:
        """
        params = {
            "From_Account": from_account,
            "To_Account": to_account,
            "MsgKey": msg_key
        }
        return self._request(path=ApiList.ADMIN_MSG_WITHDRAW, params=params)

    def admin_set_msg_read(self, report_account, peer_account):
        """
        设置单聊消息已读
        :param report_account:必填	进行消息已读的用户 UserId
        :param peer_account:必填	进行消息已读的单聊会话的另一方用户 UserId
        :return:
        """
        params = {
            "Report_Account": report_account,
            "Peer_Account": peer_account
        }
        return self._request(path=ApiList.ADMIN_SET_MSG_READ, params=params)

    # ------------------------------- 全员推送 -------------------------------

    # ------------------------------- 资料管理 -------------------------------

    def portrait_set(self, from_account, profile_item):
        """
        设置资料
        :param from_account: 必填	需要设置该 UserID 的资料
        :param profile_item:必填	待设置的用户的资料对象数组，数组中每一个对象都包含了 Tag 和 Value
        :return:
        """
        params = {
            "From_Account": from_account,
            "ProfileItem": profile_item
        }
        return self._request(path=ApiList.PORTRAIT_SET, params=params)

    def portrait_get(self, to_account, tag_list):
        """
        拉取资料
        :param to_account:必填	需要拉取这些 UserID 的资料；注意：每次拉取的用户数不得超过100，避免因回包数据量太大以致回包失败
        :param tag_list:必填	指定要拉取的资料字段的 Tag
        :return:
        """
        params = {
            "To_Account": to_account,
            "TagList": tag_list
        }
        return self._request(path=ApiList.PORTRAIT_GET, params=params)

    # -------------------------------关系链管理-------------------------------

    def friend_add(self, from_account, add_friend_item, add_type="Add_Type_Both", force_add_flags=1):
        """
        添加好友
        :param from_account:必填	需要为该 UserID 添加好友
        :param add_friend_item:必填	好友结构体对象
        :param add_type:选填	加好友方式（默认双向加好友方式）：Add_Type_Single 表示单向加好友 Add_Type_Both 表示双向加好友
        :param force_add_flags:选填	管理员强制加好友标记：1表示强制加好友，0表示常规加好友方式
        :return:
        """
        params = {
            "From_Account": from_account,
            "AddFriendItem": add_friend_item,
            "AddType": add_type,
            "ForceAddFlags": force_add_flags
        }
        return self._request(path=ApiList.FRIEND_ADD, params=params)

    def friend_import(self, from_account, add_friend_item):
        """
        导入好友
        :param from_account:必填	需要为该 UserID 添加好友
        :param add_friend_item:	必填	好友结构体对象
        :return:
        """
        params = {
            "From_Account": from_account,
            "AddFriendItem": add_friend_item
        }
        return self._request(path=ApiList.FRIEND_IMPORT, params=params)

    def friend_update(self, from_account, update_item):
        """
        更新好友
        :param from_account:必填	需要更新该 UserID 的关系链数据
        :param update_item:必填	需要更新的好友对象数组
        :return:
        """
        params = {
            "From_Account": from_account,
            "UpdateItem": update_item
        }
        return self._request(path=ApiList.FRIEND_UPDATE, params=params)

    def friend_delete(self, from_account, to_account, delete_type="Delete_Type_Single"):
        """
        删除好友
        :param from_account: 必填	需要删除该 UserID 的好友
        :param to_account:必填	待删除的好友的 UserID 列表，单次请求的 To_Account 数不得超过1000
        :param delete_type:选填	删除模式:1.Delete_Type_Single 单向删除2.Delete_Type_Both双向删除
        :return:
        """
        params = {
            "From_Account": from_account,
            "To_Account": to_account,
            "DeleteType": delete_type
        }
        return self._request(path=ApiList.FRIEND_DELETE, params=params)

    def friend_delete_all(self, from_account, delete_type="Delete_Type_Single"):
        """
        删除所有好友
        :param from_account:必填	指定要清除好友数据的用户的 UserID
        :param delete_type:选填	删除模式，默认删除单向好友 1.Delete_Type_Single 单向删除2.Delete_Type_Both双向删除
        :return:
        """
        params = {
            "From_Account": from_account,
            "DeleteType": delete_type
        }
        return self._request(path=ApiList.FRIEND_DELETE_ALL, params=params)

    def friend_check(self, from_account, to_account, check_type):
        """
        校验好友
        :param from_account: 必填	需要校验该 UserID 的好友
        :param to_account:必填	请求校验的好友的 UserID 列表，单次请求的 To_Account 数不得超过1000
        :param check_type:必填	校验模式:1.CheckResult_Type_Single 单向校验2.CheckResult_Type_Both 双向校验
        :return:
        """
        params = {
            "From_Account": from_account,
            "To_Account": to_account,
            "CheckType": check_type
        }
        return self._request(path=ApiList.FRIEND_CHECK, params=params)

    def friend_get(self, from_account, start_index, standard_sequence=0, custom_sequence=0):
        """
        拉取好友
        :param from_account: 必填	指定要拉取好友数据的用户的 UserID
        :param start_index:必填	分页的起始位置
        :param standard_sequence:选填	上次拉好友数据时返回的 StandardSequence，如果 StandardSequence 字段的值与后台一致，后台不会返回标配好友数据
        :param custom_sequence:选填	上次拉好友数据时返回的 CustomSequence，如果 CustomSequence 字段的值与后台一致，后台不会返回自定义好友数据
        :return:
        """
        params = {
            "From_Account": from_account,
            "StartIndex": start_index,
            "StandardSequence": standard_sequence,
            "CustomSequence": custom_sequence
        }
        return self._request(path=ApiList.FRIEND_GET, params=params)

    def friend_get_list(self, from_account, to_account, tag_list):
        """
        拉取指定好友
        :param from_account: 必填	指定要拉取好友数据的用户的 UserID
        :param to_account:必填	好友的 UserID 列表 建议每次请求的好友数不超过100，避免因数据量太大导致回包失败
        :param tag_list:必填	指定要拉取的资料字段及好友字段：
        :return:
        """
        params = {
            "From_Account": from_account,
            "To_Account": to_account,
            "TagList": tag_list
        }
        return self._request(path=ApiList.FRIEND_GET_LIST, params=params)

    def black_list_add(self, from_account, to_account):
        """
        添加黑名单
        :param from_account:必填	请求为该 UserID 添加黑名单
        :param to_account:必填	待添加为黑名单的用户 UserID 列表，单次请求的 To_Account 数不得超过1000
        :return:
        """
        params = {
            "From_Account": from_account,
            "To_Account": to_account
        }
        return self._request(path=ApiList.BLACK_LIST_ADD, params=params)

    def black_list_delete(self, from_account, to_account):
        """
        删除黑名单
        :param from_account:必填	需要删除该 UserID 的黑名单
        :param to_account:必填	待删除的黑名单的 UserID 列表，单次请求的 To_Account 数不得超过1000
        :return:
        """
        params = {
            "From_Account": from_account,
            "To_Account": to_account
        }
        return self._request(path=ApiList.BLACK_LIST_DELETE, params=params)

    def black_list_get(self, from_account, start_index, max_limited, last_sequence):
        """
        拉取黑名单
        :param from_account: 必填	需要拉取该 UserID 的黑名单
        :param start_index:必填	拉取的起始位置
        :param max_limited:必填	每页最多拉取的黑名单数
        :param last_sequence:必填	上一次拉黑名单时后台返回给客户端的 Seq，初次拉取时为0
        :return:
        """
        params = {
            "From_Account": from_account,
            "StartIndex": start_index,
            "MaxLimited": max_limited,
            "LastSequence": last_sequence
        }
        return self._request(path=ApiList.BLACK_LIST_GET, params=params)

    def black_list_check(self, from_account, to_account, check_type="BlackCheckResult_Type_Both"):
        """
        校验黑名单
        :param from_account: 必填	需要校验该 UserID 的黑名单
        :param to_account:必填	待校验的黑名单的 UserID 列表，单次请求的 To_Account 数不得超过1000
        :param check_type:必填	校验模式:1.单向校验黑名单关系	BlackCheckResult_Type_Single2.双向校验黑名单关系	BlackCheckResult_Type_Both
        :return:
        """
        params = {
            "From_Account": from_account,
            "To_Account": to_account,
            "CheckType": check_type
        }
        return self._request(path=ApiList.BLACK_LIST_CHECK, params=params)

    def group_add(self, from_account, group_name, to_account=None):
        """
        添加分组
        :param from_account:必填	需要为该 UserID 添加新分组
        :param group_name:必填	新增分组列表
        :param to_account:选填	需要加入新增分组的好友的 UserID 列表
        :return:
        """
        params = {
            "From_Account": from_account,
            "GroupName": group_name,
            "To_Account": to_account
        }
        if to_account:
            params["To_Account"] = to_account
        return self._request(path=ApiList.GROUP_ADD, params=params)

    def group_delete(self, from_account, group_name):
        """
        删除分组
        :param from_account:必填	需要删除该 UserID 的分组
        :param group_name:必填	要删除的分组列表
        :return:
        """
        params = {
            "From_Account": from_account,
            "GroupName": group_name,
        }
        return self._request(path=ApiList.GROUP_DELETE, params=params)

    def group_get(self, from_account, last_sequence=0, need_friend="", group_name=None):
        """
        拉取分组
        :param from_account:必填	指定要拉取分组的用户的 UserID
        :param last_sequence:选填	上次拉取分组的Sequence, 如果 Sequence 字段的值与后台一致，后台不会返回分组数据, 只有 GroupName 为空时有效,
        :param need_friend:选填	是否需要拉取分组下的 User 列表, Need_Friend_Type_Yes: 需要拉取, 不填时默认不拉取, 只有 GroupName 为空时有效.
        :param group_name:	选填	要拉取的分组名称
        :return:
        """
        params = {
            "From_Account": from_account,
            "NeedFriend": need_friend,
            "LastSequence": last_sequence,
            "GroupName": group_name
        }
        if last_sequence:
            params["LastSequence"] = last_sequence
        if need_friend:
            params["NeedFriend"] = need_friend
        if group_name:
            params["GroupName"] = group_name
        return self._request(path=ApiList.GROUP_GET, params=params)

    # ------------------------------- 群组管理 -------------------------------

    # ------------------------------全局禁言管理------------------------------

    # ------------------------------- 运营管理 -------------------------------
