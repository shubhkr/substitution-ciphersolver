from itertools import combinations
import sys
import time
from os import path

with open(path.join(path.dirname(__file__), "100k.txt"), "r") as f:
	full_dict = [i.lower() for i in f.read().split("\n") if len(i) > 0] #tk there's some interesting stuff to find out the optimal dict size.
d = full_dict[:26000]

def invert(key):
	key_inverse = {}
	for i in key:
		key_inverse[key[i]] = i
	return key_inverse

def pattern_match(a, b): #ciphertext, plaintext
	if len(a) != len(b):
		return None
	key = {}
	for i in range(len(a)):
		if b[i] in invert(key) and invert(key)[b[i]] != a[i]:
			return None
		if a[i] in key and not b[i] == key[a[i]]:
			return None
		key[a[i]] = b[i]
	return key

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
def warning(x):
	return bcolors.WARNING + x + bcolors.ENDC
def fail(x):
	return bcolors.FAIL + x + bcolors.ENDC
UPPERCASE = map(chr, range(65, 91))
LOWERCASE = map(chr, range(97, 123))
def decrypt(ct, key, color = True):
	r = ""
	for i in ct:
		if i.lower() in key:
			if i in LOWERCASE:
				r += key[i.lower()]
			elif i in UPPERCASE:
				r += key[i.lower()].upper()
		elif i in UPPERCASE or i in LOWERCASE:
			if color:
				r += fail(i)
			else:
				r += i
		elif i == " ":
			r += i
		else:
			if color:
				r += warning(i)
			else:
				r += i
	return r

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
	

def crack(ct, seed = None):
	words_tree = [getKeyMatches(i) for i in [i.lower() for i in ct.split(" ")]]
	words_tree.sort(key = lambda x: len(x)) #increases efficiency by a shitton
	
	if seed == None:
		master_keys = words_tree[0]
		words_tree = words_tree[1:]
	else:
		master_keys = [seed]
	for new_keys in words_tree:    #cycle through each next set
		new_master_keys = []
		for new_key in new_keys:       #each possible key of the next word
			for m_key in master_keys:  #with each previously thought possible key
				c_key = combine(m_key, new_key)
				if c_key != None:
					new_master_keys.append(c_key)
		master_keys = []
		for i in new_master_keys:
			if i not in master_keys:
				master_keys.append(i)
	
	master_keys = sorted(master_keys, key = lambda k: sum(map(lambda x: d.index(x), decrypt(ct, k).split(" "))))
	return master_keys

def hellaCrack(ct, seed = None): #seed for key is for very edge cases, manual inputting
	words = []
	for i in ct.split(" "):
		if i not in words and len(getKeyMatches(i)) > 0: words.append(i) #remove duplicates
	for l in range(1, len(words) + 1)[::-1]: #words: start at all, then length - 1, length - 2, etc.
		print ("trying with %s/%s words" % (l, len(words)))
		c = 1
		combos = combinations(words, l)
		temp = combinations(words, l)
		possibilities = len(list(temp))
		for i in list(combos): #one iteration per list of selected words
			sys.stdout.write("\r%s - %s/%s" % (percentagebar(0, possibilities, c), c, possibilities))
			sys.stdout.flush()
			test = crack(" ".join(list(i)), seed)
			if len(test) > 0:
				print
				return test
			c += 1
		#~ if l == len(words): #tk
			#~ print "\nincreasing dict size"
			#~ global d
			#~ d = full_dict[:40000]
		#~ else:
			#~ print
		print

def getKeyMatches(word):
	r = []
	for d_word in d:
		p = pattern_match(word, d_word)
		if p != None:
			r.append(p)
	return r

def pad(text, length = 79, pad = " "):
	if len(text) > length:
		if length > 10:
			return text[:length - 3] + "..."
		return text[:length]
	else:
		return text + (pad * (length - len(text)))
def map_(small, big, current):
	return float(current - small)/float(big - small)
def percentagebar(small, big, current, bars = 20):
	percent = map_(small, big, current)
	bar = int(round(bars * percent))
	return "[%s]" % (pad("="*bar, bars))

#"MCU tfjph pqib nf nsumi nsb xumd xbxwbyc fa nsb J.C. qmnbppqobmeb efxxjmqnd tsf tfyi nf ibbl fjy efjmnyd cuab."

def stripPunctuation(word):
	while word[-1] not in UPPERCASE + LOWERCASE:
		word = word[:-1]
	while word[0] not in UPPERCASE + LOWERCASE:
		word = word[1:]
	return word.replace("'", "").replace(".", " ").replace("-", " ")

def purifyCT(CT):
	ct = []
	for word in CT.split(" "):
		good = True
		word = stripPunctuation(word)
		for char in word:
			if char not in UPPERCASE + LOWERCASE + [" "]:
				good = False
		if good:
			ct.append(word.lower())
	return " ".join(ct)

def main(CT = None, ismain = __name__ == "__main__"):
	if CT == None:
		if len(sys.argv) < 2:
			print "enter ciphertext:"
			CT = raw_input(">")
		else:
			CT = " ".join(sys.argv[1:])
	start_time = time.time()
	
	ct = purifyCT(CT)
	k = hellaCrack(ct)
	t = time.time() - start_time
	if ismain:
		print "%s solutions found in %s seconds" % (len(k), t)
		for i in range(len(k)):
			print "-"*(40) + pad(str(i), 40, "-")
			print decrypt(CT, k[i])
			print k[i]
		print
	return k, t

if __name__ == "__main__":
	NSA_CTs = ["MC.VHMTGR CSZSWAU FJTBAM GRA GACZ 'DGAZ' QRTWA DRA QJCNAM SG GRA BSGTJBSW DFTABFA YJHBMSGTJB TB GRA ASCWU 2000D.",
				"MCU tfjph pqib nf nsumi nsb xumd xbxwbyc fa nsb J.C. qmnbppqobmeb efxxjmqnd tsf tfyi nf ibbl fjy efjmnyd cuab.",
				"IGH OXCKHQQVCYTB KCCIMTBB KXTYZGVQH KXCF OVIIQMRXEG, OT, GTQ DCY QVA BHTERH IVIBHQ, FCXH IGTY TYN CIGHX IHTF QVYZH IGH FHXEHX.",
				'"MKRR GUH UKRU" AR K GHVUQALDH XE VXNMPXNARAQW KOOAGAXQKS NKVUAQHR XQ K QHGYXPJ KEGHP XQH AR RDVVHRREDSSZ HBMSXAGHO."']
	import random
	def _time(f, repeat, *args):
		start_time = time.time()
		for i in range(repeat):
			f(*args)
		return time.time() - start_time
	
	def rand_word(l):
		return "".join([random.choice(LOWERCASE) for i in range(l)])
	
	def rand_pt(l, known_to):
		di = full_dict[:known_to]
		return " ".join([random.choice(di) for i in range(l)])
	
	def rand_key():
		k = {}
		l = map(chr, range(97, 123))
		for i in range(ord("a"), ord("z") + 1):
			k[chr(i)] = l.pop(random.choice(range(len(l))))
		return k
	
	len_CT = 10
	test_count = 50
	key = rand_key()
	solution = []
	for unknown in range(4):
		total = 0
		for t in range(test_count):
			ct = decrypt(rand_pt(len_CT - unknown, 26000) + " ".join([rand_word(random.choice(range(5, 10))) for i in range(unknown+1)]), key)
			print "length:", len(ct.split(" "))
			total += _time(main, 1, ct, False)
		solution.append("%s	%s" % (unknown, total))
	print "\n".join(solution)
	
