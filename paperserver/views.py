# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
import ipfsapi
import os
import json

ROOT_PATH = '/home/huangjunqin/msgserver/paperserver/'

# Create your views here.
def paperdetect(request, hash):
	api = ipfsapi.connect('127.0.0.1', 5001)
	# {u'Hash': u'QmWRgQyPcg82D9V5rNqnHnRybeYNDZiZjCBvoGEXuTtmhP', u'Name': u'blockchain.pdf'}
	# {u'Hash': u'QmZEymLZZNdKCRc8SrePsMeMoWHRgWbgm18oh8iRY4upfc', u'Name': u'D7051245_flow_toEditor_Content_6_456910.pdf'}
	pdf = api.cat(hash)
	num = len(os.listdir(ROOT_PATH + 'data/pdf/'))
	filename = str(num)
	similarity = 0.0
	fp = open(ROOT_PATH + 'data/pdf/' + filename + '.pdf', 'w+')
	fp.write(pdf)
	fp.close()
	try:
	    os.system("python /usr/local/bin/pdf2txt.py -o {} {}".format(ROOT_PATH + 'data/txt/' + filename + '.txt', ROOT_PATH + 'data/pdf/' + filename + '.pdf'))
	    os.system("python " + ROOT_PATH + "src/preprocess.py {} {} {}".format(ROOT_PATH + 'data/txt/' + filename + '.txt', ROOT_PATH + 'data/stopwords.txt', ROOT_PATH + 'data/word.dict'))
	    for i in xrange(num):
	    	output = os.popen("python " + ROOT_PATH + "src/isSimilar.py {} {} {} {} -c 0.8".format(ROOT_PATH + 'data/txt/' + filename + '.txt', ROOT_PATH + 'data/txt/' + str(i) + '.txt', ROOT_PATH + 'data/stopwords.txt', ROOT_PATH + 'data/word.dict'))
	    	res = output.read()
	    	res = float(res)
	    	if res > similarity:
	    		similarity = res
	except Exception:
	    print "ERROR: ", filename
	json_data = {}
	json_data['similarity'] = similarity
	return HttpResponse(json.dumps(json_data), content_type = "application/json")