import time

def getNow():
  now = time.localtime()
  return now
  
def getData():
  now = getNow()
  if now.tm_wday == 0:
    wday = "월"
  elif now.tm_wday == 1:
    wday = "화"
  elif now.tm_wday == 2:
    wday = "수"
  elif now.tm_wday == 3:
    wday = "목"
  elif now.tm_wday == 4:
    wday = "금"
  elif now.tm_wday == 5:
    wday = "토"
  elif now.tm_wday == 6:
    wday = "일"
    
  r_date = "%d년 %d월 %d일 %s요일"%(now.tm_year, now.tm_mon, now.tm_mday, wday)
  return r_date

def getTime():
  now = getNow()
  r_time = "%d시 %d분 %d초"%(now.tm_hour, now.tm_min, now.tm_sec)
  return r_time
