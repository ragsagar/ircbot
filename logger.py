#!/usr/bin/python

#Module to log the messages passed from connect.py
import time

class Log:
	"""Class to log the message"""
	
	def __init__(self, channel):
		"the filename is the combination of channel name and time at which we join the channel"	
		filename = channel+'_'+'_'.join(time.ctime().split())+'.log'
		path = 'logs/'+filename
		try :
			self.log_file = file(path, "w")
		except IOError, error :
			print "Problem while writing to '%s', %s "	% (path,error)
			self.log_file = file(filename, "w")

	def log(self, message):
		"copy the message to the file object"
		message='['+time.ctime()+'] '+message
		print >> self.log_file, message
		
		
	
