ClassList = ['-1','1','2','0']
ListPre_recall_fscore = [] #for Storing List of Confusion Matrix
AccuracyList = []


# Accuracy Class defination
class ConfusionMatrix:
    
    
    matrix = {}

    #Initialize all the value to Zero.
    def __init__(self):
        self.matrix = {0: {0: 0, 1: 0, 2: 0, -1: 0}, 1: {0: 0, 1: 0, 2: 0, -1: 0}, 2: {0: 0, 1: 0, 2: 0, -1: 0}, -1: {0: 0, 1: 0, 2: 0, -1: 0}}

    def printMatrix(self):
        print 'Confusion Matrix:  '
        print '%8.0f' %0,'%3.0f' %1,'%3.0f' %2,'%3.0f' %-1
        for i in self.matrix:

            #print i,"  ", 
            print '%3.0f' %i,"|", (self.matrix[i]).values() 


# -------------------------------------------------------------------------------------------------------------------------------------------




#calculate precision
def calculate_precision_recall_fscore(confusionMatrix):
    #applying the formula: precision = (TP)/(TP + FP)
    #fscore = 2(Precision)(recall)/(precision+recall)
    
    dictionary = {}
    Summarydict ={}
    myKeys = confusionMatrix.keys()
    for key in ClassList:
        key = int(key)
        
        #precision
        if(sum(float(confusionMatrix[key][x]) for x in list(confusionMatrix)) == 0):
            dictionary['p'] =   None
        else:
            dictionary['p'] =   round(confusionMatrix[key][key]/(sum(float(confusionMatrix[key][x]) for x in list(confusionMatrix))),2)

        #recall
        if(sum(float(confusionMatrix[x][key]) for x in list(confusionMatrix)) == 0):
            dictionary['r'] = None
        else:
            dictionary['r'] =   round(confusionMatrix[key][key]/(sum(float(confusionMatrix[x][key]) for x in list(confusionMatrix))),2)

        #fscore
        if( dictionary['r'] == None or dictionary['p'] == None):
            dictionary['f'] = None
        else:
            dictionary['f'] =  round(2*dictionary['r']*dictionary['p'] /(dictionary['p']+dictionary['r']),2)
        
   
        
        print "For Class- ", key," (p = ", dictionary['p'] ,", r = ", dictionary['r'] ,", f-score = ",dictionary['f'] ,")"
        #return dictionary['f']
        Summarydict[key] = dictionary
        
        
        dictionary ={}
    
    ListPre_recall_fscore.append(Summarydict)
    Summarydict = {}      


def calculateAvgPrecisionRecallFscore(ListPre_recall_fscore,nFold):
    myList = ['p','r','f']
    FinalTable = {0: {'p': 0, 'r': 0, 'f': 0}, 1: {'p': 0, 'r': 0, 'f': 0}, 2: {'p': 0, 'r': 0, 'f': 0}, -1: {'p': 0, 'r': 0, 'f': 0}}
   
    for label in ClassList:
        for i in range(nFold):
            for par in myList:
                
                FinalTable[int(label)][par] += ListPre_recall_fscore[i][int(label)][par]
        # avg out
        for par in myList:
            FinalTable[int(label)][par] = round(FinalTable[int(label)][par]/nFold,2)
    print "Average precision, recall and f-score is: "
    for label in ClassList:
        print "for Class: ",label," ", FinalTable[int(label)]
    
                
#calculate classdistribution
def calculate_classDistribution(confusionMatrix):
    myKeys = confusionMatrix.keys()
    labelClass = {}
    for key in myKeys:
        labelClass[key] = sum(confusionMatrix[key][x] for x in list(confusionMatrix[key]))
    print labelClass
    return labelClass
    


