import pygame

class Button: # Source: https://www.youtube.com/watch?v=4_9twnEduFA + (I made some changes to make it more appealing for me)
    def __init__(self, colour, x, y, width, height, textSize, text=''):
        self.colour = colour
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.textSize = textSize

    def draw(self, display, outline=None, hover = False):
        if outline:
            pygame.draw.rect(display, outline, (self.x-2, self.y-2, self.width+4, self.height+4), 0)

        if hover == True:
            self.colour = (200, 200, 200)
        else:   
            self.colour = (255, 255, 255)
        pygame.draw.rect(display, self.colour, (self.x, self.y, self.width, self.height), 0)


        if self.text != '':
            font = pygame.font.SysFont(None, self.textSize)
            text = font.render(self.text, 1, (0, 0, 0))
            display.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
    def changeText(self, text):
        if text == 'back':
            hi = self.text[:-1]
            self.text = hi
        elif len(self.text) < 17:
            self.text = self.text + text

    def changeTextPORT(self, text):
        if text == 'back':
            hi = self.text[:-1]
            self.text = hi
        elif len(self.text) < 6:
            self.text = self.text + text
        return False

    def getText(self):
        return self.text
