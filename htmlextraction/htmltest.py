import urllib2

if __name__ == '__main__':
	#page = urllib2.urlopen("http://www.example.com")
	page = urllib2.urlopen("http://sports.news.naver.com/record/index.nhn?uCategory=kbaseball&category=kbo")
	text = page.read()
	print text

	#where = text.find("This domain is")

	#print where
	#print text[where:where+10]

