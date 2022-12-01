from urllib.parse import quote
import json
import requests


s = requests.session()


def ck_encode(cookie_str):
    cookie_dict = {cookie.split('=')[0]: cookie.split(
        '=')[-1] for cookie in cookie_str.split(';')}
    pin = quote(cookie_dict['pt_pin'])
    cookie = "pt_key="+cookie_dict['pt_key']+";pt_pin="+pin+";"
    return pin, cookie


def gettoken(address, client_id, client_secret):  # 查询青龙Token
    url = 'http://{0}/open/auth/token?client_id={1}&client_secret={2}'.format(
        address, client_id, client_secret)
    res = requests.get(url)
    token = json.loads(res.text)["data"]['token']
    if res.status_code == 200:  # 判断 HTTP返回状态码
        return True, token
    else:
        return False,


def newck(pin, token, address):  # 查询账号是否已登录
    url = 'http://{0}/open/envs?searchValue={1}'.format(address, pin)
    headers = {'Authorization': 'Bearer {0}'.format(token)}
    res = requests.get(url=url, headers=headers)
    if res.status_code == 200:
        newuser = res.json()["data"]
        if newuser == []:  # 未登录账号
            return True, True,
        else:  # 已登录账号
            id = newuser[0]["id"]
            return True, False, id
    else:
        return False, False, 0


def old(token, cookie, id, address):
    url = 'http://{0}/open/envs'.format(address)
    headers = {'Authorization': 'Bearer {0}'.format(
        token), 'Content-Type': 'application/json'}
    data = json.dumps({"name": "JD_COOKIE", "value": cookie, "id": id})
    res = s.put(url=url, headers=headers, data=data)
    if res.status_code == 200:  # 判断 HTTP返回状态码
        r = enbleck(token, id, address)
        if r:
            return True
        else:
            return False
    else:
        return False


def enbleck(token, id, address):
    url = 'http://{0}/open/envs/enable'.format(address)
    headers = {'Authorization': 'Bearer {0}'.format(
        token), 'Content-Type': 'application/json'}
    data = json.dumps(["{0}".format(id)])
    res = s.put(url=url, headers=headers, data=data)
    if res.status_code == 200:  # 判断 HTTP返回状态码
        return True
    else:
        return False


def new(token, cookie, address):
    url = 'http://{0}/open/envs'.format(address)
    headers = {'Authorization': 'Bearer {0}'.format(
        token), 'Content-Type': 'application/json'}
    datas = json.dumps([{"name": "JD_COOKIE", "value": cookie}])
    res = s.post(url=url, headers=headers, data=datas)
    if res.status_code == 200:  # 判断 HTTP返回状态码
        return True
    else:
        return False
