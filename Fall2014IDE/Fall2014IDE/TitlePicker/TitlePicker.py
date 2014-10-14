import io
import shelve
import pickle
import random
import string

class Title(object):

    def __init__(self, rTitle, fTitle, posList):
        self.rawTitle = rTitle
        self.formatTitle = fTitle
        self.posList = posList

    def __str__(self):
        result = "RAW TITLE: {0}\n".format(self.rawTitle)
        result += "FORMAT TITLE: {0}\n".format(self.formatTitle)
        result += "POS LIST: {0}".format(self.posList)

        return result


"""The actual title picker that returns a title to be processed."""
class TitlePicker(object):

    #Constructor
    def __init__(self, shelfname):
        self.index = 0
        self.titles = self.titleArray(shelve.open(shelfname))

    def titleArray(self, shelf):
        titles = []

        for key in shelf.keys():
            titles.append(shelf[key])

        return titles

    def getCurrentTitle(self):
        return self.titles[self.index]

    def updateTitle(self):
        self.index = (self.index + 1) % len(self.titles)