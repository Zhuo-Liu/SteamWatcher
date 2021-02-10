from PyWeChatSpy import WeChatSpy
from PyWeChatSpy.command import *
from lxml import etree
import requests
import time
import logging
import base64
import os
import time

from updater import *
from game_fetcher import *
from player import *


logger = logging.getLogger(__file__)
formatter = logging.Formatter('%(asctime)s [%(threadName)s] %(levelname)s: %(message)s')
sh = logging.StreamHandler()
sh.setFormatter(formatter)
sh.setLevel(logging.DEBUG)
logger.addHandler(sh)
logger.setLevel(logging.INFO)

contact_list = []
chatroom_list = []

wx_id_siyu = "wxid_ntjypfumpplf12"
wx_id_jixiang = "wxid_8930319308012"
wx_id_chatroomtest1 = "26514418133@chatroom"
wx_id_chatroomtest2 = "17646022445@chatroom"
wx_id_chatroomtest_peking = "17506685111@chatroom"
wx_id_chatroomtest_dota = "17337914266@chatroom"

def my_proto_parser(data):
    if data.type == WECHAT_CONNECTED:
        print("-"*10, "微信连接成功", "-"*10)
    elif data.type == WECHAT_LOGIN:
        print("-"*10, "微信登录成功", "-"*10)
        spy.get_login_info()
    elif data.type == WECHAT_LOGOUT:
        print("-"*10, "微信登出", "-"*10)
    elif data.type == LOGIN_INFO:
        print("-"*10, "登录信息", "-"*10)
        print(data.login_info.wxid)
        print(data.login_info.nickname)
        print(data.login_info.wechatid)
        print(data.login_info.phone)
        print(data.login_info.profilephoto)
    elif data.type == CONTACTS:
        pass
    elif data.type == MESSAGE:
        # 消息
        for message in data.message:
            if message.type == 1:
                print("-"*10, "文本消息", "-"*10)
                if "受的什么教育" in message.content:
                    spy.send_text(message.wxid1, f"内华达数学系")
                if "nmsl" in message.content:
                    spy.send_text(message.wxid1, f"nmysl")
                if "傻狗" in message.content:
                    spy.send_text(message.wxid1, f"傻帕克")
                if "你喊什么" in message.content:
                    spy.send_text(message.wxid1, f"啊啊啊啊啊")
            elif message.type == 3:
                print("-"*10, "图片消息", "-"*10)
                continue
            elif message.type == 37:
                print("-"*10, "好友请求消息", "-"*10)
                continue
            elif message.type == 49 and "邀请你加入群聊" in message.content:
                print("-" * 10, "群邀请", "-" * 10)
                continue
            else:
                print("-"*10, f"其他消息:{message.type}", "-"*10)
            print("来源1:", message.wxid1)
            print("来源2:", message.wxid2)
            print("消息头:", message.head)
            print("消息内容:", message.content)
    elif data.type == QRCODE:
        print("-"*10, "登录二维码", "-"*10)
    elif data.type == CONTACT_EVENT:
        print("-"*10, "联系人事件", "-"*10)
    elif data.type == CHATROOM_MEMBERS:
        print("-"*10, "群成员列表", "-"*10)
    elif data.type == CONTACT_STATUS:
        print("-"*10, "联系人状态", "-"*10)
    elif data.type == HEART_BEAT:
        # 心跳
        pass
    elif data.type == SET_REMARK:
        print("-" * 10, "备注设置完成", "-" * 10)
    elif data.type == CONTACT_STATUS:
        print("-" * 10, "联系人状态", "-" * 10)
    elif data.type == GET_CHATROOM_INVITATION_URL:
        print("-" * 10, "群邀请链接", "-" * 10)
    elif data.type == DECRYPT_IMAGE:
        print("-" * 10, "解密后的图片", "-" * 10)

spy = WeChatSpy(parser=my_proto_parser)
spy.run(r"C:\Program Files (x86)\Tencent\WeChat\WeChat.exe")
input()
print("开始监控")

# if __name__ == '__main__':
#     #spy = WeChatSpy(parser=my_proto_parser, key="3ea954244f76a8cfb7e5f8f544cf6878", logger=logger)
#     spy = WeChatSpy(parser=my_proto_parser)
#     spy.run(r"C:\Program Files (x86)\Tencent\WeChat\WeChat.exe")
#     #spy.send_text(wx_id_chatroomtest,f"啊啊啊")

#     #spy.send_text(wx_id_siyu, f"???")

#     input()
#     # player_list_temp = [
#     #     ["Zard-", "104744847"]
#     # ]
#     # player_list = []
#     # for player_temp in player_list_temp:
#     #     nickname = player_temp[0]
#     #     steam_id = player_temp[1]
#     #     try:
#     #         last_match_id = get_last_match_id_by_steamID(steam_id)
#     #     except DOTA2HTTPError:
#     #         last_match_id = "-1"

#     #     player_list.append(player(steam_id,nickname,last_match_id))
    
#     # print(player_list)
#     # print("玩家载入完毕")
#     # while True:
#     #     reports = update(player_list)
#     #     spy.send_text(wx_id_chatroomtest,reports[0])
#     #     time.sleep(30)
