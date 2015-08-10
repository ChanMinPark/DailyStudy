import time
import urllib2

def getWeek():
  now = time.localtime()
  
  today = now.tm_mday
  wday = now.tm_wday #Mon:0 ~ Sun:6
  
  line_1 = returnMonth(now.tm_mon) + "#Mon The Wed Thu Fri Sat Sun "
  line_2 = "%02d #"%(today)
  
  weekdays = [0,0,0,0,0,0,0]
  weekdays[wday] = today
  
  temp = wday
  while temp > 0:
    temp = temp - 1
    weekdays[temp] = weekdays[temp+1] - 1
    
  temp = wday
  while temp < 6:
    temp = temp + 1
    weekdays[temp] = weekdays[temp-1] + 1
  
  
  sche_day = getSchedules()
  
  for dd in weekdays:
    if (now.tm_mon-1) in [1,3,5,7,8,10,12]:
      if dd < 1:
        dd = 31-dd
    else:
      if dd < 1:
        dd = 30-dd
        
    if now.tm_mon in [1,3,5,7,8,10,12]:
      if dd > 31:
        dd = dd-31
    else:
      if dd > 30:
        dd = dd-30
    
    if dd in sche_day:
      line_2 = line_2 + "*%02d "%(dd)
    else:
      line_2 = line_2 + " %02d "%(dd)
  
  lines = ["",""]
  lines[0] = line_1
  lines[1] = line_2
  
  return lines

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

def getSchedules():
  page = urllib2.urlopen("https://169.254.1.89:8000/myapp/default/project_tablebar_setting")
	text = page.read()
	
	schedule_record = text.split('<Table')[1].split('</th>')[6].split('</Table>')[0].split('/tr')
	
	schedules = []
	
	for record in schedule_record:
	  data = {}
	  data['date'] = record.split('<td>')[1].split('</td>')[0]
	  data['location'] = record.split('<td>')[2].split('</td>')[0]
	  data['content'] = record.split('<td>')[3].split('</td>')[0]
	  schedules.append(data)
	  print data
	
	schedules_day = []
	for i in schedules:
	  schedules_day.append(i['date'])
	
	return schedules_day
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
