import pygame

class Player ():
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
            self.shotsList.append(PlayerBullet(self.currentSurface, self.dmg, self.shotSpd, pygame.Vector2(self.position.x+80,self.position.y+40)))
            self.currentShotCoolDown = 0 + self.shotCoolDown

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
