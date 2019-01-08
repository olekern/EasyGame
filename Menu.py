import pygame
from pygame.locals import *

class Menu:
    def __init__(self, game):
        self.game = game

        self.buttons = []

        for i in range(game.LEVEL_COUNT):
            j = i + 1
            button = Button(self, game, (game.SCREEN_WIDTH/6)*(i+1), game.SCREEN_HEIGHT/2)
            self.buttons.append(button)

    def update(self, screen, events):
        for event in events:
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                mouse = pygame.mouse.get_pos()
                for i in range(self.game.LEVEL_COUNT):
                    self.buttons[i].collide(mouse)

        screenColor = (95, 187, 210)
        screen.fill(screenColor)

        text = self.game.font.render('Pygame', False, (255, 255, 255))
        textWidth = text.get_rect().width
        screen.blit(text, (self.game.SCREEN_WIDTH/2 - textWidth/2, self.game.SCREEN_HEIGHT/5))

        text = self.game.font.render('Magnus, Kristoffer, Steinar og Ole', False, (255, 255, 255))
        textWidth = text.get_rect().width
        screen.blit(text, (self.game.SCREEN_WIDTH/2 - textWidth/2, self.game.SCREEN_HEIGHT/5 + 50))

        for i in range(self.game.LEVEL_COUNT):
            self.buttons[i].draw(screen)

    

class Button:
    def __init__(self, menu, game, x, y):
        self.menu = menu
        self.game = game
        self.x = x
        self.y = y
        self.width = 150
        self.height = 65

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y, self.game.SCREEN_WIDTH/6, 65)) 

    def collide(self, mouse):
        x_pos = mouse[0]
        y_pos = mouse[1]

        if (x_pos >= self.x and x_pos <= self.x + self.width) and (y_pos >= self.y and y_pos <= self.y + self.height):
            #Button is clicked
            self.menu.game.loadLevel("maps/Map1.json")

    