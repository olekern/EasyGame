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

pygame.font.init()
font = pygame.font.SysFont('Arial', 20)

tile_image = pygame.image.load('res/tileGround.png').convert()

class MapLoader:
    def __init__(self, path):
        self.test = 0

class Tile:
    def __init__(self, x, y):
        #self.image = tile_image
        self.x = x
        self.y = y

    def draw(self, screen):
        screen.blit(tile_image, (self.x*TILE_SIZE, self.y*TILE_SIZE))
    
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
        
        if not self.grounded:
            self.vy += GRAVITY * dt
        else:
            self.vy = 0

        if keys[pygame.K_SPACE] and self.grounded:
            self.vy = JUMP_FORCE
        
    
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
                        self.y = tile.y*TILE_SIZE - self.h -1 
                else:
                    if cw > -ch: # BOTTOM
                        self.vy = 0
                    else: # LEFT
                        self.vx = 0
 
    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, (self.x, self.y, self.w, self.h))

class Target:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, (self.x*TILE_SIZE, self.y*TILE_SIZE, TILE_SIZE, TILE_SIZE))

player = Player(100, 100)
target = Target(22, 22)
running = True
tiles = []

for i in range(NUM_COLS):
    tiles.append(Tile(i, NUM_ROWS-1))

while running:
    dt = clock.tick(60) / 1000
    print(dt)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    player.update(0.016)
    player.checkCollisions(tiles)
    player.lateUpdate()

    screen.fill((0, 0, 0))
    
    for tile in tiles:
        tile.draw(screen)
    
    player.draw(screen)
    target.draw(screen)

    time = pygame.time.get_ticks() / 1000
    text = font.render('Tid: ' + str(time), True, (255, 255, 255))
    screen.blit(text, (10, 10))
    

    pygame.display.flip()

pygame.quit()