import pygame
import json
import random
from pygame.locals import *


TILE_SIZE = 32
GRAVITY = 80
WALK_SPEED = 0.7
JUMP_FORCE = -15
DAMPING_STOP = 0.8
DAMPING_TURNING = 0.6
DAMPING_RUNNING = 0.4
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 500

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Beste spillet")
clock = pygame.time.Clock()

pygame.font.init()
font = pygame.font.SysFont('Arial', 40)


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

class Camera(object):
    def __init__(self, player):
        self.player = player
        self.x = 0
        self.y = 0
    
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
        self.startX = x
        self.startY = y
        self.x = x
        self.y = y
        self.w = 24
        self.h = 40

        self.spriteSheet = SpriteSheet("res/player.png", self.w, self.h)
        self.idle_sprites_right = self.spriteSheet.getImages(0)
        self.idle_sprites_left = []
        for sprite in self.idle_sprites_right:
            self.idle_sprites_left.append(pygame.transform.flip(sprite, True, False))
        
        self.running_sprites_right = self.spriteSheet.getImages(1)
        self.running_sprites_left = []
        for sprite in self.running_sprites_right:
            self.running_sprites_left.append(pygame.transform.flip(sprite, True, False))

        self.air_sprites_right = self.spriteSheet.getImages(2)
        self.air_sprites_left = []
        for sprite in self.air_sprites_right:
            self.air_sprites_left.append(pygame.transform.flip(sprite, True, False))


        self.vx = 0
        self.vy = 0
        self.grounded = False
        self.facingRight = True
        self.spriteDT = 0.1
        self.spriteTime = 0.0
        self.spriteIndex = 0
        self.timeInAir = 0.0

    def update(self, dt, events):
        self.prevY = self.y
        self.spriteTime += dt
        if self.spriteTime > self.spriteDT:
            self.spriteTime -= self.spriteDT
            self.spriteIndex += 1
            if self.spriteIndex >= len(self.idle_sprites_right):
                self.spriteIndex = 0

        keys = pygame.key.get_pressed()
        dx = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += 1
        
        self.vx += dx * WALK_SPEED
        if dx == 0:
            self.vx *= (1-DAMPING_STOP)**(dt*10)
        elif self.vx/dx < 0:
            self.vx *= (1-DAMPING_TURNING)**(dt*10)
        else:
            self.vx *= (1-DAMPING_RUNNING)**(dt*10)

        if abs(self.vx) < 0.1:
            self.vx = 0

        self.vy += GRAVITY * dt
        if not self.grounded:
            self.timeInAir += dt
        

        if keys[pygame.K_SPACE] and self.timeInAir < 0.03:
            self.vy = JUMP_FORCE
        
        for event in events:
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                if self.vy < 0:
                    self.vy /= 2

    
    def lateUpdate(self):
        self.x += self.vx
        self.y += self.vy
        
        if self.vx < 0:
            self.facingRight = False
        if self.vx > 0:
            self.facingRight = True

        if self.x < 0:
            self.x = 0
        if self.x > len(tiles[0])*TILE_SIZE - player.w:
            self.x = len(tiles[0])*TILE_SIZE - player.w
        
        if self.y>len(tiles)*TILE_SIZE:
            self.x = self.startX
            self.y = self.startY
            self.vx = 0
            self.vy = 0

    def checkCollisions(self, tiles):
        self.grounded = False
        if self.vy > 0:
            yCheck = self.y + self.h + self.vy
            xCheck1 = self.x
            xCheck2 = self.x + self.w - 1
            tile1 = getTile(int(xCheck1 / TILE_SIZE), int(yCheck / TILE_SIZE), tiles)
            tile2 = getTile(int(xCheck2 / TILE_SIZE), int(yCheck / TILE_SIZE), tiles)
            if (tile1 is not 0 and tile1 is not None) or (tile2 is not 0 and tile2 is not None):
                self.timeInAir = 0
                self.grounded = True
                self.vy = 0
                self.y = int(yCheck / TILE_SIZE)*TILE_SIZE - self.h
        elif self.vy < 0:
            yCheck = self.y + self.vy
            xCheck1 = self.x
            xCheck2 = self.x + self.w - 1
            tile1 = getTile(int(xCheck1 / TILE_SIZE), int(yCheck / TILE_SIZE), tiles)
            tile2 = getTile(int(xCheck2 / TILE_SIZE), int(yCheck / TILE_SIZE), tiles)
            if (tile1 is not 0 and tile1 is not None) or (tile2 is not 0 and tile2 is not None):
                self.vy = 0
                self.y = int(yCheck / TILE_SIZE + 1)*TILE_SIZE
        
        if self.vx > 0:
            xCheck = self.x + self.w + self.vx
            yCheck1 = self.y
            yCheck2 = self.y + self.h - 1
            tile1 = getTile(int(xCheck / TILE_SIZE), int(yCheck1 / TILE_SIZE), tiles)
            tile2 = getTile(int(xCheck / TILE_SIZE), int(yCheck2 / TILE_SIZE), tiles)
            if (tile1 is not 0 and tile1 is not None) or (tile2 is not 0 and tile2 is not None):
                self.vx = 0
                self.x = int(xCheck / TILE_SIZE)*TILE_SIZE - self.w
        elif self.vx < 0:
            xCheck = self.x + self.vx
            yCheck1 = self.y
            yCheck2 = self.y + self.h - 1
            tile1 = getTile(int(xCheck / TILE_SIZE), int(yCheck1 / TILE_SIZE), tiles)
            tile2 = getTile(int(xCheck / TILE_SIZE), int(yCheck2 / TILE_SIZE), tiles)
            if (tile1 is not 0 and tile1 is not None) or (tile2 is not 0 and tile2 is not None):
                self.vx = 0
                self.x = int(xCheck / TILE_SIZE + 1)*TILE_SIZE
        

 
    def draw(self, screen):
        if self.prevY != self.y:
            index = 1
            if self.timeInAir < 0.1:
                index = 0
            elif self.vy > 0:
                index = 2                
            
            if self.facingRight:
                sprite = self.air_sprites_right[index]
            else:
                sprite = self.air_sprites_left[index]
        elif self.vx > 0:
            sprite = self.running_sprites_right[self.spriteIndex]
        elif self.vx < 0:
            sprite = self.running_sprites_left[self.spriteIndex]
        elif self.facingRight:
            sprite = self.idle_sprites_right[self.spriteIndex]
        else:
            sprite = self.idle_sprites_left[self.spriteIndex]
            
        screen.blit(sprite, (self.x - camera.x, self.y - camera.y))
            
class Cloud:
    def __init__(self, x, y, sprite, speed):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.speed = speed

    def update(self, dt):
        self.x -= self.speed*dt
        if self.x < -self.sprite.get_rect().width:
            self.x = SCREEN_WIDTH + random.randint(0, 100)
            self.y = random.randint(0, SCREEN_HEIGHT/3)
            self.speed = random.randint(10, 50)

    def draw(self, screen):
        screen.blit(self.sprite, (self.x - camera.x/50, self.y - camera.y/50))

    
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


spriteSheet = SpriteSheet("res/sprites.png", TILE_SIZE, TILE_SIZE)

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
camera = Camera(player)

sun = pygame.image.load("res/sun.png").convert_alpha()

running = True

map1 = MapLoader("maps/Map1.json")
tiles = map1.getTiles("Ground")
decorations = map1.getTiles("Decoration")

cloudImg = pygame.image.load("res/cloud.png").convert_alpha()
clouds = []

for i in range(5):
    x = random.randint(0, SCREEN_WIDTH)
    y = random.randint(0, int(SCREEN_HEIGHT/3))
    speed = random.randint(10, 50)
    clouds.append(Cloud(x, y, cloudImg, speed))

while running:
    dt = clock.tick(60) / 1000
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    player.update(dt, events)
    player.checkCollisions(tiles)
    player.lateUpdate()

    camera.update()

    screen.fill((95, 187, 210))
    screen.blit(sun, (SCREEN_WIDTH-600, 0))

    for cloud in clouds:
        cloud.update(dt)
        cloud.draw(screen)
    
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

    time = pygame.time.get_ticks() / 1000
    text = font.render('Tid: ' + str(time), True, (255, 255, 255))
    screen.blit(text, (10, 10))

    text = font.render('DT: '+ str(dt), True, (255, 255, 255))
    screen.blit(text, (10, 50))

    """
    text = font.render('playerX: '+ str(player.x) + '  (' + str(player.x//TILE_SIZE) + ')', True, (255, 255, 255))
    screen.blit(text, (10, 90))

    text = font.render('playerY: '+ str(player.y) + '  (' + str(player.y//TILE_SIZE) + ')', True, (255, 255, 255))
    screen.blit(text, (10, 130))

    text = font.render('vx: '+ str(player.vx), True, (255, 255, 255))
    screen.blit(text, (10, 170))

    text = font.render('vy: '+ str(player.vy), True, (255, 255, 255))
    screen.blit(text, (10, 210))

    text = font.render('grounded: '+ str(player.grounded), True, (255, 255, 255))
    screen.blit(text, (10, 250))
    """

    pygame.display.flip()

pygame.quit()