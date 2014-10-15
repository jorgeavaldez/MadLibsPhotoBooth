from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import os
import time
from TitlePicker import TitlePicker
from TitlePicker import Title
import pygame
from pygame.locals import *

# program creates final image when raw images are all available

TEMPLATE_PATH = r"D:\Github\Fall2014IDE\Fall2014IDE\Fall2014IDE\PictureManipulation\Resources\tedx2014template.png"
FONT_PATH = r"D:\Github\Fall2014IDE\Fall2014IDE\Fall2014IDE\PictureManipulation\Resources\helvetica-neue-thin.ttf"

TEST_IMG_IN_PATH = r"D:\Github\Fall2014IDE\Fall2014IDE\Fall2014IDE\PictureManipulation\Input Images\IMG0.jpg"
TEST_IMG_OUT_PATH = r"D:\Github\Fall2014IDE\Fall2014IDE\Fall2014IDE\PictureManipulation\Output Images\TEST%04d.png"

def imgout(textIn, pi1, pi2, pi3, pi4, pictureOut):

	#opens all input imgs
    originPic1 = Image.open(pi1)
    originPic1 = originPic1.rotate(270)

    originPic2 = Image.open(pi2)
    originPic2 = originPic2.rotate(270)

    originPic3 = Image.open(pi3)
    originPic3 = originPic3.rotate(270)

    originPic4 = Image.open(pi4)
    originPic4 = originPic4.rotate(270)

    #Crops the images
    head1 = originPic1.crop((0, 0, 225, 287 - 129))
    word1 = originPic1.crop((0, 287 - 129, 225, 287))

    head2 = originPic2.crop((0, 0, 225, 287 - 129))
    word2 = originPic2.crop((0, 287 - 129, 225, 287))

    head3 = originPic3.crop((0, 0, 225, 287 - 129))
    word3 = originPic3.crop((0, 287 - 129, 225, 287))

    head4 = originPic4.crop((0, 0, 225, 287 - 129))
    word4 = originPic4.crop((0, 287 - 129, 225, 287))

    #opens the template
    
    template = Image.open(TEMPLATE_PATH)

    #all headshot imgs opened to 225x287 px, word imgs open to 263x129 px:
    head1.thumbnail((225,287))
    word1.thumbnail((263,129))

    head2.thumbnail((225,287))
    word2.thumbnail((263,129))

    head3.thumbnail((225,287))
    word3.thumbnail((263,129))

    head4.thumbnail((225,287))
    word4.thumbnail((263,129))

    template.thumbnail((1400,900))

    #Draws the Background
    draw = ImageDraw.Draw(template)

    #Line draw for testing purposes
    #draw.line((0, 420, 1400, 420), 0)
    
    """
    #OLD
    #Paste images

    #Left two word board images
    template.paste(word1, (360, 41))
    template.paste(word3, (652, 41))

    #Right two word board images
    template.paste(word2, (510, 195))
    template.paste(word4, (902, 195))
    """

    #RENDER BLOCK

    currX = 100
    currY = 41

    wordPics = [word1, word2, word3, word4]
    wordPicsIndex = 0

    fontSize = 100
    helvetica = ImageFont.truetype(FONT_PATH, fontSize)

    #print(textIn.strip())
    #print(textIn.strip().split(" "))

    textInArr = textIn.strip().split(" ")

    for word in textInArr:

        if not ("{" in word):
            wordSize = draw.textsize(word, helvetica)

            if (currX + wordSize[0] >= 1300):
                if ((153 + currY) <= 500):
                    currY += 153
                    currX = 100

                else:
                    break

            draw.text((currX, currY), word, (0, 0, 0), helvetica)
            currX += wordSize[0] + 28

        else:
            if ((currX + 263) >= 1300):
                if ((153 + currY) <= 500):
                    currY += 153
                    currX = 100

                else:
                    break

            template.paste(wordPics[wordPicsIndex], (currX, (currY - (129 - 93)/2)))
            currX += 263
    #Person 1
    template.paste(head1, (143, 550))

    #Person 2
    template.paste(head2, (439, 550))

    #Person 3
    template.paste(head3, (733, 550))

    #Person 4
    template.paste(head4, (1030, 550))

    #Save the picture
    template.save(pictureOut)

def main():
    picker = TitlePicker("titles")
    titles = picker.titles

    picIndex = 0

    watchDirectoryPi1 = r"\\RASPBERRYPI\pihome\CameraBooth\Images"

    beforePi1 = dict ([(file, None) for file in os.listdir (watchDirectoryPi1)])
    beforePi2 = dict ([(file, None) for file in os.listdir (watchDirectoryPi2)])
    beforePi3 = dict ([(file, None) for file in os.listdir (watchDirectoryPi3)])
    beforePi4 = dict ([(file, None) for file in os.listdir (watchDirectoryPi4)])

    newImagesPi1 = []
    newImagesPi2 = []
    newImagesPi3 = []
    newImagesPi4 = []

    while True:
        time.sleep(10)

        afterPi1 = dict ([(file, None) for file in os.listdir (watchDirectoryPi1)])
        addedPi1 = [file for file in after if not file in beforePi1]
        removedPi1 = [file for file in before if not file in afterPi1]

        afterPi2 = dict ([(file, None) for file in os.listdir (watchDirectoryPi2)])
        addedPi2 = [file for file in after if not file in beforePi2]
        removedPi2 = [file for file in before if not file in afterPi2]

        afterPi3 = dict ([(file, None) for file in os.listdir (watchDirectoryPi3)])
        addedPi3 = [file for file in after if not file in beforePi3]
        removedPi3 = [file for file in before if not file in afterPi3]

        afterPi4 = dict ([(file, None) for file in os.listdir (watchDirectoryPi4)])
        addedPi4 = [file for file in after if not file in beforePi4]
        removedPi4 = [file for file in before if not file in afterPi4]

        if addedPi1:
            for file in added:
                if "img1" in str(file):
                    newImagesPi1.append(file)

        if addedPi2:
            for file in added:
                if "img2" in str(file):
                    newImagesPi2.append(file)

        if addedPi3:
            for file in added:
                if "img3" in str(file):
                    newImagesPi3.append(file)

        if addedPi4:
            for file in added:
                if "img3" in str(file):
                    newImagesPi4.append(file)

        if (picIndex < len(newImagesPi1)) and (picIndex < len(newImagesPi2)) and (picIndex < len(newImagesPi3)) and (picIndex < len(newImagesPi4)):
                imgOut = TEST_IMG_OUT_PATH%picIndex

                imgout(titles[picIndex], newImagesPi1[picIndex], newImagesPi2[pixIndex], newImagesPi3[picIndex], newImagesPi4[picIndex], imgOut)

                picIndex += 1

                if picIndex == len(titles):
                    picIndex = 0

                # TODO: Here's where we display the image on the TV

        before = after

#checks for new file in directory to draw
if __name__ == "__main__":
    pygame.init()

    infoObject = pygame.display.Info()
    screen = pygame.display.set_mode((1366, 768), pygame.FULLSCREEN)
    pygame.display.set_caption('TV Coolness')
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((255, 255, 255))

    screen.blit(background, (0, 0))
    pygame.display.flip()

    picker = TitlePicker("titles")

    for i in range(len(picker.titles)):
        imgout(picker.titles[i].formatTitle, TEST_IMG_IN_PATH, TEST_IMG_IN_PATH, TEST_IMG_IN_PATH, TEST_IMG_IN_PATH, (TEST_IMG_OUT_PATH%i))
        print("RENDERING TITLE NUMBER %04d\n"%i)
        background = pygame.image.load(TEST_IMG_OUT_PATH%i)
        background = pygame.transform.scale(background, (1366, 768))
        
        imageRect = background.get_rect()

        screen.blit(background, screen.get_rect())
        pygame.display.flip()
        time.sleep(5)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and event.key == K_ESCAPE:
                break