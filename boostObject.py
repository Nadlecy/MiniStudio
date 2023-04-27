import pygame
import random
from animation import *
class BoostObject():
    def __init__(self, type, currentSurface, currentVisuals = "boosts_coin_gun", animationType = "boost_bouclier", position:pygame.Vector2 = (0,0)  ):
        self.type = type
        self.position = position
        self.currentSurface = currentSurface
        self.currentVisuals = currentVisuals
        self.animationType = animationType

        # animation

        animation_init(self, spritesheet_name = self.currentVisuals, animationType = self.animationType)



    def enemyAnimate(self):
        # change the size values to adapt with the screen size
        animate_loop(self, rescale_size = (80,80))

    def spawn(self):
        if self.position == pygame.Vector2(0,0):
             self.position = pygame.Vector2(self.currentSurface.get_width() , random.randint ((self.currentSurface.get_height()/9)*2 , (self.currentSurface.get_height()/9)*7 ))

        return self

    def ai(self,dt):
        self.position.x -= (self.currentSurface.get_width()/6) * dt 
        animate_loop(self, rescale_size = (self.currentSurface.get_width()/16, self.currentSurface.get_height()/9))