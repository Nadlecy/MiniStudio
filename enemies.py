import random
import pygame
from animation import animation_init, animate_loop, animate_one

#making the Enemy class for everything that revolves around basic adversaries
class Enemy():
    def __init__(self, currentSurface, currentVisuals = "enemy_anim1", hp:int = 1, enemyType:int = 0, speed:int = 800, position:pygame.Vector2 = (0,0), isOnScreen:bool = False):
        self.currentSurface = currentSurface
        self.currentVisuals = currentVisuals # which spritesheet will be used to animate the player
        self.hp = hp
        self.enemyType = enemyType
        self.speed = speed
        self.position = position
        self.isOnScreen = isOnScreen
        self.shotSpeed = 2
        self.damage = 1
        self.currentShotCoolDown = random.randint(10,12)
        self.shotCooldown = 70
        self.shotsList = []

        # animation
        animation_init(self, spritesheet_name = self.currentVisuals, animationType = "enemy")
        
    

    def enemyAnimate(self):
        # change the size values to adapt with the screen size
        animate_loop(self, rescale_size = (80,80))



    # generating the enemy and starting its script
    def spawn(self):
        if self.position == pygame.Vector2(0,0):
            self.position = pygame.Vector2(self.currentSurface.get_width() , random.randint ( (self.currentSurface.get_height()/9) , (self.currentSurface.get_height()/9)*7 ))

        # maybe delete that next line and do something smarter
        return self
    
    def shoot (self):
        if self.currentShotCoolDown < 1:
            self.shotsList.append(EnemyBullet(self.currentSurface, self.damage, self.shotSpeed,0,False, pygame.Vector2(self.position.x-self.currentSurface.get_width()/16, self.position.y+self.currentSurface.get_height()/72)))
            self.currentShotCoolDown = 0 + self.shotCooldown
    
    def shoot_bis(self):
        if self.currentShotCoolDown < 1:
            self.shotsList.append(EnemyBullet(self.currentSurface, self.damage, self.speed,0,False,pygame.Vector2(self.position.x-self.currentSurface.get_width()/16, self.position.y+self.currentSurface.get_height()/72)))
            self.currentShotCoolDown = 0 + self.shotCooldown

    #everything that happens every frame while the enemy exists
    def ai(self,player,dt):
        match self.enemyType:
            #change movement values to take in account the framerate
            case 0:
                self.position.x -= (self.currentSurface.get_width()/6) * dt 
                self.shoot()
                animate_loop(self, rescale_size = (self.currentSurface.get_width()/16, self.currentSurface.get_height()/9))
            case 1:
                dir = (self.position - player.position).normalize()
                self.position -= dir * self.currentSurface.get_width()/3 * dt
                animate_loop(self, rescale_size = (self.currentSurface.get_width()/16, self.currentSurface.get_height()/9))
            case 2:
                self.position.x -= (self.speed - 600) * dt
                self.shoot_bis()
                animate_loop(self,rescale_size=(self.currentSurface.get_width()/16,self.currentSurface.get_height()/9))

    # checks if the enemy has 0 or less health points
    def die(self):
        return self.hp <= 0 
    

    
class EnemyBullet ():
    def __init__(self, currentSurface, dmg, spd,rotation,broken, position = pygame.Vector2(0,0)):
        self.currentSurface = currentSurface
        self.dmg = 1
        self.spd = 2
        self.position = position
        self.bullet_sprite = pygame.transform.scale(pygame.image.load('image/enemy_laser.png'),(self.currentSurface.get_width()/16, self.currentSurface.get_height()/9))
        self.rotation = rotation
        self.broken = broken

    #making the visible bullets move every frame
    def move(self, dt):
        if 40 < self.position.x:
            self.currentSurface.blit(self.bullet_sprite, self.position)
            self.position.x -= self.currentSurface.get_width()/5 * dt * self.spd
            return True
        else:
            return False
    
    def move_bis(self, dt,player,enemy):
        if not self.broken and self.position.x <= player.position.x + 150 and 40 < self.position.x:
            enemy.shotsList.append(EnemyBullet(self.currentSurface, self.dmg, self.spd,1,True,pygame.Vector2(self.position.x-self.currentSurface.get_width()/16, self.position.y+self.currentSurface.get_height()/72)))
            enemy.shotsList.append(EnemyBullet(self.currentSurface, self.dmg, self.spd,0,True,pygame.Vector2(self.position.x-self.currentSurface.get_width()/16, self.position.y+self.currentSurface.get_height()/72)))
        elif 40 < self.position.x :
            self.currentSurface.blit(pygame.transform.scale(pygame.image.load('image/egg.png'),(self.currentSurface.get_width()/32, self.currentSurface.get_height()/16)), self.position)
            self.position.x -= self.currentSurface.get_width()/5 * dt * self.spd
            return True
        else:
            return False
        
    def move_test(self, dt):
        if 40 < self.position.x and self.broken and self.rotation == 1:
            self.currentSurface.blit(pygame.transform.scale(pygame.image.load('image/egg.png'),(self.currentSurface.get_width()/32, self.currentSurface.get_height()/16)), self.position)
            self.position.y -= self.currentSurface.get_height()/5 * dt
            return True
        elif 40 < self.position.x and self.broken and self.rotation == 0:
            self.currentSurface.blit(pygame.transform.scale(pygame.image.load('image/egg.png'),(self.currentSurface.get_width()/32, self.currentSurface.get_height()/16)), self.position)
            self.position.y += self.currentSurface.get_height()/5 * dt
            return True
        else :
            return False
        
    def isCollision (self,Object:pygame.Vector2,size):
        vect = Object + pygame.Vector2(size/2,size/2)
        distance = (vect-self.position).magnitude()
        if distance < size/2:
            return True
        else:
            return False