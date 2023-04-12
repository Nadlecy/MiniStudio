# Example file showing a circle moving on screen
import pygame

#///////////////
# Game Classes 
#///////////////

# Creating a player class for player and game info
class player ():
    def __init__(self, currentSurface, shotVisu = "shot.png",dmg = 1,shotSpd = 2, shotCoolDown = 20, currentShotCoolDown = 0, shotsList = [] , position = pygame.Vector2(0,0) ,lives = 3):
        self.currentSurface = currentSurface
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
            self.shotsList.append(plrBullet(self.currentSurface, self.dmg, self.shotSpd, pygame.Vector2(self.position.x,self.position.y)))
            self.currentShotCoolDown = 0 + self.shotCoolDown

# creating a shot class for each shot by the player
class plrBullet ():
    def __init__(self, currentSurface, dmg, spd, position = pygame.Vector2(0,0)):
        self.currentSurface = currentSurface
        self.dmg = dmg
        self.spd = spd
        self.position = position
    
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


running = True
dt = 0

thisPlayer=player(currentSurface=screen, position = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2))

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    pygame.draw.circle(screen, "red", thisPlayer.position, 40)

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
    if keys[pygame.K_z] or keys[pygame.K_UP]:
        thisPlayer.position.y -= 400 * dt
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        thisPlayer.position.y += 400 * dt
    if keys[pygame.K_q] or keys[pygame.K_LEFT]:
        thisPlayer.position.x -= 400 * dt
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        thisPlayer.position.x += 400 * dt
    if keys[pygame.K_SPACE]:
        thisPlayer.shoot()

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()