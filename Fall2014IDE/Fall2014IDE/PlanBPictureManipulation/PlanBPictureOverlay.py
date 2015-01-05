from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import os
import time
from TitlePicker import TitlePicker
from TitlePicker import Title
import pygame
from pygame.locals import *
import shutil

# program creates final image when raw images are all available

TEMPLATE_PATH = r"Resources\tedx2014template.png"
FONT_PATH = r"Resources\helvetica-neue-thin.ttf"

TEST_IMG_IN_PATH = r"Input Images\IMG0.jpg"
TEST_IMG_OUT_PATH = r"Output Images\TEST%04d.png"

def generatePicture(textIn, pi1, pi2, pi3, pi4, pictureOut):

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
            wordPicsIndex += 1
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

    #Pygame init shit
    pygame.init()

    infoObject = pygame.display.Info()
    screen = pygame.display.set_mode((1366, 768), pygame.FULLSCREEN)
    pygame.display.set_caption('TV Coolness')
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((255, 255, 255))

    screen.blit(background, (0, 0))
    pygame.display.flip()

    #Begin picking out the correct titles
    picker = TitlePicker("titles")
    titles = picker.titles

    #Just to make sure
    #print(titles)

    picIndex = 0

    watchDirectoryPi1 = r"Z:\CameraBooth\Images"
    watchDirectoryPi2 = r"Y:\CameraBooth\Images"
    watchDirectoryPi3 = r"X:\CameraBooth\Images"
    watchDirectoryPi4 = r"W:\CameraBooth\Images"

    pi1ImagesIn = dict ([(file, None) for file in os.listdir (watchDirectoryPi1)])
    pi2ImagesIn = dict ([(file, None) for file in os.listdir (watchDirectoryPi2)])
    pi3ImagesIn = dict ([(file, None) for file in os.listdir (watchDirectoryPi3)])
    pi4ImagesIn = dict ([(file, None) for file in os.listdir (watchDirectoryPi4)])

    for i in range(len(titles)):

        if ((picIndex < len(titles)) and (picIndex < len(pi1ImagesIn)) and (picIndex < len(pi2ImagesIn)) and (picIndex < len(pi3ImagesIn)) and (picIndex < len(pi4ImagesIn))):
            imgOut = TEST_IMG_OUT_PATH%picIndex

            print(imgOut)
            time.sleep(5)

            rasp1formatname = "1_{0}{1}.jpg".format(titles[picIndex].posList[0], "%04d"%(picIndex))
            rasp2formatname = "2_{0}{1}.jpg".format(titles[picIndex].posList[1], "%04d"%(picIndex))
            rasp3formatname = "3_{0}{1}.jpg".format(titles[picIndex].posList[2], "%04d"%(picIndex))
            rasp4formatname = "4_{0}{1}.jpg".format(titles[picIndex].posList[3], "%04d"%(picIndex))

            generatePicture(titles[picIndex].formatTitle, os.path.join(watchDirectoryPi1, rasp1formatname), os.path.join(watchDirectoryPi2, rasp2formatname), os.path.join(watchDirectoryPi3, rasp3formatname), os.path.join(watchDirectoryPi4, rasp4formatname), imgOut)

            background = pygame.image.load(imgOut)
            background = pygame.transform.scale(background, (1366, 768))
        
            imageRect = background.get_rect()

            screen.blit(background, screen.get_rect())
            pygame.display.flip()
            time.sleep(5)
                
            picIndex += 1

            if picIndex == len(titles):
                picIndex = 0
            
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and event.key == K_ESCAPE:
                break

#checks for new file in directory to draw
if __name__ == "__main__": main()

#Old test main method
def test():

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
        generatePicture(picker.titles[i].formatTitle, TEST_IMG_IN_PATH, TEST_IMG_IN_PATH, TEST_IMG_IN_PATH, TEST_IMG_IN_PATH, (TEST_IMG_OUT_PATH%i))
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