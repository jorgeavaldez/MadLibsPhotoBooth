import pygame
import time
from pygame.locals import *
import picamera
from os.path import expanduser, join
import os
import socket
import asyncore

""" Socket Stuff"""
UDP_IP = "192.168.1.104"
UDP_PORT = 9998

sock = socket.socket(socket.AF_INET , socket.SOCK_DGRAM)

sock.bind((UDP_IP, UDP_PORT))

"""End socket stuff"""

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

        phrases = ["Hello there!", POS, "Press SPACE to take a picture!", "Have a good day!!!"]

        drawWords(background, screen, phrases)


def main():    
    pygame.init()

    infoObject = pygame.display.Info()
    screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h), pygame.FULLSCREEN)
    pygame.display.set_caption('Basic Pygame Test')

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))

    redrawBackground(background, screen, "WAITING FOR SERVER")

    client = ServerClient("localhost", 9998)
    client.setBackground(background)
    client.setScreen(screen)
    client.setMessage("R")
    asyncore.loop()

    with picamera.PiCamera() as camera:

        camera.resolution = (1000, 800)
        camera.vflip = True
        camera.rotation = 90

        camera.start_preview()

        camera.preview.fullscreen = False

        camera.preview.window = (172, 40, 1000, 1000)

        #camera.preview.rotation = 270
        #camera.preview.vflip = True
        #camera.preview.hflip = True

        picNum = 0

        while 1:
            pos = client.getPOS()

            for event in pygame.event.get():
                if event.type == QUIT:
                    camera.stop_preview()
                    return

                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    camera.stop_preview()
                    return

                if event.type == KEYDOWN and event.key == K_SPACE and data:
                    background.fill((255, 255, 255))
                    screen.blit(background, (0, 0))
                    drawWords(background, screen, ["3", "2", "1", "STAY STILL!!!"], True)
                    pygame.display.flip()
                    camera.capture("Images/picture{0}.jpg".format(picNum), resize=(268, 225))
                    #time.sleep(0.05)
                    background.fill((0, 0, 0))
                    picNum += 1

            screen.blit(background, (0, 0))
            pygame.display.flip()

if __name__ == '__main__': main()

class ServerClient(asyncore.dispatcher):
    """Sends messages to the server and receives responses."""
    
    def __init__(self, host, port, chunk_size=512):
        self.received_data = []
        self.chunk_size = chunk_size
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, port))
        return
    
    def handle_close(self):
        self.close()
        return
    
    def writable(self):
        return bool(self.to_send)

    def handle_write(self):
        sent = self.send(self.message)

    def handle_read(self):
        data = self.recv(self.chunk_size)
        self.received_data.append(data)

    def setMessage(self, message):
        self.message = message

    def getPOS(self):
        return self.received_data.pop()

    def setBackground(self, bg):
        self.bg = bg

    def setScreen(self, scr):
        self.scr = scr