from PIL import Image
import os
import glob

class PictureManager(object):

    Y_LIMIT = 481
    faceBoxes = [(143, 174, 225, 287), (438, 174, 225, 287), (734, 174, 225, 287), (1029, 174, 225, 287)]

    def __init__(self, path):
        self.path = path
        self.dataFiles = os.listdir(path)
        self.newestImage = Image.open(max(glob.iglob(os.path.join(directory, '*.jpeg')), key=os.path.getctime))
        self.templateImage = Image.open("D:\Github\Fall2014IDE\Fall2014IDE\Fall2014IDE\PictureManipulation\Template Images\tedx2014template.png")
        self.outputImage = templateImage.copy()

    def cutWord(self):
        self.newestImage.crop(