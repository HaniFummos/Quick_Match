import pygame
import os

BASE_IMG_PATH = 'C:/Users/HaniA/OneDrive - Vrije Universiteit Amsterdam/Dokumente/CS/Quick_Match/images/'
BASE_IMG_PATH = 'C:/Users/HaniA/OneDrive - Vrije Universiteit Amsterdam/Desktop/UNI/CS DOCS/Quick_Match/images/'
BASE_IMG_PATH = 'images/'


def load_black_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert() #.convert helps performance alot
    img.set_colorkey((0, 0, 0)) # if an image has a black background
    return img
def load_white_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert() #.convert helps performance alot
    img.set_colorkey((255, 255, 255)) # if an image has a white background
    return img
def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert() #idk if should remove .convert
    return img

def load_images(path):
    images = []
    for img_name in sorted (os.listdir(BASE_IMG_PATH + path)): # alphabetical, so do 01 - 10 so that 10 isn't after 1
        images.append(load_black_image(path + '/' + img_name))
    return images

class Animation:
    def __init__(self, images, img_dur=5, loop = True):
        self.images = images
        self.loop = loop
        self.img_duration = img_dur
        self.done = False
        self.frame = 0
    
    def pointerCopy(self):
        return Animation(self.images, self.img_duration, self.loop)
    
    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_duration * len(self.images)) 
        else:
            self.frame = min(self.frame + 1, self.img_duration * len(self.images) - 1)
            if self.frame >= self.img_duration * len(self.images) - 1:
                self.done = True
    
    def img(self):
        return self.images[int(self.frame / self.img_duration)] # frame = frame of the game. It returns which frame of the animation we should be at at a certain frame in the gae
    