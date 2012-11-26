from HTMLParser import HTMLParser

class m(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

class stripper():
	def __init__(self,d):
		self._html = d
		self.strip_tags(self._html)
		self.rdata = None

	def strip_tags(self,html):
		s = m()
		s.feed(html)
		self._rdata = s.get_data()
	
	def get_data(self):
		return self._rdata
