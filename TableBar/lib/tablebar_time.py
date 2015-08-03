import time

def getNow():
  now = time.localtime()
  return now
  
def getData():
  now = getNow()
  if now.tm_wday == 0:
    wday = "Mon"
  elif now.tm_wday == 1:
    wday = "Tue"
  elif now.tm_wday == 2:
    wday = "Wed"
  elif now.tm_wday == 3:
    wday = "Thu"
  elif now.tm_wday == 4:
    wday = "Fri"
  elif now.tm_wday == 5:
    wday = "Sat"
  elif now.tm_wday == 6:
    wday = "Sun"
    
  r_date = "%4d-%2d-%2d-%s"%(now.tm_year, now.tm_mon, now.tm_mday, wday)
  return r_date

def getTime():
  now = getNow()
  r_time = "%2d:%2d:%2d"%(now.tm_hour, now.tm_min, now.tm_sec)
  return r_time