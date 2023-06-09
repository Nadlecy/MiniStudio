import pygame
import json

class Spritesheet:
    def __init__(self, filename, animationType):
        self.filename = filename
        self.sprite_sheet = pygame.image.load(filename).convert_alpha()

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

def load_backgrounds(spritesheet_name, animationType):
    my_spritesheet = Spritesheet('spritesheets/' + spritesheet_name + '.png', animationType)
    background_set = []
    for i in range (my_spritesheet.length) :
        print(i)
        background_set.append(my_spritesheet.parse_sprite(animationType + " " + str(i) + ".png"))
    return background_set
