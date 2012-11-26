__description__ = 'Class to summarize a body of text into a list of keywords'
__author__ = 'Brandon Dixon'
__version__ = '1.0'
__date__ = '2012/10/26'

try:
	import string
	import logging
	import ConfigParser
	import os
	import hashlib
	import feedparser

	from stripper import *
	from summarize import *
	from utility import *
	from mongodb import *
except ImportError, e:
	import sys
	print str(e)
	sys.exit(1)

class hippo:
	def __init__(self,flist=None):
		self._config = ConfigParser.ConfigParser()
#		self._config.read("/opt/bookworm/settings/settings.cfg")
		self._config.read(os.getcwd() + "/settings/settings.cfg")
		ll = self._config.get("general","logging").upper()
		self._log = utility.logger(self.__class__.__name__,ll)

		self._kword_amt = self._config.get("feeder","keyword_amount")
		mhost = self._config.get("db_mongo", "host")
		mport = self._config.get("db_mongo", "port")
		mdb = self._config.get("db_mongo", "database")
		mcollection = self._config.get("db_mongo", "collection")

		self._mongodb_handle = mongodb(mhost,mport,mdb,mcollection)							 
		self._mdb = self._mongodb_handle.get_con()

		self._processed = []

		if flist == None:
			self._fl_loc = self._config.get("feeder","feed_list")
			self._log.debug("Grabbing feed file: %s" % self._fl_loc)
			self._feed_list = open(self._fl_loc,"r")
		else:
			self._log.debug("Using passed in feed file")
			self._feed_list = open(flist,"r")

		self.process_feed()

	def process_feed(self):

		for f in self._feed_list:
			self._link = f
			self._fburned = feedparser.parse(self._link)

			# grab the details from the burned feed
			self._furl = self._fburned['url']
			self._fversion = self._fburned['version']
			self._flang = ""

			self._log.info("Processing articles for %s: %s, %s" % (self._furl,str(self._fversion),self._flang.strip()) )

			self._articles = []

			for i in self._fburned['items']:
				self._aframe = {'title':None,'date':None,'link':None,'keywords':[],'feed':None,'language':None}
				
				try:
					self._ititle = i['title']
					#self._isummary = i['summary']
					self._idate = i['published']
					self._ilink = i['link']								
					self._ctext = stripper(i['summary']).get_data() #strip out HTML
					self._sum = summarize(self._ctext,self._kword_amt) #summarize the article
					self._kwords = self._sum.get_most_used_words()
				except Exception,e:
					print str(e)
					self._log.error("Failed to process %s" % i['title'])	
			
				self._log.debug("Processed article: \ntitle:%s \ndate:%s \nlink:%s \nkeywords:%s" % (self._ititle,self._idate,self._ilink,self._kwords))
				
				self._aframe['title'] = self._ititle
				self._aframe['date'] = self._idate
				self._aframe['link'] = self._ilink
				self._aframe['keywords'] = self._kwords
				self._aframe['feed'] = self._furl
				self._aframe['language'] = self._flang
				hashed = hashlib.sha256(str(self._aframe)).hexdigest() #hash the contents to check in DB
				self._aframe['hashed'] = hashed
				self._articles.append(self._aframe)

				if self._mongodb_handle._not_processed(hashed):
					self._log.info("Adding %s (%s)" % (self._ititle,hashed))
					self._mongodb_handle._insert_full(self._aframe)

#			self._log.debug(self._frame)

	def get_processed(self):
		return self._processed
