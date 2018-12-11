import pygame
import Game
class Tile:

    def __init__(self):
        self.image = pygame.image.load('res/tile.png')

    def show(self, screen, x, y):
        screen.blit(self.image, (x*Game.TILE_SIZE, y*Game.TILE_SIZE))
        