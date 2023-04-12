import pygame
astronaute = pygame.image.load("image/astronaute.gif")
SCREEN_WITDH = 1280
SCREEN_HEIGT = 720
screen = pygame.display.set_mode((SCREEN_WITDH, SCREEN_HEIGT))
class player:
    hp = 3
    pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
    dmg = 1
    speed = 500