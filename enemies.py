import random
import pygame, time
from animation import animation_init, animate_loop, animate_one
from helpers import lerp, clamp01
from spritesheet import Spritesheet

#making the Enemy class for everything that revolves around basic adversaries
class Enemy():
    def __init__(self, currentSurface, hp, currentVisuals = "enemy_anim1", enemyType:int = 0, animationType = "enemy", speed:int = 800, position:pygame.Vector2 = (0,0), isOnScreen:bool = False):
        self.currentSurface = currentSurface
        self.animationType = animationType
        self.currentVisuals = currentVisuals # which spritesheet will be used to animate the player
        self.hp = hp
        self.enemyType = enemyType
        self.speed = speed
        self.position = position
        self.isOnScreen = isOnScreen
        self.shotSpeed = 2
        self.damage = 1
        self.currentShotCoolDown = random.randint(3,6)
        self.shotCooldown = 70
        self.laserCooldown = 8
        self.currentLaserCoolDown = int(random.randint(self.laserCooldown / 2, self.laserCooldown) * 60)
        self.laserCooldown *= 60
        self.shotsList = []
        self.lasersList = []
        self.up = False

        if self.enemyType == 1:
            self.isGoingUp = True

        # animation
        
        animation_init(self, spritesheet_name = self.currentVisuals, animationType = self.animationType)
        
    

    def enemyAnimate(self):
        # change the size values to adapt with the screen size
        animate_loop(self, rescale_size = (80,80))



    # generating the enemy and starting its script
    def spawn(self):
        if self.enemyType == 0 or 1 or 2 or 3:
            if self.position == pygame.Vector2(0,0):
                self.position = pygame.Vector2(self.currentSurface.get_width() , random.randint ( (self.currentSurface.get_height()/9)*2 , (self.currentSurface.get_height()/9)*7 ))
        if self.enemyType == 4:
            self.position = pygame.Vector2(self.currentSurface.get_width() , self.currentSurface.get_height()/6)
        if self.position == pygame.Vector2(0,0):
            self.position = pygame.Vector2(self.currentSurface.get_width() , random.randint ( (self.currentSurface.get_height()/9) , (self.currentSurface.get_height()/9)*7 ))


        return self
    
    def shoot_type1 (self):
        if self.currentShotCoolDown < 1:
            self.shotsList.append(EnemyBullet(self.currentSurface, self.damage, self.shotSpeed,0,False, pygame.Vector2(self.position.x-self.currentSurface.get_width()/16, self.position.y+self.currentSurface.get_height()/72)))
            self.currentShotCoolDown = 0 + self.shotCooldown
    
    def shoot_type2(self):
        if self.currentShotCoolDown < 1:
            self.shotsList.append(EnemyBullet(self.currentSurface, self.damage, self.speed,0,False,pygame.Vector2(self.position.x-self.currentSurface.get_width()/16, self.position.y+self.currentSurface.get_height()/72)))
            self.currentShotCoolDown = 0 + self.shotCooldown

    def shoot_boss1_type1(self):
        if self.currentShotCoolDown < 7:
            self.shotsList.append(EnemyBullet(self.currentSurface, self.damage, self.speed,0,False,pygame.Vector2(self.position.x-self.currentSurface.get_width()/16, self.position.y+self.currentSurface.get_height()/2)))
            self.shotsList.append(EnemyBullet(self.currentSurface, self.damage, self.speed,0,False,pygame.Vector2(self.position.x-self.currentSurface.get_width()/16, self.position.y+self.currentSurface.get_height()/4)))
            self.shotsList.append(EnemyBullet(self.currentSurface, self.damage, self.speed,0,False,pygame.Vector2(self.position.x-self.currentSurface.get_width()/16, self.position.y+self.currentSurface.get_height()/16)))
            self.currentShotCoolDown = 0 + self.shotCooldown

    def shoot_boss1_type2(self, surf, plr):
        self.currentLaserCoolDown += 1
        if self.currentLaserCoolDown >= self.laserCooldown:
            ray = Ray(surf, plr, self.position)
            self.lasersList.append(ray)
            self.currentLaserCoolDown = 0

    #everything that happens every frame while the enemy exists
    def ai(self,player,dt):
        match self.enemyType:
            #change movement values to take in account the framerate

            #penguin
            case 0:
                self.position.x -= (self.currentSurface.get_width()/6) * dt 
                self.shoot_type1()
                animate_loop(self, rescale_size = (self.currentSurface.get_width()/16, self.currentSurface.get_height()/9))

            #swallow
            case 1:
                dir = (self.position - player.position).normalize()
                self.position -= dir * self.currentSurface.get_width()/3 * dt
                animate_loop(self, rescale_size = (self.currentSurface.get_width()/16, self.currentSurface.get_height()/9))

            #chicken
            case 2:
                self.position.x -= (self.speed - 700) * dt
                self.shoot_type2()
                animate_loop(self,rescale_size=(self.currentSurface.get_width()/16,self.currentSurface.get_height()/9))

            #pigeon
            case 3:
                animate_loop(self,rescale_size=(self.currentSurface.get_width()/16,self.currentSurface.get_height()/9))
                self.shoot_type1()
                if self.position.x > self.currentSurface.get_width()-self.currentSurface.get_width()/16:
                    self.position.x -= (self.speed - 700) * dt
                else:
                    if self.position.y >= self.currentSurface.get_height()/10 and self.up == False:
                        self.position.y -= round((self.speed - 500) * dt)
                        if self.position.y < self.currentSurface.get_height()/9:
                            self.up = True
                    elif self.position.y + 80 < (self.currentSurface.get_height() - self.currentSurface.get_height()/9) and self.up == True:
                        self.position.y += round((self.speed - 500) * dt)
                        if self.position.y + 85 > self.currentSurface.get_height() - self.currentSurface.get_height()/9:
                            self.up = False
            #boss 1
            case 4:
                self.shoot_boss1_type1()
                self.shoot_boss1_type2(self.currentSurface, player)
                animate_loop(self, rescale_size = (self.currentSurface.get_width()/3, self.currentSurface.get_height()/1.5))
                if self.position.x > self.currentSurface.get_width()-self.currentSurface.get_width()/3:
                    self.position.x -= (self.speed - 350) * dt
                else:
                    if self.position.y >= self.currentSurface.get_height()/11 and self.up == False:
                        self.position.y -= round((self.speed - 500) * dt)
                        if self.position.y < self.currentSurface.get_height()/10:
                            self.up = True
                    elif self.position.y + 80 < (self.currentSurface.get_height() - self.currentSurface.get_height()/9) and self.up == True:
                        self.position.y += round((self.speed - 500) * dt)
                        if self.position.y +self.currentSurface.get_height()/1.5 > self.currentSurface.get_height() - self.currentSurface.get_height()/9:
                            self.up = False

    # removing the enemy from the screen etc
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
    def move_type1(self, dt):
        if 40 < self.position.x:
            self.currentSurface.blit(self.bullet_sprite, self.position)
            self.position.x -= self.currentSurface.get_width()/5 * dt * self.spd
            return True
        else:
            return False
    
    def move_type2_state1(self, dt,player,enemy):
        if not self.broken and self.position.x <= player.position.x + 150 and 40 < self.position.x:
            enemy.shotsList.append(EnemyBullet(self.currentSurface, self.dmg, self.spd,1,True,pygame.Vector2(self.position.x-self.currentSurface.get_width()/16, self.position.y+self.currentSurface.get_height()/72)))
            enemy.shotsList.append(EnemyBullet(self.currentSurface, self.dmg, self.spd,0,True,pygame.Vector2(self.position.x-self.currentSurface.get_width()/16, self.position.y+self.currentSurface.get_height()/72)))
        elif 40 < self.position.x :
            self.currentSurface.blit(pygame.transform.scale(pygame.image.load('image/egg.png'),(self.currentSurface.get_width()/32, self.currentSurface.get_height()/16)), self.position)
            self.position.x -= self.currentSurface.get_width()/8 * dt * self.spd
            return True
        else:
            return False
        
    def move_type2_state2(self, dt):
        if 40 < self.position.x and self.broken and self.rotation == 1:
            self.currentSurface.blit(pygame.transform.scale(pygame.image.load('image/egg_top.png'),(self.currentSurface.get_width()/64, self.currentSurface.get_height()/32)), self.position)
            self.position.y -= self.currentSurface.get_height()/7 * dt
            return True
        elif 40 < self.position.x and self.broken and self.rotation == 0:
            self.currentSurface.blit(pygame.transform.scale(pygame.image.load('image/egg_bottom.png'),(self.currentSurface.get_width()/64, self.currentSurface.get_height()/32)), self.position)
            self.position.y += self.currentSurface.get_height()/7 * dt
            return True
        else :
            return False
        
    def move_boss_type1(self, dt):
        if 40 < self.position.x:
            self.currentSurface.blit(pygame.transform.scale(pygame.image.load('image/plume_proj.png'),(self.currentSurface.get_width()/32, self.currentSurface.get_height()/16)), self.position)
            self.position.x -= self.currentSurface.get_width()/5 * dt * self.spd
            return True
        else:
            return False
    
    def move_boss_type1(self, dt):
        if 40 < self.position.x:
            self.currentSurface.blit(pygame.transform.scale(pygame.image.load('spritesheets/plume_proj_off.png'),(self.currentSurface.get_width()/32, self.currentSurface.get_height()/16)), self.position)
            self.position.x -= self.currentSurface.get_width()/5 * dt * self.spd
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

class Ray:
    duration = 1
    sprite_count = 15
    ray_width_ratio = 0.7

    def __init__(self, surf, player, enemy_pos):
        self.displaySurf = surf
        self.player = player
        self.position = (0, enemy_pos.y + surf.get_width()/3*0.5)
        self.lifetime = 0
        self.alpha = 0
        self.dealth_damage = False
        self.sprite_index = 0
        self.sprites = []
        self.spritesheet = Spritesheet("spritesheets/laser_Boss.png", "laser_Boss")
        self.expired = False
        self.ray_height = surf.get_width()/8
        self.ray_size = (surf.get_width() * self.ray_width_ratio, self.ray_height)
        self.load_frames()
        self.hitbox_size = (self.ray_size[0], self.ray_size[1] * 0.6)
        self.rect = pygame.Rect(self.position + pygame.Vector2(0, self.ray_size[1] * .2), self.hitbox_size)

    def update(self, dt):
        self.lifetime += dt
        self.alpha = clamp01(self.lifetime / self.duration)
        self.player_collision()

        self.expired = self.lifetime >= self.duration
    
    def render(self):
        self.displaySurf.blit(self.get_sprite(), self.position)

    def get_sprite(self):
        self.sprite_index = int(lerp(0, self.sprite_count, self.alpha))
        return self.sprites[self.sprite_index]

    def player_collision(self):
        plr_size = self.displaySurf.get_width() / 16
        plr_rect = pygame.Rect(self.player.position, pygame.Vector2(1,1) * plr_size)
        if self.rect.colliderect(plr_rect) and not self.dealth_damage:
            if 5 < self.sprite_index < 13:
                self.dealth_damage = True
                self.player.lives -= 1
                self.player.lastHitTime = time.time()

    def load_frames(self):
        for i in range (self.spritesheet.length):
            sprite = self.spritesheet.parse_sprite("laser_Boss " + str(i) + ".png")
            upscale_sprite = pygame.transform.scale(sprite, self.ray_size)
            self.sprites.append(upscale_sprite)