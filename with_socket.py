import websocket
import time


def STT(msg):
    '''
    忽略对@的转义，遇到具体问题再修改
    :param msg:
    :return:
    '''

    #分割'/'
    info_group = msg.split('/')
    info = []
    t = ''
    while info_group: #处理转义'/'
        temp = info_group.pop(0)
        if temp[-2:] != '@S':
            t += temp
            info.append(t)
            t = ''
        else:
            t += temp[:-2]

    #提取信息
    info_dict = {}
    for i in info:
        if i.find('@=')>=0:
            info_dict[i.split('@=')[0]] = i.split('@=')[1]
    return info_dict

def dy_encode(msg):
    '''
    按照字符串数据按照斗鱼协议封装为字节流
    :param msg:
    :return:
    '''
    data_len = len(msg) + 9
    msg_byte = msg.encode('utf-8')
    len_byte = int.to_bytes(data_len, 4, 'little')
    #小端序
    send_byte = bytearray([0xb1, 0x02, 0x00, 0x00])
    end_byte = bytearray([0x00])

    data = len_byte + len_byte + send_byte + msg_byte + end_byte

    return data


def login(ws):
    msg = 'type@=loginreq/roomid@=71415/'
    msg_bytes = dy_encode(msg)
    ws.send(msg_bytes)


def join_group(ws):
    msg = 'type@=joingroup/rid@=71415/gid@=-9999/'
    msg_bytes = dy_encode(msg)
    ws.send(msg_bytes)


def on_open(ws):
    print('open')
    login(ws)
    print('hello')
    #time.sleep(1)
    join_group(ws)

def on_error(ws):
    print('error')

def on_message(ws, message):
    msg = message.decode(encoding='utf-8', errors='ignore')
    index = msg.find('type')
    if index<0: return
    else:
        pass
    #print(message)
    print('----')
ws = websocket.WebSocketApp('wss://danmuproxy.douyu.com:8502/',
                         on_open = on_open, on_message= on_message, on_error=on_error)
print(ws)#ws.run_forever()
