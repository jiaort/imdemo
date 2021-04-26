

class ApiList(object):
    # 账号管理
    ACCOUNT_IMPORT = "im_open_login_svc/account_import"  # 导入单个帐号
    MULTI_ACCOUNT_IMPORT = "im_open_login_svc/multiaccount_import"  # 导入多个帐号
    ACCOUNT_DELETE = "im_open_login_svc/account_delete"  # 删除帐号
    ACCOUNT_CHECK = "im_open_login_svc/account_check"  # 查询帐号
    KICK = "im_open_login_svc/kick"  # 失效帐号登录态
    QUERY_STATE = "openim/querystate"  # 查询帐号在线状态

    # 单聊消息
    SEND_MSG = "openim/sendmsg"  # 单发单聊消息
    BATCH_SEND_MSG = "openim/batchsendmsg"  # 批量发单聊消息
    IMPORT_MSG = "openim/importmsg"  # 导入单聊消息
    ADMIN_GET_ROAM_MSG = "openim/admin_getroammsg"  # 查询单聊消息
    ADMIN_MSG_WITHDRAW = "openim/admin_msgwithdraw"  # 撤回单聊消息
    ADMIN_SET_MSG_READ = "openim/admin_set_msg_read"  # 设置单聊消息已读

    # 全员推送
    IM_PUSH = "all_member_push/im_push"  # 全员推送
    IM_SET_ATTR_NAME = "all_member_push/im_set_attr_name"  # 设置应用属性名称
    IM_GET_ATTR_NAME = "all_member_push/im_get_attr_name"  # 获取应用属性名称
    IM_GET_ATTR = "all_member_push/im_get_attr"  # 获取用户属性
    IM_SET_ATTR = "all_member_push/im_set_attr"  # 设置用户属性
    IM_REMOVE_ATTR = "all_member_push/im_remove_attr"  # 删除用户属性
    IM_GET_TAG = "all_member_push/im_get_tag"  # 获取用户标签
    IM_ADD_TAG = "all_member_push/im_add_tag"  # 添加用户标签
    IM_REMOVE_TAG = "all_member_push/im_remove_tag"  # 删除用户标签
    IM_REMOVE_ALL_TAGS = "all_member_push/im_remove_all_tags"  # 删除用户所有标签

    # 资料管理
    PORTRAIT_GET = "profile/portrait_get"  # 拉取资料
    PORTRAIT_SET = "profile/portrait_set"  # 设置资料

    # 关系链管理
    FRIEND_ADD = "sns/friend_add"  # 添加好友
    FRIEND_IMPORT = "sns/friend_import"  # 导入好友
    FRIEND_UPDATE = "sns/friend_update"  # 更新好友
    FRIEND_DELETE = "sns/friend_delete"  # 删除好友
    FRIEND_DELETE_ALL = "sns/friend_delete_all"  # 删除所有好友
    FRIEND_CHECK = "sns/friend_check"  # 校验好友
    FRIEND_GET = "sns/friend_get"  # 拉取好友
    FRIEND_GET_LIST = "sns/friend_get_list"  # 拉取指定好友
    BLACK_LIST_ADD = "sns/black_list_add"  # 添加黑名单
    BLACK_LIST_DELETE = "sns/black_list_delete"  # 删除黑名单
    BLACK_LIST_GET = "sns/black_list_get"  # 拉取黑名单
    BLACK_LIST_CHECK = "sns/black_list_check"  # 校验黑名单
    GROUP_ADD = "sns/group_add"  # 添加分组
    GROUP_DELETE = "sns/group_delete"  # 删除分组
    GROUP_GET = "sns/group_get"  # 拉取分组

    # 群组管理
    CREATE_GROUP = "group_open_http_svc/create_group"  # 创建群组
    GET_GROUP_INFO = "group_open_http_svc/get_group_info"  # 获取群组详细资料
    GET_GROUP_MEMBER_INFO = "group_open_http_svc/get_group_member_info"  # 获取群成员详细资料
    MODIFY_GROUP_BASE_INFO = "group_open_http_svc/modify_group_base_info"  # 修改群组基础资料
    ADD_GROUP_MEMBER = "group_open_http_svc/add_group_member"  # 增加群组成员
    DELETE_GROUP_MEMBER = "group_open_http_svc/delete_group_member"  # 删除群组成员
    MODIFY_GROUP_MEMBER_INFO = "group_open_http_svc/modify_group_member_info"  # 修改群组成员资料
    DESTROY_GROUP = "group_open_http_svc/destroy_group"  # 解散群组
    GET_JOINED_GROUP_LIST = "group_open_http_svc/get_joined_group_list"  # 获取用户所加入的群组
    GET_ROLE_IN_GROUP = "group_open_http_svc/get_role_in_group"  # 查询用户在群组中的身份
    FORBID_SEND_MSG = "group_open_http_svc/forbid_send_msg"  # 批量禁言和取消禁言
    GET_GROUP_SHUTTED_UIN = "group_open_http_svc/get_group_shutted_uin"  # 获取群组被禁言用户列表
    SEND_GROUP_MSG = "group_open_http_svc/send_group_msg"  # 在群组中发送普通消息
    SEND_GROUP_SYSTEM_NOTIFICATION = "group_open_http_svc/send_group_system_notification"  # 在群组中发送系统通知
    GROUP_MSG_RECALL = "group_open_http_svc/group_msg_recall"  # 群组消息撤回
    CHANGE_GROUP_OWNER = "group_open_http_svc/change_group_owner"  # 转让群组
    IMPORT_GROUP = "group_open_http_svc/import_group"  # 导入群基础资料
    IMPORT_GROUP_MSG = "group_open_http_svc/import_group_msg"  # 导入群消息
    IMPORT_GROUP_MEMBER = "group_open_http_svc/import_group_member"  # 导入群成员
    SET_UNREAD_MSG_NUM = "group_open_http_svc/set_unread_msg_num"  # 设置成员未读消息计数
    DELETE_GROUP_MSG_BY_SENDER = "group_open_http_svc/delete_group_msg_by_sender"  # 删除指定用户发送的消息
    GROUP_MSG_GET_SIMPLE = "group_open_http_svc/group_msg_get_simple"  # 拉取群漫游消息
    GET_ONLINE_NUM = "group_open_http_svc/group_msg_get_simple"  # 获取直播群在线人数

    # 全局禁言管理
    SET_NO_SPEAKING = "openconfigsvr/setnospeaking"  # 设置全局禁言
    GET_NO_SPEAKING = "openconfigsvr/getnospeaking"  # 查询全局禁言

    # 运营管理
    GET_APP_INFO = "openconfigsvr/getappinfo"  # 拉取运营数据
    GET_HISTORY = "open_msg_svc/get_history"  # 下载消息记录
    GET_IP_LIST = "ConfigSvc/GetIPList"  # 获取服务器 IP 地址
