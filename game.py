# Example file showing a circle moving on screen
import pygame
import math

#///////////////
# Game Classes 
#///////////////

# Creating a gameState class for game info
class gameState ():
    def __init__(self, Map, currentScrollDirection = "H"):
        self.Map = Map
        self.currentScrollDirection = currentScrollDirection


# Creating a player class for the player 
class player ():
    def __init__(self, currentSurface, visual = "image/astronaute.gif", shotVisu = "shot.png",dmg = 1,shotSpd = 2, shotCoolDown = 20, currentShotCoolDown = 0, shotsList = [] , position = pygame.Vector2(0,0) ,lives = 3):
        self.currentSurface = currentSurface
        self.visual = visual
        self.shotVisu = shotVisu
        self.dmg = dmg
        self.shotSpd = shotSpd
        self.shotCoolDown = shotCoolDown
        self.currentShotCoolDown = currentShotCoolDown
        self.position = position
        self.shotsList = shotsList
        self.lives = 3
    
    def shoot (self):
        if self.currentShotCoolDown < 1:
            self.shotsList.append(plrBullet(self.currentSurface, self.dmg, self.shotSpd, pygame.Vector2(self.position.x+80,self.position.y+40)))
            self.currentShotCoolDown = 0 + self.shotCoolDown

# creating a shot class for each shot by the player
class plrBullet ():
    def __init__(self, currentSurface, dmg, spd, position = pygame.Vector2(0,0)):
        self.currentSurface = currentSurface
        self.dmg = dmg
        self.spd = spd
        self.position = position
    
    #making the visible bullets move every frame
    def move(self):
        if self.currentSurface.get_width() + 40 > self.position.x:
            pygame.draw.circle(self.currentSurface, "green", self.position, 10)
            self.position.x += 300 * dt * self.spd
            return True
        else:
            return False   

# pygame setup
pygame.init()
#creating a screen
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

dt = 0
thisPlayer=player(currentSurface=screen, position = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2))

#preparing the scrolling screen
bg = pygame.transform.scale(pygame.image.load("image/background2.jpg"),(1005,screen.get_height()))
bg_width = bg.get_width()
scroll = 0
tiles = math.ceil(screen.get_width() / bg_width) +1

#showing the player character
plrVisual = pygame.transform.scale(pygame.image.load("image/astronaute.gif"),(80,80))

#launching the game
running = True
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

    #test character circle
    screen.blit(plrVisual, thisPlayer.position)

    thisPlayer.currentShotCoolDown -=1
    if thisPlayer.shotsList:
        toDelete=[]
        for i in range(len(thisPlayer.shotsList)):
            keeping = thisPlayer.shotsList[i].move()
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