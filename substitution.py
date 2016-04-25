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

import random
secret_key = {}
values = list("abcdefghijklmnopqrstuvwxyz")
for i in "abcdefghijklmnopqrstuvwxyz":
	secret_key[i] = values.pop(random.choice(range(len(values))))
print secret_key
secret_message = " ".join(random.choice(d) for i in range(10))
print secret_message

ct = decrypt(secret_message, invert(secret_key))


#~ ct1 = "k wkau pz nhofmu yzp puo tzmphkyo ze kiyzjvo ofao jrp puo tzmphkyo ze puo aphoyrzra vkeo"

print ct
for i in crack(ct):
	print i
	print  decrypt(ct, i)
