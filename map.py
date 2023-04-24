import pygame
    
class GridObjects():
    def __init__(self, visualPath, sizeOnGrid = [1, 1]):
        self.size = sizeOnGrid
        self.image = pygame.image.load(visualPath)
        #, (self.size[0] * (pygame.display.get_surface().get_width() / 9),self.size[1]  * (pygame.display.get_surface().get_height() / 9))) 

#one grid is 7x16
#each grid contains a list of all the objects it will load, along with their positions
#each grid knows which grid comes next
#some grids have two following grids, that's where the player may split paths
class MapSection():
    def __init__(self, gridItems, nextSection, secondarySection = None, pixelsAdvanced = 0):
        self.gridItems = gridItems
        self.nextSection = nextSection
        self.secondarySection = secondarySection
        self.pixelsAdvanced = pixelsAdvanced

    def loadGrid(self, screen):
        # shows and gives collision to elements in the grid
        pass

    def advance(self):
        pass
