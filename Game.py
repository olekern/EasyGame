import pygame

from Menu import Menu
from SpriteSheet import SpriteSheet
from Tile import Tile
from Level import Level

from pygame.locals import *
from pathlib import Path
import os.path
  

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
        pygame.display.set_caption("EasyGame")
        self.clock = pygame.time.Clock()

        pygame.mixer.init() 
        pygame.mixer.music.load("sounds/music.mp3") 
        pygame.mixer.music.play(-1,0.0)
        

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

    
# Starter spillet
game = Game()
game.run()
