import pygame

NUM_ROWS = 24
NUM_COLS = 24
TILE_SIZE = 32
GRAVITY = 50
WALK_SPEED = 500
JUMP_FORCE = -20
BLUE = (0, 0, 255)

class Tile:
    def __init__(self, x, y):
        self.image = pygame.image.load('res/tileGround.png')
        self.x = x
        self.y = y

    def draw(self, screen):
        screen.blit(self.image, (self.x*TILE_SIZE, self.y*TILE_SIZE))
    
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 16
        self.h = 40
        self.vx = 0
        self.vy = 0
        self.grounded = False

    def update(self, dt):
        self.vx = 0

        keys = pygame.key.get_pressed()
        dx = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= WALK_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += WALK_SPEED
        self.vx = dx * dt

        if keys[pygame.K_SPACE] and self.grounded:
            self.vy = JUMP_FORCE
        self.vy += GRAVITY * dt
        
    
    def lateUpdate(self):
        self.x += self.vx
        self.y += self.vy

    def checkCollisions(self, tiles):
        hw = (TILE_SIZE+self.w) / 2
        hh = (TILE_SIZE+self.h) / 2

        self.grounded = False
        for tile in tiles:
            dx = (self.x + self.w/2) - (tile.x * TILE_SIZE + TILE_SIZE/2)
            dy = (self.y + self.h/2) - (tile.y * TILE_SIZE + TILE_SIZE/2)
            if abs(dx) <= hw and abs(dy) < hh:
                cw = hw*dx
                ch = hh*dy
                if cw > ch:
                    if cw > -ch: # RIGHT
                        self.vx = 0
                    else: # TOP
                        self.vy = 0
                        self.grounded = True
                        self.y = tile.y*TILE_SIZE - self.h
                else:
                    if cw > -ch: # BOTTOM
                        self.vy = 0
                    else: # LEFT
                        self.vx = 0
    
    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, (self.x, self.y, self.w, self.h))


running = True
pygame.init()
screen = pygame.display.set_mode((NUM_COLS*TILE_SIZE,NUM_ROWS*TILE_SIZE))
pygame.display.set_caption("Beste spillet")
clock = pygame.time.Clock()

tiles = []
def createTiles():
    for x in range(NUM_COLS):
        tiles.append(Tile(x, NUM_ROWS-1))

tiles.append(Tile(4, 4))
createTiles()

player = Player(100, 100)

while running:
    dt = clock.tick(60) / 1000

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    player.update(dt)
    player.checkCollisions(tiles)
    player.lateUpdate()

    screen.fill((0, 0, 0))
    
    for tile in tiles:
        tile.draw(screen)
    player.draw(screen)

    pygame.display.flip()

pygame.quit()
