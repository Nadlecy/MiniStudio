import pygame
from helpers import lerp
from easing_functions import *

class FadingSurf:
    def __init__(self, surf:pygame.Surface, fadingSpeed:float=1.0):
        self.surf = surf
        self.t = 0
        self.order = 1
        self.speed = fadingSpeed
        
    def fade(self, dt):
        self.t += dt * self.speed * self.order
        if 0.0 >= self.t or self.t >= 1.0:
            self.order *= -1
        alpha = lerp(255, 0, self.t, QuadEaseIn())
        self.surf.set_alpha(alpha)