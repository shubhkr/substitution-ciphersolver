from substackframe import *
import sys

with open("dictionary.txt", "r") as f:
	d = [i.lower() for i in f.read().split("\n") if len(i) > 0]
#~ d = d + ["devices", "security", "reputation", "it", "earned", "nsas", 'at', 'the', "a", "bletchley", "codenamed", 'was', "is", "an", "securing", "communications", "and"]

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

def decrypt(ct, key):
	r = ""
	for i in ct:
		if i.lower() in key:
			r += key[i]
		elif i == " ":
			r += i
		else:
			r += i.upper()
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
	words = [i.lower() for i in ct.split(" ")]
	words_tree = [[] for i in range(len(words))]
	for i in range(len(words)):
		for w in d:
			key = pattern_match(words[i], w)
			if key != None:
				words_tree[i].append(key)
	words_tree.sort(key = lambda x: len(x)) #increases efficiency by a shitton
	
	#need to account for words that aren't in the dict
	
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
		#~ print new_master_keys
		#~ if len(new_master_keys) < 1:
		master_keys = []
		for i in new_master_keys:
			if i not in master_keys:
				master_keys.append(i)
	return master_keys

def getlenNsubsets(ls, n):
	r = []
	if n == 1:
	for i in range(n):
		

def hellaCrack(ct):
	words = ct.split(" ")
	for blocked_words in range(words):
		

def getKeyMatches(word):
	r = []
	for d_word in d:
		p = pattern_match(word, d_word)
		if p != None:
			r.append(p)
	return r

def pad(text, length = len("xxx.xxx.xxx.xxx"), pad = " "):
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

import random
secret_key = {}
values = list("abcdefghijklmnopqrstuvwxyz")
for i in "abcdefghijklmnopqrstuvwxyz":
	secret_key[i] = values.pop(random.choice(range(len(values))))
print secret_key
secret_message = " ".join(random.choice(d) for i in range(10))
print secret_message

ct = decrypt(secret_message, invert(secret_key))

for word in secret_message.split(" "):
	print "%s %s" % (word, len(getKeyMatches(word)))

k = crack(ct)
for i in k:
	print decrypt(ct, i)
