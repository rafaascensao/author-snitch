import sys
import os
import pickle

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
		
def probUni(phr, authorsList, unigramsAuthors):
    probs = {}

    for a in authorsList:
	probs[a] = 0

    for f in phr:
	p = phraseUnigram(f, authorsList, unigramsAuthors)
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
   
def probBi(phr, authorsList, unigramsAuthors, bigramsAuthors):
    probs = {}

    for a in authorsList:
	probs[a] = 0

    for f in phr:
	p = phraseBigram(f, authorsList, unigramsAuthors, bigramsAuthors)
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

def phraseUnigram(frase, authorsList, unigramsAuthor):
    words = frase.split()
    probs = {};
    for a in authorsList:
        unigramsCount = unigramsAuthor[a]
        probabilidade = 1;
	count = getNumWords(unigramsCount)
        for w in words:
	    if w in unigramsCount:
            	value = float(unigramsCount[w])/float(count)
	    else:
		value = 0
            probabilidade = probabilidade * value
        probs[a] = probabilidade
    return probs
 
 
def phraseBigram(frase, authorsList, unigramsAuthors, bigramsAuthors):
    words = frase.split()
    probs = {};
    for a in authorsList:
        bgramsCount = bigramsAuthors[a]
	unigramsCount = unigramsAuthors[a]
        probabilidade = 1;
	count = getUniqueWords(unigramsCount)
	value = calculateProbBiLaplace(words, bigramsCount, unigramsCount, "meter-aqui-o-metodo-que-se-quer-de-alisamento", count)
        probs[a] = probabilidade
    return probs
   
def calculateProbBiLaplace(words, bigramsCount, unigramsCount, flag, count):
        previousWord = "<s>" 
        for w in words:
	    if previousWord in bgramsCount:
		if w in bgramsCount[previousWord]:
            		value = (float(bgramsCount[previousWord][w]) + 1)/float(unigramsCount[previousWord] + count)
		else:
			value = float(1) /float(unigramsCount[previousWord] + count)
	    else:
		value = float(1) /float(count)

            probabilidade = probabilidade * value
	    previousWord = w
	return value
		
def guardamedia(p):
    filename=str(inFile)+'-list.txt'
    f = open(filename, 'w')
    pickle.dump(p, f)
   
def media(p):
    num_f = len(p)
    num_w = 0
    for f in p:
        words = f.split()
        num_w = num_w + len(words)
       
    media = float(num_w)/float(num_f)
   
    return media

def probFrasePalavras(p):
    authorsList=getAuthors()
    probs = {}
    chosenOne = ' '
    maximum = sys.maxint - 1
    dif = 0
    for a in authorsList:
    	filename= 'target/' + a + '.txt-list.txt'
        f = open(filename, 'r')
    	probs[a] = media(pickle.load(f))
    print '#############################'  
    print 'media:' + str(media(p)) +'\n'   
    for a in authorsList:
        print a + '  ' + str(probs[a]) + '\n'
       
        if abs(media(p) - probs[a]) < maximum:
            maximum = abs(media(p) - probs[a])
            chosenOne = a
    print chosenOne + '\n'
    print '#############################'
    return chosenOne
   
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
	guardamedia(p)

elif flag == '-t':	
	authorsList = getAuthors()
	authorsBigrams = {}
	authorsUnigrams = {}
	method = sys.argv[3]
	for author in authorsList:
		authorsBigrams[author] = loadBigrams(author)
		authorsUnigrams[author] = loadUnigrams(author)
	if method == 'uni':
		probUni(splitPhrases(inFile), authorsList, authorsUnigrams)		

	elif method == 'bi':
		probBi(splitPhrases(inFile), authorsList, authorsUnigrams, authorsBigrams)

	elif method == 'medium':
		probUni(splitPhrases(inFile), authorsList, authorsUnigrams)
