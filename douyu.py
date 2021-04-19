import time
import websocket
from MyMongo import myDB
from tools import *
from datetime import datetime, timedelta, timezone

PROXY = 'wss://danmuproxy.douyu.com:8502/'
TIMEZONE = timezone(timedelta(hours=+8))

class Douyu:
    def __init__(self, rid):
        self.rid = rid
        self.db = myDB(rid)
        self.proxy = danmu_proxy(rid, self.db)

    def get_danmu(self):
        self.proxy.run()

class danmu_proxy():
    def __init__(self, rid, db, gid=-9999):
        self.__rid = rid
        self.__group = gid
        self.db = db
        self.tiktok = None

    @property
    def groupid(self):
        return self.__group

    @groupid.setter
    def groupid(self, group_id):
        self.__group = group_id

    def login(self, ws):
        msg = 'type@=loginreq/roomid@={}/'.format(self.__rid)
        msg_bytes = dy_encode(msg)
        ws.send(msg_bytes)

    def join_group(self,ws):
        msg = 'type@=joingroup/rid@={}/gid@={}/'.format(self.__rid, self.__group)
        msg_bytes = dy_encode(msg)
        ws.send(msg_bytes)

    def keep_alive(self,ws):
        import datetime
        msg = 'type@=keeplive/@tick@={}'.format(int(time.time()))
        msg_bytes = dy_encode(msg)
        ws.send(msg_bytes)

    def on_open(self,ws):
        print('open')
        self.login(ws)
        self.join_group(ws)
        self.keep_alive(ws)
        self.tiktok = datetime.now()

    def on_error(self, exc):
        print('error')

    def on_close(self, ws):
        print('close')

    def on_message(self, ws, message):
        now = datetime.now()
        if (now-self.tiktok).seconds > 45:
            self.keep_alive(ws)
            self.tiktok = now
        msg = message.decode(encoding='utf-8', errors='ignore')
        index = msg.find('type')
        if index < 0:
            return
        else:
            info_dict = STT(msg[index:])
        filted = danmu_filter(info_dict)
        if filted:
            date = datetime.today().astimezone(TIMEZONE)
            filted['dbid'] = '{name}-{year}-{month}-{day}'.format(name=filted['type'], year=date.year,
                                                                  month=date.month, day=date.day)
            filted['time'] = '{hour}-{minute}-{second}'.format(hour=date.hour, minute=date.minute, second=date.second)
            self.db.insert(filted)

    def run(self):
        ws = websocket.WebSocketApp(PROXY, on_open=self.on_open, on_message=self.on_message, on_error=self.on_error)
        ws.run_forever()

#start = datetime.now()
while True:
    Douyu('71415').get_danmu()
    #end = datetime.now()
    print(datetime.now())
#print(end-start)