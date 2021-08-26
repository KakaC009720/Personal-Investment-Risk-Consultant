from __future__ import unicode_literals
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import configparser
import socket

HOST = '140.112.77.223'
# HOST = '192.168.50.33'
PORT = 8001
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)#創建socket
s.connect((HOST, PORT))

import random

app = Flask(__name__)

# LINE 聊天機器人的基本資料
config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))


cust_dict = {'陳水扁':'0xDB5D3FF6B7FE584CAE62A6C482194282E627EE8F9BBB37D0BBA43B012950E3D0', '謝和弦':'0x1879388A362A9CE3DB27F651C333F9BF4B66460538CFD835F4F77E45604CFD4F',
             '馬國畢':'0x2CC4318BDB487149593968E62D0DC8C9E8A3F944D53E8B8F04157D1FF190C110', '管中閔':'0xDEB36E25115FA1D4110585FEBCACA4CA47C0CD20F9B72C70D763367D7C39A95A',
             '沈玉琳':'0x7B83CC2F7277C326BF453700F5B7BB3AA724ED1D70C20610506636E8238BC33D', 'Roger':'0x9F1EEE596FF0826776B7A06872551DDE4C255E2C8DB062C2B659AE30F715A70A',
             '澎恰恰':'0xE826AF7E13E31F58DF029FBAEE6DD595DE0E80B0BD04E40EB52E60B7E5872D05', '吳卓源':'0x3D9FB8340B7224458A12155729070B01EE3FDF4FC93E81CBCD2087AE87B81EE1',
             '冰冰姐':'0x60468F34540AC80C2DB243C8B815B1348596E0A6B7E030F28373BC72FE32CE05', '伍佰':'0xCB749C009EDD7BDE588EBF4EAAC84E486A2960C3B4FA58D951C54EEB1DEA326E',
             '郭台銘':'0xCFEAD510FA89A8C96F85B748FAA9C815F9E2F5D3D3FE51DB48174EACCA042026'}

com_dict = {'台積電':'0x991E478FD3C620A5ECF41EAC7211CDAF','鴻海':'0x456FEE4ACB733FD682DEDE7D1EF34F61','高端疫苗':'0xA73B841C849CBE3015E8EBF37ACB39C5',
            '元大台灣50':'0x36844187BB864E60FF2BF0CC345E94F1','統一':'0x4FCCF5F8C79FD5E3F5FE45D4D14C6602','長榮':'0xC572EEDFBDA2296DD716B89D211EBD4E',
            '台達電':'0xFE7DF6B9A1C916501388DBAFF03EE3CE','HTC':'0xAD2C8534816572ABC628C0CACF414D7C','王品':'0xC3DF87C14AA2ACD0B2DB6FD8F57F4B72',
            '巨大':'0xF4FB551DCFD5C725F31FEF1BE8DCC7FB', '大立光':'0x0D146D60FF69F2BD8B3367E1574A8A5D'}



def json(obj):
    if isinstance(obj, bytes):
        return str(obj, encoding='utf-8')

# 接收 LINE 的資訊
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        print(body, signature)
        handler.handle(body, signature)

    except InvalidSignatureError:
        abort(400)

    return 'OK'


# 學你說話
@handler.add(MessageEvent, message=TextMessage)
def echo(event):

    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":

        # #根據使用者輸入
        # if event.message.text == '1':
        #     line_bot_api.reply_message(
        #         event.reply_token,
        #         TextSendMessage(text='one')
        #     )
        # elif event.message.text == '2':
        #     line_bot_api.reply_message(
        #         event.reply_token,
        #         TextSendMessage(text='two')
        #     )
        # else:
        #     line_bot_api.reply_message(
        #         event.reply_token,
        #         TextSendMessage(text='third')
        #     )


        x = event.message.text.split(',')
        cust_num = x[0]
        com_num = x[1]
        stock_num = x[2]
        type = x[3]

        msg = cust_dict[cust_num] + ',' + com_dict[com_num] + ',' + stock_num + ',' + type


        s.sendall(msg.encode('utf-8'))  # 發送
        data = s.recv(1024)  # 接收伺服器訊息
        data = json(data)
        if data == '0':
            data = '此交易未偵測到異常，祝您交易愉快！'
        elif data == '1':
            data = '！！！此交易偵測為異常，請再次確認！！！'
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=data))



        # s.close()

        ###### repeat
        # if event.message.text:
        #     line_bot_api.reply_message(
        #         event.reply_token,
        #         TextSendMessage(text=event.message.text)
        #     )

        ##### add
        # add = '加什麼'
        # if event.message.text:
        #     line_bot_api.reply_message(
        #         event.reply_token,
        #         TextSendMessage(text=event.message.text + add)
        #     )


if __name__ == "__main__":
    app.run()


