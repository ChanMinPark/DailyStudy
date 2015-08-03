import time

def getWeek():
  now = time.localtime()
  
  today = now.tm_mday
  wday = now.tm_wday
  
  #(작성중...)
