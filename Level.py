import pygame
import random

from Player import Player
from Camera import Camera
from Cloud import Cloud
from MapLoader import MapLoader

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

