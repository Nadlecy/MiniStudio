class boosObject():
    def __init__(self,position,currentSurface,Visual,name):
        self.position = position
        self.currentSurface = currentSurface
        self.visual = Visual
        self.name = name

    def afficher(self):
        self.currentSurface.blit(self.visual,self.position)