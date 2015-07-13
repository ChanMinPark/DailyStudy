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
	i = 0
	for record in teamrecord:
		record_after[i] = {}
		record_after[i]['teamName'] = teamName(record.split(',')[3].split(':')[1][1:2])
		record_after[i]['play'] = record.split(',')[10].split(':')[1]
		record_after[i]['won'] = record.split(',')[8].split(':')[1]
		record_after[i]['lost'] = record.split(',')[2].split(':')[1]
		record_after[i]['drawn'] = record.split(',')[11].split(':')[1]
		i++
		
	for record in record_after:
		print record
		print " "

def teamName(teamcode):
	if teamcode is "SS":
		return "Samsung Lions"
	elif teamcode is "NC":
		return "NC Dinos"
	elif teamcode is "OB":
		return "Doosan Bears"
	elif teamcode is "WO":
		return "Nexen Heroes"
	elif teamcode is "HH":
		return "HanHwa Eagles"
	elif teamcode is "SK":
		return "SK Wyverns"
	elif teamcode is "HT":
		return "Kia Tigers"
	elif teamcode is "LT":
		return "Lotte Giants"
	elif teamcode is "LG":
		return "LG Twins"
	elif teamcode is "KT":
		return "KT Wiz"
#####################################################################################

if __name__ == '__main__':
	getBaseBallRank()
	
