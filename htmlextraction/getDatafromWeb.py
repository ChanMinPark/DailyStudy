#  For BaseBall Data
import urllib2
#  For LCD connection
import sys
from lcd import *

#####################################################################################
#########################  For BaseBall Data  #######################################
#####################################################################################
def printTeaminfo(name, info):
	lcd_string('%s' %(name), LCD_LINE_1,2)
	lcd_string('%s' %(info), LCD_LINE_2,1)
	time.sleep(2)
	index = 0
	while index <= (len(info)-16):
		lcd_string('%s' %(info), LCD_LINE_2,1)
		temp_info = info[:1]
		info = info[1:]
		info += temp_info
		time.sleep(1)
		index += 1

def printLCDColor(name):
	if name == "Samsung Lions":
		blueLCDon()
	elif name == "NC Dinos":
		skyeLCDon()
	elif name == "Doosan Bears":
		whiteLCDon()
	elif name == "Nexen Heroes":
		redLCDon()
	elif name == "HanHwa Eagles":
		yellowLCDon()
	elif name == "SK Wyvern":
		skyeLCDon()
	elif name == "Kia Tigers":
		pinkLCDon()
	elif name == "Lotte Giants":
		greenLCDon()
	elif name == "LG Twins":
		redLCDon()
	elif name == "KT Wiz":
		whiteLCDon()
	else:
		whiteLCDon()
#####################################################################################


#####################################################################################
#########################  For BaseBall Data  #######################################
#####################################################################################
def getBaseBallRank():
	page = urllib2.urlopen("http://sports.news.naver.com/record/index.nhn?uCategory=kbaseball&category=kbo")
	text = page.read()
	#print text
	
	teamrecord = text.split('var jsonTeamRecord')[1].split('var teamCount')[0].split(':[{')[1].split('},{')
		
	record_after = []

	for record in teamrecord:
		data = {}
		data['teamName'] = teamName(record.split(',')[3].split(':')[1][1:3])
		data['play'] = record.split(',')[10].split(':')[1]
		data['won'] = record.split(',')[8].split(':')[1]
		data['lost'] = record.split(',')[2].split(':')[1]
		data['drawn'] = record.split(',')[11].split(':')[1]
		data['rank'] = record.split(',')[5].split(':')[1]
		record_after.append(data)
		
	for record in record_after:
		print "Team Name : %s" %(record['teamName'])
		name_text = record['teamName']
		printLCDColor(name_text)
		if record['rank'] == "1":
			print "%sst (%swin-%slost-%sdrawn)" %(record['rank'],record['won'],record['lost'],record['drawn'])
			info_text = record['rank']+"st ("+record['won']+"win-"+record['lost']+"lost-"+record['drawn']+"drawn)"
		elif (record['rank'] == "2")|(record['rank'] == "3"):
			print "%snd (%swin-%slost-%sdrawn)" %(record['rank'],record['won'],record['lost'],record['drawn'])
			info_text = record['rank']+"nd ("+record['won']+"win-"+record['lost']+"lost-"+record['drawn']+"drawn)"
		else:
			print "%sth (%swin-%slost-%sdrawn)" %(record['rank'],record['won'],record['lost'],record['drawn'])
			info_text = record['rank']+"th ("+record['won']+"win-"+record['lost']+"lost-"+record['drawn']+"drawn)"
		printTeaminfo(name_text, info_text)
		time.sleep(1)

def teamName(teamcode):
	if teamcode == "SS":
		return "Samsung Lions"
	elif teamcode == "NC":
		return "NC Dinos"
	elif teamcode == "OB":
		return "Doosan Bears"
	elif teamcode == "WO":
		return "Nexen Heroes"
	elif teamcode == "HH":
		return "HanHwa Eagles"
	elif teamcode == "SK":
		return "SK Wyverns"
	elif teamcode == "HT":
		return "Kia Tigers"
	elif teamcode == "LT":
		return "Lotte Giants"
	elif teamcode == "LG":
		return "LG Twins"
	elif teamcode == "KT":
		return "KT Wiz"
	else:
		return "default"
#####################################################################################

if __name__ == '__main__':
	lcd_init()
	try:
		while True:
			getBaseBallRank()
	except KeyboardInterrupt:
		pass
	finally:
		lcd_byte(0x01, LCD_CMD)
		lcd_string("Goodbye!",LCD_LINE_1,2)
		GPIO.cleanup()
	
