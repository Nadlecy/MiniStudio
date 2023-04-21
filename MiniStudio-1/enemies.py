import random
import pygame
import math

#making the Enemy class for everything that revolves around basic adversaries
class Enemy():
    def __init__(self, currentSurface, hp:int = 1, enemyType:int = 0, visualsList:str = "", speed:int = 1, position:pygame.Vector2 = (0,0), isOnScreen:bool = False):
        self.currentSurface = currentSurface
        self.hp = hp
        self.enemyType = enemyType
        self.visualsList = visualsList
        self.speed = speed
        self.position = position
        self.isOnScreen = isOnScreen

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
                self.currentSurface.blit(pygame.transform.scale(pygame.image.load("image/enemy_0.png"),(80,80)), self.position)


    # removing the enemy from the screen etc
    def die(self):
        return self.hp <= 0 
