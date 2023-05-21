import bitarray
import random
import os

consonant = "qwrtpsdfghjklzxcvbnm"
vowels = "aeuioy"

def chooseLetter(letters, bitGen):
	while len(letters)>1:
		middle = int(len(letters)/2)
		if bitGen():
			letters = letters[:middle]
		else:
			letters = letters[middle:]
	return letters[0]


choice = input("Encode (Y) or Decode (n)")
if not choice == "n": #encode
	hidden = input("Hidden payload:")

	if os.path.exists(hidden) and os.path.isfile(hidden):
		path = hidden
		with open(path, "rb") as f:
			hidden = f.read()
		print(f"Succesfully read file: {path}")
	else: hidden = hidden.decode()
	ba = bitarray.bitarray()
	ba.frombytes(hidden)
	bits = ba.tolist()
	for i in range(8): bits.append(False)
	curBit = 0
	bitGen = lambda : bits.pop(0) if len(bits)>0 else random.random()<0.5
	cap = True
	out = ""
	while len(bits)>0:
		sentence_len = max(6, int(random.gauss(7, 3)))
		cap = True
		for j in range(sentence_len):
			word_len = max(3, int(random.gauss(7, 3)))
			for i in range(word_len):
				if bitGen():
					c = chooseLetter(vowels, bitGen)
				else:
					c = chooseLetter(consonant, bitGen)
				if cap:
					cap = False
					c = c.upper()
				out += c
			if j == sentence_len-1:	out+="."
			out+=" "

	if len(out) < 10_000:
		print(out)
	else:
		print(f"{len(out)} characters. Too much to display.")

	outFile = input("Output file name; press enter for no file")
	if not outFile == "":
		with open(outFile, "w") as f:
			f.write(out)
		print("Succesfully written to file.")

else: #decode
	mask = input("The masked text:")
	if os.path.exists(hidden) and os.path.isfile(hidden):
		path = mask
		with open(path, "r") as f:
			mask = f.read()
		print(f"Succesfully read file: {path}")
	bits = []
	for c in mask:
		if c in (" ", "."): continue
		c = c.lower()
		if c in vowels:
			letters = vowels
			bits.append(True)
		elif c in consonant:
			letters = consonant
			bits.append(False)
		else: continue

		idx = letters.index(c)
		while len(letters)>1:
			middle = int(len(letters)/2)
			if idx < middle:
				bits.append(True)
				letters = letters[:middle]
			else:
				bits.append(False)
				idx -= middle
				letters = letters[middle:]
	for i in range(0, len(bits)-8, 8):
		flag = True
		for j in range(0, 8):
			if bits[i + j]:
				flag = False
				break
		if flag:
			bits = bits[:i]
			break

	out = bitarray.bitarray(bits).tobyes()
	
	if len(out) < 10_000:
		print(out.decode())
	else:
		print(f"{len(out.decode())} characters. Too much to display.")

	outFile = input("Output file name; press enter for no file")
	if not outFile == "":
		with open(outFile, "wb") as f:
			f.write(out)
		print("Succesfully written to file.")


