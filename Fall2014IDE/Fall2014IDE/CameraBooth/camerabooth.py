import pygame
import time
from pygame.locals import *
import picamera
from os.path import expanduser, join
import os
import socket
import asyncore
import RPi.GPIO as GPIO
import uinput

CAMERA_BUTTON_IN = 40
CAMERA_BUTTON_OUT = 38

#THIS PI'S NUMBER. THIS DETERMINES THE FILE THAT'S READ FROM AND
#THE ORDER PICTURES ARE PUT ON THE FINAL IMAGE
PI_NUMBER = 1

#The path to where the picture should go
IMG_OUT = "Images/img" + str(PI_NUMBER) + "_{0}{1}.jpg"

def partOfSpeech(POS):
    if (POS == "N"):
        return "a NOUN"

    elif (POS == "V"):
        return "a VERB"

    elif (POS == "PN"):
        return "a PROPER NOUN"

    elif (POS == "ADV"):
        return "an ADVERB"

    elif (POS == "ADJ"):
        return "an ADJECTIVE"

    else:
        return "INVALID INPUT"

def drawWords(background, screen, phrases, timed=False):
    pygame.font.init()

    if timed: 
        factor = 2.0
        font = pygame.font.Font("helvetica-neue-thin.ttf", 126)
    
    else: 
        factor = 4.5
        font = pygame.font.Font("helvetica-neue-thin.ttf", 64)

    i = 0
    for word in phrases:
        if timed:
            text = pygame.transform.rotate(font.render(word, True, (255, 0, 0)), 90)
            textpos = text.get_rect()
            textpos.centerx = background.get_rect().centerx + factor * text.get_rect().width
            textpos.centery = background.get_rect().centery
            background.blit(text, textpos)
            factor += 1
            screen.blit(background, (0, 0))
            pygame.display.flip()

            if word is not "STAY STILL!!!":
                time.sleep(1)
        
        else:
            if i == 2:
                text = pygame.transform.rotate(font.render(word, True, (255, 0, 0)), 90)
                textpos = text.get_rect()
                textpos.centerx = background.get_rect().centerx + factor * text.get_rect().width
                textpos.centery = background.get_rect().centery
                background.blit(text, textpos)

            else:
                text = pygame.transform.rotate(font.render(word, True, (255, 255, 255)), 90)
                textpos = text.get_rect()
                textpos.centerx = background.get_rect().centerx + factor * text.get_rect().width
                textpos.centery = background.get_rect().centery
                background.blit(text, textpos)

            factor += 1.2
            #background.blit(text, (100, 100))

        i += 1

    screen.blit(background, (0, 0))
    pygame.display.flip()

def redrawBackground(background, screen, POS):
        background.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        
        previewBox = Rect(100, 100, 1000, 840)
        previewBox.centery = background.get_rect().centery
        pygame.draw.rect(background, (255, 255, 255), previewBox)

        pygame.font.init()
        font = pygame.font.Font("helvetica-neue-thin.ttf", 64)

        phrases = ["Welcome to TEDxSMU 2014!", "Please write", "{0}".format(partOfSpeech(POS)), "on the whiteboard, and then", "press the button to", "take a picture!"]

        drawWords(background, screen, phrases)

def main():    
    pygame.init()

    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(40, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

    with open("rasp{0}list.txt".format(PI_NUMBER), "r") as file:
        posList = [line.strip() for line in file]

    infoObject = pygame.display.Info()
    screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h), pygame.FULLSCREEN)
    pygame.display.set_caption('Camera Booth')

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))

    picNum = 0

    redrawBackground(background, screen, posList[picNum])

    dt = time.time();

    with picamera.PiCamera() as camera:

        camera.resolution = (1000, 800)
        camera.vflip = True
        camera.hflip = True
        camera.rotation = 90

        camera.start_preview()

        camera.preview.fullscreen = False

        camera.preview.window = (172, 40, 1000, 1000)

        #camera.preview.rotation = 270
        #camera.preview.vflip = True
        #camera.preview.hflip = True

        ui = uinput.Device([uinput.KEY_SPACE])

        def pressesSpace(channel):
            ui.emit_click(uinput.KEY_SPACE)

        GPIO.add_event_detect(40, GPIO.BOTH, callback=pressesSpace, bouncetime=300)

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    camera.stop_preview()
                    return

                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    camera.stop_preview()
                    return

                #I like to assume this is where the button callback would occur
                #I kinda just set it in a different thread

                if event.type == KEYDOWN and event.key == K_SPACE:

                    if (time.time() - dt) > 15: 
                        background.fill((255, 255, 255))
                        screen.blit(background, (0, 0))
                        drawWords(background, screen, ["3", "2", "1", "STAY STILL!!!"], True)
                        pygame.display.flip()
                        camera.capture(IMG_OUT.format(posList[picNum], "%04d"%(picNum)), resize=(268, 225))
                        #time.sleep(0.05)
                        background.fill((0, 0, 0))
                        picNum += 1
                    
                        if picNum == len(posList):
                            picNum = 0   
                            
                        dt = time.time();   

            screen.blit(background, (0, 0))
            redrawBackground(background, screen, posList[picNum])
            pygame.display.flip()

if __name__ == '__main__': main()