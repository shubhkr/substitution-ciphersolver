from itertools import combinations
import sys
import time

with open("/home/qazxvy/Documents/Code/Github/substitution-ciphersolver/20k.txt", "r") as f:
	d = [i.lower() for i in f.read().split("\n") if len(i) > 0]

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
def decrypt(ct, key):
	r = ""
	for i in ct:
		if i.lower() in key:
			if i in LOWERCASE:
				r += key[i.lower()]
			elif i in UPPERCASE:
				r += key[i.lower()].upper()
		elif i in UPPERCASE or i in LOWERCASE:
			r += fail(i)
		elif i == " ":
			r += i
		else:
			r += warning(i)
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
	return master_keys

def hellaCrack(ct, seed = None): #seed for key is for very edge cases, manual inputting
	words = []
	for i in ct.split(" "):
		if i not in words and len(getKeyMatches(i)) > 0: words.append(i) #remove duplicates
	for l in range(1, len(words) + 1)[::-1]: #words: start at all, then length - 1, length - 2, etc.
		#BUG: sys.stdout.write(...) fails
		print ("trying with %s/%s words" % (l, len(words)))
		c = 1
		combos = combinations(words, l)
		temp = combinations(words, l)
		possibilities = len(list(temp))
		for i in list(combos): #one iteration per list of selected words
			print ("%s - %s/%s" % (percentagebar(0, possibilities, c), c, possibilities))
			test = crack(" ".join(list(i)), seed)
			if len(test) > 0:
				return test
			c += 1

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
	return word.replace("'", "")

def purifyCT(CT):
	ct = []
	for word in CT.split(" "):
		good = True
		word = stripPunctuation(word)
		for char in word:
			if char not in UPPERCASE + LOWERCASE:
				good = False
		if good:
			ct.append(word.lower())
	return " ".join(ct)

def main(CT = None):
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
	print "%s solutions found in %s seconds" % (len(k), t)
	for i in range(len(k)):
		print "-"*(40) + pad(str(i), 40, "-")
		print decrypt(CT, k[i])
		print k[i]
	return k, t

if __name__ == "__main__":
	main()
