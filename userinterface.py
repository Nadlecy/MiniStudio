import pygame
from fade import FadingSurf

from pygame.mouse import get_pos as mouse_pos
from pygame.mouse import get_pressed as mouse_buttons

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
        self.splash = pygame.transform.scale(pygame.image.load('image/menu_bg_space.png'), (self.width,self.height))
        self.logo = pygame.transform.scale(pygame.image.load('image/menu_logo.png'), (self.width/2.5, self.height/2.5))
        self.msg =  pygame.transform.scale(pygame.image.load('image/press_start.png'), (self.width/2.5, self.height/20))
        self.fadingText = FadingSurf(self.msg, 0.5)

        self.newGameButton = Button((160*self.width/550, 32*self.height/300),(self.width/4.75,self.height/1.75),'image/new_game_min.png')
        self.newGameButton.bind(self.handleNewGame)
        self.resumeButton = Button((160*self.width/550, 32*self.height/300),(self.width/1.999,self.height/1.75),'image/resume_min.png')
        self.resumeButton.bind(self.handleResume)
        self.howToPlayButton = Button((160*self.width/550, 32*self.height/300),(self.width/4.75,self.height/1.4),'image/how_to_min.png')
        self.howToPlayButton.bind(self.handleHowToPlay)
        self.optionsButton = Button((160*self.width/550, 32*self.height/300),(self.width/1.999,self.height/1.4),'image/options_min.png')
        self.optionsButton.bind(self.handleOptions)
        self.quitButton = Button((64*self.width/600, 32*self.height/300),(self.width/160,self.height/1.12),'image/quit.png')
        self.quitButton.bind(self.handleQuit)
        self.backButton = Button((64*self.width/600, 32*self.height/300),(self.width/160,self.height/1.12),'image/quit.png')
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
        self
        self.surf.blit(self.splash, (0, 0))

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
    def __init__(self):
        pass

