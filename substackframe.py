def invert(key):
	key_inverse = {}
	for i in key:
		key_inverse[key[i]] = i
	return key_inverse

def combine(key1, key2):
	#make sure all keys are either distinct or match
	indexes = key1.keys() + key2.keys()
	for i in indexes:
		if i in key1 and i in key2: #if not distinct
			if key1[i] != key2[i]:  #must match
				return None
	#must be true of all values as well
	indexes = invert(key1).keys() + invert(key2).keys()
	for i in indexes:
		if i in invert(key1) and i in invert(key2): #if not distinct
			if invert(key1)[i] != invert(key2)[i]:  #must match
				return None
	combined_key = {}
	for i in key1.keys() + key2.keys():
		if i in key1:
			combined_key[i] = key1[i]
		else:
			combined_key[i] = key2[i]
	return combined_key

class Tree(object):
	def __init__(self):
		self.levels = []
	def addLevel(self, lvl):
		self.levels.append(lvl)
		self.sortLevels()
	def sortLevels(self):
		self.levels = sorted(self.levels, key = lambda x: len(x.keylist))
	def isExhausted(self):
		e = True
		for i in self.levels:
			if i.state < len(i.keylist):
				e = False
	def increaseState(self):
		l = len(self.levels) - 1
		if self.isExhausted():
			return False
		while self.levels[l].isExhausted():
			self.levels[l].state = 0
			l -= 1
		self.levels[l].nextState()
	def getKeyCombination(self):
		k = {}
		for l in self.levels:
			k = combine(k, l.cKey())
			if k == None:
				return None
		return k
	def combinations(self):
		s = 1
		for i in self.levels:
			s *= len(i.keylist)
		return s

class Level(object):
	def __init__(self, keylist):
		self.state = 0
		self.keylist = keylist
	def isExhausted(self):
		return self.state >= len(self.keylist)
	def cKey(self):
		if self.isExhausted():
			return {} #null key, exhausted level
		return self.keylist[self.state]
	def nextState(self):
		self.state += 1

