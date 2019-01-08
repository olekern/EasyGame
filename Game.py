import pygame
import json
import random
import Menu
from Menu import Menu
from pygame.locals import *
from pathlib import Path
import os.path

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
        game = self.player.level.game
        self.x = self.player.x - game.SCREEN_WIDTH / 2
        self.y = self.player.y - game.SCREEN_HEIGHT / 2
        
        if self.x < 0:
            self.x = 0
        elif self.x > len(game.level.tiles[0])*game.TILE_SIZE - game.SCREEN_WIDTH:
            self.x = len(game.level.tiles[0])*game.TILE_SIZE - game.SCREEN_WIDTH
        
        if self.y > len(game.level.tiles)*game.TILE_SIZE - game.SCREEN_HEIGHT:
            self.y = len(game.level.tiles)*game.TILE_SIZE - game.SCREEN_HEIGHT

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
    def __init__(self, game, id, image):
        self.game = game
        self.id = id
        self.image = image

    def draw(self, screen, x, y):
        screen.blit(self.image, (x*self.game.TILE_SIZE - self.game.level.camera.x, y*self.game.TILE_SIZE - self.game.level.camera.y))
    
class Player:
    def __init__(self, level, x, y):
        self.level = level
        self.startX = x
        self.startY = y
        self.x = x
        self.y = y
        self.w = 24
        self.h = 40
        self.WALK_SPEED = 100
        self.JUMP_FORCE = -15
        self.DAMPING_STOP = 0.8
        self.DAMPING_TURNING = 0.6
        self.DAMPING_RUNNING = 0.4

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
        
        self.vx = dx * self.WALK_SPEED
        """if dx == 0:
            self.vx *= (1-DAMPING_STOP)**(dt*10)
        elif self.vx/dx < 0:
            self.vx *= (1-DAMPING_TURNING)**(dt*10)
        else:
            self.vx *= (1-DAMPING_RUNNING)**(dt*10)"""
        

        if abs(self.vx) < 0.1:
            self.vx = 0

        self.vy += self.level.GRAVITY * dt
        if not self.grounded:
            self.timeInAir += dt
        

        if keys[pygame.K_SPACE] and self.timeInAir < 0.03:
            self.vy = self.JUMP_FORCE
        
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
        if self.x > len(self.level.tiles[0])*self.level.game.TILE_SIZE - self.w:
            self.x = len(self.level.tiles[0])*self.level.game.TILE_SIZE - self.w
        
        if self.y>len(self.level.tiles)*self.level.game.TILE_SIZE:
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
            tile1 = getTile(int(xCheck1 / self.level.game.TILE_SIZE), int(yCheck / self.level.game.TILE_SIZE), tiles)
            tile2 = getTile(int(xCheck2 / self.level.game.TILE_SIZE), int(yCheck / self.level.game.TILE_SIZE), tiles)
            if (tile1 is not 0 and tile1 is not None) or (tile2 is not 0 and tile2 is not None):
                self.timeInAir = 0
                self.grounded = True
                self.vy = 0
                self.y = int(yCheck / self.level.game.TILE_SIZE)*self.level.game.TILE_SIZE - self.h
        elif self.vy < 0:
            yCheck = self.y + self.vy
            xCheck1 = self.x
            xCheck2 = self.x + self.w - 1
            tile1 = getTile(int(xCheck1 / self.level.game.TILE_SIZE), int(yCheck / self.level.game.TILE_SIZE), tiles)
            tile2 = getTile(int(xCheck2 / self.level.game.TILE_SIZE), int(yCheck / self.level.game.TILE_SIZE), tiles)
            if (tile1 is not 0 and tile1 is not None) or (tile2 is not 0 and tile2 is not None):
                self.vy = 0
                self.y = int(yCheck / self.level.game.TILE_SIZE + 1)*self.level.game.TILE_SIZE
        
        if self.vx > 0:
            xCheck = self.x + self.w + self.vx
            yCheck1 = self.y
            yCheck2 = self.y + self.h - 1
            tile1 = getTile(int(xCheck / self.level.game.TILE_SIZE), int(yCheck1 / self.level.game.TILE_SIZE), tiles)
            tile2 = getTile(int(xCheck / self.level.game.TILE_SIZE), int(yCheck2 / self.level.game.TILE_SIZE), tiles)
            if (tile1 is not 0 and tile1 is not None) or (tile2 is not 0 and tile2 is not None):
                self.vx = 0
                self.x = int(xCheck / self.level.game.TILE_SIZE)*self.level.game.TILE_SIZE - self.w
        elif self.vx < 0:
            xCheck = self.x + self.vx
            yCheck1 = self.y
            yCheck2 = self.y + self.h - 1
            tile1 = getTile(int(xCheck / self.level.game.TILE_SIZE), int(yCheck1 / self.level.game.TILE_SIZE), tiles)
            tile2 = getTile(int(xCheck / self.level.game.TILE_SIZE), int(yCheck2 / self.level.game.TILE_SIZE), tiles)
            if (tile1 is not 0 and tile1 is not None) or (tile2 is not 0 and tile2 is not None):
                self.vx = 0
                self.x = int(xCheck / self.level.game.TILE_SIZE + 1)*self.level.game.TILE_SIZE
        

 
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
            
        screen.blit(sprite, (self.x - self.level.camera.x, self.y - self.level.camera.y))
            
class Cloud:
    def __init__(self, level, x, y, sprite, speed):
        self.level = level
        self.x = x
        self.y = y
        self.sprite = sprite
        self.speed = speed

    def update(self, dt):
        self.x -= self.speed*dt
        if self.x < -self.sprite.get_rect().width:
            self.x = self.level.game.SCREEN_WIDTH + random.randint(0, 100)
            self.y = random.randint(0, self.level.game.SCREEN_HEIGHT/3)
            self.speed = random.randint(10, 50)

    def draw(self, screen):
        screen.blit(self.sprite, (self.x - self.level.camera.x/50, self.y - self.level.camera.y/50))

    
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


class Game:
    def __init__(self):
        self.TILE_SIZE = 32
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)

        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.LEVEL_COUNT = 4

        pygame.init()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        #screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Beste spillet")
        self.clock = pygame.time.Clock()

        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', 40)

        spriteSheet = SpriteSheet("res/sprites.png", self.TILE_SIZE, self.TILE_SIZE)

        self.TILE_GRASS_TOP = Tile(self, 2, spriteSheet.getImageAt(1, 0))
        self.TILE_GRASS_TOP_LEFT = Tile(self, 1, spriteSheet.getImageAt(0, 0))
        self.TILE_GRASS_TOP_RIGHT = Tile(self, 3, spriteSheet.getImageAt(2, 0))
        self.TILE_GRASS_LEFT = Tile(self, 9, spriteSheet.getImageAt(0, 1))
        self.TILE_DIRT = Tile(self, 10, spriteSheet.getImageAt(1,1))
        self.TILE_GRASS_RIGHT = Tile(self, 11, spriteSheet.getImageAt(2, 1))
        self.TILE_GRASS_BOTTOM = Tile(self, 18, spriteSheet.getImageAt(1, 2))
        self.TILE_GRASS_BOTTOM_LEFT = Tile(self, 17, spriteSheet.getImageAt(0, 2))
        self.TILE_GRASS_BOTTOM_RIGHT = Tile(self, 19, spriteSheet.getImageAt(2, 2))

        self.ALL_TILES = [self.TILE_GRASS_TOP, self.TILE_GRASS_TOP_LEFT, self.TILE_GRASS_TOP_RIGHT, self.TILE_GRASS_LEFT, self.TILE_DIRT, self.TILE_GRASS_RIGHT, self.TILE_GRASS_BOTTOM, self.TILE_GRASS_BOTTOM_LEFT, self.TILE_GRASS_BOTTOM_RIGHT]

        self.DECORATION_GRASS = Tile(self, 4, spriteSheet.getImageAt(3, 0))
        self.DECORATION_SIGN_5 = Tile(self, 5, spriteSheet.getImageAt(4, 0))
        self.DECORATION_SIGN_6 = Tile(self, 6, spriteSheet.getImageAt(5, 0))
        self.DECORATION_SIGN_7 = Tile(self, 7, spriteSheet.getImageAt(6, 0))
        self.DECORATION_SIGN_8 = Tile(self, 8, spriteSheet.getImageAt(7, 0))
        self.DECORATION_SIGN_13 = Tile(self, 13, spriteSheet.getImageAt(4, 1))
        self.DECORATION_SIGN_14 = Tile(self, 14, spriteSheet.getImageAt(5, 1))
        self.DECORATION_SIGN_15 = Tile(self, 15, spriteSheet.getImageAt(6, 1))
        self.DECORATION_SIGN_16 = Tile(self, 16, spriteSheet.getImageAt(7, 1))
        self.DECORATION_SIGN_21 = Tile(self, 21, spriteSheet.getImageAt(4, 2))
        self.DECORATION_SIGN_22 = Tile(self, 22, spriteSheet.getImageAt(5, 2))
        self.DECORATION_GOAL_23 = Tile(self, 23, spriteSheet.getImageAt(6, 2))
        self.DECORATION_GOAL_31 = Tile(self, 31, spriteSheet.getImageAt(6, 3))


        self.ALL_DECORATIONS = [self.DECORATION_GRASS, self.DECORATION_SIGN_5, self.DECORATION_SIGN_6, self.DECORATION_SIGN_7, self.DECORATION_SIGN_8, self.DECORATION_SIGN_13, self.DECORATION_SIGN_14, self.DECORATION_SIGN_15, self.DECORATION_SIGN_16, self.DECORATION_SIGN_21, self.DECORATION_SIGN_22, self.DECORATION_GOAL_23, self.DECORATION_GOAL_31]
        self.isPlaying = True
        self.level = Level(self, "maps/Map1.json")


        self.menu = Menu(self)

    def loadLevel(self, levelPath):
        self.level = Level(self, levelPath)
        self.isPlaying = True

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(60) / 1000
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            if self.isPlaying:
                self.level.update(self.screen, events, dt)
            else:
                self.menu.update(self.screen, events)

            pygame.display.flip()


        pygame.quit()



class Level:
    numLevels = 4
    def __init__(self, game, mapRef):
        self.game = game
        self.mapRef = mapRef
        self.player = Player(self, game.TILE_SIZE*2, 0)
        self.camera = Camera(self.player)
        self.sun = pygame.image.load("res/sun.png").convert_alpha()
        self.map1 = MapLoader(mapRef)
        self.tiles = self.map1.getTiles("Ground")
        self.decorations = self.map1.getTiles("Decoration")
        self.GRAVITY = 80

        cloudImg = pygame.image.load("res/cloud.png").convert_alpha()
        self.clouds = []
        for i in range(5):
            x = random.randint(0, self.game.SCREEN_WIDTH)
            y = random.randint(0, self.game.SCREEN_HEIGHT/3)
            speed = random.randint(10, 50)
            self.clouds.append(Cloud(self, x, y, cloudImg, speed))
    
    def update(self, screen, events, dt):
        self.player.update(dt, events)
        self.player.checkCollisions(self.tiles)
        self.player.lateUpdate()

        self.camera.update()

        screen.fill((95, 187, 210))
        screen.blit(self.sun, (self.game.SCREEN_WIDTH-600, 0))

        for cloud in self.clouds:
            cloud.update(dt)
            cloud.draw(screen)
        
        minY = int((self.camera.y) / self.game.TILE_SIZE)
        maxY = int((self.camera.y + self.game.SCREEN_HEIGHT) / self.game.TILE_SIZE) + 1
        minX = int((self.camera.x) / self.game.TILE_SIZE)
        maxX = int((self.camera.x + self.game.SCREEN_WIDTH) / self.game.TILE_SIZE) + 1
        for y in range(minY, maxY):
            for x in range(minX, maxX):
                tileID = getTile(x, y, self.tiles)
                if tileID is not None:
                    tile = getTileWithId(tileID, self.game.ALL_TILES)
                    if tile is not None:
                        tile.draw(screen, x, y)
                decorID = getTile(x, y, self.decorations)
                if decorID is not None:
                    decor = getTileWithId(decorID, self.game.ALL_DECORATIONS)
                    if decor is not None:
                        decor.draw(screen, x, y)

        

        self.player.draw(screen)

        time = pygame.time.get_ticks() / 1000
        text = self.game.font.render('Tid: ' + str(time), True, (255, 255, 255))
        screen.blit(text, (10, 10))

        text = self.game.font.render('DT: '+ str(dt), True, (255, 255, 255))
        screen.blit(text, (10, 50))

    def writeFile(level, rec):
        
        if(os.path.isfile("records.txt")):
            print("Records file exists")
            outfile = open("records.txt", "r")
            content = outfile.readlines()
            print(content)
            content[level-1] = str(level) + " " + str(rec)
            if(level < numLevels):
                content[level-1] += "\n"
            
            with open('records.txt', 'w') as file:
                file.writelines(content)
        else:
            print("Records file does not exist")
            outfile = open("records.txt", "w")
            for i in range(1, numLevels+1):
                if(i == level):
                    outfile.write(str(level) + " " +str(rec))
                outfile.write("\n")
        
        outfile.close()
        
        print("Record file successfully written!")
        outfile.close()
        
    #RETURNS LIST OF RECORDS FOR EACH LEVEL
    def readFile():
        outfile = open("records.txt","r")
        content = outfile.readlines()
        outfile.close()
        i = []
        for str in content:
            array = str.split(" ")
            j = array[1]
            j = j.replace("\n", "")
            i.append(int(j))
        return i


game = Game()
game.run()