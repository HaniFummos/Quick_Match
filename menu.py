import button
import pygame
import sys

class Menu:
    def __init__(self, gameState):
        self.gameStateRun = True
        self.gameState = gameState
        pygame.init()

        self.newPos = (0,0)

        self.screen = pygame.display.set_mode((800, 450)) # 1600, 900
        self.display = pygame.Surface((400, 225)) # AAA weird scaling
        
        self.quickMatchButton = button.Button((255,255,255),110,100,180,30,40,'Quick Match') # The Quick play button
        self.quickMatchButton2 = button.Button((255,255,255),110,140,180,30,40,'Lobby') # The Quick play button
        self.quickMatchButton3 = button.Button((255,255,255),110,180,180,30,40,'Local')

        self.font = pygame.font.SysFont(None, 14) 
        
    def text(self, text, font, colour, x, y):
        img = font.render(text, True, colour)
        self.display.blit(img, (x, y))

    

    def run(self):
        while self.gameStateRun:
            self.display.fill((60, 242, 150)) # color

            self.quickMatchButton2.draw(self.display, (0,0,0))
            self.quickMatchButton2.draw(self.display, (0,0,0))
            self.quickMatchButton3.draw(self.display, (0,0,0))
            self.text("If the images aren't loading properly, please go to 'utilities.py' and change the", self.font, (0,0,0), 0, 0) # 400 / 225
            self.text("base image path", self.font, (0,0,0), 0, 11) # 400 / 225
            
            for event in pygame.event.get(): # looks through all events that are picked up
                pos = pygame.mouse.get_pos()
                self.newPos = (pos[0] / 2, pos[1] / 2) #/4 for fullscreen
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                          
                if event.type == pygame.MOUSEBUTTONUP:
                    if self.quickMatchButton2.isOver(self.newPos):
                        self.gameState.setState('joinLobby')
                        self.gameStateRun = False
                        self.newPos = (0,0)
                    if self.quickMatchButton3.isOver(self.newPos):
                        self.gameState.setState('quickMatch')
                        self.gameStateRun = False
                        self.newPos = (0,0)


            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            if self.quickMatchButton2.isOver(self.newPos):
                self.quickMatchButton2.draw(self.display, (0,0,0), True)
            elif self.quickMatchButton3.isOver(self.newPos):
                self.quickMatchButton3.draw(self.display, (0,0,0), True)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                        
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()   
        self.gameStateRun = True      

# test = Menu()
# test.run()
