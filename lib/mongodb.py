__description__ = 'Class to connect to Mongo tracking DB'
__author__ = 'Brandon Dixon'
__version__ = '1.0'
__date__ = '2012/08/09'

try:
	import os
	import logging
	import sys
	import pymongo
	import ConfigParser
	from pymongo import Connection

	from utility import *
except ImportError, e:
	print str(e)

class mongodb:
	def __init__(self,host,port,database,collection):
		'''
		Init
		@param	host		host of the mongo server
		@param	port		port of the mongodb server
		@param	database	name of the database
		@param	logging		logging level
		'''

		self._config = ConfigParser.ConfigParser()
#		self._config.read("/opt/bookworm/settings/settings.cfg")
		self._config.read(os.getcwd() + "/settings/settings.cfg")
		ll = self._config.get("general","logging").upper()
		self._log = utility.logger(self.__class__.__name__,ll)

		self._host = host
		self._port = int(port)
		self._database = database
		self._collection = collection

		self._connect_db()

	def get_con(self):
		return self._collection

	def _connect_db(self):
		connection = Connection(self._host, self._port)
		db = connection[self._database]
		self._db = db
		collection = db[self._collection]
		self._collection = collection

	def _not_processed(self,shash):
		res = self._collection.find({"hashed":shash}).count()
		if res >= 1:
			self._log.info("Hash already processed")
			return False
		else:
			self._log.info("Hash processing")
			return True

	def _get_full(self,shash):
		res = self._collection.find_one({"hashed":shash},{"_id":0})
		return res

	def _insert_full(self,full):
		try:
			res = self._collection.insert(full) #add safe checks to this
		except Exception, exc:
			self._log.error("Failed to insert chunk into MongoDB")
			notify("Failed to insert chunk",str(exc),"INFO",True)	

	def _update_chunk(self,shash,chunk,piece):
		try:
			res = self._collection.update({"sha256":shash},{"$set": { "additional." + piece : chunk } })
		except Exception, exc:
			self._log.error("Failed to insert %s chunk into MongoDB" % (piece))
			notify("Failed to insert %s chunk" % (piece),str(exc),"INFO",True)

	def _get_last_processed(self):
		res = self._collection.find_one()
		return res['last_processed']

	def _update_processed(self,count):
		try:
			tmp = self._collection.find_one()
			id = tmp['_id']
			self._collection.update({"_id":id},{ "$set": { "last_processed" : count} } )
		except Exception, exc:
			self._log.error("Failed to update last mail processed")
			notify("Failed to update last mail processed",str(exc),"INFO",True)
