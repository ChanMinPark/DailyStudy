import time

def getWeek():
  now = time.localtime()
  
  today = now.tm_mday
  wday = now.tm_wday
  
  line_1 = returnMonth(now.tm_mon) + "#Sun Mon The Wed Thu Fri Sat "
  line_2 = "%02d #"%(now.tm_mday)
  
  temp = wday
  while temp>=0


def returnWday(a):
  if a == 0:
    return "Sun"
  elif a == 1:
    return "Mon"
  elif a == 2:
    return "Tue"
  elif a == 3:
    return "Wed"
  elif a == 4:
    return "Thu"
  elif a == 5:
    return "Fri"
  elif a == 6:
    return "Sat"


def returnMonth(a):
  if a == 1:
    return "Jan"
  elif a == 2:
    return "Feb"
  elif a == 3:
    return "Mar"
  elif a == 4:
    return "Apr"
  elif a == 5:
    return "May"
  elif a == 6:
    return "Jun"
  elif a == 7:
    return "Jul"
  elif a == 8:
    return "Aug"
  elif a == 9:
    return "Sep"
  elif a == 10:
    return "Oct"
  elif a == 11:
    return "Nov"
  elif a == 12:
    return "Dec"

  #(작성중...)
