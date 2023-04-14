import random
import pygame
import math

#making the Enemy class for everything that revolves around basic adversaries
class Enemy():
    def __init__(self, screen, hp:int = 1, enemyType:int = 1, speed:int = 1, position:pygame.Vector2 = (0,0)):
        self.screen = screen
        self.hp = hp
        self.type = enemyType
        self.speed = speed
        self.position = position

    # generating the enemy and starting its script
    def spawn(self):
        pass

    #everything that happens while the enemy exists
    def ai(self):
        pass

    # removing the enemy from the screen etc
    def die(self):
        pass
