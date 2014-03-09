import re
from itertools import ifilterfalse
from stemming.porter2 import stem
from nltk.stem import WordNetLemmatizer

ClassList = ['-1','1','2','0']

####################################################################################################################
###         Clean Tweets
###
####################################################################################################################

# Twitter Data contain some hyperlinks that is no use for mining
def cleaning_http(line):
	
	line = re.sub(r'http[\w:/.]+',"",line)
	line = line.strip()
	return line

#Stemming of the word List by using porter stemmer
def word_stemming(wordList,myStemmer):

        
	for i,word in enumerate(wordList):
		wordList[i] =stem(word)
	
	return wordList


# remove Special words such as ['?','!','.',',','%','no','if']
def filterListofWords(all_words,SpeicalWords):
	
	all_words[:] = ifilterfalse(lambda i: (len(i)<3 ) , all_words)    
	return all_words


# In tweet we have lots of unnecessary characters
# Some hashtag contains word #Obamawin, here we need to seperate out it ["#","Obama","win"]
# remove all the 'll, 're words
# convert the data into unicode



def format_tweet(line):
	
	#still need to improve this list
	hList = ["'ve","'m","'re","'ll"]
	#line is list of words that are tokenized by nltk tokenizer

	splitList = [".","-","/","~","\\",",","is","the","_","="]

	#Regular Expression Initialization to seperate out words
	f1 = re.compile('\w+')
	f3 = re.compile('\d+')
	f2 = re.compile( '(obama|romney|\d+|mitt|barack)')

	try:
		for i,word in enumerate(line):
			line[i] = str(unicode(word, errors='ignore'))

		
		newLine = []
		for i,word in enumerate(line):

			if not(word.find('obama') > -1 or word.find('romney')>-1):
				newLine.append(word)
				continue
			else:
				newWord = " ".join(f2.split(" ".join(f1.findall(word))))
			
				newWord = newWord.strip()
				if(len(newWord) == 0):
					continue
				
				newLine.extend(newWord.split(" "))    

		line =  newLine
		
		
		# to append the username with the tag
		while( "@" in line):
			index = line.index("@")
			line[index] = line[index] + line[index+1]
			line.remove(line[index+1])

		# hashtag append
		while( "#" in line):
			index = line.index("#")
			line[index] = line[index] + line[index+1]
			line.remove(line[index+1])  
		
		# n't to not
		while( "n't" in line):
			index = line.index("n't")
			line[index] = "not"

		#remove the 's from the data
		while( "'s" in line):
			line.remove("'s")

		#please refer to this word
		for halfWord in hList:
			while(halfWord in line):
				line.remove(halfWord)

		# remvove the "hyphen" from the tweets
		matchword = '\'[\\w]*'
		
		
		for i, word in enumerate(line):
			hashOpinion = re.findall(matchword,word)
			if(len(hashOpinion) > 0):
				line[i] = word.replace("'","")


		
	except:

		return None

	return line
def clean_formatData(line):
    formated = []
    #print(line)
    try:
        label = line.pop(len(line)-1)
    except:
        return None
    if label in ClassList:
        formated.append(line)
        formated.append(label)
        return formated
    else:
        return None


