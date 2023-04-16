import pygame

class Player ():
    def __init__(self, currentSurface, visualsList = [], visualsDelayer = 0, shotVisuals = "shot.png",damage = 1,shotSpeed = 2, shotCoolDown = 20, currentShotCoolDown = 0, shotsList = [] , position = pygame.Vector2(0,0) ,lives = 3):
        self.currentSurface = currentSurface
        self.visualsList = visualsList
        self.visualsDelayer = visualsDelayer
        self.shotVisuals = shotVisuals
        self.damage = damage
        self.shotSpeed = shotSpeed
        self.shotCoolDown = shotCoolDown
        self.currentShotCoolDown = currentShotCoolDown
        self.position = position
        self.shotsList = shotsList
        self.lives = 3

    def shoot (self):
        if self.currentShotCoolDown < 1:
            self.shotsList.append(PlayerBullet(self.currentSurface, self.damage, self.shotSpeed, pygame.Vector2(self.position.x+80,self.position.y+40)))
            self.currentShotCoolDown = 0 + self.shotCoolDown
    
    def animate (self):
        self.visualsDelayer +=1
        if self.visualsDelayer == 28:
                self.visualsDelayer = 0
        if self.visualsDelayer <= 14 :
            return pygame.transform.scale(pygame.image.load(self.visualsList[0]),(80,80))
        else:
            return pygame.transform.scale(pygame.image.load(self.visualsList[1]),(80,80))


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
