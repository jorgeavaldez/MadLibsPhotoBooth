from Title import Title
from textblob import TextBlob
import string
import json
import io

#Change path to wherever it is locally
formattedNames = open(r"D:\Github\Fall2014IDE\Resources\formattednames.txt", "r")
taggedNames = open(r"D:\Github\Fall2014IDE\Resources\taggednames.txt", "w")
jsonFile = open(r"D:\Github\Fall2014IDE\Resources\titles.json", "w")

#Makes any object json writable
def convert_to_builtin_type(obj):
    jsonFile.writelines('default(' + repr(obj) + ')')

    # Convert objects to a dictionary of their representation
    d = { '__class__':obj.__class__.__name__, 
          '__module__':obj.__module__,
          }
    d.update(obj.__dict__)
    return d

print("Processing...")

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
        json.dump(title, jsonFile, default=convert_to_builtin_type, sort_keys=True, indent=4)

print("DONE!!!")