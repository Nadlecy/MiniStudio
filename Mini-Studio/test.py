# Example file showing a circle moving on screen
import pygame
import math
from pygame.locals import *
from player import player

SCREEN_WITDH = 1280
SCREEN_HEIGT = 720


astronaute = pygame.image.load("image/astronaute.gif")
bg1 = pygame.image.load("image/background2.jpg")
# pygame setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WITDH, SCREEN_HEIGT))
clock = pygame.time.Clock()
running = True
dt = 0
bg = pygame.transform.scale(pygame.image.load("image/background2.jpg"),(1005,SCREEN_HEIGT))
bg_width = bg.get_width()
astronautebis = pygame.transform.scale(pygame.image.load("image/astronaute.gif"),(80,80))
scroll = 0
tiles = math.ceil(SCREEN_WITDH / bg_width) +1




while running:


    # draw scrolling background
    for i in range(0, tiles):
        screen.blit(bg,(i*bg_width+ scroll,0))

    

    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    scroll -= 5
    #scroll reset
    if abs(scroll) > bg_width:
        scroll = 0

    # fill the screen with a color to wipe away anything from last frame
    screen.blit(astronautebis, player.pos)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_z] or keys[pygame.K_UP]:
        player.pos.y -= player.speed * dt
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
       player.pos.y += player.speed * dt
    if keys[pygame.K_q] or keys[pygame.K_LEFT]:
        player.pos.x -= player.speed * dt
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        player.pos.x += player.speed * dt


    pygame.display.update()
   
    pygame.display.flip()

    
    dt = clock.tick(60) / 1000

pygame.quit()