#Author : ChanMin Park, https://github.com/ChanMinPark
#Abstract : Simple code for getting a web page using urllib2 module

import urllib2

if __name__ == '__main__':
	page = urllib2.urlopen("http://www.example.com")
	text = page.read()
	print text
	
	# If you want to know the location of certain text, use below code.
	#where = text.find("This domain is")
	#print where
	#print text[where:where+10]

