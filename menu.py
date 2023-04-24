import pygame

class Button:
    def __init__(self):
        self.name = "Ratio"

class Menu:
    def __init__(self):
        self.surf = pygame.display.get_surface()
        self.width = self.surf.get_width()
        self.height = self.surf.get_height()
        self.splash = pygame.transform.scale(pygame.image.load('image/menu_bg_space.png'), (self.width,self.height))
        self.logo = pygame.transform.scale(pygame.image.load('image/menu_logo.png'), (self.width/2.5, self.height/2.5))
        self.msg =  pygame.transform.scale(pygame.image.load('image/press_start.png'), (self.width/2.5, self.height/20))
        # 0:no update,  1:continue, 2:quit 
        self.status = 0

    def splash_screen(self):
        self.surf.blit(self.splash, (0, 0))
        logo_mid_width = self.logo.get_width()/2
        logo_mid_height = self.logo.get_height()/2
        self.surf.blit(self.logo, (self.width/2-logo_mid_width, self.height/3.5-logo_mid_height))
        msg_mid_width = self.logo.get_width()/2
        msg_mid_height = self.logo.get_height()/2
        self.surf.blit(self.msg, (self.width/2-msg_mid_width, self.height-msg_mid_height))
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                self.status = 1
            elif event.type == pygame.QUIT:
                self.status = 2

    def menu_screen(self):
        pass
