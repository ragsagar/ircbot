#!/usr/bin/python
from mechanize import Browser
from HTMLParser import HTMLParser

class FSFHeadLineParser(HTMLParser):
	"""find the news headlines in fsf.org/news and creates a list of headlines"""
	def __init__(self):
		self.in_header = False
		self.in_headline = False
		self.headlines = []
		HTMLParser.__init__(self)
		
	def handle_starttag(self, tag, attrs):
		if tag == 'h2' :
			self.in_header = True 
		if tag == 'a' and self.in_header:
			self.in_headline = True
			
	def handle_endtag(self, tag):
		if tag == 'h2' :
			self.in_header = False
		if tag == 'a' :
			self.in_headline = False
			
	def handle_data(self, data):
		if self.in_headline :
			self.headlines.append(data)

class SDotHeadLineParser(HTMLParser):
	""" Find the news headlines in slashdot and creates a list of headlines"""
	def __init__(self):
		self.in_header = False
		self.in_headline = False
		self.headlines = []
		HTMLParser.__init__(self)
	
	def handle_starttag(self, tag, attrs):
		if tag == 'item':
			self.in_header = True
		if tag == 'title' and self.in_header:
			self.in_headline = True
			
	def handle_endtag(self, tag):
		if tag == 'item':
			self.in_header = False
		if tag == 'title':
			self.in_headline = False
			
	def handle_data(self, data):
		if self.in_headline :
			self.headlines.append(data)
									
		
class SDotDescriptionParser(HTMLParser):
	"""To find the description of the news"""
	def __init__(self):
		self.in_header = False
		self.in_description = False
		self.descriptions = []
		HTMLParser.__init__(self)
	
	def handle_starttag(self, tag, attrs):
		if tag == 'item' :
			self.in_header = True
		if tag == 'description' and self.in_header :
			self.in_description = True
			
	def handle_endtag(self, tag):
		if tag == 'item' :
			self.in_header = False
		if tag == 'description' :
			self.in_description = False
	
	def handle_data(self, data):
		if self.in_description and len(data) > 150 :
			self.descriptions.append(data)
			
		
					
class WikipediaParser(HTMLParser):
	"""A class to parse the wikipedia search contents"""
	def __init__(self):
		self.in_header = False
		self.in_description = False
		self.SearchResults = []
		
	def handle_starttag(self, tag, attrs):
		"handles the start tags."
		if tag == 'ul' :
			self.in_header = True
		if tag == 'li' and self.in_header :
			self.in_description = True
	
	def handle_endtag(self, tag):
		"handles the end tags."	
		if tag == 'ul' :
			self.in_header = False
		if tag == 'li' :
			self.in_description = False
	
	def handle_data(self, data):
		"handles the text inside the tags"
		if self.in_description :
			self.SearchResults.append(data)
			
							


#url = 'http://www.google.com/search?q=define%3A+'				
#searchitem = 'phenny'
#searchurl = url+searchitem
#br=Browser()
#response=br.open(searchurl)
#par=WikipediaParser()
#par.feed(response.read())
#for headline in par.SearchResults :
	#print "===================="
	#print headline
#par.close()	
	

			
		
