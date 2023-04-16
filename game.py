# Example file showing a circle moving on screen
import pygame
import math
from player import Player

# Creating a gameState class for game info
class gameState ():
    def __init__(self, Map, currentScrollDirection = "H"):
        self.Map = Map
        self.currentScrollDirection = currentScrollDirection

# pygame setup
pygame.init()
#creating a screen
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

thisPlayer=Player(currentSurface=screen, visualsList=["image/astronaute_1.png","image/astronaute_2.png"], position = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2))
walkCycle = 0

#preparing the scrolling screen
bg = pygame.transform.scale(pygame.image.load("image/background2.jpg"),(1005,screen.get_height()))
bg_width = bg.get_width()
scroll = 0
tiles = math.ceil(screen.get_width() / bg_width) +1

"""#showing the player character
plrVisual = pygame.transform.scale(pygame.image.load("image/astronaute.gif"),(80,80))
"""
#launching the game
running = True
dt = 0

#preparing shown enemy storage list
enemiesOnScreen = []

while running:

    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # draw scrolling background
    for i in range(0, tiles):
        screen.blit(bg,(i*bg_width+ scroll,0))
    scroll -= 5
    #scroll reset
    if abs(scroll) > bg_width:
        scroll = 0
    
    #animating the player character
    screen.blit(thisPlayer.animate(), thisPlayer.position)

    thisPlayer.currentShotCoolDown -=1
    if thisPlayer.shotsList:
        toDelete=[]
        for i in range(len(thisPlayer.shotsList)):
            keeping = thisPlayer.shotsList[i].move(dt)
            print(i, ",    ", keeping)
            if not keeping:
                toDelete.append(i)
        if toDelete:
            for i in toDelete:
                del thisPlayer.shotsList[i]
    
    
    keys = pygame.key.get_pressed()
    if (keys[pygame.K_z] or keys[pygame.K_UP]) and thisPlayer.position.y > 0:
        thisPlayer.position.y -= 400 * dt
    if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and thisPlayer.position.y < screen.get_height() - 80:
        thisPlayer.position.y += 400 * dt
    if (keys[pygame.K_q] or keys[pygame.K_LEFT]) and thisPlayer.position.x > 0:
        thisPlayer.position.x -= 400 * dt
    if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and thisPlayer.position.x < screen.get_width() - 80:
        thisPlayer.position.x += 400 * dt
    if keys[pygame.K_SPACE]:
        thisPlayer.shoot()

    pygame.display.update()
    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()