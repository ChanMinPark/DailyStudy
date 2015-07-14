#  For BaseBall Data
import urllib2
#  For LCD connection
import sys
from lcd import *
#  For Audio play
import pygame

#####################################################################################
#########################  For Audio play  ##########################################
#####################################################################################
def playTeamSong(name):
	try:
		if pygame.mixer.get_busy() == True:
			pygame.mixer.stop()
		#pygame.mixer.init()
		if name == "Samsung Lions":
			pygame.mixer.music.load("samsung_song.mp3")
		elif name == "NC Dinos":
			pygame.mixer.music.load("nc_song.mp3")
		elif name == "Doosan Bears":
			pygame.mixer.music.load("doosan_song.mp3")
		elif name == "Nexen Heroes":
			pygame.mixer.music.load("nexen_song.mp3")
		elif name == "HanHwa Eagles":
			pygame.mixer.music.load("samsung_song.mp3")
		elif name == "SK Wyvern":
			pygame.mixer.music.load("samsung_song.mp3")
		elif name == "Kia Tigers":
			pygame.mixer.music.load("kia_song.mp3")
		elif name == "Lotte Giants":
			pygame.mixer.music.load("samsung_song.mp3")
		elif name == "LG Twins":
			pygame.mixer.music.load("samsung_song.mp3")
		elif name == "KT Wiz":
			pygame.mixer.music.load("samsung_song.mp3")
		else:
			pygame.mixer.music.load("samsung_song.mp3")
		pygame.mixer.music.set_volume(0.2)
		pygame.mixer.music.play()
		#pygame.mixer.quit()
	except KeyboardInterrupt:
		pass
	
#####################################################################################

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
		playTeamSong(name_text)
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
	pygame.mixer.init()
	try:
		while True:
			getBaseBallRank()
	except KeyboardInterrupt:
		pass
	finally:
		pygame.mixer.quit()
		lcd_byte(0x01, LCD_CMD)
		lcd_string("Goodbye!",LCD_LINE_1,2)
		GPIO.cleanup()
	
