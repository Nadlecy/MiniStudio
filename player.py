import pygame
from animation import animation_init, animate_loop
import time

class Player ():
    def __init__(self, currentSurface, currentVisuals, shotVisuals = "shot.png",damage = 1,shotSpeed = 3, shotCoolDown = 20, currentShotCoolDown = 0, shotsList = [] , position = pygame.Vector2(0,0) ,lives = 3,laserSprite = "laserSprite.png"):
        # general data
        self.currentSurface = currentSurface # which surface the player is currently seen
        self.currentVisuals = currentVisuals # which spritesheet will be used to animate the player
        self.position = position # the player's position on screen
        self.lives = lives # number of lives the player has
        self.speed = 400
        # bullet data
        self.shotVisuals = shotVisuals # what the player's attacks look like
        self.damage = damage # the current damage dealt by the player's attacks
        self.shotSpeed = shotSpeed # the speed at which the player's attacks will travel
        self.shotCoolDown = shotCoolDown # total delay between each attack
        self.currentShotCoolDown = currentShotCoolDown # decreases over time, counts time before next attack
        self.shotsList = shotsList # stores every bullet fired by the player
        self.lastHitTime = 0
        self.powerUps = []
        self.inventoryBoost = {
            "ASPBoost" : 1,
            "Shield" : 0,
            "Grenade": 0,
            "Laser" : 0,
            "Heal" : 0
        }
        self.shield = False
        self.laser = True
        self.laserSprite = laserSprite
        animation_init(self, spritesheet_name = self.currentVisuals, animationType = "player_anim")



    def playerAnimate(self):
        animate_loop(self, rescale_size = (self.currentSurface.get_width()/16, (self.currentSurface.get_height()/9)*2))

    def laserColision(self,Object:pygame.Vector2,size):
        pass

    def shoot (self):
        if self.currentShotCoolDown < 1:
            self.shotsList.append(PlayerBullet(self.currentSurface, self.damage, self.shotSpeed, pygame.Vector2(self.position.x+80,self.position.y+20)))
            self.currentShotCoolDown = 0 + self.shotCoolDown


    def Collision (self,Object:pygame.Vector2,size):
        offset = pygame.Vector2(size/2,size/2)
        obj_vect = Object + offset
        player_vect = self.position + offset
        distance = (obj_vect-player_vect).magnitude()
        if distance < size:
            return True
        else:
            return False
        

class PlayerBullet ():
    def __init__(self, currentSurface, dmg, spd, position = pygame.Vector2(0,0)):
        self.currentSurface = currentSurface
        self.dmg = dmg
        self.spd = spd
        self.position = position
        self.bullet_sprite = pygame.transform.scale(pygame.image.load('image/player_laser.png'),(self.currentSurface.get_width()/16, self.currentSurface.get_height()/9))


    #making the visible bullets move every frame
    def move(self, dt):
        if self.currentSurface.get_width() + 40 > self.position.x:
            self.currentSurface.blit(self.bullet_sprite, self.position)
            self.position.x += self.currentSurface.get_width()/4 * dt * self.spd
            return True
        else:
            return False
        
    def isCollision (self,Object:pygame.Vector2,size):
        offset = pygame.Vector2(size/2,size/2)
        vect = Object + pygame.Vector2(size/2,size/2)
        bullet_vect = self.position + offset
        distance = (vect-bullet_vect).magnitude()
        if distance < size/2:
            return True
        else:
            return False


