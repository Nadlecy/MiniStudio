import random
import pygame
from animation import animation_init, animate_loop, animate_one

#making the Enemy class for everything that revolves around basic adversaries
class Enemy():
    def __init__(self, currentSurface, currentVisuals = "enemy_anim1", hp:int = 1, enemyType:int = 0, speed:int = 1, position:pygame.Vector2 = (0,0), isOnScreen:bool = False):
        self.currentSurface = currentSurface
        self.currentVisuals = currentVisuals # which spritesheet will be used to animate the player
        self.hp = hp
        self.enemyType = enemyType
        self.speed = speed
        self.position = position
        self.isOnScreen = isOnScreen
        self.shotSpeed = 2
        self.damage = 1
        self.currentShotCoolDown = random.randint(10, 55)
        self.shotCooldown = 55
        self.shotsList = []

        if self.enemyType == 1:
            self.isGoingUp = True

        # animation
        
        animation_init(self, spritesheet_name = self.currentVisuals, animationType = "enemy")
        
    

    def enemyAnimate(self):
        # change the size values to adapt with the screen size
        animate_loop(self, rescale_size = (80,80))



    # generating the enemy and starting its script
    def spawn(self):
        if self.position == pygame.Vector2(0,0):
            self.position = pygame.Vector2(self.currentSurface.get_width() , random.randint ( (self.currentSurface.get_height()/9)*2 , (self.currentSurface.get_height()/9)*8 ))

        # maybe delete that next line and do something smarter
        return self
    
    def shoot (self):
        if self.currentShotCoolDown < 1:
            self.shotsList.append(EnemyBullet(self.currentSurface, self.damage, self.shotSpeed, pygame.Vector2(self.position.x,self.position.y+40)))
            self.currentShotCoolDown = 0 + self.shotCooldown

    #everything that happens every frame while the enemy exists
    def ai(self):
        match self.enemyType:
            #change movement values to take in account the framerate
            case 0:
                self.position.x -= 2
                self.shoot()
                animate_loop(self, rescale_size = (80,80))
            case 1:
                if self.isGoingUp:
                    self.position.x -= 2
                    self.position.y -= 1 + self.position.y/96
                    if self.position.y < (self.currentSurface.get_height() / 6) - 80:
                        self.isGoingUp = False
                else:
                    self.position.x -= 2
                    self.position.y += 1 + (self.currentSurface.get_height() - self.position.y)/96
                    if self.position.y > (self.currentSurface.get_height() - (self.currentSurface.get_height() / 6)):
                        self.isGoingUp = True
                animate_loop(self, rescale_size = (80,80))



    # removing the enemy from the screen etc
    def die(self):
        return self.hp <= 0 
    
class EnemyBullet ():
    def __init__(self, currentSurface, dmg, spd, position = pygame.Vector2(0,0)):
        self.currentSurface = currentSurface
        self.dmg = dmg
        self.spd = spd
        self.position = position

    #making the visible bullets move every frame
    def move(self, dt):
        if 40 < self.position.x:
            pygame.draw.circle(self.currentSurface, "red", self.position, 10)
            self.position.x -= 200 * dt * self.spd
            return True
        else:
            return False
        
    def isCollision (self,Object:pygame.Vector2,size):
        vect = Object + pygame.Vector2(size/2,size/2)
        distance = (vect-self.position).magnitude()
        if distance < size/2:
            return True
        else:
            return False