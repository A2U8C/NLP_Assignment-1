import sys
import string
import json
import math
import os
import re


#stopwords
stopword=['a', 'able', 'about', 'above', 'across', 'again', "ain't", 'all', 'almost', 'along', 'also', 'am', 'among', 'amongst', 'an', 'and', 'anyhow', 'anyone', 'anyway', 'anyways', 'appear', 'are', 'around', 'as', "a's", 'aside', 'ask', 'asking', 'at', 'away', 'be', 'became', 'because', 'become', 'becomes', 'becoming', 'been', 'before', 'behind', 'below', 'beside', 'besides', 'between', 'beyond', 'both', 'brief', 'but', 'by', 'came', 'can', 'come', 'comes', 'consider', 'considering', 'corresponding', 'could', 'do', 'does', 'doing', 'done', 'down', 'downwards', 'during', 'each', 'edu', 'eg', 'eight', 'either', 'else', 'elsewhere', 'etc', 'even', 'ever', 'every', 'ex', 'few', 'followed', 'following', 'follows', 'for', 'former', 'formerly', 'from', 'further', 'furthermore', 'get', 'gets', 'getting', 'given', 'gives', 'go', 'goes', 'going', 'gone', 'got', 'gotten', 'happens', 'has', 'have', 'having', 'he', 'hed', 'hence', 'her', 'here', 'hereafter', 'hereby', 'herein', "here's", 'hereupon', 'hers', 'herself', "he's", 'hi', 'him', 'himself', 'his', 'how', 'hows', 'i', "i'd", 'ie', 'if', "i'll", "i'm", 'in', 'inc', 'indeed', 'into', 'inward', 'is', 'it', "it'd", "it'll", 'its', "it's", 'itself', "i've", 'keep', 'keeps', 'kept', 'know', 'known', 'knows', 'lately', 'later', 'latter', 'latterly', 'lest', 'let', "let's", 'looking', 'looks', 'ltd', 'may', 'maybe', 'me', 'mean', 'meanwhile', 'might', 'most', 'my', 'myself', 'name', 'namely', 'nd', 'near', 'nearly', 'need', 'needs', 'neither', 'next', 'nine', 'no', 'non', 'now', 'nowhere', 'of', 'off', 'often', 'oh', 'ok', 'okay', 'old', 'on', 'once', 'one', 'ones', 'only', 'onto', 'or', 'other', 'others', 'ought', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 'per', 'placed', 'que', 'quite', 're', 'regarding', 'said', 'same', 'saw', 'say', 'saying', 'says', 'second', 'secondly', 'see', 'seeing', 'seem', 'seemed', 'seeming', 'seems', 'seen', 'self', 'selves', 'sensible', 'sent', 'seven', 'several', 'she', "she'd", "she'll", "she's", 'since', 'six', 'so', 'some', 'somebody', 'somehow', 'someone', 'something', 'sometime', 'sometimes', 'somewhat', 'somewhere', 'soon', 'specified', 'specify', 'specifying', 'still', 'sub', 'such', 'sup', 'sure', 'take', 'taken', 'tell', 'tends', 'th', 'than', 'that', 'thats', "that's", 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'thence', 'there', 'thereafter', 'thereby', 'therefore', 'therein', 'theres', "there's", 'thereupon', 'these', 'they', "they'd", "they'll", "they're", "they've", 'think', 'third', 'this', 'those', 'though', 'three', 'through', 'thru', 'thus', 'to', 'together', 'too', 'took', 'toward', 'towards', 'tried', 'tries', 'truly', 'try', 'trying', "t's", 'twice', 'two', 'un', 'under', 'up', 'upon', 'us', 'use', 'used', 'uses', 'using', 'usually', 'value', 'various', 'very', 'via', 'viz', 'vs', 'want', 'wants', 'was', "wasn't", 'way', 'we', "we'd", "we'll", 'went', 'were', "we're", "weren't", "we've", 'what', 'whatever', "what's", 'when', 'whence', 'whenever', "when's", 'where', 'whereafter', 'whereas', 'whereby', 'wherein', "where's", 'whereupon', 'wherever', 'whether', 'which', 'while', 'whither', 'who', 'whoever', 'whole', 'whom', "who's", 'whose', 'why', "why's", 'will', 'willing', 'wish', 'with', 'within', 'without', "won't", 'would', "wouldn't", 'yes', 'yet', 'you', "you'd", "you'll", 'your', "you're", 'yours', 'yourself', 'yourselves', "you've"]



#nbmodel.txt read: (Result of nblearn.py)
tempDict = dict()
ClassProb = dict()
count = 0

with open("nbmodel.txt","r") as f:
    for item in f:
        if ':' in item:
            key,value = item.split(':', 1)
            if(count<=4):
                ClassProb[key] = value.strip(' ')
            else:
                value= value.strip('[').replace(']','')
                tempDict[key] =[(x.strip(' ')) for x in value.split(',')]
        count += 1

pos_score =0
neg_score =0
truth_score =0
decept_score =0




def AllFilesFunc(directory):
    locList = []
    for root, dirs, files in os.walk(directory):
        #print(root,"Directory", dirs,"Files", files)
        for file in files:
            if file.endswith(".txt") and "README.txt" not in os.path.join(root, file):
                locList.append(os.path.join(root, file))
    return locList


all_files=AllFilesFunc(sys.argv[1])

#print(all_files)
#print(len(all_files))



#training data file
def ClassificationFunc(all_files):
    f1=open("nboutput.txt","w")
    #if not f1.closed:
    #    print('file is opened')
    global pos_score,neg_score,truth_score,decept_score
    for file in all_files:
        f = open(file, "r").read()
        newline = re.sub('[^a-zA-Z]', ' ', f)
        tokenList = [word for word in newline.split() if ((word not in stopword) and (word.isalnum()))]
        #tokenList = [word for word in newline.split() if (word.isalnum())]
        tokenList = ' '.join([i for i in tokenList if not i.isdigit()])
        tokenList = tokenList.split()
        pos_score = 0
        decept_score = 0
        truth_score = 0
        neg_score = 0
        for token in tokenList:
            if (token in tempDict):
                pos_score += math.log(float(tempDict[token][0]))
                neg_score += math.log(float (tempDict[token][1]))
                truth_score += math.log(float(tempDict[token][2]))
                decept_score += math.log(float( tempDict[token][3]))
        pos_score += math.log(float(ClassProb['positive']))
        neg_score += math.log(float(ClassProb['negative']))
        truth_score += math.log(float(ClassProb['truthful']))
        decept_score += math.log(float(ClassProb['deceptive']))
        label_Truth_Decept = "truthful" if (truth_score > decept_score) else "deceptive"
        label_Pos_Neg = "positive" if (pos_score > neg_score) else "negative"
        f1.write(label_Truth_Decept.strip()+" "+label_Pos_Neg.strip()+" "+file)
        f1.write('\n')

ClassificationFunc(all_files)