# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from apiserver.msg import send_sms, generate_verification_code
# Create your views here.
from django.http import HttpResponse
from apiserver.models import msgcode
import datetime
from django.utils import timezone
import json

def sendMsg(request, phone):
	code = generate_verification_code()
	params = "{\"code\":\"" + code + "\"}"
	try:
		getuser = msgcode.objects.get(phone = phone)
		getuser.code = code
	except msgcode.DoesNotExist:
		getuser = msgcode(phone = phone, code = code)
	getuser.save()
	getuser = msgcode.objects.get(phone = phone)
	
	#{"Message":"OK","RequestId":"C61EF470-2E51-43C8-A19B-1E84663B5073","BizId":"108879212695^1111912814509","Code":"OK"}
	res = send_sms(phone, "链上未来", "SMS_77410045", params)
	return HttpResponse(res, content_type = "application/json")


def verifyCode(request, phone, code):
	result = True
	time = timezone.now() - datetime.timedelta(minutes = 30)
	print time
	try:
		getuser = msgcode.objects.get(phone = phone)
		if (time > getuser.time) or (getuser.code != code):
			result = False
	except msgcode.DoesNotExist:
		result = False
	json_data = {}
	json_data['result'] = result
	return HttpResponse(json.dumps(json_data), content_type = "application/json")