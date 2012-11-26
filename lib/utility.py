class utility:
	'''
	Utility class to provide static methods for all classes
	'''
	
	@staticmethod
	def logger(handler,level):
		'''
		Get a logging instance
		@param	handler	name of the logging instance
		@param	level	level in which to log
		@return	logging	object used for later on
		'''
		import logging
		
		log = logging.getLogger(handler)
		if level == "INFO":
			logging.basicConfig(level=logging.INFO)
		elif level == "DEBUG":
			logging.basicConfig(level=logging.DEBUG)
		elif level == "ERROR":
			logging.basicConfig(level=logging.ERROR)
		else:
			pass
			
		return log
		
	@staticmethod
	def grab_rule(haystack):
		'''
		Grab the rule from the email subject
		@param	haystack	email subject from VT
		@return rule name from the subject
		TODO make this more general
		'''
		init_split = haystack.split(":")
		main = init_split[0].split("]")
		return main[2].lstrip()

	@staticmethod
	def find_md5(haystack):
	
		import re
		
		s = re.compile('.[0-9a-zA-Z]{32}.')
		m = s.search(haystack)
		if m != None:
			matches = m.group()
			lhash = matches[1:len(matches)-1]
			return lhash
		else:
			return None

	@staticmethod
	def find_sha1(haystack):

	    import re

	    s = re.compile('.[0-9a-zA-Z]{40}.')
	    m = s.search(haystack)
	    if m != None:
	        matches = m.group()
	        lhash = matches[1:len(matches)-1]
	        return lhash
	    else:
	        return None

	@staticmethod
	def find_sha256(haystack):
		'''
		Find the SHA256 hash located within a block of text
		@param	haystack	block of text to search
		@return	hash if found
		'''
		import re
		
		s = re.compile('.[0-9a-zA-Z]{64}.')
		m = s.search(haystack)
		if m != None:
			matches = m.group()
			lhash = matches[1:len(matches)-1]
			return lhash
		else:
			return None
		
	@staticmethod
	def tmp_write(file,path):
		'''
		Write a file to a temp location so we can SCP later
		@param	file	file to write to the system
		@param	path	path to write to
		return boolean if write worked
		'''
		import hashlib

		fname = hashlib.md5(file).hexdigest()
		try:
			f = open(path + fname,"wb")
			f.write(file)
			f.close()
			return True
		except:
			return False

	@staticmethod
	def get_hash(data,hash_type):
		'''
		Take in data and hash it with whatever type requested
		@param	data		data to hash
		@param	hash_type	hash type to use
		@return	hashed data
		'''
		import hashlib
		
		if hash_type == "MD5":
			hashed = hashlib.md5(data).hexdigest()
		elif hash_type == "SHA1":
			hashed = hashlib.sha1(data).hexdigest()
		elif hash_type == "SHA256":
			hashed = hashlib.sha256(data).hexdigest()
		else:
			hashed = None

		return hashed

	@staticmethod
	def to_bool(value):
		'''
		Take in a value and convert it to a boolean type
		@param	value	string or int signifying a bool
		@return	a boolean for the value passed in
		'''

		if str(value).lower() in ("yes", "y", "true",  "t", "1"): return True
		if str(value).lower() in ("no",  "n", "false", "f", "0", "0.0", "", "none", "[]", "{}"): return False
		raise Exception('Invalid value for boolean conversion: ' + str(value))
