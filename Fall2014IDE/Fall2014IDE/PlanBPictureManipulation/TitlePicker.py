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

def main():
    picker = TitlePicker("titles")

    rasp1List = open("rasp1list.txt", "w")
    rasp2List = open("rasp2list.txt", "w")
    rasp3List = open("rasp3list.txt", "w")
    rasp4List = open("rasp4list.txt", "w")

    for i in range(len(picker.titles)):
        title = picker.titles[i]

        print("Opened title: " + str(title) + "\n")
        posList = title.posList

        rasp1List.writelines(posList[0] + "\n")
        print("Wrote {0} to {1}".format(posList[0], "rasp1List"))

        rasp2List.writelines(posList[1] + "\n")
        print("Wrote {0} to {1}".format(posList[1], "rasp2List"))

        rasp3List.writelines(posList[2] + "\n")
        print("Wrote {0} to {1}".format(posList[2], "rasp3List"))

        rasp4List.writelines(posList[3] + "\n")
        print("Wrote {0} to {1}".format(posList[3], "rasp4List"))

        print("\n")

if __name__ == "__main__": main()