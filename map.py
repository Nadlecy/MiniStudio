import pygame
from spritesheet import load_backgrounds
    
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
    def __init__(self, bayNumber, background, nextSection, secondarySection = None, gridItems = [], pixelsAdvanced = 0):
        #self.background = pygame.image.load()
        self.bayNumber = bayNumber
        self.background = background
        self.nextSection = nextSection
        self.secondarySection = secondarySection
        self.gridItems = gridItems
        self.pixelsAdvanced = pixelsAdvanced
        self.behindBackground = pygame.transform.scale(pygame.image.load("image/bg_space_in_game.png"),(pygame.display.get_surface().get_height()*2,pygame.display.get_surface().get_height()))
    
    # shows elements in the grid 
    def loadGrid(self, background):
        display = pygame.display.get_surface()
        display_width = display.get_width()
        display_height = display.get_height()
        display.blit(self.behindBackground, (0,0))
        display.blit(background,(display_height*2 - self.pixelsAdvanced,0))
        for objectData in self.gridItems :
            display.blit((pygame.transform.scale(objectData[0].image, (objectData[0].sizeOnGrid[0] * display_width/16, objectData[0].sizeOnGrid[1]  * display_height/9))), (objectData[1] * display_width/16 + (display_height*2 - self.pixelsAdvanced), objectData[2] * display_height/9))
        self.pixelsAdvanced += (display_height*2/240)

class Map():
    def __init__(self, currentSections = []):
        self.currentSections = currentSections

    def mapProceed(self, player):
        if self.currentSections[0].pixelsAdvanced >= pygame.display.get_surface().get_height()*4 and len(self.currentSections) == 2:
            self.currentSections[0].pixelsAdvanced = 0
            del self.currentSections[0]
            print(self.currentSections[0].bayNumber)
        if self.currentSections[0].pixelsAdvanced >= pygame.display.get_surface().get_height()*2 and len(self.currentSections) == 1:
            if self.currentSections[0].secondarySection != None and (player.position.y < (pygame.display.get_surface().get_height() / 2 + pygame.display.get_surface().get_height()/18)):
                self.currentSections.append(self.currentSections[0].secondarySection)
                print("up'd")
            else:
                self.currentSections.append(self.currentSections[0].nextSection)
                print("forwards")
        for i in self.currentSections:
            i.loadGrid(i.background)

def loadLevel1(screen):
    # Generating Backgrounds for the levels
    backgrounds = []
    for i in range(4):
        if i == 0:
            backgrounds.append(load_backgrounds("corridors_boss","corridors"))
        else:
            backgrounds.append(load_backgrounds("corridors_" + str(i),"corridors"))
    
    height= pygame.display.get_surface().get_height()
    box = GridObjects("image/testbox.png")
    bay1 = GridObjects("image/bay1.png", [4, 1])
    bay2 = GridObjects("image/bay2.png", [4, 1])
    secondcircle2= MapSection(2, pygame.transform.scale(backgrounds[2][4],(height * 2, height)) , None, gridItems=[[box, 2, 1],[box, 3, 1],[box, 4, 1]])
    secondcircle1= MapSection(2, pygame.transform.scale(backgrounds[2][5],(height * 2, height)), secondcircle2, gridItems=[[box, 6, 1]])
    testmap1 = MapSection(1, pygame.transform.scale(backgrounds[1][4],(height * 2, height)), None, gridItems=[[box, 1, 2]])
    intersection1 = MapSection(1, pygame.transform.scale(backgrounds[1][3],(height * 2, height)), testmap1, secondarySection= secondcircle1, gridItems=[[box, 2, 2],[bay1, 2, 6],[bay2, 2, 2]])
    testmap2 = MapSection(1, pygame.transform.scale(backgrounds[1][4],(height * 2, height)), intersection1, gridItems=[[box, 1, 2],[box, 4, 2]])
    testmap1.nextSection = testmap2
    secondcircle2.nextSection = intersection1
    return Map([testmap1])
