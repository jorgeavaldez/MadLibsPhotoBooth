import pygame
import os
import time
from pygame.locals import *
from subprocess import Popen
 
def main():    
    pygame.init()

    infoObject = pygame.display.Info()
    screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h), pygame.FULLSCREEN)
    pygame.display.set_caption('Basic Pygame Test')

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))

    previewBox = Rect(100, 100, 1000, 850)
    previewBox.centery = background.get_rect().centery
    pygame.draw.rect(background, (255, 255, 255), previewBox)

    pygame.font.init()
    font = pygame.font.Font("kalinga.ttf", 64)
    words = ["Hello there!", "How are you?", "Have a good day!!!", "RECT: {0}, {1}".format(previewBox.x, previewBox.y)]

    factor = 3
    for word in words:
        text = pygame.transform.rotate(font.render(word, True, (255, 255, 255)), 90)
        textpos = text.get_rect()
        textpos.centerx = background.get_rect().centerx + factor * text.get_rect().width
        textpos.centery = background.get_rect().centery
        background.blit(text, textpos)
        factor += 1
        #background.blit(text, (100, 100))

    screen.blit(background, (0, 0))
    pygame.display.flip()

    while 1:
        p = Popen(["watch", "raspistill -rot 270 -vf -hf -p '51, 100, 1000, 850'"])

        for event in pygame.event.get():
            if event.type == QUIT:
                return

            if event.type == KEYDOWN and event.key == K_ESCAPE:
                p.terminate()
                return

            if event.type == KEYDOWN and event.key == K_SPACE:
                p.terminate()
                os.system("raspistill -vf -hf -rot 270 -p '51, 100, 1000, 850'-w 1000 -h 850 -o picture1.jpg")

        screen.blit(background, (0, 0))
        pygame.display.flip()

if __name__ == '__main__': main()
