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
    def __init__(self, bayNumber, nextSection, secondarySection = None, gridItems = [], pixelsAdvanced = 0):
        self.bayNumber = bayNumber
        self.nextSection = nextSection
        self.secondarySection = secondarySection
        self.gridItems = gridItems
        self.pixelsAdvanced = pixelsAdvanced
    
    # shows elements in the grid 
    def loadGrid(self):
        display = pygame.display.get_surface()
        display_width = display.get_width()
        display_height = display.get_height()
        for objectData in self.gridItems :
            display.blit((pygame.transform.scale(objectData[0].image, (objectData[0].sizeOnGrid[0] * display_width/16, objectData[0].sizeOnGrid[1]  * display_height/9))), (objectData[1] * display_width/16 + (display_width - self.pixelsAdvanced), objectData[2] * display_height/9))
        self.pixelsAdvanced += (display_width/240)

class Map():
    def __init__(self, currentSections = [], backgrounds = []):
        self.currentSections = currentSections
        self.backgrounds = backgrounds
    
    def mapProceed(self, player):
        if self.currentSections[0].pixelsAdvanced >= pygame.display.get_surface().get_width() * 2 and len(self.currentSections) == 2:
            self.currentSections[0].pixelsAdvanced = 0
            del self.currentSections[0]
            print(self.currentSections[0].bayNumber)
        if self.currentSections[0].pixelsAdvanced >= pygame.display.get_surface().get_width() and len(self.currentSections) == 1:
            if self.currentSections[0].secondarySection != None and (player.position.y < (pygame.display.get_surface().get_height() / 2)):
                self.currentSections.append(self.currentSections[0].secondarySection)
                print("up'd")
            else:
                self.currentSections.append(self.currentSections[0].nextSection)
                print("forwards")
        for i in self.currentSections:
            i.loadGrid()