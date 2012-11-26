__description__ = 'Class to summarize a body of text into a list of keywords'
__author__ = 'Brandon Dixon'
__version__ = '1.0'
__date__ = '2012/10/26'

try:
	import string
	import logging
	import ConfigParser
	import os
	import nltk
	
	from utility import *
except ImportError, e:
	import sys
	print str(e)
	sys.exit(1)

class summarize:
	def __init__(self,text,knum):
		self._config = ConfigParser.ConfigParser()
#		self._config.read("/opt/bookworm/settings/settings.cfg")
		self._config.read(os.getcwd() + "/settings/settings.cfg")

		ll = self._config.get("general","logging").upper()
		self._log = utility.logger(self.__class__.__name__,ll)

		self._text = text
		self._n = int(knum)

		self._kwords = []

	def gen_kwords(self):
		dirty = nltk.clean_html(self._text)
		tokens = nltk.word_tokenize(dirty)
		stokens = [w for w in tokens if w.lower() not in nltk.corpus.stopwords.words('english')] #removes stopwords from the tokens
		tagged = nltk.pos_tag(stokens)
		ftagged = nltk.FreqDist(tagged)
		top = [word for (word, tag) in ftagged if tag.startswith('N')] #picks out only nouns    

		self._kwords = []
		[self._kwords.append(i) for i in top if not self._kwords.count(i)]

	def get_most_used_words(self):
		self.gen_kwords()
		return self._kwords[:self._n]
