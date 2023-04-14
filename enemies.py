import random
import pygame
import math

#making the Enemy class for everything that revolves around basic adversaries
class Enemy():
    def __init__(self, screen, hp:int = 1, enemyType:int = 1, visuals:str = "", speed:int = 1, position:pygame.Vector2 = (0,0), isOnScreen:bool = False):
        self.screen = screen
        self.hp = hp
        self.type = enemyType
        self.visuals = visuals
        self.speed = speed
        self.position = position

    # generating the enemy and starting its script
    def spawn(self):
        if self.position == pygame.Vector2(0,0):
            self.position = pygame.Vector2(self.screen.get_width(),random.randint((self.screen.get_height()/9)*2,(self.screen.get_height()/9)*8))
        

    #everything that happens while the enemy exists
    def ai(self):
        pass

    # removing the enemy from the screen etc
    def die(self):
        pass
