# -*- coding=utf8 -*-
from django.shortcuts import render,HttpResponse,redirect
from django.http.response import JsonResponse
from  zhifu import models
from django.db.models import Q
from django.db import transaction
import  requests

APPID = "wx527e7487e390ed3e"   # 小程序ID
SECRET = "4f1ea8c2187e2f4194b19e9728436af1"
MCHID = "1532076961"      # 商户号
KEY = "58e1554d2378be8590a53d438ebb0f11"        #商户平台密钥key
NOTIFY_URL = "http://127.0.0.1:8000/WeChatPayment/payback"  # 统一下单后微信回调地址

# 证书路径
WX_CERT_PATH = "static/certificate/apiclient_cert.pem"
WX_KEY_PATH = "static/certificate/apiclient_key.pem"


#获取opend
def GetOpendid(request):
    code = request.GET.get("code")
    url_path = "https://api.weixin.qq.com/sns/jscode2session"
    url = url_path+"?appid="+APPID+"&secret="+SECRET+"&js_code="+code+"&grant_type=authorization_code"
    r = requests.get(url)
    session_key = r.json()['session_key']
    openid = r.json()['openid']

    data = {}
    data['session_key'] = session_key
    data['openid'] = openid
    return JsonResponse(data)



#统一下单
import hashlib
import xmltodict
import time
import random
import string

# 生成nonce_str
def generate_randomStr():
    return ''.join(random.sample(string.ascii_letters + string.digits, 32))

# 生成签名
def generate_sign(param):
    stringA = ''

    ks = sorted(param.keys())
    # 参数排序
    for k in ks:
        stringA += k + "=" + str(param[k]) + "&"
    # 拼接商户KEY
    stringSignTemp = stringA + "key=" + KEY
    # md5加密
    hash_md5 = hashlib.md5(stringSignTemp.encode('utf8'))
    sign = hash_md5.hexdigest().upper()
    return sign


# 发送xml请求
def send_xml_request(url, param):
    # dict 2 xml
    param = {'root': param}
    xml = xmltodict.unparse(param)

    response = requests.post(url, data=xml.encode('utf-8'), headers={'Content-Type': 'text/xml'})
    # xml 2 dict
    msg = response.text
    xmlmsg = xmltodict.parse(msg)
    return xmlmsg



# 统一下单
def generate_bill(request):
    OrderNumber = request.GET.get("OrderNumber")
    Openid = request.GET.get("Openid")
    TotalFee = request.GET.get("TotalFee")
    url = "https://api.mch.weixin.qq.com/pay/unifiedorder"
    nonce_str = generate_randomStr()  # 订单中加nonce_str字段记录（回调判断使用）
    out_trade_no = OrderNumber  # 支付单号，只能使用一次，不可重复支付
    data = {}

    # 1. 参数
    param = {
        "appid": APPID,
        "mch_id": MCHID,  # 商户号
        "nonce_str": nonce_str,  # 随机字符串
        "body": 'test',  # 支付说明
        "out_trade_no": out_trade_no,  # 自己生成的订单号
        "total_fee": TotalFee,     #商品费用
        "spbill_create_ip": '127.0.0.1',  # 发起统一下单的ip
        "notify_url": NOTIFY_URL,
        "trade_type": 'JSAPI',  # 小程序写JSAPI
        "openid": Openid,
    }
    # 2. 统一下单签名
    sign = generate_sign(param)
    param["sign"] = sign  # 加入签名
    # 3. 调用接口
    xmlmsg = send_xml_request(url, param)
    # 4. 获取prepay_id
    if xmlmsg['xml']['return_code'] == 'SUCCESS':
        if xmlmsg['xml']['result_code'] == 'SUCCESS':
            prepay_id = xmlmsg['xml']['prepay_id']
            # 时间戳
            timeStamp = str(int(time.time()))
            # 5. 根据文档，六个参数，否则app提示签名验证失败，https://pay.weixin.qq.com/wiki/doc/api/app/app.php?chapter=9_12
            data = {
                "appId": APPID,
                "package": "prepay_id="+prepay_id,
                "nonceStr": nonce_str,
                "timeStamp": timeStamp,
                "signType":"MD5"
            }# 6. paySign签名
            paySign = generate_sign(data)
            data["paySign"] = paySign  # 加入签名
            # 7. 传给前端的签名后的参数
            return JsonResponse(data)



#支付回调
import xmltodict
from django.http import HttpResponse
def payback(request):
    msg = request.body.decode('utf-8')
    xmlmsg = xmltodict.parse(msg)

    return_code = xmlmsg['xml']['return_code']

    if return_code == 'FAIL':
        # 官方发出错误
        return HttpResponse("""<xml><return_code><![CDATA[FAIL]]></return_code>
                                    <return_msg><![CDATA[Signature_Error]]></return_msg></xml>""",
                            content_type='text/xml', status=200)
    elif return_code == 'SUCCESS' :
        # 拿到这次支付的订单号
        out_trade_no = xmlmsg['xml']['out_trade_no']
        #order = Order.objects.get(out_trade_no=out_trade_no)
        # if xmlmsg['xml']['nonce_str'] != order.nonce_str:
        #     # 随机字符串不一致
        #     return HttpResponse("""<xml><return_code><![CDATA[FAIL]]></return_code>
        #                                             <return_msg><![CDATA[Signature_Error]]></return_msg></xml>""",
        #                         content_type='text/xml', status=200)

            # 根据需要处理业务逻辑

        return HttpResponse("""<xml><return_code><![CDATA[SUCCESS]]></return_code>
                                    <return_msg><![CDATA[OK]]></return_msg></xml>""",
                                content_type='text/xml', status=200)





#体现  发送携带证书的xml请求
def send_cert_request(url, param):
    # dict 2 xml
    param = {'root': param}
    xml = xmltodict.unparse(param)

    response = requests.post(url, data=xml.encode('utf-8'),
                             headers={'Content-Type': 'text/xml'},
                             cert=(WX_CERT_PATH, WX_KEY_PATH))
    # xml 2 dict
    msg = response.text
    xmlmsg = xmltodict.parse(msg)

    return xmlmsg



#体现
def withdraw(request):
    Opneid = request.GET.get("Opneid")
    withdraw_trade_no = request.GET.get("withdraw_trade_no")
    withdraw_value = request.GET.get("withdraw_value")
    url = "https://api.mch.weixin.qq.com/mmpaymkttransfers/promotion/transfers"
    param = {
        "mch_appid": "wx527e7487e390ed3e",
        # "mch_appid":   #商户账号APPID
        "mchid": MCHID,  # 商户号
        "nonce_str": generate_randomStr(),  # 随机字符串
        "partner_trade_no": "74566876898",
        # "partner_trade_no": withdraw_trade_no,  #商户订单号
        "openid": "oNbql5OEuAYLujrCmSOmpIWIjQMY",  # 获取openid见obtain_openid_demo.py
        "check_name": "NO_CHECK",
        "amount": 1,
        # "amount": withdraw_value,  # 提现金额，单位为分
        "desc": "工钱体现到账",  # 提现说明
        "spbill_create_ip": "127.0.0.1",  # 发起提现的ip
    }
    sign = generate_sign(param)
    param["sign"] = sign
    # 携带证书
    xmlmsg = send_cert_request(url, param)

    print(xmlmsg)

    if xmlmsg['xml']['return_code'] == 'SUCCESS' and xmlmsg['xml']['result_code'] == 'SUCCESS':

        return  JsonResponse(xmlmsg)


    return JsonResponse(xmlmsg)