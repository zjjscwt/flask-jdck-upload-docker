import os
import ql
from flask import Flask, request

app = Flask(__name__)


@app.route('/', methods=["GET"])
def index():
    return "Ohhhhhhhhh"


@app.route('/jd', methods=["GET"])
def jd():
    address = os.getenv('address')
    client_id = os.getenv('client_id')
    client_secret = os.getenv('client_secret')
    cookie_str = request.args.get("ck")
    encoder = ql.ck_encode(cookie_str)
    pin = encoder[0]  # 截取pt_pin并转义
    cookie = encoder[1]
    token = ql.gettoken(address, client_id, client_secret)  # Token获取-网络状态
    if token[0]:  # Token获取-网络状态
        token = token[1]
        id = ql.newck(pin, token, address)
        if id[0]:  # 用户信息-网络状态
            if id[1]:
                r = ql.new(token, cookie, address)
                if r:
                    return ("用户提交成功")
                else:
                    return ("用户提交失败")
            else:
                id = id[2]
                r = ql.old(token, cookie, id, address)
                if r:
                    return ("用户更新成功")
                else:
                    return ("用户更新失败")
        else:
            return ("用户信息获取失败")
    else:
        return ("服务器链接失败")


if __name__ == '__main__':
    app.run()
