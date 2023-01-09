import sys, string, json
import os
import re
from collections import defaultdict


def AllFilesFunc(directory):
    f = []
    for root, dirs, files in os.walk(directory):
        # print(root,"Directory", dirs,"Files", files)
        for file in files:
            if file.endswith(".txt"):
                if "fold1" not in os.path.join(root, file):
                    f.append(os.path.join(root, file))
                # f_dict[os.path.join(root, file)]={'v1': , 'v2': }
    return f


f1 = AllFilesFunc(sys.argv[1] + "/positive_polarity")
f2 = AllFilesFunc(sys.argv[1] + "/negative_polarity")

# print(f1)

all_files = f1 + f2

# print(all_files)

# for i in all_files:
# print(i)


labeldict = {}
for f in all_files:
    # print(f)
    class1, class2, fold, fname = f.split("/")[-4:]
    if class1 in "positive_polarity":
        if class2 in "truthful_from_TripAdvisor":
            labeldict[f] = {'v1': 'truthful', 'v2': 'positive'}
        else:
            labeldict[f] = {'v1': 'deceptive', 'v2': 'positive'}
    else:
        if class2 in "truthful_from_Web":
            labeldict[f] = {'v1': 'truthful', 'v2': 'negative'}
        else:
            labeldict[f] = {'v1': 'deceptive', 'v2': 'negative'}

# print(labeldict)

stopword = ['a', 'able', 'about', 'above', 'across', 'again', "ain't", 'all', 'almost', 'along', 'also', 'am', 'among',
            'amongst', 'an', 'and', 'anyhow', 'anyone', 'anyway', 'anyways', 'appear', 'are', 'around', 'as', "a's",
            'aside', 'ask', 'asking', 'at', 'away', 'be', 'became', 'because', 'become', 'becomes', 'becoming', 'been',
            'before', 'behind', 'below', 'beside', 'besides', 'between', 'beyond', 'both', 'brief', 'but', 'by', 'came',
            'can', 'come', 'comes', 'consider', 'considering', 'corresponding', 'could', 'do', 'does', 'doing', 'done',
            'down', 'downwards', 'during', 'each', 'edu', 'eg', 'eight', 'either', 'else', 'elsewhere', 'etc', 'even',
            'ever', 'every', 'ex', 'few', 'followed', 'following', 'follows', 'for', 'former', 'formerly', 'from',
            'further', 'furthermore', 'get', 'gets', 'getting', 'given', 'gives', 'go', 'goes', 'going', 'gone', 'got',
            'gotten', 'happens', 'has', 'have', 'having', 'he', 'hed', 'hence', 'her', 'here', 'hereafter', 'hereby',
            'herein', "here's", 'hereupon', 'hers', 'herself', "he's", 'hi', 'him', 'himself', 'his', 'how', 'hows',
            'i', "i'd", 'ie', 'if', "i'll", "i'm", 'in', 'inc', 'indeed', 'into', 'inward', 'is', 'it', "it'd", "it'll",
            'its', "it's", 'itself', "i've", 'keep', 'keeps', 'kept', 'know', 'known', 'knows', 'lately', 'later',
            'latter', 'latterly', 'lest', 'let', "let's", 'looking', 'looks', 'ltd', 'may', 'maybe', 'me', 'mean',
            'meanwhile', 'might', 'most', 'my', 'myself', 'name', 'namely', 'nd', 'near', 'nearly', 'need', 'needs',
            'neither', 'next', 'nine', 'no', 'non', 'now', 'nowhere', 'of', 'off', 'often', 'oh', 'ok', 'okay', 'old',
            'on', 'once', 'one', 'ones', 'only', 'onto', 'or', 'other', 'others', 'ought', 'our', 'ours', 'ourselves',
            'out', 'over', 'own', 'per', 'placed', 'que', 'quite', 're', 'regarding', 'said', 'same', 'saw', 'say',
            'saying', 'says', 'second', 'secondly', 'see', 'seeing', 'seem', 'seemed', 'seeming', 'seems', 'seen',
            'self', 'selves', 'sensible', 'sent', 'seven', 'several', 'she', "she'd", "she'll", "she's", 'since', 'six',
            'so', 'some', 'somebody', 'somehow', 'someone', 'something', 'sometime', 'sometimes', 'somewhat',
            'somewhere', 'soon', 'specified', 'specify', 'specifying', 'still', 'sub', 'such', 'sup', 'sure', 'take',
            'taken', 'tell', 'tends', 'th', 'than', 'that', 'thats', "that's", 'the', 'their', 'theirs', 'them',
            'themselves', 'then', 'thence', 'there', 'thereafter', 'thereby', 'therefore', 'therein', 'theres',
            "there's", 'thereupon', 'these', 'they', "they'd", "they'll", "they're", "they've", 'think', 'third',
            'this', 'those', 'though', 'three', 'through', 'thru', 'thus', 'to', 'together', 'too', 'took', 'toward',
            'towards', 'tried', 'tries', 'truly', 'try', 'trying', "t's", 'twice', 'two', 'un', 'under', 'up', 'upon',
            'us', 'use', 'used', 'uses', 'using', 'usually', 'value', 'various', 'very', 'via', 'viz', 'vs', 'want',
            'wants', 'was', "wasn't", 'way', 'we', "we'd", "we'll", 'went', 'were', "we're", "weren't", "we've", 'what',
            'whatever', "what's", 'when', 'whence', 'whenever', "when's", 'where', 'whereafter', 'whereas', 'whereby',
            'wherein', "where's", 'whereupon', 'wherever', 'whether', 'which', 'while', 'whither', 'who', 'whoever',
            'whole', 'whom', "who's", 'whose', 'why', "why's", 'will', 'willing', 'wish', 'with', 'within', 'without',
            "won't", 'would', "wouldn't", 'yes', 'yet', 'you', "you'd", "you'll", 'your', "you're", 'yours', 'yourself',
            'yourselves', "you've"]

tempDict = dict()


# Properly assigning labels to the specific tokenList generated from specific folder
def LabelsDictFunc(label, tokenList):
    if (labeldict[file][label]) == 'positive':
        wordDict(tokenList, 0)
    if (labeldict[file][label]) == 'negative':
        wordDict(tokenList, 1)
    if (labeldict[file][label]) == 'truthful':
        wordDict(tokenList, 2)
    if (labeldict[file][label]) == 'deceptive':
        wordDict(tokenList, 3)


# Creating a global token dict
def wordDict(tokenList, index):
    global cpos, cneg, cdef, ctru
    for token in tokenList:
        if (token in tempDict):
            tempDict[token][index] = int(tempDict[token][index]) + int('1')
        else:
            tempDict[token] = [0, 0, 0, 0]
            tempDict[token][index] = int(tempDict[token][index]) + int('1')


for file in all_files:
    f = open(file, "r").read()
    # print(f)
    newline = re.sub('[^a-zA-Z]', ' ', f)
    tokenList = [word for word in newline.split() if ((word not in stopword) and (word.isalnum()))]
    # tokenList = [word for word in newline.split() if (word.isalnum())]
    tokenList = ' '.join([i for i in tokenList if not i.isdigit()])
    tokenList = tokenList.split()
    # print(tokenList)
    if (file in labeldict.keys()):
        LabelsDictFunc('v1', tokenList)
        LabelsDictFunc('v2', tokenList)


# print(tempDict)

# Smoothing
def smoothing():
    for key, val in tempDict.items():
        for i in range(0, 4):
            tempDict[key][i] += 1


smoothing()

newcpos = 0
newctru = 0
newcneg = 0
newcdef = 0


def LabelCounterFunc():
    global newcneg, newcpos, newcdef, newctru
    for key, val in tempDict.items():
        newcpos += val[0]
        newcneg += val[1]
        newctru += val[2]
        newcdef += val[3]


LabelCounterFunc()


# print(newcpos)
# print(newcneg)
# print(newctru)
# print(newcdef)


def ProbCalculator():
    for key, val in tempDict.items():
        tempDict[key][0] /= float(newcpos)
        tempDict[key][1] /= float(newcneg)
        tempDict[key][2] /= float(newctru)
        tempDict[key][3] /= float(newcdef)


ProbCalculator()

# print(tempDict)

totalProb = newcpos + newcneg
totalProb2 = newcdef + newctru
ClassProbabilityDict = {}
ClassProbabilityDict['positive'] = newcpos / float(totalProb)
ClassProbabilityDict['negative'] = newcneg / float(totalProb)
ClassProbabilityDict['truthful'] = newctru / float(totalProb2)
ClassProbabilityDict['deceptive'] = newcdef / float(totalProb2)

# print(ClassProbabilityDict['deceptive'])


with open("nbmodel.txt", "w") as f:
    f.write("Prior Class Probabilities" + '\n')
    for key, value in ClassProbabilityDict.items():
        f.write('%s:%s\n' % (key, value))
    for key, value in tempDict.items():
        f.write('%s:%s\n' % (key, value))

