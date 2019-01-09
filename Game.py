import pygame
import random

from Menu import Menu
from SpriteSheet import SpriteSheet
from Camera import Camera
from MapLoader import MapLoader
from Tile import Tile
from Player import Player

from pygame.locals import *
from pathlib import Path
import os.path

      
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


class Game:
    def __init__(self):
        self.TILE_SIZE = 32
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)

        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.LEVEL_COUNT = 4
        self.records = []
        self.loadRecords()

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
        self.isPlaying = False
        self.menu = Menu(self)

    def loadLevel(self, levelPath, levelIndex):
        self.level = Level(self, levelPath, levelIndex)
        self.isPlaying = True
    
    def saveRecords(self):
        if(os.path.isfile("records.txt")):
            print("Records file exists")
            outfile = open("records.txt", "r")
            content = []
            for record in self.records:
                content.append("%.2f" % record + "\n")
            
            with open('records.txt', 'w') as file:
                file.writelines(content)
        else:
            print("Records file does not exist")
            outfile = open("records.txt", "w")
            for record in self.records:
                outfile.write("%.2f" % record + "\n")
        outfile.close()
        
    def loadRecords(self):
        if os.path.isfile("records.txt"):
            outfile = open("records.txt","r")
            lines = outfile.readlines()
            outfile.close()
            records = []
            for line in lines:
                if line is not "":
                    records.append(float(line))
            for i in range(self.LEVEL_COUNT-len(records)):
                records.append(0.0)
            
            self.records = records
        else:
            self.records = []
            for i in range(self.LEVEL_COUNT):
                self.records.append(0)

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(100) / 1000
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.isPlaying:
                            self.isPlaying = False
                        else:
                            running = False

            if self.isPlaying:
                self.level.update(self.screen, events, dt)
            else:
                self.menu.update(self.screen, events)

            pygame.display.flip()


        pygame.quit()

    def getTile(self, x, y, group):
        if y < 0 or x < 0:
            return
        if y >= len(group) or x >= len(group[y]):
            return
        return group[y][x]

    def getTileWithId(self, id, group):
        for tile in group:
            if tile.id == id:
                return tile
        return



class Level:
    def __init__(self, game, mapRef, levelIndex):
        self.game = game
        self.mapRef = mapRef
        self.levelIndex = levelIndex
        self.map = MapLoader(mapRef)
        self.tiles = self.map.getTiles("Ground")
        self.decorations = self.map.getTiles("Decoration")
        self.GRAVITY = 80

        playerSpawn = self.map.getPlayerSpawn()
        self.goalRect = self.map.getGoalRect()

        self.player = Player(self, playerSpawn[0], playerSpawn[1])
        self.camera = Camera(self.player)
        self.sun = pygame.image.load("res/sun.png").convert_alpha()
        cloudImg = pygame.image.load("res/cloud.png").convert_alpha()
        self.clouds = []
        self.finished = False
        self.newRecord = False
        self.time = 0.0
        for i in range(5):
            x = random.randint(0, self.game.SCREEN_WIDTH)
            y = random.randint(0, self.game.SCREEN_HEIGHT/3)
            speed = random.randint(10, 50)
            self.clouds.append(Cloud(self, x, y, cloudImg, speed))
    
    def complete(self):
        if not self.finished:
            self.finished = True
            self.newRecord = self.game.records[self.levelIndex] == 0.0 or self.game.records[self.levelIndex] > self.time
            if self.newRecord:
                self.game.records[self.levelIndex] = self.time
                self.game.saveRecords()
                
    def restart(self):
        self.player.x = self.player.startX
        self.player.y = self.player.startY
        self.player.vx = 0
        self.player.vy = 0
        self.time = 0
        self.finished = False
        self.newRecord = False
            
    def update(self, screen, events, dt):
        if not self.finished:
            self.time += dt
        
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
                tileID = self.game.getTile(x, y, self.tiles)
                if tileID is not None:
                    tile = self.game.getTileWithId(tileID, self.game.ALL_TILES)
                    if tile is not None:
                        tile.draw(screen, x, y)
                decorID = self.game.getTile(x, y, self.decorations)
                if decorID is not None:
                    decor = self.game.getTileWithId(decorID, self.game.ALL_DECORATIONS)
                    if decor is not None:
                        decor.draw(screen, x, y)

        

        self.player.draw(screen)

        text = self.game.font.render('Tid: ' + "%.2f" % self.time, True, (255, 255, 255))
        screen.blit(text, (10, 10))

        text = self.game.font.render('DT: '+ str(dt), True, (255, 255, 255))
        screen.blit(text, (10, 50))

        if self.finished:
            if self.newRecord:
                text = self.game.font.render('Ny rekord!', True, (255, 255, 255))
                screen.blit(text, (300, 200))
            else:
                text = self.game.font.render('Din gamle rekord var på: ' + "%.2f" % self.game.records[self.levelIndex] , True, (255, 255, 255))
                screen.blit(text, (200, 200))
            text = self.game.font.render("Trykk på 'escape' for å gå tilbake eller 'space' for å restarte", True, (255, 255, 255))
            screen.blit(text, (5, 300))


    

game = Game()
game.run()
