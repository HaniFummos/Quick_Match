import pygame
import sys
from player import PhysicsEntity

class Logic:
    def __init__(self, game):
        self.game = game
        self.globalTimer = 0
        
        self.movement = [False, False]
        self.movement2 = [False, False]
        self.lastPressedDirection = 'right'
        self.lastPressedDirection2 = 'left'
        self.currentdirections = 'right'
        self.currentdirections2 = 'left'

        self.wahoo = 1
        self.wahoo2 = 1

        self.move0 = 'none'
        self.move = 'none'
        
        self.damage = 0
        self.damage2 = 0

        self.windup0 = 0
        self.windup = 0
        

        self.down0 = False
        self.down = False
        

        self.inAMove0 = False
        self.inAMoveTimer0 = 0
        self.inAMove = False
        self.inAMoveTimer = 0

        self.stocks = 3
        self.stocks2 = 3

        self.wholeLag0 = 0
        self.wholeLag = 0

        self.player_hitbox = self.game.player.rect()
        self.player2_hitbox = self.game.player2.rect()

        self.matchStartTimer = 0
        self.f=0 # colour fade

    def gameStateLoop(self):
        self.player_hitbox = self.game.player.rect()
        self.player2_hitbox = self.game.player2.rect()

        self.globalTimer+= 1
        if self.globalTimer > 59: # if 60.....
            self.globalTimer = 0

        self.dead = self.game.player.update(self.game.tilemap, (self.movement[1] - self.movement[0], 0), self.wahoo) #calls update
        self.dead2 = self.game.player2.update(self.game.tilemap, (self.movement2[1] - self.movement2[0], 0), self.wahoo2) 

        self.wahoo = .9 # reset running
        self.wahoo2 = .9
        self.movement2 = [False, False]
        self.movement = [False, False]

        if self.globalTimer %2 == 1: # alternate rendering ! :)
            self.game.player.render(self.game.display)
            self.game.player2.render(self.game.display) 
        else:
            self.game.player2.render(self.game.display)
            self.game.player.render(self.game.display)    

        if self.dead == True:
            self.stocks -= 1
            self.damage = 0
        if self.dead2 == True:
            self.stocks2 -= 1
            self.damage2 = 0

        if self.stocks < 1 or self.stocks2 < 1: # reset game
            self.game.gameState.setState('start')
            self.game.gameStateRun = False
        
        for i in range(2):
            if i == 1:
                horizon = 124
                icon = self.game.stockIcon
                looper = self.stocks
            else:
                horizon = 230
                icon = self.game.stockIcon2
                looper = self.stocks2
            x = 0
            for _ in range(looper):
                self.game.display.blit(icon, (horizon + x, 170))
                x += 10

        self.game.text("RED", self.game.font, (255,0,0), 124, 185) # 400 / 225
        self.game.text("BLUE", self.game.font, (0,0,255), 230, 185) # 400 / 225

        self.game.text(str(self.damage) + "%", self.game.font, (255,255,255), 124, 201) # 400 / 225
        self.game.text(str(self.damage2) + "%", self.game.font, (255,255,255), 230, 201) # 400 / 225

        self.dead = ''


    def controlLoop(self): # you should lose your rights 1 frame after getting hit so there is no port priority
        key = pygame.key.get_pressed()
        if key[pygame.K_a] == True:
            self.movement[0] = True
            self.currentdirections = 'left'
        if key[pygame.K_d] == True:
            self.movement[1] = True
            self.currentdirections = 'right'
        if key[pygame.K_a] == True and key[pygame.K_d] == True:
            self.currentdirections = 'both'
        if key[pygame.K_r] == True:
            self.wahoo = 1.1

        self.orientation = self.game.player.orientation()

        if self.currentdirections == 'both' and self.lastPressedDirection == 'left':
            self.movement[1] = False
        elif self.currentdirections == 'both' and self.lastPressedDirection == 'right':
            self.movement[0] = False

        #(4 frames windup, 2 frames hit for side ) * 3
        # (2 frames windup, 5 frames hit ) * 2

        if self.inAMoveTimer0 < 0:
            self.inAMoveTimer0 +=1
        if self.inAMoveTimer0 == 0:
            self.inAMoveTimer0 = 0
            self.move0 = 'none'
            self.inAMove0 = False
        if self.windup0 > 0:
            self.windup0 -= 1

        if self.wholeLag0 > 0:
            self.wholeLag0 -= 1

        if not self.inAMove0 and self.wholeLag0 == 0:
            self.down0 = False

            if self.orientation == 'right':
                if key[pygame.K_t] == True and key[pygame.K_s] and not self.game.player.grounded():
                    self.move0 = 'downRightHit'
                    self.down0 = True
                elif key[pygame.K_t] == True and key[pygame.K_w]:
                    self.move0 = 'upRightHit'
                elif key[pygame.K_t] == True:
                    self.move0 = 'rightHit'
            elif self.orientation == 'left': 
                if key[pygame.K_t] == True and key[pygame.K_s] and not self.game.player.grounded():
                    self.move0 = 'downLeftHit'
                    self.down0 = True
                elif key[pygame.K_t] == True and key[pygame.K_w]:
                    self.move0 = 'upLeftHit'
                elif key[pygame.K_t] == True:
                    self.move0 = 'leftHit'

            if self.game.online2:
                self.move0 = self.game.VARIABLES[3]
        
        if self.inAMoveTimer0 != 0:
            self.game.player.weInAMove()
             
        if self.move0 != 'none' and self.inAMoveTimer0 == 0:
            self.inAMove0 = True
            if 'down' in self.move0 or 'up' in self.move0:
                self.inAMoveTimer0 = -7 * 2
                self.windup0 = 3 * 2
                self.wholeLag0 = 30
            else:                 
                self.inAMoveTimer0 = -7 * 2
                self.windup0 = 4 * 2
                self.wholeLag0 = 33

        if self.inAMove0:
            self.Hit0(self.move0, self.down0)

        self.controlLoop2()

    def Hit0(self, moveName, down):
        if 'down' in moveName or 'up' in moveName:
            self.game.player.vertHitAnim(down)
        else:
            self.game.player.sideHitAnim()
         
        if self.windup0 == 0:
            moveRect = self.game.player.rect(moveName)
            if moveRect.colliderect(self.player2_hitbox): # if 1 kills b
                self.game.player2.FIGHTING(moveName, self.damage2)
                if 'down' in moveName or 'up' in moveName:
                    self.damage2 += 1
                else:
                    self.damage2 += 3
                self.game.player2.getJumpBackAfterGettingHit()

    def eventloop(self):
        for event in pygame.event.get(): # looks through all events that are picked up
            if event.type == pygame.QUIT:
                if self.game.online == True or self.game.online2 == True:
                    self.game.socket.close()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN: # which button started getting pressed just now ?                     
                if event.key == pygame.K_a:
                    self.lastPressedDirection = 'left'
                if event.key == pygame.K_d:
                    self.lastPressedDirection = 'right'
                if event.key == pygame.K_w:
                    self.game.player.jump()
                if event.key == pygame.K_y:
                    self.game.player.velocity[1] = 12

                if event.key == pygame.K_LEFT:
                    self.lastPressedDirection2 = 'left'
                if event.key == pygame.K_RIGHT:
                    self.lastPressedDirection2 = 'right'
                if event.key == pygame.K_UP:
                    self.game.player2.jump()
                if event.key == pygame.K_PERIOD:
                    self.game.player2.velocity[1] = 12


    def controlLoop2(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] == True:
            self.movement2[0] = True
            self.currentdirections2 = 'left'
        if key[pygame.K_RIGHT] == True:
            self.movement2[1] = True
            self.currentdirections2 = 'right'
        if key[pygame.K_LEFT] == True and key[pygame.K_RIGHT] == True:
            self.currentdirections2 = 'both'
        if key[pygame.K_m] == True:
            self.wahoo2 = 1.1

        self.orientation2 = self.game.player2.orientation()

        if self.currentdirections2 == 'both' and self.lastPressedDirection2 == 'left':
            self.movement2[1] = False
        elif self.currentdirections2 == 'both' and self.lastPressedDirection2 == 'right':
            self.movement2[0] = False

        #(4 frames windup, 2 frames hit for side ) * 3
        # (2 frames windup, 5 frames hit ) * 2


        if self.inAMoveTimer < 0:
            self.inAMoveTimer +=1
        if self.inAMoveTimer == 0:
            self.inAMoveTimer = 0
            self.move = 'none'
            self.inAMove = False
        if self.windup > 0:
            self.windup -= 1

        if self.wholeLag > 0:
            self.wholeLag -= 1

        if not self.inAMove and self.wholeLag == 0:
            self.down = False

            if self.orientation2 == 'right':
                if key[pygame.K_COMMA] == True and key[pygame.K_DOWN] and not self.game.player2.grounded():
                    self.move = 'downRightHit'
                    self.down = True
                elif key[pygame.K_COMMA] == True and key[pygame.K_UP]:
                    self.move = 'upRightHit'
                elif key[pygame.K_COMMA] == True:
                    self.move = 'rightHit'
            elif self.orientation2 == 'left': 
                if key[pygame.K_COMMA] == True and key[pygame.K_DOWN] and not self.game.player2.grounded():
                    self.move = 'downLeftHit'
                    self.down = True
                elif key[pygame.K_COMMA] == True and key[pygame.K_UP]:
                    self.move = 'upLeftHit'
                elif key[pygame.K_COMMA] == True:
                    self.move = 'leftHit'

            if self.game.online:
                self.move = self.game.VARIABLES[3]
        
        if self.inAMoveTimer != 0:
            self.game.player2.weInAMove()

             
        if self.move != 'none' and self.inAMoveTimer == 0:
            self.inAMove = True
            if 'down' in self.move or 'up' in self.move:
                self.inAMoveTimer = -7 * 2
                self.windup = 3 * 2
                self.wholeLag = 30
            else:                 
                self.inAMoveTimer = -7 * 2
                self.windup = 4 * 2
                self.wholeLag = 33

        if self.inAMove:
            self.Hit(self.move, self.down)
            

    def Hit(self, moveName, down):
        if 'down' in moveName or 'up' in moveName:
            self.game.player2.vertHitAnim(down)
        else:
            self.game.player2.sideHitAnim()
        
        if self.windup == 0:
            moveRect = self.game.player2.rect(moveName)
            if moveRect.colliderect(self.player_hitbox): # if 1 kills b
                self.game.player.FIGHTING(moveName, self.damage)
                if 'down' in moveName or 'up' in moveName:
                    self.damage += 1
                else:
                    self.damage += 3
                self.game.player.getJumpBackAfterGettingHit()

    def resetGame(self):
        self.stocks = 3
        self.stocks2 = 3
        self.damage = 0
        self.damage2 = 0
        self.lastPressedDirection = 'right'
        self.lastPressedDirection2 = 'left'
        self.game.player.resetpos(1)
        self.game.player2.resetpos(2)

        self.movement = [False, False]
        self.movement2 = [False, False]
        self.wahoo = 1
        self.wahoo2 = 1
        self.f = 0
        self.matchStartTimer = 0

    def awesometext(self):
        if self.matchStartTimer < 220:
            self.matchStartTimer += 1
            self.f += 1.42
        if self.matchStartTimer < 60:
            self.game.text("3", self.game.big_font_backdrop, (0, 0, 0), 170, 15) # 400 / 225
            self.game.text("3", self.game.big_font, (255, 0+self.f, 0), 170, 15) # 400 / 225
        elif self.matchStartTimer < 120:
            self.game.text("2", self.game.big_font_backdrop, (0, 0, 0), 170, 15) # 400 / 225
            self.game.text("2", self.game.big_font, (255, 0+self.f, 0), 170, 15) # 400 / 225
        elif self.matchStartTimer < 180:
            self.game.text("1", self.game.big_font_backdrop, (0, 0, 0), 170, 15) # 400 / 225
            self.game.text("1", self.game.big_font, (255, 0+self.f, 0), 170, 15) # 400 / 225
        elif self.matchStartTimer < 220:
            self.game.text("GO", self.game.big_font_backdrop, (0, 0, 0), 115, 15) # 400 / 225
            self.game.text("GO", self.game.big_font, (0, 255, 0), 115, 15) # 400 / 225
            return True
        else:
            return True
        return False
