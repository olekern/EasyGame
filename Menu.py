import pygame
from pygame.locals import *

SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("EasyGame")

pygame.font.init()
font40 = pygame.font.SysFont('Arial', 40)
font25 = pygame.font.SysFont('Arial', 25)

lvls = 4

running = True

class Button:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 150
        self.height = 65

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y, 150, 65)) 

    def collide(self, mouse):
        x_pos = mouse[0]
        y_pos = mouse[1]

        if (x_pos >= self.x and x_pos <= self.x + self.width) and (y_pos >= self.y and y_pos <= self.y + self.height):
            #Button is clicked


buttons = []

for i in range(lvls):
    j = i + 1
    button = Button(i*200 + 150, SCREEN_HEIGHT/2)
    buttons.append(button)

while running: 

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            mouse = pygame.mouse.get_pos()
            for i in range(lvls):
                buttons[i].collide(mouse)

    screenColor = (95, 187, 210)
    screen.fill(screenColor)

    text = font40.render('Pygame', False, (255, 255, 255))
    textWidth = text.get_rect().width
    screen.blit(text, (SCREEN_WIDTH/2 - textWidth/2, SCREEN_HEIGHT/5))

    text = font25.render('Magnus, Kristoffer, Steinar og Ole', False, (255, 255, 255))
    textWidth = text.get_rect().width
    screen.blit(text, (SCREEN_WIDTH/2 - textWidth/2, SCREEN_HEIGHT/5 + 50))

    for i in range(lvls):
        buttons[i].draw(screen)

    pygame.display.flip()


pygame.quit()