import random
import pygame
from animation import animation_init, animate

#making the Enemy class for everything that revolves around basic adversaries
class Enemy():
    def __init__(self, currentSurface, currentVisuals = "enemy_anim1", hp:int = 1, enemyType:int = 0, visualsList:str = "", speed:int = 1, position:pygame.Vector2 = (0,0), isOnScreen:bool = False):
        self.currentSurface = currentSurface
        self.currentVisuals = currentVisuals # which spritesheet will be used to animate the player
        self.hp = hp
        self.enemyType = enemyType
        self.visualsList = visualsList
        self.speed = speed
        self.position = position
        self.isOnScreen = isOnScreen


        # animation
        
        animation_init(self, spritesheet_name = self.currentVisuals, animationType = "enemy")
        

    def enemyAnimate(self):
        animate(self, rescale_size = (80,80))



    # generating the enemy and starting its script
    def spawn(self):
        if self.position == pygame.Vector2(0,0):
            self.position = pygame.Vector2(self.currentSurface.get_width() , random.randint ( (self.currentSurface.get_height()/9)*2 , (self.currentSurface.get_height()/9)*8 ) )

        # maybe delete that next line and do something smarter
        return self



    #everything that happens every frame while the enemy exists
    def ai(self):
        match self.enemyType:
            case 0:
                self.position.x -= 2
                animate(self, rescale_size = (80,80))


    # removing the enemy from the screen etc
    def die(self):
        return self.hp <= 0 