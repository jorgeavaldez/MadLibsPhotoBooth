import pygame
import time
from pygame.locals import *
import picamera
from os.path import expanduser, join
import os
import socket
import asyncore
import re

#THIS PI'S NUMBER. THIS DETERMINES THE FILE THAT'S READ FROM AND
#THE ORDER PICTURES ARE PUT ON THE FINAL IMAGE
PI_NUMBER = 1

def partOfSpeech(POS):
    if (POS == "N"):
        return "a noun"

    elif (POS == "V"):
        return "a verb"

    elif (POS == "PN"):
        return "a proper noun"

    elif (POS == "ADV"):
        return "an adverb"

    elif (POS == "ADJ"):
        return "an adjective"

    else:
        return "INVALID INPUT"

def drawWords(background, screen, phrases, timed=False):
    pygame.font.init()

    if timed: 
        factor = 2.0
        font = pygame.font.Font("kalinga.ttf", 126)
    
    else: 
        factor = 4
        font = pygame.font.Font("kalinga.ttf", 64)

    for word in phrases:
        if timed:
            text = pygame.transform.rotate(font.render(word, True, (255, 0, 0)), 90)
            textpos = text.get_rect()
            textpos.centerx = background.get_rect().centerx + factor * text.get_rect().width
            textpos.centery = background.get_rect().centery
            background.blit(text, textpos)
            factor += 0.75
            screen.blit(background, (0, 0))
            pygame.display.flip()
            if word is not "STAY STILL!!!":
                time.sleep(1)
        
        else:
            text = pygame.transform.rotate(font.render(word, True, (255, 255, 255)), 90)
            textpos = text.get_rect()
            textpos.centerx = background.get_rect().centerx + factor * text.get_rect().width
            textpos.centery = background.get_rect().centery
            background.blit(text, textpos)
            factor += 1
            #background.blit(text, (100, 100))

    screen.blit(background, (0, 0))
    pygame.display.flip()

def redrawBackground(background, screen, POS):
        background.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        
        previewBox = Rect(100, 100, 1000, 840)
        previewBox.centery = background.get_rect().centery
        pygame.draw.rect(background, (255, 255, 255), previewBox)

        pygame.font.init()
        font = pygame.font.Font("kalinga.ttf", 64)

        phrases = ["Welcome to TEDxSMU 2014!", "", "Please write {0} on the".format(partOfSpeech(POS)), "whiteboard, and then press", "the button to take a picture!"]

        drawWords(background, screen, phrases)

def main():    
    pygame.init()

    with open("rasp{0}list.txt".format(PI_NUMBER), "r") as file:
        posList = [line.strip() for line in file]

    infoObject = pygame.display.Info()
    screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h), pygame.FULLSCREEN)
    pygame.display.set_caption('Basic Pygame Test')

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))

    picNum = 0

    redrawBackground(background, screen, posList[picNum])

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

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    camera.stop_preview()
                    return

                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    camera.stop_preview()
                    return

                if event.type == KEYDOWN and event.key == K_SPACE:
                    background.fill((255, 255, 255))
                    screen.blit(background, (0, 0))
                    drawWords(background, screen, ["3", "2", "1", "STAY STILL!!!"], True)
                    pygame.display.flip()
                    camera.capture("Images/IMG{0}.jpg".format(picNum), resize=(268, 225))
                    #time.sleep(0.05)
                    background.fill((0, 0, 0))
                    picNum += 1

            screen.blit(background, (0, 0))
            redrawBackground(background, screen, posList[picNum])
            pygame.display.flip()

if __name__ == '__main__': main()