import websocket
import threading
import time
from wechat_bot import spy, wx_id_chatroomtest_peking, wx_id_chatroomtest_dota
import requests
import pandas as pd
import os
import numpy as np

#IMPORTNANT_MESSAGE = ['888888888','秒了吧','好起来了','咱不受这气','哭哭','烦死了','哭了','啊啊啊啊啊啊','好！','哈哈哈哈哈哈哈哈哈哈哈哈']
#i = 0
status = 0
last_report_time = 0
save_time = time.time()
#url_douyu = 'https://web.sinsyth.com/lxapi/douyujx.x?roomid=60937'
url_douyu = 'https://www.douyu.com/gapi/rkc/directory/mixList/2_3/1'
hao_count = 0
ha_count = 0
eight_count = 0
time_before = time.time()
hao_list = []
ha_list = []
eight_list = []

class DouyuError(Exception):
    pass

def on_error(ws, error):
    print(error)

def on_close(ws):
    print('close')

def __login(ws,room_id):
    #login_msg = 'type@=loginreq/room_id@=%s/dfl@=sn@A=105@Sss@A=1/username@=%s/uid@=%s/ver@=20190610/aver@=218101901/ct@=0/' % (self.__room_id, '61609154', '61609154')
    login_msg = 'type@=loginreq/room_id@=%s/' % (room_id)
    ws.send(dy_encode(login_msg))

def __join_group(ws,room_id):
    join_group_msg = 'type@=joingroup/rid@=%s/gid@=-9999/' % (room_id)
    ws.send(dy_encode(join_group_msg))

# def __start_heartbeat(ws):
#     __heartbeat_thread = threading.Thread(target=__heartbeat(ws))
#     __heartbeat_thread.start()

def __heartbeat(ws):
    heartbeat_msg = 'type@=mrkl/'
    heartbeat_msg_byte = dy_encode(heartbeat_msg)
    global status

    while True:
        try:
            response_douyu = requests.get(url_douyu)
        except requests.RequestException:
            raise DouyuError("Requests Douyu Error")

        if response_douyu.status_code >= 400:
            raise DouyuError("Connection Douyu Failed")
            
        x = response_douyu.json()
        room_id_list = []
        room_name_list = []
        for room in x['data']['rl']:
            room_id_list.append(room['rid'])
            room_name_list.append(room['rn'])
        if 60937 in room_id_list:
            temp = status
            status = 1
            if status != temp and status == 1:
                title = room_name_list[room_id_list.index(60937)]
                open_content="xg 开播了！！！直播间标题：{}  https://www.douyu.com/60937".format(title)
                print(open_content)
                #spy.send_text(wx_id_chatroomtest_peking,open_content)
                #spy.send_text(wx_id_chatroomtest_dota, open_content)
        else:
            status = 0
            print("room closed")

        for j in range(10):  
            ws.send(heartbeat_msg_byte)
            time.sleep(45)


def on_open(ws):
    room_id='60937'
    __login(ws,room_id)
    __join_group(ws,room_id)
    __heartbeat_thread = threading.Thread(target=__heartbeat,args=(ws,))
    __heartbeat_thread.start()

def on_message(ws,msg):
    global time_before
    global last_report_time
    global save_time
    global hao_count
    global ha_count
    global eight_count

    global hao_list
    global ha_list
    global eight_list

    time_now = time.time()

    if status == 1:
        if time_now - time_before > 60:
            # print("好："+str(hao_count))
            # print("哈："+str(ha_count))
            # print("888："+str(eight_count))
            hao_list.append(hao_count)
            ha_list.append(ha_count)
            eight_list.append(eight_count)
            if time_now - last_report_time >5600:
                if hao_count+ha_count > 100 or eight_count >25:
                    content= "注意，xg好像又在做菜了！！！速来 https://www.douyu.com/60937 下饭！注：过去60秒，”好“在弹幕中出现了{}次，“哈哈哈“在弹幕中出现了{}次,“888”在弹幕中出现了{}次".format(hao_count,ha_count,eight_count)
                    #spy.send_text(wx_id_chatroomtest_peking, content)
                    #spy.send_text(wx_id_chatroomtest_dota, content)
                    print(content)
                    last_report_time = time_now
            hao_count = 0
            ha_count = 0
            eight_count = 0
            time_before = time_now

        chat_message = get_chat_messages(msg)
        if chat_message is not None:
            for entry in chat_message:
                if "好" in entry:
                    hao_count = hao_count + 1
                if "哈哈哈" in entry:
                    ha_count = ha_count + 1
                if "888" in entry:
                    eight_count = eight_count + 1
                #print(chat_message)
                #global i
                #i = i + 1
                #print(i)
                # if i % 5 ==0 and i<1000000:
                    # for ma in IMPORTNANT_MESSAGE:
                    #     if ma in chat_message[0]:
                    #         global last_report_time
                    #         report_time = time.time()
                    #         if report_time - last_report_time > 1800:
                    #             content= "注意，xg好像又在做菜了！！！速来 https://www.douyu.com/60937 下饭！注：提示源为出现弹幕：{}".format(chat_message)
                    #             spy.send_text(wx_id_chatroomtest1,content)
                    #             # print("向微信群播报")
                    #             # print(content)
                    #             last_report_time = report_time
                    #             print(i)
    if time_now - save_time > 20000:
        data = [hao_list,ha_list,eight_list]
        ydata = np.array(data).T
        data_pd=pd.DataFrame(data=ydata)
        data_pd.to_csv('./danmu_data2.csv')
        print("output!")
        os._exit(0)

def dy_encode(msg):
    # 头部8字节，尾部1字节，与字符串长度相加即数据长度
    # 为什么不加最开头的那个消息长度所占4字节呢？这得问问斗鱼^^
    data_len = len(msg) + 9
    # 字符串转化为字节流
    msg_byte = msg.encode('utf-8')
    # 将数据长度转化为小端整数字节流
    len_byte = int.to_bytes(data_len, 4, 'little')
    # 前两个字节按照小端顺序拼接为0x02b1，转化为十进制即689（《协议》中规定的客户端发送消息类型）
    # 后两个字节即《协议》中规定的加密字段与保留字段，置0
    send_byte = bytearray([0xb1, 0x02, 0x00, 0x00])
    # 尾部以'\0'结束
    end_byte = bytearray([0x00])
    # 按顺序拼接在一起
    data = len_byte + len_byte + send_byte + msg_byte + end_byte

    return data

def dy_decode(msg_byte):
    pos = 0
    msg = []

    while pos < len(msg_byte):
        content_length = int.from_bytes(msg_byte[pos: pos + 4], byteorder='little')
        content = msg_byte[pos + 12: pos + 3 + content_length].decode(encoding='utf-8', errors='ignore')
        msg.append(content)
        pos += (4 + content_length)

    return msg

def __parse_msg(raw_msg):
    #res = []
    attrs = raw_msg.split('/')[0:-1]
    for attr in attrs:
        attr = attr.replace('@S', '/')
        attr = attr.replace('@A', '@')
        couple = attr.split('@=')
        if couple[0] == 'type' and couple[1] != 'chatmsg':
            return None
        if couple[0] == 'txt':
            return couple[1]
    
    return None

def get_chat_messages(msg_byte):
    decode_msg = dy_decode(msg_byte)
    messages = []

    for msg in decode_msg:
        res = __parse_msg(msg)
        if res is not None and res !='':
            messages.append(res)
    if len(messages) !=0:
        return messages
    else:
        return None



def start_douyu_watcher():
    ws = websocket.WebSocketApp('wss://danmuproxy.douyu.com:8504/', 
    on_message=on_message, on_error=on_error, 
    on_close=on_close, on_open=on_open)

    ws.run_forever()

if __name__ == "__main__":
    # spy = WeChatSpy(parser=my_proto_parser)
    # spy.run(r"C:\Program Files (x86)\Tencent\WeChat\WeChat.exe")

    ws = websocket.WebSocketApp('wss://danmuproxy.douyu.com:8504/', 
        on_message=on_message, on_error=on_error, 
        on_close=on_close, on_open=on_open)

    ws.run_forever()
