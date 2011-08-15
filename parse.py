#!/usr/bin/python

from urllib2 import urlopen, URLError

class Parse:
	"""Parser class..Call the corresponding funtions for corresponding commands"""
	def __init__(self):
		pass
		
	def FSFnewsCommand(self):
		"Returns a list of headlines is fsf.org/news."			 
		from htmlparser import FSFHeadLineParser
		obj = FSFHeadLineParser()
		try :
			obj.feed(urlopen('http://www.fsf.org/news/').read())
		except URLError, error:
			print "Unable to open requested page due to %s" % error
			return None
		return obj.headlines
		
	def SDotnewsCommand(self):
		"Returns a list of headlines in slashdot.org ."
		from htmlparser import SDotHeadLineParser
		obj = SDotHeadLineParser()
		try:
			obj.feed(urlopen('http://rss.slashdot.org/Slashdot/slashdot').read())
		except URLError, error:
			print "Unable to open the requested page due to %s" % error	
			return None
		return obj.headlines
		
	def WeatherFinder(self, city):
		"Returns a list of weather conditions in the city passed"
		from xmlparser import WeatherFinder
		from xml.sax import make_parser
		from xml.sax.handler import ContentHandler
		try :
			response = urlopen('http://www.google.com/ig/api?weather='+city)
		except URLError:
			return None 
		obj = WeatherFinder()
		parser = make_parser()
		parser.setContentHandler(obj)
		parser.parse(response)
		return obj.weather_list    	
	
	def GetFortune(self):
		from commands import getoutput
		fortune = getoutput('fortune 100% fortunes -s')
		return fortune 
	
	def GetLoveQuote(self):
		from commands import getoutput
		quote = getoutput('fortune 100% love -s')
		return quote
