# -*- coding: utf-8 -*- 

import urllib2

def getWeather():
  pre_url = "http://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&ie=utf8&query=%EB%82%A0%EC%94%A8+"+urllib2.quote(getLocation())
  print pre_url
  req = urllib2.Request(pre_url, headers={'User-Agent': 'Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)'})
  #url = urllib2.quote(pre_url, '/:')
  #print url
  page = urllib2.urlopen(req)
  text = page.read()
	
  data = {}
  print text.split('c_body')[1].split('tldw_tbl')[0]
  data['now_temp'] = text.split('c_body')[1].split('tldw_tbl')[0].split('<em>')[1].split('<span>')[0]
  print data['now_temp']
  data['now_weather'] = text.split('현재,1시간 예보')[1].split('3시간 예보')[0].split('<strong>')[1].split('</strong>')[0]
  data['one_later'] = text.split('현재,1시간 예보')[1].split('3시간 예보')[0].split('<em>')[2].split('<p>')[1].split('</p>')[0]
  data['two_later'] = text.split('현재,1시간 예보')[1].split('3시간 예보')[0].split('<em>')[3].split('<p>')[1].split('</p>')[0]
  
  return data
  
def getLocation():
  page = urllib2.urlopen("https://169.254.1.89:8000/myapp/default/project_tablebar_setting")
  text = page.read()
	
  set_localation = text.split('설정된 지역 : ')[1].split('</td>')[0]
  
  return set_localation
