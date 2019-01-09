import pygame
import random

# Cloud er objektene for skyene på himmelen
class Cloud:
    def __init__(self, level, x, y, sprite, speed):
        self.level = level
        self.x = x
        self.y = y
        self.sprite = sprite
        self.speed = speed

    # Hvert bilde oppdaterer skyen sin posisjon seg
    def update(self, dt):
        self.x -= self.speed*dt

        # Dersom skyen er utenfor vinduet blir den flyttet tilbake til andre siden
        if self.x < -self.sprite.get_rect().width:
            self.x = self.level.game.SCREEN_WIDTH + random.randint(0, 100)
            self.y = random.randint(0, self.level.game.SCREEN_HEIGHT/3)
            self.speed = random.randint(10, 50)

    # Tegner skyen
    def draw(self, screen):
        screen.blit(self.sprite, (self.x - self.level.camera.x/50, self.y - self.level.camera.y/50))


