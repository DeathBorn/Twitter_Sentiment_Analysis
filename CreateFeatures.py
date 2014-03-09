from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk.collocations import*
from nltk.corpus import wordnet
from sentiwordnet import SentiWordNetCorpusReader, SentiSynset
import itertools
import re

negWordfile = "negative-words.txt"
posWordfile = "positive-words.txt"
swn_filename = 'SentiWordNet_3.0.0_20121119.txt'  #Sentiword net dictionary




swn = SentiWordNetCorpusReader(swn_filename)

#function List
def createWordList(wordfileName):
    #This file assume that words in the files are sperated by "enter" = "\n" delimeter
    wordfile = open(wordfileName,'r')
    
    wordlist = []

    for word in wordfile:
        word = word.replace("\n","")
                 
        wordlist.append(word)
        
    wordfile.close()
    return wordlist


NEG_WORDS = createWordList(negWordfile)
POS_WORDS = createWordList(posWordfile)


def get_words_in_tweets(tweets):
    all_words = []
      
    for (words, sentiment) in tweets:
      labelCount[int(sentiment)] += 1
      all_words.extend(words)
      
      
    return all_words


def entity_extraction(all_words,matchword):
    extracted_entities = []
    matchword = r'[\w]*'+matchword+'[\w]*'
    for word in all_words:
        
        if(len(re.findall(matchword,word)) > 0):
            extracted_entities.append(word)
            
    return list(set(extracted_entities))


def getFeatureFromTweet(tweet):
    
    icount = 0
    inotFound = 0
    iProfDictFound = 0
    features = {}
    senti= ""

    
    features =  bigram_word_feats(tweet, score_fn=BigramAssocMeasures.chi_sq, n=200)
    
    SentimentDict = {'p':0, 'n':0,'o':0}
    if len(entity_extraction(tweet,'bama'))> 0:
        features['oba'] = True
    else:
        features['oba'] = False
    if len(entity_extraction(tweet,'mney'))> 0:
        features['rom'] = True
    else:
        features['rom'] = False
       
    if ("?" in tweet> 0):
        features['?!'] = True
    else:
        features['?!'] = False
        


    for word in tweet:
        if(checkEnglishWord(word)):
            try:
                if(word in NEG_WORDS or word in POS_WORDS):
                        iProfDictFound = iProfDictFound +1
                    
                senti = swn.senti_synsets(word)[0]
                SentimentDict['p'] += senti.pos_score
                SentimentDict['n'] += senti.neg_score
                SentimentDict['o'] += senti.obj_score
                    
                    
                icount = icount + 1
            except:

                inotFound = inotFound  +1

    if(len(entity_extraction(tweet,'mney'))> 0 and len(entity_extraction(tweet,'bama'))> 0):
        features['Mix'] = True
    else:
        features['Mix'] = False

        if(SentimentDict['p'] > SentimentDict['n']):
            features['Pos'] = True
        else:
           features['Neg'] = True
    

    return features
                   


def bigram_word_feats(words, score_fn=BigramAssocMeasures.chi_sq, n=300):
    bigram_finder = BigramCollocationFinder.from_words(words)
    bigrams = bigram_finder.nbest(score_fn, n)
    return dict([(ngram, True) for ngram in itertools.chain(words, bigrams)])



#Classifier feature functions

def get_words_in_tweets(tweets):
    all_words = []
      
    for (words, sentiment) in tweets:
      labelCount[int(sentiment)] += 1
      all_words.extend(words)
      
      
    return all_words


def get_word_features(wordlist):
    #print(len(wordlist))
    
    wordlist = nltk.FreqDist(wordlist)
    word_features = wordlist.keys()
    x = wordlist.values()
    
    return word_features
def calculateFreqDist(wordlist):
    wordFreq = []
    wordFreq = nltk.FreqDist(wordlist)
    return wordFreq



#using Wordnet Synset to see, if a word is present in english dictionary
def checkEnglishWord(word):
    if not wordnet.synsets(word):
      return False
    else:
      return True


  
