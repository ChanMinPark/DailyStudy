import urllib2

def getBaseBallRank():
	page = urllib2.urlopen("http://sports.news.naver.com/record/index.nhn?uCategory=kbaseball&category=kbo")
	text = page.read()
	#print text
	
	teamrecord = text.split('var jsonTeamRecord')[1].split('var teamCount')[0].split(':[')[1].split('},{')
	
	for record in teamrecord
		print record
		print " "

if __name__ == '__main__':
	getBaseBallRank()
	
