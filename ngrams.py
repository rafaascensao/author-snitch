import sys

def bigrams(file):
   bigramsCount = {"<s>" : {}}
   with open(file, 'r') as i:
      lines = i.readlines
      for line in lines:
         wordsInLine = line.split()
         for i in range(0,len(wordsInLine)):
            word = wordsInLine[0]
            if i == 0:
               tempDict = bigramsCount["<s>"]
               if word in tempDict:
                  counter = tempDict[word] + 1
               else:
                  counter = 1
               tempDict[word] = counter
               bigramsCount["<s>"] = tempDict
            else:
               previousWord = wordsInLine[i-1]
               if previousWord in bigramsCount:
                  tempDict = bigramsCount[wordsInLine[i-1]]
                  if word in tempDict:
                     counter = tempDict[word] + 1
                  else:
                     counter = 1
                  tempDict[word] = counter         
                  bigramsCount[previousWord] = tempDict
               else:
                  bigramsCount[previousWord] = {word : 1}
   return bigramsCount

def unigrams(file):
   uniigramsCount = {"<s>" : 0 }
   with open(file, 'r') as i:
      lines = i.readlines
      for line in lines:
         counter = unigramsCount["<s>"] + 1
         unigramsCount["<s>"] = counter
         wordsInLine = line.split()
         for word in wordsInLine:
            if word in unigramsCount:
               counter = unigramsCount[word] + 1
            else:
               counter = 1
            unigramsCount[word] = counter
   return unigramsCount
   

option = sys.argv[1]
inFile = sys.argv[2]

if option == "uni":
   unigrams(inFile)

elif option == "bi":
   bigrams(inFile)