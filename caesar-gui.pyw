# Caesar cipher encoder/decoder and frequency analysis tool
# Written and developed by l0cal_gh0st

from tkinter import *
from tkinter import ttk

alpha = 'abcdefghijklmnopqrstuvwxyz'
alphaFreq = 'etaoinshrdlcumwfgypbvkjxqz'
alphaDouble = ['th', 'ea', 'of', 'to', 'in', 'it', 'is', 'be', 'as', 'at', 'so', 'we', 'he', 'by', 'or', 'on', 'do', 'if', 'me', 'my', 'up']
alphaRepeat = ['ss', 'ee', 'tt', 'ff', 'll', 'mm', 'oo']
alphaTriple = ['the', 'est', 'for', 'and', 'his', 'ent', 'tha']

def caesarEncrypt():
	plainText = str(caesarInput.get()).lower()
	shiftKey = int(caesarKey.get())
	cipherText = []
	i = 0
	j = 0
	
	while i < len(plainText):
		if not plainText[i].isspace(): #Fix to include special characters and numbers in filter
			while j < 26:
				if plainText[i] == alpha[j]:
					found = j
					j = 0
					break
				else:
					j += 1
			newFound = (found + shiftKey) % 26
			cipherText.append(alpha[newFound])
			i += 1
		else:
			cipherText.append(" ")
			i += 1
	
	output = "".join(cipherText)	
	caesarOutput.set(output)
		
def caesarDecrypt(cipherText, shiftKey):
	plainText = []
	i = 0
	j = 0
	
	while i < len(cipherText):
		if not cipherText[i].isspace(): #Fix to include special characters and numbers in filter
			while j < 26:
				if cipherText[i] == alpha[j]:
					found = j
					j = 0
					break
				else:
					j += 1
			newFound = (found - shiftKey) % 26
			plainText.append(alpha[newFound])
			i += 1
		else:
			plainText.append(" ")
			i += 1
	
	output = "".join(plainText)	
	return output
	
def decryptHandler():
	cipherText = str(caesarInput.get()).lower()
	shiftKey = int(caesarKey.get())
	if shiftKey == 0:
		guessOutput = freqAnalysis(cipherText)
		caesarOutput.set(guessOutput)
	else:
		output = caesarDecrypt(cipherText, shiftKey)
		caesarOutput.set(output)
		
def initDict():
	freqCount = {}
	i = 0
	
	while i < 26:
		freqCount.update({alpha[i]:0})
		i += 1
	
	return freqCount
	
def maxValue(freqCount):
	val=list(freqCount.values())
	key=list(freqCount.keys())
	return key[val.index(max(val))]
	
def freqAnalysis(cipherText):
	freqCount = initDict()
	potSolutions = []
	i = 0
	j = 0
	
	while i < len(cipherText):
		if not cipherText[i].isspace():
			while j < 26:
				if cipherText[i] == alpha[j]:
					freqCount[alpha[j]] += 1
					j = 0
					break
				else:
					j += 1
			i += 1
		else:
			i += 1
	
	max = maxValue(freqCount)
	x = 0
	z = 0
	
	while z < 10:	
		y = 0
	
		while y < 26:
			if alphaFreq[x] == alpha[y]:
				foundFreq = y
			if max == alpha[y]:
				foundMax = y
			y += 1
	
		potKey = (foundMax - foundFreq) % 26
		potSolutions.append(caesarDecrypt(cipherText, potKey))
		x += 1
		z += 1
	
	scores = [10, 9, 8, 7, 7, 6, 6, 6, 5, 5]
	solNum = 0
	
	for sol in potSolutions:
		for double in alphaDouble:
			if double in sol:
				scores[solNum] += 1
		for repeat in alphaRepeat:
			if repeat in sol:
				scores[solNum] += 1
		for triple in alphaTriple:
			if triple in sol:
				scores[solNum] += 1
		solNum += 1
	
	bestScore = scores[0]
	bestIndex = 0
	k = 0
	while k < 10:
		if bestScore < scores[k]:
			bestScore = scores[k]
			bestIndex = k
		k += 1
	
	debugOutput.set(scores)
	bestSol = potSolutions[bestIndex]
	return bestSol
	
root = Tk()
root.title("Caesar Cipher")

frame = ttk.Frame(root, padding="3 3 12 12") #Expand frame size
frame.grid(column=0, row=0, sticky=(N, W, E, S))
frame.columnconfigure(0, weight=1)
frame.rowconfigure(0, weight=1)

caesarInput = StringVar()
caesarOutput = StringVar()
caesarKey = StringVar()
debugOutput = StringVar()

ttk.Label(frame, text="Input:   ").grid(column=1, row=1, sticky=E)
text_entry = ttk.Entry(frame, width=20, textvariable=caesarInput)
text_entry.grid(column=2, row=1, sticky=(W, E))

ttk.Label(frame, text="Key (1-26):   ").grid(column=1, row=2, sticky=E)
key_entry = ttk.Entry(frame, width=5, textvariable=caesarKey)
key_entry.grid(column=2, row=2, sticky=(W, E)) 
ttk.Label(frame, text="  (0 for guess)").grid(column=3, row=2, sticky=W)

ttk.Label(frame, text="Output:   ").grid(column=1, row=3, sticky=E)
ttk.Label(frame, textvariable=caesarOutput).grid(column=2, row=3, sticky=(W, E)) #Change output mechanics to allow for copy/paste

ttk.Button(frame, text="Encrypt", command=caesarEncrypt).grid(column=1, row=4, sticky=W)
ttk.Button(frame, text="Decrypt", command=decryptHandler).grid(column=3, row=4, sticky=E)

ttk.Label(frame, text="Debug:    ").grid(column=1, row=5, sticky=E)
ttk.Label(frame, textvariable=debugOutput).grid(column=2, row=5, sticky=(W, E))

text_entry.focus()

root.mainloop()