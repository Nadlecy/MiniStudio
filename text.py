import pygame

class Text:

    def __init__(self, font:str, fontSize:int):
        self.surf = pygame.display.get_surface()
        self.font = font
        self.textFont = pygame.font.SysFont(self.font,fontSize)
        

    def drawText(self, text, text_col):
        self.msg = self.textFont.render(text, True, text_col)
        return self.msg

