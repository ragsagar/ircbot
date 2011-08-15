#!/usr/bin/python

import socket,sys,parse
from logger import Log

#TODO LIST : ~define, ~wiki , add more tips

#quitmessage = ':ragsagar!n=ragsagar@117.204.98.53 QUIT :Client Quit'
#ordmsg = ':ragsagar!n=ragsagar@117.204.98.53 PRIVMSG #aymer :hi pelly'
#/memsg = ':ragsagar!n=ragsagar@117.204.98.53 PRIVMSG #aymer :ACTION hi'
#joinmsg = ':ragsagar!n=ragsagar@117.204.98.53 JOIN :#aymer'
#server = 'irc.freenode.net'
#port = 6667
#channel = '#aymer'
#nick = 'pelly'
#realname = 'Pell The Bot'


class Bot:
	"""the bot class"""
	
	def __init__(self, server = 'irc.freenode.net', port=6667):
		self.MeetingMode = False
		self.sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connection = self.sock.connect_ex((server, port))
		self.input = self.sock.makefile('rb',0)
		self.output = self.sock.makefile('wb',0)
		if self.connection is 0:
			print "Connected"
						
	def identify(self, nick = 'pelly', realname = 'Pelly The Bot'):
		"passes nickname and username to the server"
		self.nick = nick
		#self.output.write('PASS botmaker\r\n')
		self.output.write('NICK '+nick+'\r\n')
		self.output.write('USER '+nick+' 8 * :'+realname+'\r\n')
			
	def join_channel(self, channel='#aymer'):
		"Joins a channel by passing 'JOIN <channel>'"
		self.channel = channel
		done = True
		while  done :
			text = self.input.readline().strip()
			print text
			#if text.find('End of /MOTD command') == -1:
			if text.find('PRIVMSG') == -1:
				done = True
			else:
				self.output.write('JOIN '+channel+'\r\n')
				done = False
		print self.input.readline().strip()		
		self.logmessage = Log(channel)
		return 0		
				
	def work(self):
		"Stay in the channel"		
		message = self.input.readline().strip()
		self.left_nicks = []
		
		while True :
			new = True
			#print message
			if self.MeetingMode : #executes this set only if the meeting mode is on
				if message.find('JOIN :'+self.channel) != -1:
					new_comer = message.split('!')[0][1:]
					#print new_comer
					if len(self.left_nicks) is not 0 :
						for nick in self.left_nicks:
							if nick == new_comer or nick+'_' == new_comer or nick+'__' == new_comer :
								print "Not a new guy"
								new = False
					if new	:
						self.output.write('PRIVMSG '+self.channel+' :'+new_comer+': Welcome to '+self.channel+', Please Introduce Yourself\r\n')
			
				if message.find('QUIT :') != -1 or message.find('PART') != -1:
					self.left_nicks.append(message.split('!')[0][1:]) 
					
			if message.find('PRIVMSG')!=-1:
				self.parseMessage(message)
				message = message.split()
				if message[0] is 'PING':
					self.output.write('PONG '+message[1]+'\n')
			message = self.input.readline().strip()
	
	def parseMessage(self,message):
		" Using a series of if commands finds and does the corresponding actions for commands "
		#msg=message.split(' ')[2]
		parser = parse.Parse()
		msg = ' '.join(message.strip().split(' ')[3:])[1:]
		author = message.split(':')[1].split('!')[0]
		if author != 'freenode-connect':
			self.logmessage.log("%s : %s " % (author,msg))
		print "%s : %s " % (author,msg)
		msgl=msg.lower()
		if msgl.find('hi '+self.nick) != -1 or  msgl.find(self.nick+', hi') != -1 or msgl.find('hello '+self.nick) != -1 or msgl.find(self.nick+': hello') != -1 or msgl.find(self.nick+': hi') != -1 :
			res=author+', hi'
			self.logmessage.log(self.nick+' : '+res)
			self.output.write('PRIVMSG '+self.channel+' : '+res+'\r\n')
		elif msgl.find('yo '+self.nick) != -1 or msgl.find(self.nick+': yo') != -1 or msgl.find(self.nick+', yo') != -1 :
			res='yo '+author
			self.logmessage.log(self.nick+' : '+res)
			self.output.write('PRIVMSG '+self.channel+' : '+res+'\r\n')
		elif msgl.find('bye') != -1 and msgl.find(self.nick) != -1:
			res='see ya '+author
			self.logmessage.log(self.nick+' : '+res)
			self.output.write('PRIVMSG '+self.channel+' : '+res+'\r\n')
					
		if msg[0] is '~' and msg[1:].strip() != '' :
			#parser.Parse(msg[1:])
			if msgl[1:] == 'fsf':
				news = parser.FSFnewsCommand()
				if news is None:
					self.output.write('PRIVMSG '+author+' : Sorry unable to retrieve data due to net problems \r\n')
					return
				self.output.write('PRIVMSG '+author+' :=============Top 5 fsf news=========== \r\n')
				for i in range(5):
					self.output.write('PRIVMSG '+author+' : '+str(i+1)+'] '+news[i]+'\r\n')
				
			if msgl[1:] == 'slashdot':
				news = parser.SDotnewsCommand()
				if news is None:
					self.output.write('PRIVMSG '+author+' : Sorry unable to retrieve data due to net problems \r\n')
					return
				self.output.write('PRIVMSG '+author+' :==============Top 5 Slashdot  Stories===========\r\n')
				for i in range(5):
					self.output.write('PRIVMSG '+author+' : '+str(i+1)+'] '+news[i]+'\r\n')
					
			if msgl[1:] == 'whoami':
				res='you are '+author+', silly'
				self.logmessage.log(self.nick+' : '+res)
				self.output.write('PRIVMSG '+self.channel+' : '+res+'\r\n')		
			
			if msgl[1:] == 'fortune':
				fortune = parser.GetFortune()
				res = author+': '+fortune
				self.logmessage.log(self.nick+' : '+res)
				self.output.write('PRIVMSG '+self.channel+' : '+res+'\r\n')
			
			if msgl[1:] == 'love':
				quote = parser.GetLoveQuote()
				res = author+': '+quote
				self.logmessage.log(self.nick+' : '+res)
				self.output.write('PRIVMSG '+self.channel+' : '+res+'\r\n')	
									
						
			if msgl[1:] == 'help':
				self.output.write('PRIVMSG '+author+' : ==========Commands list======== \r\n')
				self.output.write('PRIVMSG '+author+' : ~help , ~whoami , ~fsf , ~slashdot , ~weather <city> , ~fortune , ~love , ~meeting [on, off, state] \r\n')
			
			if msgl[1:].split()[0] == 'meeting':
				try :
					state = msgl[1:].split()[1]
				except IndexError:
					self.output.write('PRIVMSG '+author+' : Syntax : ~meeting [on, off, state] \r\n')
					return
				if state == 'on':
					self.MeetingMode = True
					self.output.write('PRIVMSG '+author+' : Meeting mode is now ON\r\n')							
				elif state == 'off':
					self.MeetingMode = False
					self.left_nicks = []
					self.output.write('PRIVMSG '+author+' : Meeting mode is now OFF\r\n')
				elif state == 'state':
					if self.MeetingMode :
						self.output.write('PRIVMSG '+author+' : Meeting Mode is in ON state\r\n')
					else :
						self.output.write('PRIVMSG '+author+' : Meeting Mode is in OFF state\r\n')		
				
			if msgl[1:].split()[0] == 'weather':
				try :
					city = msgl[1:].split()[1]
				except IndexError:
					self.output.write('PRIVMSG '+author+' : Syntax : ~weather <city> \r\n')
					return
				weather_list = parser.WeatherFinder(city)	
				if weather_list is None :
					self.output.write('PRIVMSG '+author+' : Sorry, Unable to fetch data \r\n')
				elif weather_list == [] :
					self.output.write('PRIVMSG '+author+' : Sorry, Try another city \r\n')										
				else :
					self.output.write('PRIVMSG '+author+' : ========Weather Conditions in '+city+'========\r\n')
					for weather in weather_list:
						self.output.write('PRIVMSG '+author+' : '+weather+'\r\n') 
				
						
		
			
	def close(self):
		"Close the connection"
		del self.logmessage.log_file
		self.sock.close()
		print "Closed"
	
			
		
if __name__=='__main__':
	bot=Bot(server='irc.efnet.org')
	bot.identify('pybotty')
	status=bot.join_channel('#aymer')
	if status==0:
		bot.work()		
	else :
		bot.close()	

