INFO_MAP ={'chatmsg': {'uid':'uid', '昵称':'nn', '内容': 'txt', '平台等级': 'level', '粉丝牌': 'bnn', '粉丝牌等级':'bl'},
           'ssd': {'超级弹幕':'sdid', '内容':'content'},
           'dgb': {'礼物id':'gfid', '礼物样式':'gs', 'uid':'uid', '昵称':'nn', '礼物个数':'gfcnt'}}

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

def danmu_filter(ori):
    '''
    获取一种类型的弹幕
    :param ori:
    :param filter:
    :return:
    '''
    info = {}
    if ori['type'] in INFO_MAP:
        info_map = INFO_MAP[ori['type']]
        info['type'] = ori['type']
        for key in info_map:
            info[key] = ori[info_map[key]]
    return info