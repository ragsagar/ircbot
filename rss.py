#!/usr/bin/python

from urllib2 import urlopen
from BeautifulSoup import BeautifulSoup
#import re

def getlist(place='fsf'):
	url = 'http://rss.slashdot.org/Slashdot/slashdot'
	response=urlopen(url)
	txt = response.read()
	soup = BeautifulSoup(txt)
	headers=soup.findAll('description') 
	headlines=[]
	for header in headers:
		header=str(header)
		headlines.append(header)
	return headlines	
	
newslist=getlist()
print newslist[0]	
	
	
	
	
