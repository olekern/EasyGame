import pygame
import json
from pygame.locals import *


TILE_SIZE = 32
GRAVITY = 100
WALK_SPEED = 300
JUMP_FORCE = -20
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Beste spillet")
clock = pygame.time.Clock()

pygame.font.init()
font = pygame.font.SysFont('Arial', 40)

class SpriteSheet:
    def __init__(self, filename):
        self.spriteSheet = pygame.image.load(filename).convert_alpha()

    def getImageAt(self, x, y):
        rect = pygame.Rect((x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE))
        image = pygame.Surface(rect.size, pygame.SRCALPHA)
        image.blit(self.spriteSheet, (0, 0), rect)
        return image

class Camera(object):
    def __init__(self, player):
        self.player = player
        self.x = player.x
        self.y = player.y
    
    def update(self):
        self.x = self.player.x - SCREEN_WIDTH / 2
        self.y = self.player.y - SCREEN_HEIGHT / 2
        
        if self.x < 0:
            self.x = 0
        elif self.x > len(tiles[0])*TILE_SIZE - SCREEN_WIDTH:
            self.x = len(tiles[0])*TILE_SIZE - SCREEN_WIDTH
        
        if self.y > len(tiles)*TILE_SIZE - SCREEN_HEIGHT:
            self.y = len(tiles)*TILE_SIZE - SCREEN_HEIGHT

class MapLoader:
    def __init__(self, path):
        with open(path, "r") as file:
            self.data = json.load(file)

    def getTiles(self, layerName):
        tiles = []
        layers = self.data["layers"]
        for layer in layers:
            if layer["name"] == layerName:
                width = int(layer["width"])
                tileData = layer["data"]
                numRows = len(tileData)//width
                for r in range(numRows):
                    row = []
                    for c in range(width):
                        row.append(tileData[r*width + c])
                    tiles.append(row)
                break
        return tiles

class Tile:
    def __init__(self, id, image):
        self.id = id
        self.image = image

    def draw(self, screen, x, y):
        screen.blit(self.image, (x*TILE_SIZE - camera.x, y*TILE_SIZE - camera.y))
    
class Player:
    def __init__(self, x, y):
        self.sprite_right = pygame.image.load("res/player.png").convert_alpha()
        self.sprite_left = pygame.transform.flip(self.sprite_right, True, False)
        self.x = x
        self.y = y
        self.w = 23
        self.h = 40
        self.vx = 0
        self.vy = 0
        self.grounded = False
        self.facingRight = True

    def update(self, dt):
        self.vx = 0

        keys = pygame.key.get_pressed()
        dx = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= WALK_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += WALK_SPEED
        self.vx = dx * dt
        
        """dy = 0
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy -= WALK_SPEED
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy += WALK_SPEED
        self.vy = dy * dt"""

        if not self.grounded:
            self.vy += GRAVITY * dt
        else:
            self.vy = 0

        if keys[pygame.K_SPACE] and self.grounded:
            self.vy = JUMP_FORCE
        
    
    def lateUpdate(self):
        self.x += self.vx
        self.y += self.vy
        
        if self.vx < 0:
            self.facingRight = False
        if self.vx > 0:
            self.facingRight = True

        if self.x < 0:
            self.x = 0

    def checkCollisions(self, tiles):
        self.grounded = False
        if self.vy > 0:
            yCheck = self.y + self.h + self.vy
            xCheck1 = self.x
            xCheck2 = self.x + self.w
            tile1 = getTile(int(xCheck1 / TILE_SIZE), int(yCheck / TILE_SIZE), tiles)
            tile2 = getTile(int(xCheck2 / TILE_SIZE), int(yCheck / TILE_SIZE), tiles)
            if tile1 is not 0 or tile2 is not 0:
                self.grounded = True
                self.vy = 0
                self.y = int(yCheck / TILE_SIZE)*TILE_SIZE - self.h
 
    def draw(self, screen):
        if self.facingRight:
            screen.blit(self.sprite_right, (self.x - camera.x, self.y - camera.y))
        else:
            screen.blit(self.sprite_left, (self.x - camera.x, self.y - camera.y))
            

class Target:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, (self.x*TILE_SIZE - camera.x, self.y*TILE_SIZE - camera.y, TILE_SIZE, TILE_SIZE))

def getTile(x, y, group):
    if y < 0 or x < 0:
        return
    if y >= len(group) or x >= len(group[y]):
        return
    return group[y][x]

def getTileWithId(id, group):
    for tile in group:
        if tile.id == id:
            return tile
    return


spriteSheet = SpriteSheet("res/sprites.png")

TILE_GRASS_TOP = Tile(2, spriteSheet.getImageAt(1, 0))
TILE_GRASS_TOP_LEFT = Tile(1, spriteSheet.getImageAt(0, 0))
TILE_GRASS_TOP_RIGHT = Tile(3, spriteSheet.getImageAt(2, 0))
TILE_GRASS_LEFT = Tile(9, spriteSheet.getImageAt(0, 1))
TILE_DIRT = Tile(10, spriteSheet.getImageAt(1,1))
TILE_GRASS_RIGHT = Tile(11, spriteSheet.getImageAt(2, 1))

ALL_TILES = [TILE_GRASS_TOP, TILE_GRASS_TOP_LEFT, TILE_GRASS_TOP_RIGHT, TILE_GRASS_LEFT, TILE_DIRT, TILE_GRASS_RIGHT]

DECORATION_GRASS = Tile(4, spriteSheet.getImageAt(3, 0))
DECORATION_SIGN_5 = Tile(5, spriteSheet.getImageAt(4, 0))
DECORATION_SIGN_6 = Tile(6, spriteSheet.getImageAt(5, 0))
DECORATION_SIGN_7 = Tile(7, spriteSheet.getImageAt(6, 0))
DECORATION_SIGN_8 = Tile(8, spriteSheet.getImageAt(7, 0))
DECORATION_SIGN_13 = Tile(13, spriteSheet.getImageAt(4, 1))
DECORATION_SIGN_14 = Tile(14, spriteSheet.getImageAt(5, 1))
DECORATION_SIGN_15 = Tile(15, spriteSheet.getImageAt(6, 1))
DECORATION_SIGN_16 = Tile(16, spriteSheet.getImageAt(7, 1))
DECORATION_SIGN_21 = Tile(21, spriteSheet.getImageAt(4, 2))
DECORATION_SIGN_22 = Tile(22, spriteSheet.getImageAt(5, 2))
DECORATION_GOAL_17 = Tile(17, spriteSheet.getImageAt(0, 2))
DECORATION_GOAL_25 = Tile(25, spriteSheet.getImageAt(0, 3))


ALL_DECORATIONS = [DECORATION_GRASS, DECORATION_SIGN_5, DECORATION_SIGN_6, DECORATION_SIGN_7, DECORATION_SIGN_8, DECORATION_SIGN_13, DECORATION_SIGN_14, DECORATION_SIGN_15, DECORATION_SIGN_16, DECORATION_SIGN_21, DECORATION_SIGN_22, DECORATION_GOAL_17, DECORATION_GOAL_25]

player = Player(TILE_SIZE*2, 0)
target = Target(0, 0)
camera = Camera(player)

running = True

map1 = MapLoader("maps/Map1.json")
tiles = map1.getTiles("Ground")
decorations = map1.getTiles("Decoration")

while running:
    dt = clock.tick(60) / 1000
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    player.update(dt)
    player.checkCollisions(tiles)
    player.lateUpdate()

    camera.update()

    screen.fill((95, 187, 210))

    
    minY = int((camera.y) / TILE_SIZE)
    maxY = int((camera.y + SCREEN_HEIGHT) / TILE_SIZE) + 1
    minX = int((camera.x) / TILE_SIZE)
    maxX = int((camera.x + SCREEN_WIDTH) / TILE_SIZE) + 1
    for y in range(minY, maxY):
        for x in range(minX, maxX):
            tileID = getTile(x, y, tiles)
            if tileID is not None:
                tile = getTileWithId(tileID, ALL_TILES)
                if tile is not None:
                    tile.draw(screen, x, y)
            decorID = getTile(x, y, decorations)
            if decorID is not None:
                decor = getTileWithId(decorID, ALL_DECORATIONS)
                if decor is not None:
                    decor.draw(screen, x, y)




    player.draw(screen)
    target.draw(screen)

    time = pygame.time.get_ticks() / 1000
    text = font.render('Tid: ' + str(time), True, (255, 255, 255))
    screen.blit(text, (10, 10))

    text = font.render('DT: '+ str(dt), True, (255, 255, 255))
    screen.blit(text, (10, 50))

    text = font.render('playerX: '+ str(player.x) + '  (' + str(player.x//TILE_SIZE) + ')', True, (255, 255, 255))
    screen.blit(text, (10, 90))

    text = font.render('playerY: '+ str(player.y) + '  (' + str(player.y//TILE_SIZE) + ')', True, (255, 255, 255))
    screen.blit(text, (10, 130))

    text = font.render('cameraX: '+ str(camera.x), True, (255, 255, 255))
    screen.blit(text, (10, 170))

    text = font.render('cameraY: '+ str(camera.y), True, (255, 255, 255))
    screen.blit(text, (10, 210))

    pygame.display.flip()

pygame.quit()