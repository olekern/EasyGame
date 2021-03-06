import pygame
from pygame.locals import *

from SpriteSheet import SpriteSheet

# Spilleren på spillet
class Player:

    # Initialiserer alle bildene av spilleren og andre verdier
    def __init__(self, level, x, y):
        self.level = level
        self.startX = x
        self.startY = y
        self.x = x
        self.y = y
        self.w = 24
        self.h = 40
        self.WALK_SPEED = 440
        self.JUMP_FORCE = -16

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

    #Oppdaterer hvert bilde
    def update(self, dt, events):

        #Bestemmer hvilket bilde i animasjonen som skal spilles
        self.prevY = self.y
        self.spriteTime += dt
        if self.spriteTime > self.spriteDT:
            self.spriteTime -= self.spriteDT
            self.spriteIndex += 1
            if self.spriteIndex >= len(self.idle_sprites_right):
                self.spriteIndex = 0

        # Dersom man trykker på piltastene eller A/D lagrer den hvor spilleren skal flytte seg
        keys = pygame.key.get_pressed()
        dx = 0
        if not self.level.finished:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                dx -= 1
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                dx += 1
        self.vx = dx * self.WALK_SPEED * dt
        

        if abs(self.vx) < 0.1:
            self.vx = 0


        # Legger til tyngdekraften i farten til spilleren
        self.vy += self.level.GRAVITY * dt
        if not self.grounded:
            self.timeInAir += dt
        

        # Sjekker om man kan hoppe
        if not self.level.finished:
            if keys[pygame.K_SPACE] and self.timeInAir < 0.03:
                self.vy = self.JUMP_FORCE

        elif keys[pygame.K_SPACE]:
            self.level.restart()
        
        for event in events:
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                if self.vy < 0:
                    self.vy /= 2



    # Sjekker for kollisjon med der spilleren ønsker å flytte seg til og bakken
    def checkCollisions(self, tiles):
        self.grounded = False

        # Sjekker under spilleren dersom han/hun beveger seg nedover
        if self.vy > 0:
            yCheck = self.y + self.h + self.vy
            xCheck1 = self.x
            xCheck2 = self.x + self.w - 1
            tile1 = self.level.game.getTile(int(xCheck1 / self.level.game.TILE_SIZE), int(yCheck / self.level.game.TILE_SIZE), tiles)
            tile2 = self.level.game.getTile(int(xCheck2 / self.level.game.TILE_SIZE), int(yCheck / self.level.game.TILE_SIZE), tiles)
            if (tile1 is not 0 and tile1 is not None) or (tile2 is not 0 and tile2 is not None):
                self.timeInAir = 0
                self.grounded = True
                self.vy = 0
                self.y = int(yCheck / self.level.game.TILE_SIZE)*self.level.game.TILE_SIZE - self.h
        elif self.vy < 0: # Sjekker under spilleren dersom han/hun beveger seg oppover
            yCheck = self.y + self.vy
            xCheck1 = self.x
            xCheck2 = self.x + self.w - 1
            tile1 = self.level.game.getTile(int(xCheck1 / self.level.game.TILE_SIZE), int(yCheck / self.level.game.TILE_SIZE), tiles)
            tile2 = self.level.game.getTile(int(xCheck2 / self.level.game.TILE_SIZE), int(yCheck / self.level.game.TILE_SIZE), tiles)
            if (tile1 is not 0 and tile1 is not None) or (tile2 is not 0 and tile2 is not None):
                self.vy = 0
                self.y = int(yCheck / self.level.game.TILE_SIZE + 1)*self.level.game.TILE_SIZE
        
        # Sjekker til siden av spilleren dersom han/hun beveger seg til høyre
        if self.vx > 0:
            xCheck = self.x + self.w + self.vx
            yCheck1 = self.y
            yCheck2 = self.y + self.h - 1
            tile1 = self.level.game.getTile(int(xCheck / self.level.game.TILE_SIZE), int(yCheck1 / self.level.game.TILE_SIZE), tiles)
            tile2 = self.level.game.getTile(int(xCheck / self.level.game.TILE_SIZE), int(yCheck2 / self.level.game.TILE_SIZE), tiles)
            if (tile1 is not 0 and tile1 is not None) or (tile2 is not 0 and tile2 is not None):
                self.vx = 0
                self.x = int(xCheck / self.level.game.TILE_SIZE)*self.level.game.TILE_SIZE - self.w
        elif self.vx < 0: # Sjekker til siden av spilleren dersom han/hun beveger seg til venstre
            xCheck = self.x + self.vx
            yCheck1 = self.y
            yCheck2 = self.y + self.h - 1
            tile1 = self.level.game.getTile(int(xCheck / self.level.game.TILE_SIZE), int(yCheck1 / self.level.game.TILE_SIZE), tiles)
            tile2 = self.level.game.getTile(int(xCheck / self.level.game.TILE_SIZE), int(yCheck2 / self.level.game.TILE_SIZE), tiles)
            if (tile1 is not 0 and tile1 is not None) or (tile2 is not 0 and tile2 is not None):
                self.vx = 0
                self.x = int(xCheck / self.level.game.TILE_SIZE + 1)*self.level.game.TILE_SIZE
        
    # Etter at det har blitt sjekket for kollisjon flytter spilleren på seg så lenge den ikke treffer på noe
    def lateUpdate(self):
        self.x += self.vx
        self.y += self.vy
        
        if self.vx < 0:
            self.facingRight = False
        if self.vx > 0:
            self.facingRight = True

        # Begrenser spilleren til å være innenfor banen
        if self.x < 0:
            self.x = 0
        if self.x > len(self.level.tiles[0])*self.level.game.TILE_SIZE - self.w:
            self.x = len(self.level.tiles[0])*self.level.game.TILE_SIZE - self.w
        
        # Starter på nytt dersom spilleren er under banen
        if self.y>len(self.level.tiles)*self.level.game.TILE_SIZE:
            self.level.restart()
        
        # Sjekker om man er i mål
        if self.level.goalRect.colliderect(Rect(self.x, self.y, self.w, self.h)):
            self.level.complete()
 
    # Tegner spilleren med den riktige animasjonen
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
      