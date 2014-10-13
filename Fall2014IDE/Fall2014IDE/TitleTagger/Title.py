from textblob import TextBlob
import string
import json
import io

#Abstraction of the things we need for our titles
#This can be rebuilt using the code I found online ;)

class Title(object):
    """Title Abstraction"""

    def __init__(self, rTitle, fTitle, posList):
        self.rawTitle = rTitle
        self.formatTitle = fTitle
        self.posList = posList