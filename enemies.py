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



    #everything that happens every frame while the enemy exists
    def ai(self):
        match self.enemyType:
            #change movement values to take in account the framerate
            case 0:
                self.position.x -= 2
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