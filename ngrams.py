import sys
import os

# not tested, and somethings may be missing

def bigrams(phr):
   bigramsCount = {"<s>" : {}}
   for p in phr:
	words = p.split()
	previousWord = '<s>'
	i = 0
	for word in words:
		if word in bigramsCount[previousWord]:
			bigramsCount[previousWord][word] = bigramsCount[previousWord][word] + 1
		else:
			bigramsCount[previousWord][word] = 1 			 			 
		if word not in bigramsCount:
	        	bigramsCount[word] = {}	

		if i == len(words)-1:
			if "</s>" in bigramsCount[word]:
				bigramsCount[word]["</s>"] = bigramsCount[word]["</s>"] + 1
			else:
				bigramsCount[word]["</s>"] = 1 			 			 
			
		previousWord = word
		i = i + 1
		
   f = "bgrams-" + inFile
   filebgram = open(f, 'w')
   for key in bigramsCount.keys():
   	for k in bigramsCount[key].keys():
   		filebgram.write(key + ' ' + k + ' ' + str(bigramsCount[key][k]) + str( '\n'))
			
   return bigramsCount


def unigrams(phr):
   unigramsCount = {"<s>" : 0 }
   for p in phr:
	unigramsCount["<s>"] = unigramsCount["<s>"] + 1
	words = p.split()
	for word in words:
		if word in unigramsCount:
			unigramsCount[word] = unigramsCount[word] + 1
		else:
			unigramsCount[word] = 1
   unigramsCount["</s>"] = unigramsCount["<s>"]
   f = "unigrams-" + inFile
   fileunigram = open(f, 'w')
   for key in unigramsCount.keys():
	fileunigram.write(key + ' ' + str(unigramsCount[key]) + '\n') 
	
   return unigramsCount 

def loadUnigrams(author):
	unigrams = {}
	f = "target/unigrams-" + author + ".txt" 
	with open(f, 'r') as i:
		lines = i.readlines()
		for line in lines:
			words = line.split()
			unigrams[words[0]]=int(words[1])
	return unigrams

def loadBigrams(author):
	bigrams = {"<s>": {}}
	f = "target/bgrams-" + author + ".txt"
	with open(f, 'r') as i:
		lines = i.readlines()
		for line in lines:
			words = line.split()
			bigrams[words[0]] = {words[1] : 0}
			bigrams[words[0]][words[1]] = int(words[2])
	return bigrams 

def splitPhrases(f):
   phrases = []
   delimiter = ['.','!','?']
   with open(f, 'r') as i:
       text = i.read().replace('\n',' ').lower()
       words = text.split()
       phrase = ""
       for word in words:
           if word in delimiter:
		phrase = phrase + word
		phrases = phrases + [phrase]
		phrase = ""
           else:
 		phrase = phrase + word + " " 
   return phrases
   
def getNumWords(unigrams):
	counter = 0
	for key in unigrams:
		counter = counter + unigrams[key]
	return counter

def getUniqueWords(unigrams):
	counter = 0
	for key in unigrams:
		counter = counter + 1
	return counter - 2
		
def probUni(phr):
    authorsList = getAuthors()
    probs = {}

    for a in authorsList:
	probs[a] = 0

    for f in phr:
	p = prob_phr_uni(f)
	for author in probs:
		probs[author] = probs[author] + p[author]
      
    maximum = -sys.maxint - 1
    chosenOne = ""
    for a in authorsList:
	if probs[a] > maximum:
		maximum = probs[a]
		chosenOne = a
    print probs
    print chosenOne
    return chosenOne 
   
def probBi(phr):
    authorsList = getAuthors()
    probs = {}

    for a in authorsList:
	probs[a] = 0

    for f in phr:
	p = prob_phr_bi(f)
	for author in probs:
		probs[author] = ( probs[author] + p[author] ) * getUniqueWords(loadUnigrams(author))
      
    maximum = -sys.maxint - 1
    chosenOne = ""
    for a in authorsList:
	if probs[a] > maximum:
		maximum = probs[a]
		chosenOne = a
    print probs
    print chosenOne
    return chosenOne 

def prob_phr_uni(frase):
    words = frase.split()
    authorsList = getAuthors()
    probs = {};
    for a in authorsList:
        unigramsCount = loadUnigrams(a)
        probabilidade = 1;
        for w in words:
	    if w in unigramsCount:
            	value = float(unigramsCount[w])/float(getNumWords(unigramsCount))
	    else:
		value = 0
            probabilidade = probabilidade * value
        probs[a] = probabilidade
    return probs
 
 
def prob_phr_bi(frase):
    words = frase.split()
    authorsList = getAuthors()
    probs = {};
    for a in authorsList:
        bgramsCount = loadBigrams(a)
	unigramsCount = loadUnigrams(a)
        probabilidade = 1;
        count = 0
        for w in words:
	    if w == words[len(words)-1]:
		break
	    if w in bgramsCount:
		if words[count+1] in bgramsCount[w]:
            		value = (float(bgramsCount[w][words[count+1]]) + 1)/float(unigramsCount[w] + getUniqueWords(unigramsCount))
		else:
			value = float(1) /float(unigramsCount[w] + getUniqueWords(unigramsCount))
	    else:
		value = float(1) /float(getUniqueWords(unigramsCount))
            probabilidade = probabilidade * value
            count=count+1
        probs[a] = probabilidade
    return probs
   
   
   
def getAuthors():
    authorsList = []
    for subdirs in os.walk("target/corpora/treino"):
        for dirs in subdirs[1]:
            authorsList.append(dirs)
    return authorsList
flag = sys.argv[1]
inFile = sys.argv[2]
if flag == '-d':
	p = splitPhrases(inFile)
	bigrams(p)
	unigrams(p)
elif flag == '-t':	
	probBi(splitPhrases("normalized-text1.txt"))
	probBi(splitPhrases("normalized-text2.txt"))
	probBi(splitPhrases("normalized-text3.txt"))
	probBi(splitPhrases("normalized-text4.txt"))
	probBi(splitPhrases("normalized-text5.txt"))
	probBi(splitPhrases("normalized-text6.txt"))






