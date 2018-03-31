# -*- coding:utf-8 -*-
import json
from flask import Flask,request,make_response,render_template
import hashlib
import xmltodict
import time
import urllib2
from config import Config
from . import wechat_blue

APPID = Config.APPID
APPSECRET = Config.APPSECRET
TOKEN = Config.TOKEN



class AccessToken(object):
    _access_token ={
        'access_token': '',
        'create_time': int(time.time()),
        'expires_in': 7000
    }
    @classmethod
    def get_access_token(cls):
        acs = cls._access_token
        nowtime = int(time.time()) - acs.get('create_time')
        if not acs.get('access_token') or nowtime - acs.get('expires_in') > 200:
            url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (APPID,APPSECRET)
            resp = urllib2.urlopen(url).read()
            response = json.loads(resp)
            if "errcode" in response:
                raise Exception(response.get('errmsg'))
            cls._access_token['access_token'] = response.get('access_token')
            cls._access_token['expires_in'] = response.get('expires_in')
            cls._access_token['create_time'] = time.time()
            # cls._access_token = {
            #     'access_token': response.get('access_token'),
            #     'create_time': int(time.time()),
            #     'expire_in': response.get( 'expire_in')
            # }

        return acs.get('access_token')





@wechat_blue.route('/wechat',methods=['GET','POST'])
def wechat():
    # 获取参数
    data = request.args
    signature = data.get('signature')
    timestamp = data.get('timestamp')
    nonce = data.get('nonce')
    echostr = data.get('echostr')
    # 对参数进行字典排序，拼接字符串
    temp = [timestamp, nonce, TOKEN]
    temp.sort()
    temp_str = ''.join(temp)
    # 加密
    if hashlib.sha1(temp_str).hexdigest() == signature:

        if request.method == 'POST':
            xml = request.data
            request_str = xmltodict.parse(xml).get('xml')
            if 'text' == request_str.get('MsgType'):
                resp = {
                    'ToUserName': request_str.get('FromUserName'),
                    'FromUserName': request_str.get('ToUserName'),
                    'CreateTime': int(time.time()),
                    'MsgType': 'text',
                    'Content': request_str.get('Content')
                }
                xml = xmltodict.unparse({'xml': resp})
                return xml
            elif request_str.get('MsgType') == 'voice':
                recognition = request_str.get('Recognition',u'无法识别')
                resp = {
                    'ToUserName': request_str.get('FromUserName', ''),
                    'FromUserName': request_str.get('ToUserName', ''),
                    'CreateTime': int(time.time()),
                    'MsgType': 'text',
                    'Content': recognition
                }
                xml = xmltodict.unparse({'xml': resp})
                return xml
            elif request_str.get('MsgType') == 'event':
                if request_str.get('Event') == 'subscribe':
                    resp = {
                        'ToUserName': request_str.get('FromUserName', ''),
                        'FromUserName': request_str.get('ToUserName', ''),
                        'CreateTime': int(time.time()),
                        'MsgType': 'text',
                         "Content":u"感谢您的关注！"
                    }
                    if None != request_str.get("EventKey"):
                        resp["Content"] += u"场景值:"
                        resp["Content"] += request_str.get("EventKey")[8:]
                    elif "SCAN" == request_str.get("Event"):
                        resp = {
                            "ToUserName": request_str.get("FromUserName", ""),
                            "FromUserName": request_str.get("ToUserName", ""),
                            "CreateTime": int(time.time()),
                            "MsgType": "text",
                            "Content": u"您扫描的场景值为：%s" % request_str.get("EventKey")
                        }
                    else:
                        resp = resp
                    xml = xmltodict.unparse({'xml': resp})
                else: xml ==''
                return xml
            else:
                resp = {
                    'ToUserName': request_str.get('FromUserName', ''),
                    'FromUserName': request_str.get('ToUserName', ''),
                    'CreateTime': int(time.time()),
                    'MsgType': 'text',
                    'Content': 'THANKS'
                }
                xml = xmltodict.unparse({'xml': resp})
                return xml

        return make_response(echostr)
    return ''



@wechat_blue.route('/<int:scene_id>')
def get_ticket(scene_id):
    access_token = AccessToken.get_access_token()
    url = 'https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token=%s' % access_token
    # 构造请求参数，设置scene_id
    req_body = {
        'expire_seconds': 800000,
        'action_name': 'QR_SCENE',
        'action_info': {'scene': {'scene_id': scene_id}}
    }
    #将字典转成STR
    req_data = json.dumps(req_body)
    # # 构建请求对象
    # req = urllib2.Request(url,data=req_data)
    #获取响应数据
    resp = urllib2.urlopen(url,data=req_data).read()

    if 'errcode' in resp:
        return 'error'

    response = json.loads(resp)
    ticket = response.get('ticket')
    return '<img src="https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket=%s">' % ticket
