# -*- coding: utf-8 -*-

import httplib
import time
import json

conn = httplib.HTTPConnection("10.255.255.65")

#Hue 켜기
def hue_on(light):
	conn.request("PUT","/api/newdeveloper/lights/"+str(light)+"/state", '{"on":true}')
	response = conn.getresponse()
	data = response.read()

	if data[3:10] is "success":
		return True
	else:
		return False


#Hue 끄기
def hue_off(light):
	conn.request("PUT","/api/newdeveloper/lights/"+str(light)+"/state", '{"on":false}')
	response = conn.getresponse()
	data = response.read()

	if data[3:10] is "success":
		return True
	else:
		return False

#Hue의 saturation변화 0~255 0 흰색
def hue_putSat(light, sat):
	saturation = {}
	saturation['sat'] = sat
	saturation = json.dumps(saturation)

	conn.request("PUT","/api/newdeveloper/lights/"+str(light)+"/state", saturation)
	response = conn.getresponse()
	data = response.read()

	if data[3:10] is "success":
		return True
	else:
		return False


#Hue의 밝기 변화 0~255 
def hue_putBri(light, bri):
	bright = {}
	bright['bri'] = bri
	bright = json.dumps(bright)

	conn.request("PUT","/api/newdeveloper/lights/"+str(light)+"/state", bright)
	response = conn.getresponse()
	data = response.read()

	if data[3:10] is "success":
		return True
	else:
		return False


#Hue의 hue값 변화  0~65535
def hue_putHue(light, hue):
	color = {}
	color['hue'] = hue
	color = json.dumps(color)

	conn.request("PUT","/api/newdeveloper/lights/"+str(light)+"/state", color)
	response = conn.getresponse()
	data = response.read()

	if data[3:10] is "success":
		return True
	else:
		return False

def hue_alert(light, mode):
	halert={}
	if mode is 0:
		halert['alert']="none"
	elif mode is 1:
		halert['alert']="select"
	elif mode is 2:
		halert['alert']="lselect"
	halert = json.dumps(halert)

	conn.request("PUT","/api/newdeveloper/lights/"+str(light)+"/state", halert)
	response = conn.getresponse()
	data = response.read()

	if data[3:10] is "success":
		return True
	else:
		return False
		
def hue_effect(light, mode):
	heffect={}
	if mode is 0:
		heffect['effect']="none"
	elif mode is 1:
		heffect['effect']="colorloop"
	heffect = json.dumps(heffect)

	conn.request("PUT","/api/newdeveloper/lights/"+str(light)+"/state", heffect)
	response = conn.getresponse()
	data = response.read()

	if data[3:10] is "success":
		return True
	else:
		return False

#Hue 상태 가져오기 json객체 작성중
def getState(light):
	conn.request("GET","/api/newdeveloper/lights/"+str(light))
	response = conn.getresponse()
	raw_data = json.loads(response.read())
	data = raw_data

	ret =[]
	ret.append(str(data['name']))
	ret.append(str(data['state']['on']))
	ret.append(str(data['state']['bri']))
	ret.append(str(data['state']['hue']))
	ret.append(str(data['state']['sat']))
	ret.append(str(data['state']['alert']))
	ret.append(str(data['state']['effect']))
	
	return ret
