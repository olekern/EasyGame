import pygame
import Tile

NUM_ROWS = 24
NUM_COLS = 24
TILE_SIZE = 32





running = True

pygame.init()
screen = pygame.display.set_mode((NUM_COLS*TILE_SIZE,NUM_ROWS*TILE_SIZE))
pygame.display.set_caption("Beste spillet")

clock = pygame.time.Clock()

tile = Tile()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        else:
            print(event)

    screen.fill((120, 120, 120))
    
    tile.show(screen, 0, 1)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
