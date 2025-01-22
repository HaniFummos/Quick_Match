import pygame

class PhysicsEntity:
    def __init__(self, game, entity_type, pos, size):
        self.game = game
        self.type = entity_type
        self.pos = list(pos) #position of the topleft of the entity []
        self.size = size
        self.jumps = 2

        self.velocity = [0, 0]
        self.smashVelocity = 0
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}

        self.air_time = 0

        self.sideAttacking = False
        self.vertAttacking = False
        self.downAttacking = False
        self.lastVert = 0

        self.inAMove = False

        self.action = ''
        self.anim_offset = (-3, -3) # images render outside the hitbox of the player
        self.flip = False
        self.set_action('idle')

    def playerDefaultDirection(self):
        self.flip = False
    def player2DefaultDirection(self):
        self.flip = True
    def orientation(self):
        if self.flip == True:
            return 'left'
        else:
            return 'right'
    

    def resetpos(self, player):
        if player == 1:
            self.pos = list([80+48, 128])
        else:
            self.pos = list((311-48, 128))

    def rect(self, type = ''): # a rect will be created at player, and will later do physics checks
        if type == 'rightHit':
            #pygame.draw.rect(self.game.display, (120,120,120), (self.pos[0] + self.size[0], self.pos[1] , 13, 10))
            return pygame.Rect(self.pos[0] + self.size[0], self.pos[1], 13, 10) #aleviates the topleft issue, as going to size = bottomright
        elif type == 'leftHit':
           # pygame.draw.rect(self.game.display, (120,120,120), (self.pos[0] - 13, self.pos[1] , 13, 10))
            return pygame.Rect(self.pos[0] - 13, self.pos[1], 13, 10) #aleviates the topleft issue, as going to size = bottomright
        elif type == 'upLeftHit':
            #pygame.draw.rect(self.game.display, (120,120,120), (self.pos[0] - 6, self.pos[1] - 8 , 15, 9))
            return pygame.Rect(self.pos[0] - 6, self.pos[1] - 8 , 15, 9) #aleviates the topleft issue, as going to size = bottomright
        elif type == 'upRightHit':
            #pygame.draw.rect(self.game.display, (120,120,120), (self.pos[0] - 2, self.pos[1] - 8 , 15, 9))
            return pygame.Rect(self.pos[0] - 2, self.pos[1] - 8 , 15, 9) #aleviates the topleft issue, as going to size = bottomright
        elif type == 'downRightHit':
            #pygame.draw.rect(self.game.display, (120,120,120), (self.pos[0] - 2, self.pos[1] + 12 , 15, 9))
            return pygame.Rect(self.pos[0] - 2, self.pos[1] + 12 , 15, 9) #aleviates the topleft issue, as going to size = bottomright
        elif type == 'downLeftHit':
            #pygame.draw.rect(self.game.display, (120,120,120), (self.pos[0] - 6, self.pos[1] + 12 , 15, 9))
            return pygame.Rect(self.pos[0] - 6, self.pos[1] + 12 , 15, 9) #aleviates the topleft issue, as going to size = bottomright
        else:
            #pygame.draw.rect(self.game.display, (255,255,255), (self.pos[0], self.pos[1], self.size[0], self.size[1]))
            return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1]) #aleviates the topleft issue, as going to size = bottomright
            #FLIP THE RECT

    def FIGHTING(self, type, damage):
        if type == 'rightHit':
            self.velocity[0] = damage / 20 + 1.0
            self.velocity[1] = -(damage / 20 + 1.0)
            return
        elif type == 'leftHit':
           self.velocity[0] = -(damage / 20 + 1.0)
           self.velocity[1] = -(damage / 20 + 1.0)
           return
        elif type == 'upRightHit':
            self.velocity[0] = damage / 100 +.1
            self.velocity[1] = -(damage / 20 + 2.5)
        elif type == 'upLeftHit':
            self.velocity[0] = -(damage / 100 +.1)
            self.velocity[1] = -(damage / 20 + 2.5)
        elif type == 'downRightHit':
           self.velocity[0] = damage / 100 +.1
           self.velocity[1] = damage / 20 + 2.5
        elif type == 'downLeftHit':
           self.velocity[0] = - (damage / 100 +.1)
           self.velocity[1] = damage / 20 + 2.5

        self.smashVelocity = self.velocity[1]

    def sideHitAnim(self):
        self.sideAttacking = True
    
    def grounded(self):
        if self.jumps == 3:
            return True
        else:
            return False

    def vertHitAnim(self, down = False):
        self.vertAttacking = True
        if down:
            self.downAttacking = True
        else:
            self.downAttacking = False

    def getXvelocity(self):
        return self.velocity[0]

    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.type + '/' + self.action].pointerCopy() # ex: player/idle

    def update(self, tilemap, movement = (0, 0), yippieMeter=1): # 0,0 or False False is default
        dead = False
        
        if self.pos[1] > 400 or self.pos[0] > 450 or self.pos[0] < -50 or (self.pos[1] < -40 and self.action == 'tumble'):
            self.pos = [195, 22]
            self.velocity = [0,0] # maybe make falling down the lower blastzone only send you back up (but you're stunned)
            dead = True
            self.jumps = 2


        if abs(self.velocity[0]) < .1:
            self.velocity[0] = 0
        elif abs(self.velocity[0]) > 0: # when being knocked back
            self.velocity[0] -= (self.velocity[0] / 12)  # creates a perfect arc when getting knowcked back
        if abs(self.velocity[0]) > 1:
            yippieMeter = .5 #makes DI less OP
            
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}

        frame_movement = (movement[0] * yippieMeter + self.velocity[0], movement[1] + self.velocity[1])

        self.pos[0] += frame_movement[0] * 2

        entity_rect = self.rect() # uses above function
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect): # if collision with wall
                if frame_movement[0] > 0: # if currently moving right
                    entity_rect.right = rect.left # make the right edge of entity snap to left edge of the tile
                    self.collisions['right'] = True
                if frame_movement[0] < 0: # if moving left
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x # player position is now rect's position

        
        self.pos[1] += frame_movement[1] #y
        entity_rect = self.rect() # we create a new entity, because we have an updated pos now, we don't need to look at he pos thats partly in the ground (disasterous)
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect): # if collision with floor
                if frame_movement[1] > 0: # if currently moving down
                    entity_rect.bottom = rect.top # make the bottom edge of entity snap to top edge of the tile
                    self.jumps = 3
                    self.velocity[0] -= (self.velocity[0] / 2) #you wont slide around due to knockback if you land on the ground
                    self.collisions['down'] = True

                    # ADD A STAGESPIKE VARIABLE WHEN SPIKES ARE ADDED

                if frame_movement[1] < 0: # if moving up
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = entity_rect.y # player position is now rect's position

        self.velocity[1] += .4
        if self.smashVelocity < 0:
            self.smashVelocity += .4
        else:
            self.smashVelocity -= .4
        if self.collisions['down'] and self.smashVelocity > .5:
            print (self.smashVelocity)
            self.velocity[1] = -self.velocity[1]
        elif self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0

        if self.jumps == 3 and abs(self.velocity[1]) > 2: # if jumps = 3 and not grounded
            self.jumps -= 1

        if self.inAMove == False:
            if movement[0] > 0:
                self.flip = False
            elif movement[0] < 0:
                self.flip = True

        self.air_time += 1
        if self.collisions['down']:
            self.air_time = 0

    
        if abs(self.velocity[0]) > .3 or abs(self.smashVelocity) > .4:
            self.set_action('tumble')
        elif self.sideAttacking == True:
            self.set_action('sideHit')
        elif self.vertAttacking == True:
            self.set_action('vertHit')
        elif self.air_time > 3:
            self.set_action('jump')
        elif movement[0] != 0:
            self.set_action('walk')
        else:
            self.set_action('idle')

        if self.jumps < 1:
            self.velocity[1] += .5

        self.animation.update()
        self.sideAttacking = False
        self.vertAttacking = False
        self.inAMove = False
        return dead
    
    def weInAMove(self):
        self.inAMove = True
    
    def render(self, surf): # rendering character. also im pretty sure that self gets ignored
        if self.action == 'sideHit': 
            surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] - 9 + self.anim_offset[0], self.pos[1] + self.anim_offset[1]))
        elif self.action == 'vertHit':
            if self.downAttacking:
                surf.blit(pygame.transform.flip(self.animation.img(), self.flip, True), (self.pos[0] - 9 + self.anim_offset[0], self.pos[1] - 9 + self.anim_offset[1]))
            else:
                surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] - 9 + self.anim_offset[0], self.pos[1] - 9 + self.anim_offset[1]))
        elif self.flip and self.action == 'idle':
            surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] - 8 + self.anim_offset[0], self.pos[1] + self.anim_offset[1]))
        elif self.flip and self.action == 'walk': 
            surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] - 8 + self.anim_offset[0], self.pos[1] + self.anim_offset[1]))
        else:
            surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] + self.anim_offset[0], self.pos[1] + self.anim_offset[1]))


    def jump(self):
        if self.jumps:
            if self.jumps == 3:
                self.velocity[1] = -4
            elif self.jumps == 2:
                self.velocity[1] = -5
            else:
                self.velocity[1] = -11
            self.jumps -=1

    def getJumpBackAfterGettingHit(self):
        if self.jumps < 1:
            self.jumps = 1
    
    

                    
