import time
  
def getData():
  now = time.localtime()
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
    
  r_date = "%04d-%02d-%02d-%s"%(now.tm_year, now.tm_mon, now.tm_mday, wday)
  return r_date

def getTime():
  now = time.localtime()
  r_time = "%02d:%02d:%02d"%(now.tm_hour, now.tm_min, now.tm_sec)
  return r_time
