import sys
import nltk
from nltk import word_tokenize
from nltk.util import ngrams
from collections import Counter

with open('test.txt', 'r') as myfile:
    data=myfile.read().replace('\n', '')
    
token = nltk.word_tokenize(data)
unigrams = ngrams(token,1)
bigrams = ngrams(token,2)

bgm = nltk.FreqDist(bigrams)
uni = nltk.FreqDist(bigrams)

fileunigram = open('unigramsout.txt', 'w')
filebgram = open('bgramsout.txt', 'w')

for key,key1 in uni.items():
	fileunigram.write(key[0] + ' ' + str(key1) + '\n')  
	
for key,key1 in bgm.items():
	filebgram.write(key[0] + ' ' +  key[1] + ' ' + str(key1) + '\n')  

fileunigram.close()       	
filebgram.close() 


