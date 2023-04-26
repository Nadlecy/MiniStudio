import pygame
from fade import FadingSurf
from player import Player

from pygame.mouse import get_pos as mouse_pos
from pygame.mouse import get_pressed as mouse_buttons
from pygame.image import load

class Button:
  def __init__(self, size, pos, sprite_path):
    self.displaySurf = pygame.display.get_surface()
    self.size = size
    self.position = pos
    self.sprite = pygame.transform.scale(pygame.image.load(sprite_path), size)
    self.to = None
    self.isPressed = False

  def bind(self, to):
    self.to = to

  def draw(self):
    rect = self.displaySurf.blit(self.sprite, self.position)
    
    if self.to and not self.isPressed and rect.collidepoint(mouse_pos()) and mouse_buttons()[0]:
      self.isPressed = True
      self.to()
    else:
      self.isPressed = False


class Menu:
    def __init__(self):
        self.surf = pygame.display.get_surface()
        self.width = self.surf.get_width()
        self.height = self.surf.get_height()
        self.splash = pygame.transform.scale(pygame.image.load('image/menu/bg_space.png'), (self.width,self.height))
        self.logo = pygame.transform.scale(pygame.image.load('image/menu/menu_logo.png'), (self.width/2.5, self.height/2.5))
        self.msg =  pygame.transform.scale(pygame.image.load('image/menu/press_start.png'), (self.width/2.5, self.height/20))
        self.fadingText = FadingSurf(self.msg, 0.5)

        largeButtonSize = (160*self.width/550, 32*self.height/300)
        smallButtonSize = (64*self.width/600, 32*self.height/300)
        self.newGameButton = Button(largeButtonSize,(self.width/4.75,self.height/1.75),'image/menu/new_game_min.png')
        self.resumeButton = Button(largeButtonSize,(self.width/1.999,self.height/1.75),'image/menu/resume_min.png')
        self.howToPlayButton = Button(largeButtonSize,(self.width/4.75,self.height/1.4),'image/menu/how_to_min.png')
        self.optionsButton = Button(largeButtonSize,(self.width/1.999,self.height/1.4),'image/menu/options_min.png')
        self.quitButton = Button(smallButtonSize,(self.width/160,self.height/1.12),'image/menu/quit.png')
        self.backButton = Button(smallButtonSize,(self.width/160,self.height/1.12),'image/menu/quit.png')
        self.newGameButton.bind(self.handleNewGame)
        self.resumeButton.bind(self.handleResume)
        self.howToPlayButton.bind(self.handleHowToPlay)
        self.optionsButton.bind(self.handleOptions)
        self.quitButton.bind(self.handleQuit)
        self.backButton.bind(self.handleBack)

        # 0:no update,  1:continue, 2:quit 
        self.splash_status = 0
        self.home_status = 0

    def splash_screen(self,dt):
        self.surf.blit(self.splash, (0, 0))
        logo_mid_width = self.logo.get_width()/2
        logo_mid_height = self.logo.get_height()/2
        self.surf.blit(self.logo, (self.width/2-logo_mid_width, self.height/3.5-logo_mid_height))
        msg_mid_width = self.logo.get_width()/2
        msg_mid_height = self.logo.get_height()/2
        self.surf.blit(self.msg, (self.width/2-msg_mid_width, self.height-msg_mid_height))
        self.fadingText.fade(dt, 255, 0)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                self.splash_status = 1
            elif event.type == pygame.QUIT:
                self.splash_status = 2

    def menu_screen(self):
        self.surf.blit(self.splash, (0, 0))
        logo_mid_width = self.logo.get_width()/2
        logo_mid_height = self.logo.get_height()/2
        self.surf.blit(self.logo, (self.width/2-logo_mid_width, self.height/3.5-logo_mid_height))

        self.newGameButton.draw()
        self.resumeButton.draw()
        self.howToPlayButton.draw()
        self.optionsButton.draw()
        self.quitButton.draw()

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.QUIT:
                    self.home_status = 2

    def handleNewGame(self):
        self.home_status = 1

    def handleResume(self):
        print("Resuming")
        # Handles its shit
        pass

    def handleHowToPlay(self):
        print("How to play ?")
        # Handles its shit
        pass

    def handleOptions(self):
        self.surf.blit(self.splash, (0, 0))

    def musicOption():
        pass


    def handleQuit(self):
        pygame.quit()

    def handleBack(self):
        self.home_status = 1

    def menu_pause(self):
        pass
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pass


class ATH:
    img_life_array = {3:"three_lives.png", 2:"two_lives.png", 1:"one_life.png", 0:"zero_lives.png"}
    img_nade_array = {3:"three_nade.png", 2:"two_nade.png", 1:"one_nade.png", 0:"zero_nade.png"}
    img_heal_array = {3:"three_heal.png", 2:"two_heal.png", 1:"one_heal.png", 0:"zero_heal.png"}
    img_shield_array = {1:"one_shield.png", 0:"zero_shield.png"}
    img_gun_array = {1:"one_gun.png", 0:"zero_gun.png"}

    def __init__(self, player):
        self.surf = pygame.display.get_surface()
        self.width = self.surf.get_width()
        self.height  = self.surf.get_height()
        self.player = player

    def displayLifebar(self):
        lifebar_surf = pygame.transform.scale(load("image/ath/lifebar/"+self.img_life_array[self.player.lives]),(160*self.surf.get_width()/500,44*self.surf.get_width()/500))
        self.surf.blit(lifebar_surf, (0,0))
        if self.player.lives == 0:
            pygame.quit()


    def displayGadgetbar(self):
        resizing_width = self.width/600
        resizing_height = self.height/600
        self.gadget_surf = pygame.Surface((192*resizing_width,48*resizing_width), pygame.SRCALPHA)
        gadget_slot_one = pygame.transform.scale(load("image/ath/gadget/boost1_overlay.png"),(48*resizing_width,16*resizing_width))
        gadget_slot_two = pygame.transform.scale(load("image/ath/gadget/boost2_overlay.png"),(48*resizing_width,16*resizing_width))
        gadget_slot_three = pygame.transform.scale(load("image/ath/gadget/boost3_overlay.png"),(48*resizing_width,16*resizing_width))
        gadget_slot_four = pygame.transform.scale(load("image/ath/gadget/boost4_overlay.png"),(48*resizing_width,16*resizing_width))
        heal_icon = pygame.transform.scale(load("image/ath/gadget/"+self.img_nade_array[self.player.inventoryBoost["Heal"]]),(32*resizing_width,32*resizing_width))
        nade_icon = pygame.transform.scale(load("image/ath/gadget/"+self.img_heal_array[self.player.inventoryBoost["Grenade"]]),(32*resizing_width,32*resizing_width))
        shield_icon = pygame.transform.scale(load("image/ath/gadget/"+self.img_shield_array[self.player.inventoryBoost["Shield"]]),(32*resizing_width,32*resizing_width))
        gun_icon = pygame.transform.scale(load("image/ath/gadget/"+self.img_gun_array[self.player.inventoryBoost["ASPBoost"]]),(32*resizing_width,32*resizing_width))


        self.gadget_surf.blit(gadget_slot_one, (0,0))
        self.gadget_surf.blit(gadget_slot_two, (48*resizing_width,0))
        self.gadget_surf.blit(gadget_slot_three, (96*resizing_width,0))
        self.gadget_surf.blit(gadget_slot_four, (144*resizing_width,0))
        self.gadget_surf.blit(heal_icon, (8*resizing_width,16*resizing_height))
        self.gadget_surf.blit(nade_icon, (56*resizing_width,16*resizing_height))
        self.gadget_surf.blit(shield_icon, (104*resizing_width,16*resizing_height))
        self.gadget_surf.blit(gun_icon, (152*resizing_width,16*resizing_height))
        self.surf.blit(self.gadget_surf, (0,self.height-(75*resizing_height)))

    def displayLighting(self):
        lighting = pygame.transform.scale(load("image/ath/lueur_all.png"),(self.width, self.height))
        self.surf.blit(lighting,(0,0))
        