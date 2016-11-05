import sys
import json
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
			
   jsonDict = "bgrams-json" + inFile + ".pkl"
   with open(jsonDict, 'wb') as f:
	pickle.dump(bigramsCount,f, pickle.HIGHEST_PROTOCOL)
   
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
	
   jsonDict = "unigrams-json" + inFile + ".pkl"
   with open(jsonDict, 'wb') as f:
	pickle.dump(unigramsCount,f, pickle.HIGHEST_PROTOCOL)

   return unigramsCount 

def splitPhrases(file):
   phrases = []
   delimiter = ['.','!','?']
   with open(file, 'r') as i:
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
   
def laplace(phr):
	unigramsCount = unigrams(p)
	bigramsCount = bigrams(p)
	
	difwords = len(unigramsCount)

flag = sys.argv[1]
inFile = sys.argv[2]
if flag == '-d':
	p = splitPhrases(inFile)
	bigrams(p)
	unigrams(p)
elif flag == '-t':	
	#calculate prob of file
	laplace(inFile)
