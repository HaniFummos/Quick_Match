import pygame
import sys
import socket
import threading
import time

class Menu:
    def __init__(self, gameState):
        self.gameStateRun = True
        self.gameState = gameState
        pygame.init()

        self.my_ip = '127.0.0.1' # my pc's ipv4
        self.newPos = (0,0)

        self.screen = pygame.display.set_mode((800, 450)) # 1600, 900
        self.display = pygame.Surface((400, 225)) # AAA weird scaling

        self.big_font = pygame.font.SysFont(None, 75)
        self.big_font_backdrop = pygame.font.SysFont(None, 75, bold = True)
        self.timer = 0

    def text(self, text, font, colour, x, y):
        img = font.render(text, True, colour)
        self.display.blit(img, (x, y))

    def run(self, ipANDport, port):
        self.my_port = int(port) #this port must be yours
        self.opponent_ip, self.opponent_port = ipANDport.split(":")
        self.opponent_port = int(self.opponent_port)

        print(self.opponent_ip)
        print(self.opponent_port)

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # creates UDP socket
        self.socket.bind((self.my_ip, self.my_port))

        t1=threading.Thread(target=self.receiving, daemon=True)
        t1.start()

        t2=threading.Thread(target=self.sending, daemon=True)
        t2.start()

        while self.gameStateRun:
            self.display.fill((60, 242, 150)) # color

            self.text("Matchmaking...", self.big_font_backdrop, (0, 0, 0), 0, 150) # 400 / 225
            self.text("Matchmaking...", self.big_font, (255, 255, 255), 0, 150) # 400 / 225

            for event in pygame.event.get(): # looks through all events that are picked up
                if event.type == pygame.QUIT:
                    self.socket.close()
                    pygame.quit()
                    sys.exit()

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()   

        self.socket.close()
        self.gameStateRun = True    

    def receiving(self):
        while True:
            try:
                print('receiving')
                message, sender_address = self.socket.recvfrom(1024)  # change to receive the tuple bit by bit
                search = str(message)
                if 'searching' in search:
                    print('sleep')
                    time.sleep(2)
                    self.gameState.setState('YouAreBlue')
                    self.gameStateRun = False
                    self.newPos = (0,0)

                print(f"Message received from {sender_address}: {message.decode()}")  
            except:
                pass

    def sending(self):
        while True: # sending
            print('sending')
            message = 'searching'
            self.socket.sendto(message.encode(), (self.opponent_ip, self.opponent_port))     


# test = Menu()
# test.run()
