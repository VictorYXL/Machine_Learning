import re
import numpy
from math import *
#Load dataset
def LoadDataset(fileName):
    label = []
    sentenceList = []

    file = open(fileName, "r")
    for line in file.readlines():
        label.append(int(line[0]))
        sentenceList.append(re.split('\W+',line.lower())[1:-1])
    return {'labelList':label, 'sentenceList':sentenceList}

#Get all words vector
def GetAllWords(sentenceList):
    allWords = []
    for sentence in sentenceList:
        allWords.extend(sentence)
    return set(allWords)

#Transform sentence to vector
def SentenceToVector(keywords, sentence):
    vector = numpy.zeros(len(keywords))
    for word in sentence:
        if word in keywords:
            vector[list(keywords).index(word)] = 1
        else:
            print("Word %s not in keyword list" % word)
            return None
    return vector
#P(Ci|W) = P(W|Ci)*P(Ci)/P(W) -> P(W1|Ci)*P(W2|Ci)*...*P(Wn|Ci)*P(Ci)/(P(W1)*P(W2)*...*P(Wn)) 
#Get P(Wm|Cn), P(Ci), P(Wj)
def TrainNBModel(dataset):
    allKeyWords = GetAllWords(dataset['sentenceList'])
    trainMatrix = []
    trainLabel = dataset['labelList']
    for sentence in dataset['sentenceList']:
        trainMatrix.append(SentenceToVector(allKeyWords, sentence)) 
    
    #P(Ci)
    labelCount = len(set(trainLabel))
    ciCount = numpy.zeros(labelCount)
    for label in trainLabel:
        ciCount[label] = ciCount[label] + 1
    pCi = [item / float(len(trainLabel)) for item in ciCount]
    
    #P(Wj|Ci)
    #Ones: in order to reduce the introduction of zeros when times
    pWjWhenCi = numpy.ones((labelCount, len(allKeyWords)))
    for index, sentence in enumerate(trainMatrix): 
        label = trainLabel[index]
        pWjWhenCi[label] = pWjWhenCi[label] + sentence
    for label in set(trainLabel):
        pWjWhenCi[label] = pWjWhenCi[label] / ciCount[label]
        
    #P(Wj)
    pWj = sum(trainMatrix)
    pWj = pWj / len(trainMatrix)    

    return {'AllKeywords':allKeyWords, 'PCi':pCi, 'PWjWhenCi':pWjWhenCi, 'PWj':pWj, 'label':set(trainLabel)}

#Classifier
def ClassifyByNaiveBayes(model, sentence):
    words = re.split('\W+',sentence.lower())[:-1]
    
    sentenceVector = SentenceToVector(model['AllKeywords'], words)

    #P(Ci|w)
    pCiW = numpy.ones(len(model['PCi']))
    for label in model['label']:
        for index in range(len(sentenceVector)):
            if (sentenceVector[index] == 1):
                pCiW[label] = pCiW[label] * model['PWjWhenCi'][label][index] / model['PWj'][index]
            else:
                pCiW[label] = pCiW[label] * (1 - model['PWjWhenCi'][label][index]) / (1 - model['PWj'][index])
        pCiW[label] = pCiW[label] * model['PCi'][label]
    #print pCiW
    return pCiW / sum(pCiW)


dataset = LoadDataset("Dataset.txt")
model = TrainNBModel(dataset)
#print model
print(ClassifyByNaiveBayes(model, "I love you"))
print(ClassifyByNaiveBayes(model, "I want to help you"))
print(ClassifyByNaiveBayes(model, "I want to fuck you"))
print(ClassifyByNaiveBayes(model, "Fuck this stupid dog"))
print(ClassifyByNaiveBayes(model, "Love to fuck you"))