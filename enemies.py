import random
import pygame
import math

#making the Enemy class for everything that revolves around basic adversaries
class Enemy():
    def __init__(self, hp:int, enemyType:int, speed, position):
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
