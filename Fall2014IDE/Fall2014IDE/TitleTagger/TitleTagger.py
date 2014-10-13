from textblob import TextBlob
import string
import pickle
import shelve
import io

class Title(object):
    """Title Abstraction"""

    def __init__(self, rTitle, fTitle, posList):
        self.rawTitle = rTitle
        self.formatTitle = fTitle
        self.posList = posList

    def __str__(self):
        result = "RAW TITLE: {0}\n".format(self.rawTitle)
        result += "FORMAT TITLE: {0}\n".format(self.formatTitle)
        result += "POS LIST: {0}".format(self.posList)

        return result

#Change path to wherever it is locally
formattedNames = open(r"D:\Github\Fall2014IDE\Resources\formattednames.txt", "r")
taggedNames = open(r"D:\Github\Fall2014IDE\Resources\taggednames.txt", "w")

titleshelf = shelve.open("titles")

print("Processing...")

i = 0
for line in formattedNames:
    reformattedline = ""
    titlePOSList = []
    posTags = TextBlob(line).tags

    posTagCount = 0

    for word in posTags:
        pos = word[1]
        foundPOSTag = False

        #If POS is a Noun
        if posTagCount < 4 and pos == "NN" or pos == "NNS":
            titlePOSList.append("N")
            reformattedline += "{" + str(posTagCount) + "}"
            foundPOSTag = True

        #If POS is a Proper Noun
        elif posTagCount < 4 and pos == "NNP" or pos == "NNPS":
            titlePOSList.append("PN")
            reformattedline += "{" + str(posTagCount) + "}"
            foundPOSTag = True

        #If POS is a Verb
        elif posTagCount < 4 and pos == "VB" or pos == "VBZ" or pos == "VBP" or pos == "VBD" or pos == "VBN" or pos == "VBG":
           titlePOSList.append("V")
           reformattedline += "{" + str(posTagCount) + "}"
           foundPOSTag = True

        #If POS is a Adjective
        elif posTagCount < 4 and pos == "JJ" or pos == "JJR" or pos == "JJS":
            titlePOSList.append("ADJ")
            reformattedline += "{" + str(posTagCount) + "}"
            foundPOSTag = True

        #If POS is a Adverb
        elif posTagCount < 4 and pos == "RB" or pos == "RBR" or pos == "RBS" or pos == "RP":
            titlePOSList.append("ADV")
            reformattedline += "{" + str(posTagCount) + "}"
            foundPOSTag = True

        #It's none of these
        else:
            reformattedline += word[0]
        
        reformattedline += " "

        if foundPOSTag:
            posTagCount += 1
    
    if (len(titlePOSList) == 4):
        title = Title(line.replace("\n", ""), reformattedline, titlePOSList)
        titleshelf[str(i)] = title

        i += 1
        

print("DONE!!!")

#http://pymotw.com/2/json/