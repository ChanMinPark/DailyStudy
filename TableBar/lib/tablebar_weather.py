# -*- coding: utf-8 -*- 

import urllib2

def getWeather():
  pre_url = "http://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&ie=utf8&query=%EB%82%A0%EC%94%A8+"+urllib2.quote("날씨+"+getLocation())
  print pre_url
  req = urllib2.Request(pre_url, headers={'User-Agent' : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.30 (KHTML, like Gecko) Ubuntu/11.04 Chromium/12.0.742.112 Chrome/12.0.742.112 Safari/534.30"})
  #url = urllib2.quote(pre_url, '/:')
  #print url
  page = urllib2.urlopen(req)
  text = page.read()
	
  data = {}
  data['now_temp'] = text.split('현재,1시간 예보')[1].split('3시간 예보')[0].split('<em>')[1].split('<span>')[0]
  data['now_weather'] = text.split('현재,1시간 예보')[1].split('3시간 예보')[0].split('<strong>')[1].split('</strong>')[0]
  data['one_later'] = text.split('현재,1시간 예보')[1].split('3시간 예보')[0].split('<em>')[2].split('<p>')[1].split('</p>')[0]
  data['two_later'] = text.split('현재,1시간 예보')[1].split('3시간 예보')[0].split('<em>')[3].split('<p>')[1].split('</p>')[0]
  
  return data
  
def getLocation():
  page = urllib2.urlopen("https://169.254.1.89:8000/myapp/default/project_tablebar_setting")
  text = page.read()
	
  set_localation = text.split('설정된 지역 : ')[1].split('</td>')[0]
  
  return set_localation
