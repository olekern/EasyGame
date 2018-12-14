import pygame

NUM_ROWS = 24
NUM_COLS = 24
TILE_SIZE = 32
GRAVITY = 70
WALK_SPEED = 500
JUMP_FORCE = -20
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

pygame.init()
screen = pygame.display.set_mode((NUM_COLS*TILE_SIZE,NUM_ROWS*TILE_SIZE))
pygame.display.set_caption("Beste spillet")

clock = pygame.time.Clock()

running = True
while running:
    dt = clock.tick(60) / 1000
    print(dt)

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLUE)
    pygame.display.flip()
pygame.quit()
