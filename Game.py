import pygame

pygame.init()

background = pygame.display.set_mode((500,250))
pygame.display.set_caption("Beste spillet")

BLUE = (0, 0, 255)
background.fill(BLUE)

pygame.display.update()