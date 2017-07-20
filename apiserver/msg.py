# -*- coding: utf-8 -*-
import sys
from aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest
from aliyunsdkdysmsapi.request.v20170525 import QuerySendDetailsRequest
from aliyunsdkcore.client import AcsClient
import uuid
import random

"""
短信业务调用接口示例，版本号：v20170525

Created on 2017-06-12

"""

reload(sys)
sys.setdefaultencoding('utf8')

REGION = "cn-hangzhou"
# ACCESS_KEY_ID/ACCESS_KEY_SECRET 根据实际申请的账号信息进行替换
ACCESS_KEY_ID = "LTAIJvV4lyXsZe6U"
ACCESS_KEY_SECRET = "XOO93j3sLzLH03tNfwyLObmSznTHxV"

acs_client = AcsClient(ACCESS_KEY_ID, ACCESS_KEY_SECRET, REGION)


def send_sms(phone_numbers, sign_name, template_code, template_param=None):
    smsRequest = SendSmsRequest.SendSmsRequest()
    # 申请的短信模板编码,必填
    smsRequest.set_TemplateCode(template_code)

    # 短信模板变量参数
    if template_param is not None:
        smsRequest.set_TemplateParam(template_param)

    # 设置业务请求流水号，必填。
    business_id = uuid.uuid1()
    smsRequest.set_OutId(business_id)

    # 短信签名
    smsRequest.set_SignName(sign_name);

    # 短信发送的号码列表，必填。
    smsRequest.set_PhoneNumbers(phone_numbers)

    # 调用短信发送接口，返回json
    smsResponse = acs_client.do_action_with_exception(smsRequest)

    # TODO 业务处理

    return smsResponse


def generate_verification_code():
    ''' 随机生成6位的验证码 '''
    code_list = []

    # 0-9数字
    for i in range(10):
        code_list.append(str(i))
    
    # 从list中随机获取6个元素，作为一个片断返回
    myslice = random.sample(code_list, 6)
    
    # list to string
    verification_code = ''.join(myslice)
    
    return verification_code