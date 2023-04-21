import pygame
from spritesheet import Spritesheet

def animation_init(classname, spritesheet_name, animationType):
        pygame.sprite.Sprite.__init__(classname)
        classname.idle_frames = []
        load_frames(classname, spritesheet_name, animationType)
        print (classname.idle_frames)
        classname.rect = classname.idle_frames[0].get_rect()
        classname.rect.midbottom = (240, 244)
        classname.current_frame = 0
        classname.last_updated = 0
        classname.current_image = classname.idle_frames[0]

def animate(classname):
    now = pygame.time.get_ticks()
    if now - classname.last_updated > 50:
        classname.last_updated = now
        classname.current_frame = (classname.current_frame + 1) % len(classname.idle_frames)
        classname.current_image = classname.idle_frames[classname.current_frame]
    classname.currentSurface.blit(pygame.transform.scale (classname.idle_frames[classname.current_frame],(80,160)) , classname.position)


def load_frames(classname, spritesheet_name, animationType):

    my_spritesheet = Spritesheet('spritesheets/' + spritesheet_name + '.png', animationType)

    for i in range (my_spritesheet.length) :
        print(i)
        classname.idle_frames.append(my_spritesheet.parse_sprite(animationType + " " + str(i) + ".png"))