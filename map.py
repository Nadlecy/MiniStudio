import pygame
    
class GridObjects():
    def __init__(self, visualPath, sizeOnGrid = [1, 1]):
        self.sizeOnGrid = sizeOnGrid
        self.image = pygame.image.load(visualPath)
        #, (self.size[0] * (pygame.display.get_surface().get_width() / 9),self.size[1]  * (pygame.display.get_surface().get_height() / 9))) 

#one grid is 7x16
#each grid contains a list of all the objects it will load, along with their positions: [Gridobject, positionX, positionY]
#each grid knows which grid comes next
#some grids have a secondary grid, that's where the player may split paths
class MapSection():
    def __init__(self, nextSection, secondarySection = None, gridItems = [], pixelsAdvanced = 0):
        self.nextSection = nextSection
        self.secondarySection = secondarySection
        self.gridItems = gridItems
        self.pixelsAdvanced = pixelsAdvanced
    
    # shows and gives collision to elements in the grid       
    def loadGrid(self):
        display = pygame.display.get_surface()
        display_width = display.get_width()
        display_height = display.get_height()
        for objectData in self.gridItems :
            display.blit((pygame.transform.scale(objectData[0].image, (objectData[0].sizeOnGrid[0] * display_width/16, objectData[0].sizeOnGrid[1]  * display_height/9))), (objectData[1] * display_width/16 + (display_width - self.pixelsAdvanced), objectData[2] * display_height/16))
        self.pixelsAdvanced += (display_width/240)