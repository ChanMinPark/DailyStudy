import urllib2

def getBaseBallRank():
	page = urllib2.urlopen("http://sports.news.naver.com/record/index.nhn?uCategory=kbaseball&category=kbo")
	text = page.read()
	#print text
	
	print text.split('var jsonTeamRecord')[1].split('var teamCount')[0]

if __name__ == '__main__':
	getBaseBallRank()
	
