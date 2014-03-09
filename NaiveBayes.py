import nltk
import random
import scipy
import unicodedata
from nltk.stem import WordNetLemmatizer
from nltk.collocations import*
import numpy as np
import itertools

from FormatTweet import *
from ConfusionMatrix import *
from CreateFeatures import *
wordNetStemmer = WordNetLemmatizer()

##############################################################################
###     MODEL PARAMETS
##############################################################################

nFold = 10
DataSelection = 'O' #'O' for Obama, 'R' for Romney


if DataSelection == 'O':
   
    file = open("Obama.txt")
elif DataSelection == 'R':
    
    file = open("Romney.txt")
else:
    file = open("TrainMix.txt")

#################                    Global Variable
SpeicalWords = ['?','!','.',',','%','no','if']
tweetList = []
finalLine= []


##############################################################################
###     Convert the unstructured tweets into structred format
##############################################################################


for line in file:        
    
    #CONVERT TO THE LOWERCASE
    line = line.lower()
    line = cleaning_http(line)
    
    #to change to list of words
    line= nltk.sent_tokenize(line)
    line = [nltk.word_tokenize(sent) for sent in line]
        
    # to convert the List form "List of List"
    
    for l in line:
        finalLine.extend(l)
    
    finalLine = format_tweet(finalLine)
    finalLine = clean_formatData(finalLine)
     
    if not(finalLine == None):

        #STEM THE WORDS
        
        finalLine[0] = word_stemming(finalLine[0],wordNetStemmer)
        
        #CLEANING STEPS: remove the stop word from the tweet
        finalLine[0] = list(set(finalLine[0]) - set(nltk.corpus.stopwords.words('english')))
        
        #CLEANING OF SMALL WORDS PLUS SOME SPECIAL WORDS
        finalLine[0] = filterListofWords(list(finalLine[0]),SpeicalWords)

        tweetList.append(finalLine)
        
    finalLine = [] #re-initialize the variable


#######################################################################
### Create a list of features from structred Data
### 
########################################################################

total_feature_set = list(nltk.classify.apply_features(getFeatureFromTweet, tweetList))

#Shuffle the Data, so that we have randome uniform Distribution
random.shuffle(total_feature_set)
tweetList = [] #clean the memory

     
#######################################################################
### n-Fold Cross Validation. By doing cross validation on our data we
### will find the average accuracy of the model.
########################################################################


for i in range(0,nFold):
    
    lenOfFV = len(total_feature_set) #Length of Feature Vector
    
    validation_set = total_feature_set[(lenOfFV*i/nFold):(lenOfFV*(i+1)/nFold)]
    training_set = total_feature_set[:(lenOfFV*i/nFold)] + (total_feature_set[(lenOfFV*(i+1)/nFold):])
    
              
    #print "validation_set", len(validation_set), "and ","training_set", len(training_set)

            
    #######################################################################
    ### Training the Model
    ### We are using Naive Bayes Algorithms to Train the Model
    ### Now that we have our training set, we can train our classifier
    ########################################################################
    
    
    classifier = nltk.NaiveBayesClassifier.train(training_set)


    ## initialize the Confusion Matrix
    myConfusionMatrix = ConfusionMatrix()  #create a confusion matrix
    

    #Create a Confusion Matrix        
    for tweet,label in (validation_set):
    
       
        getLabel = classifier.classify((tweet))
        myConfusionMatrix.matrix[int(label)][int(getLabel)] += 1
                                
        
    print "-----------------"
    #Calculate precision,recall, fscore
    calculate_precision_recall_fscore(myConfusionMatrix.matrix)
            
    Accuracy = nltk.classify.accuracy(classifier, validation_set)
    AccuracyList.append(Accuracy)
    
    print 'Accuracy: %4.2f' % Accuracy
    print myConfusionMatrix.printMatrix()

    calculate_classDistribution(myConfusionMatrix.matrix)
    

avgAccuracy = sum(float(x) for x in AccuracyList)/nFold

print "Average accuracy is: ",avgAccuracy
file.close()
print "------"
calculateAvgPrecisionRecallFscore(ListPre_recall_fscore,nFold)
