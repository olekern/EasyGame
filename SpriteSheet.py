import pygame

class SpriteSheet:
    def __init__(self, filename, spriteWidth, spriteHeight):
        self.spriteSheet = pygame.image.load(filename).convert_alpha()
        self.spriteWidth = spriteWidth
        self.spriteHeight = spriteHeight

    def getImageAt(self, x, y):
        rect = pygame.Rect((x*self.spriteWidth, y*self.spriteHeight, self.spriteWidth, self.spriteHeight))
        image = pygame.Surface(rect.size, pygame.SRCALPHA)
        image.blit(self.spriteSheet, (0, 0), rect)
        return image
    
    def getImages(self, row):
        images = []
        for i in range(int(self.spriteSheet.get_rect().width/self.spriteWidth)):
            rect = pygame.Rect((i*self.spriteWidth, row*self.spriteHeight, self.spriteWidth, self.spriteHeight))
            image = pygame.Surface(rect.size, pygame.SRCALPHA)
            image.blit(self.spriteSheet, (0, 0), rect)
            images.append(image)
        return images