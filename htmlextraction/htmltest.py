import urllib2

if __name__ == '__main__':
	page = urllib2.urlopen("http://www.example.com")
	text = page.read()
	print text

	where = text.find("This domain is")

	print where
	print text[where:where+10]

