import urllib2


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
		print record.split(',')[3].split(':')[1][1:3]
		data = {}
		data['teamName'] = teamName(record.split(',')[3].split(':')[1][1:3])
		data['play'] = record.split(',')[10].split(':')[1]
		data['won'] = record.split(',')[8].split(':')[1]
		data['lost'] = record.split(',')[2].split(':')[1]
		data['drawn'] = record.split(',')[11].split(':')[1]
		record_after.append(data)
		
	for record in record_after:
		print record
		print " "

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
	getBaseBallRank()
	
