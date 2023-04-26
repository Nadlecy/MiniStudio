import pygame
from spritesheet import load_backgrounds

#one grid is 7x16
#each grid contains a list of all the objects it will load, along with their positions: [Gridobject, positionX, positionY]
#each grid knows which grid comes next
#some grids have a secondary grid, that's where the player may split paths
class MapSection():
    def __init__(self, bayNumber, background, nextSection, secondarySection = None, pixelsAdvanced = 0):
        #self.background = pygame.image.load()
        self.bayNumber = bayNumber
        self.background = background
        self.nextSection = nextSection
        self.secondarySection = secondarySection
        self.pixelsAdvanced = pixelsAdvanced
        self.behindBackground = pygame.transform.scale(pygame.image.load("image/bg_space_in_game.png"),(pygame.display.get_surface().get_height()*2,pygame.display.get_surface().get_height()))
    
    # shows elements in the grid 
    def loadGrid(self, background):
        display = pygame.display.get_surface()
        display_height = display.get_height()
        display.blit(background,(display_height*2 - self.pixelsAdvanced,0))
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
        pygame.display.get_surface().blit(self.currentSections[0].behindBackground, (0,0))
        for i in self.currentSections:
            i.loadGrid(i.background)

def loadLevel1():
    # Generating Backgrounds for the levels
    backgrounds = []
    for i in range(4):
        if i == 0:
            backgrounds.append(load_backgrounds("corridors_boss","corridors"))
        else:
            backgrounds.append(load_backgrounds("corridors_" + str(i),"corridors"))
    backgrounds.append(load_backgrounds("choice","choice"))
    
    height= pygame.display.get_surface().get_height()

    #setting the rooms
    #boss bay, this one loops on itself indefinitely
    bossCircle6= MapSection(0, pygame.transform.scale(backgrounds[0][5],(height * 2, height)) , None)
    bossCircle5= MapSection(0, pygame.transform.scale(backgrounds[0][7],(height * 2, height)) , bossCircle6)
    bossCircle4= MapSection(0, pygame.transform.scale(backgrounds[0][6],(height * 2, height)) , bossCircle5)
    bossCircle3= MapSection(0, pygame.transform.scale(backgrounds[0][1],(height * 2, height)) , bossCircle4)
    bossCircle2= MapSection(0, pygame.transform.scale(backgrounds[0][0],(height * 2, height)) , bossCircle3)
    bossCircle1= MapSection(0, pygame.transform.scale(backgrounds[0][2],(height * 2, height)) , bossCircle2)
    bossCircle6.nextSection = bossCircle1

    #fourth bay

    #third bay

    #second bay
    secondCircle2= MapSection(2, pygame.transform.scale(backgrounds[2][0],(height * 2, height)) , None)
    secondCircle1= MapSection(2, pygame.transform.scale(backgrounds[2][2],(height * 2, height)), secondCircle2)

    #first bay
    firstCircle4 = MapSection(1, pygame.transform.scale(backgrounds[1][7],(height * 2, height)), None)
    firstCircle3 = MapSection(1, pygame.transform.scale(backgrounds[0][7],(height * 2, height)), firstCircle4)
    firstCircle2 = MapSection(1, pygame.transform.scale(backgrounds[1][3],(height * 2, height)), None)
    firstCircle1 = MapSection(1, pygame.transform.scale(backgrounds[1][4],(height * 2, height)), firstCircle2)
    
    #intersections/path choices
    intersection21 = MapSection(1, pygame.transform.scale(backgrounds[4][0],(height * 2, height)), firstCircle3, secondarySection= secondCircle1)
    intersectionB = MapSection(1, pygame.transform.scale(backgrounds[4][3],(height * 2, height)), firstCircle1, secondarySection= bossCircle1)
    
    #finishing loops
    firstCircle2.nextSection = intersection21
    firstCircle4.nextSection = intersectionB
    secondCircle2.nextSection = intersection21
    
    return Map([firstCircle1])
