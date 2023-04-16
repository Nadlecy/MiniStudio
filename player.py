import pygame

class Player ():
    def __init__(self, currentSurface, visualsList = [],  currentVisualsFrame = 0, visualsDelayer = 0, shotVisuals = "shot.png",damage = 1,shotSpeed = 2, shotCoolDown = 20, currentShotCoolDown = 0, shotsList = [] , position = pygame.Vector2(0,0) ,lives = 3):
        # general data
        self.currentSurface = currentSurface # which surface the player is currently seen
        self.position = position # the player's position on screen
        self.lives = lives # number of lives the player has

        # visuals data
        self.visualsList = visualsList # list of paths to the different frames of the character's animation
        self.currentVisualsFrame =  currentVisualsFrame # which animation frame is currently displayed
        self.visualsDelayer = visualsDelayer # counts the delay between animation frames

        # bullet data
        self.shotVisuals = shotVisuals # what the player's attacks look like
        self.damage = damage # the current damage dealt by the player's attacks
        self.shotSpeed = shotSpeed # the speed at which the player's attacks will travel
        self.shotCoolDown = shotCoolDown # total delay between each attack
        self.currentShotCoolDown = currentShotCoolDown # decreases over time, counts time before next attack
        self.shotsList = shotsList # stores every bullet fired by the player


    def shoot (self):
        if self.currentShotCoolDown < 1:
            self.shotsList.append(PlayerBullet(self.currentSurface, self.damage, self.shotSpeed, pygame.Vector2(self.position.x+80,self.position.y+40)))
            self.currentShotCoolDown = 0 + self.shotCoolDown
    
    def animate (self):
        self.visualsDelayer +=1
        if self.visualsDelayer == 14:
                self.visualsDelayer = 0
                if self.currentVisualsFrame == len(self.visualsList) - 1:
                    self.currentVisualsFrame = 0
                else :
                    self.currentVisualsFrame +=1
        self.currentSurface.blit(pygame.transform.scale(pygame.image.load(self.visualsList[self.currentVisualsFrame]),(80,80)), self.position)

class PlayerBullet ():
    def __init__(self, currentSurface, dmg, spd, position = pygame.Vector2(0,0)):
        self.currentSurface = currentSurface
        self.dmg = dmg
        self.spd = spd
        self.position = position

    #making the visible bullets move every frame
    def move(self, dt):
        if self.currentSurface.get_width() + 40 > self.position.x:
            pygame.draw.circle(self.currentSurface, "green", self.position, 10)
            self.position.x += 300 * dt * self.spd
            return True
        else:
            return False
