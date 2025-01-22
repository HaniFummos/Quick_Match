import button
import pygame
import sys
import driver

class Menu:
    def __init__(self, gameState):
        self.gameStateRun = True
        self.gameState = gameState
        pygame.init()

        self.newPos = (0,0)
        self.textbox = 1

        self.screen = pygame.display.set_mode((800, 450)) # 1600, 900
        self.display = pygame.Surface((400, 225)) # AAA weird scaling
        
        self.quickMatchButtonR = button.Button((255,255,255),20,20,180,30,40,'Rejoin (Red)') # The Quick play button
        self.quickMatchButtonB = button.Button((255,255,255),210,20,180,30,40,'Rejoin (Blue)') # The Quick play button
        self.quickMatchButton0 = button.Button((255,255,255),110,60,180,30,40,'Make lobby') # The Quick play button
        self.quickMatchButton = button.Button((255,255,255),110,100,180,30,40,'Join Lobby') # The Quick play button
        self.quickMatchButton2 = button.Button((255,255,255),50,140,300,30,40,'') # The Quick play button
        self.quickMatchButton3 = button.Button((255,255,255),110,180,180,30,40,'')

    def run(self):
        while self.gameStateRun:
            self.display.fill((60, 242, 150)) # color

            self.quickMatchButtonR.draw(self.display, (0,0,0))
            self.quickMatchButtonB.draw(self.display, (0,0,0))
            self.quickMatchButton0.draw(self.display, (0,0,0))
            self.quickMatchButton.draw(self.display, (0,0,0))
            self.quickMatchButton2.draw(self.display, (0,0,0))
            self.quickMatchButton3.draw(self.display, (0,0,0))

            if self.quickMatchButtonR.isOver(self.newPos):
                self.quickMatchButtonR.draw(self.display, (0,0,0), True)
            elif self.quickMatchButtonB.isOver(self.newPos):
                self.quickMatchButtonB.draw(self.display, (0,0,0), True)
            elif self.quickMatchButton0.isOver(self.newPos):
                self.quickMatchButton0.draw(self.display, (0,0,0), True)
            elif self.quickMatchButton.isOver(self.newPos):
                self.quickMatchButton.draw(self.display, (0,0,0), True)
            if self.textbox == 1:
                    self.quickMatchButton2.draw(self.display, (0,0,0), True)
            elif self.textbox == 2:
                self.quickMatchButton3.draw(self.display, (0,0,0), True)

            for event in pygame.event.get(): # looks through all events that are picked up
                pos = pygame.mouse.get_pos()
                self.newPos = (pos[0] / 2, pos[1] / 2) #/4 for fullscreen
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONUP:
                    if self.quickMatchButtonR.isOver(self.newPos):
                        self.gameState.ip = self.quickMatchButton2.getText()
                        self.gameState.port = self.quickMatchButton3.getText()
                        self.gameState.setState('YouAreRed')
                        self.gameStateRun = False
                        self.newPos = (0,0)
                    elif self.quickMatchButtonB.isOver(self.newPos):
                        self.gameState.ip = self.quickMatchButton2.getText()
                        self.gameState.port = self.quickMatchButton3.getText()
                        self.gameState.setState('YouAreBlue')
                        self.gameStateRun = False
                        self.newPos = (0,0)    
                    elif self.quickMatchButton0.isOver(self.newPos):
                        self.gameState.ip = self.quickMatchButton2.getText()
                        self.gameState.port = self.quickMatchButton3.getText()
                        self.gameState.setState('create')
                        self.gameStateRun = False
                        self.newPos = (0,0)
                    elif self.quickMatchButton.isOver(self.newPos):
                        self.gameState.ip = self.quickMatchButton2.getText()
                        self.gameState.port = self.quickMatchButton3.getText()
                        self.gameState.setState('join')
                        self.gameStateRun = False
                        self.newPos = (0,0)
                    elif self.quickMatchButton2.isOver(self.newPos):
                        self.textbox = 1
                    elif self.quickMatchButton3.isOver(self.newPos):
                        self.textbox = 2
                    

                if event.type == pygame.KEYDOWN: # which button started getting pressed just now ?     
                    if self.textbox == 1:
                        if event.key < 58 and event.key > 47:   
                            event.key -= 48  
                            self.quickMatchButton2.changeText(str(event.key))
                        elif event.key == pygame.K_PERIOD:
                            self.quickMatchButton2.changeText('.')
                        elif event.key == pygame.K_SEMICOLON:
                            self.quickMatchButton2.changeText(':')
                        elif event.key == pygame.K_BACKSPACE:
                            self.quickMatchButton2.changeText('back')
                    if self.textbox == 2:
                        if event.key < 58 and event.key > 47: 
                            event.key -= 48  
                            self.quickMatchButton3.changeTextPORT(str(event.key))
                        elif event.key == pygame.K_BACKSPACE:
                            self.quickMatchButton3.changeTextPORT('back')
                    
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()   
        self.gameStateRun = True      

# test = Menu()
# test.run()
