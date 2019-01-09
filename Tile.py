import pygame

class Tile:
    def __init__(self, game, id, image):
        self.game = game
        self.id = id
        self.image = image

    def draw(self, screen, x, y):
        screen.blit(self.image, (x*self.game.TILE_SIZE - self.game.level.camera.x, y*self.game.TILE_SIZE - self.game.level.camera.y))
    