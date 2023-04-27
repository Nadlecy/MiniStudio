import pygame

from enemies import Enemy
from animation import animation_init, animate_loop
import time

class Player ():
    def __init__(self, currentSurface, currentVisuals, shotVisuals = "shot.png",damage = 1,shotSpeed = 3, shotCoolDown = 20, currentShotCoolDown = 0, shotsList = [] , position = pygame.Vector2(0,0) ,lives = 3,laserSprite = "laserSprite.png", playerScore = 0, playerKills = 0):
        # general data
        self.currentSurface = currentSurface # which surface the player is currently seen
        self.playerScore = playerScore
        self.playerKills = playerKills
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
            "ASPBoost" : 0,
            "Shield" : 1,
            "Grenade" : 3,
            "Laser" : 0,
            "Heal" : 2
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


    def Collision (self,Object:pygame.Vector2,size,playerSize):
        offset = pygame.Vector2(size/2,size/2)
        player_offset = pygame.Vector2(playerSize/2,playerSize/2)
        obj_vect = Object + offset
        player_vect = self.position + player_offset
        distance = (obj_vect-player_vect).magnitude()
        return distance < size/2
    
    def addScore(self, score):
        self.playerScore += score

    def addDeath(self):
        self.playerKills += 1
        
    def die(self):
        if self.lives <= 0:
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
        
    def isCollision (self,Object:pygame.Vector2,size,bulletsize):
        offset = pygame.Vector2(size/2,size/2)
        bullet_offset = pygame.Vector2(bulletsize/2,bulletsize/2)
        vect = Object + offset
        bullet_vect = self.position + bullet_offset
        distance = (vect-bullet_vect).magnitude()
        return distance < size/2
