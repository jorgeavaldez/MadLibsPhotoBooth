import Title
from textblob import TextBlob
import string

#Change path to wherever it is locally
formattedNames = open(r"D:\Github\Fall2014IDE\formattednames.txt", "r")
taggedNames = open(r"D:\Github\Fall2014IDE\taggednames.txt", "w")

print("Processing...")

for line in formattedNames:
    reformattedline = ""
    titlePOSList = []
    posTags = line.tags

    posTagCount = 0

    for word in posTags:
        pos = word[1]

        #If POS is a Noun
        if pos == "NN" or pos == "NNS":
            titlePOSList.append("N")

        #If POS is a Proper Noun
        elif pos == "NNP" or pos == "NNPS":
            titlePOSList.append("PN")

        #If POS is a Verb
        elif pos == "VB" or pos == "VBZ" or pos == "VBP" or pos == "VBD" or pos == "VBN" or pos == "VBG":
           titlePOSList.append("V")

        #If POS is a Adjective
        elif pos == "JJ" or pos == "JJR" or pos == "JJS":
            titlePOSList.append("ADJ")

        #If POS is a Adverb
        elif pos == "RB" or pos == "RBR" or pos == "RBS" or pos == "RP":
            titlePOSList.append("ADV")

        #It's none of these
        else:
            reformattedLine += word[0]

        reformattedLine += " "
        posTagCount++

print("DONE!!!")