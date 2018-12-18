import pygame
from pygame.locals import *

SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Beste spillet")

pygame.font.init()
font40 = pygame.font.SysFont('Arial', 40)
font25 = pygame.font.SysFont('Arial', 25)

running = True

class Button:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y, 150, 65)) 

buttons = []

for i in range(9):
    j = i + 1
    button = Button(SCREEN_WIDTH/j - 75, SCREEN_HEIGHT/2)
    buttons.append(button)

while running: 

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False


    screenColor = (95, 187, 210)
    screen.fill(screenColor)

    text = font40.render('Et Jævlig Bra Spill', False, (255, 255, 255))
    textWidth = text.get_rect().width
    screen.blit(text, (SCREEN_WIDTH/2 - textWidth/2, SCREEN_HEIGHT/5))

    text = font25.render('Magnus, Kristoffer, Steinar og Ole', False, (255, 255, 255))
    textWidth = text.get_rect().width
    screen.blit(text, (SCREEN_WIDTH/2 - textWidth/2, SCREEN_HEIGHT/5 + 50))

    for i in range(9):
        buttons[i].draw(screen)
    #button2.draw(screen)


    pygame.display.flip()


pygame.quit()