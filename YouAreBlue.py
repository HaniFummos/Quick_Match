import sys
import pygame
import time
import threading
import socket
import random

from player import PhysicsEntity
from game_logic import Logic
from utilities import load_white_image, load_black_image, load_images, Animation
from tilemap import Tilemap

class Game:
    def __init__(self, gameState):
        self.gameStateRun = True
        self.gameState = gameState
        pygame.init()

        self.screen = pygame.display.set_mode((800, 450)) # 1600, 900
        self.display = pygame.Surface((400, 225)) # AAA weird scaling

        pygame.display.set_caption('Quick Match')
        self.clock = pygame.time.Clock()
        


        self.assets = { # dictionary of key-value pairs
            'THESUN' : load_black_image('THESUN.png'),
            'player' : load_white_image('player.png'),
            'player2' : load_white_image('player2.png'),   
            'grass' : load_images('tiles/grass'),
            'player/idle' : Animation(load_images('player/idle'), img_dur = 6),
            'player/walk' : Animation(load_images('player/walk'), img_dur = 4), 
            'player/jump' : Animation(load_images('player/jump'), img_dur = 4),
            'player/tumble' : Animation(load_images('player/tumble'), img_dur = 4),
            'player/sideHit' : Animation(load_images('player/sideHit'), img_dur = 2),
            'player/vertHit' : Animation(load_images('player/vertHit'), img_dur = 2),
            'player2/idle' : Animation(load_images('player2/idle'), img_dur = 6),
            'player2/walk' : Animation(load_images('player2/walk'), img_dur = 4), 
            'player2/jump' : Animation(load_images('player2/jump'), img_dur = 4),
            'player2/tumble' : Animation(load_images('player2/tumble'), img_dur = 4),
            'player2/sideHit' : Animation(load_images('player2/sideHit'), img_dur = 2),
            'player2/vertHit' : Animation(load_images('player2/vertHit'), img_dur = 2),
        }

        self.player = PhysicsEntity(self, 'player', (80+48, 128), (7, 16))
        self.player2 = PhysicsEntity(self, 'player2', (311-48, 128), (7, 16))
        self.tilemap = Tilemap(self, tile_size=16)
        self.gameLogic = Logic(self)

        self.stop = False

        self.my_ip = '127.0.0.1'
        self.message = '128,112,False,none'

        self.sun = self.assets['THESUN']
        self.stockIcon = self.assets['player']
        self.stockIcon2 = self.assets['player2']

        self.online = False
        self.online2 = True

        self.random = 0

        self.start = False

        self.font = pygame.font.SysFont(None, 30)

        self.big_font = pygame.font.SysFont(None, 150)
        self.big_font_backdrop = pygame.font.SysFont(None, 155, bold = True)

        pygame.display.set_icon(self.sun)  
        
    def text(self, text, font, colour, x, y):
        img = font.render(text, True, colour)
        self.display.blit(img, (x, y))

    def run(self, ipANDport, port):
        self.my_port = int(port) #this port must be yours
        self.opponent_ip, self.opponent_port = ipANDport.split(":")
        self.opponent_port = int(self.opponent_port)

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # creates UDP socket
        self.socket.bind((self.my_ip, self.my_port))

        t1=threading.Thread(target=self.receiving, daemon=True)
        t1.start()

        t2=threading.Thread(target=self.sending, daemon=True)
        t2.start()

        self.player.playerDefaultDirection()
        self.player2.player2DefaultDirection()
        while self.gameStateRun:
            self.display.fill((100, 255, 255))
            self.tilemap.render(self.display) 

            self.randomnum = random.random()

            self.VARIABLES = self.message.split(',') # 1/2 = pos | 3 = flip | 4 = move

            self.player.pos = [float(self.VARIABLES[0]), float(self.VARIABLES[1])]
            if self.VARIABLES[2] == 'True':
                self.player.flip = True
            else:
                self.player.flip = False


            key = pygame.key.get_pressed()
            if key[pygame.K_1] == True:
                self.stop = True
            else:
                self.stop = False

            self.gameLogic.eventloop()
            self.gameLogic.gameStateLoop()

            youcanplay = self.gameLogic.awesometext()
            if youcanplay:
                self.gameLogic.controlLoop()  
              
      
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)
        self.gameLogic.resetGame()
        self.matchStartTimer = 0
        self.gameStateRun = True


    def receiving(self):
        time.sleep(0.1)
        while True:
            try:
                message, sender_address = self.socket.recvfrom(1024)  # change to receive the tuple bit by bit
                self.message = message.decode()
                #print(f"Message received from {sender_address}: {message.decode()}")  
            except:
                pass

    def sending(self):
        time.sleep(0.1)
        while True: # sending
            if self.stop == False or self.randomnum < 0.25:
                message = str(self.player2.pos[0]) + ',' + str(self.player2.pos[1]) + ',' + str(self.player2.flip) + ',' + str(self.gameLogic.move)
                self.socket.sendto(message.encode(), (self.opponent_ip, self.opponent_port))
                time.sleep(0.0167)
