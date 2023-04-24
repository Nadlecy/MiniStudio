import pygame
import json

class Spritesheet:
    def __init__(self, filename, animationType):
        self.filename = filename
        self.sprite_sheet = pygame.image.load(filename).convert()

        #determining which json to use depending on the animationType
        self.meta_data = "spritesheets/" + animationType + ".json"
        with open(self.meta_data) as f:
            self.data = json.load(f)
            self.length= len(self.data["frames"])
        f.close()


    def get_sprite(self, x, y, w, h):
        sprite = pygame.Surface((w, h))
        sprite.set_colorkey((0,0,0))
        sprite.blit(self.sprite_sheet,(0, 0),(x, y, w, h))
        return sprite

    def parse_sprite(self, name):
        sprite = self.data['frames'][name]['frame']
        x, y, w, h = sprite["x"], sprite["y"], sprite["w"], sprite["h"]
        image = self.get_sprite(x, y, w, h)
        return image
