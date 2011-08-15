#!/usr/bin/python

from xml.sax import make_parser
from xml.sax.handler import ContentHandler
from time import ctime

class WeatherFinder(ContentHandler):
	"""the main class"""
	def __init__(self):
		self.weather_list = []
		self.go_on = False
		
	def startElement(self, tag, attrs):
		"handles the opening tags"
		if tag == 'current_conditions':
			self.go_on = True
		if self.go_on :
			if tag == 'condition' :
				self.weather_list.append('Condition: '+attrs.get('data',""))
			elif tag == 'humidity' :
				self.weather_list.append(attrs.get('data',""))			
			elif tag == 'temp_c' :
				self.weather_list.append('Temperature:'+attrs.get('data',"")+'C')
			elif tag == 'wind_condition' :
				self.weather_list.append(attrs.get('data',""))
		return
		
	def endElement(self, tag):
		"handles closing tags"
		if tag == 'current_conditions':
			self.go_on = False
			
#from mechanize import Browser
#br=Browser()
		
#parser = make_parser()
#res = br.open('http://www.google.com/ig/api?weather=palghat')
#obj = WeatherFinder()
#parser.setContentHandler(obj)
#parser.parse(res) 	
#for i in obj.weather_list:
#	print i

