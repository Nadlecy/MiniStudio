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
            else:
                self.currentSections.append(self.currentSections[0].nextSection)

        pygame.display.get_surface().blit(self.currentSections[0].behindBackground, (0,0))
        for i in self.currentSections:
            i.loadGrid(i.background)

def loadLevel1():
    # Generating Backgrounds for the levels
    backgrounds = []
    for i in range(5):
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
    fourthCircle2= MapSection(3, pygame.transform.scale(backgrounds[4][6],(height * 2, height)), None) # connect to intersection41
    fourthCircle1= MapSection(3, pygame.transform.scale(backgrounds[4][5],(height * 2, height)), fourthCircle2)

    #third bay
    thirdCircle3= MapSection(3, pygame.transform.scale(backgrounds[3][1],(height * 2, height)), None) # connect to intersection32
    thirdCircle2= MapSection(3, pygame.transform.scale(backgrounds[3][0],(height * 2, height)), thirdCircle3)
    thirdCircle1= MapSection(3, pygame.transform.scale(backgrounds[3][2],(height * 2, height)), thirdCircle2)

    #second bay
    secondCircle5= MapSection(2, pygame.transform.scale(backgrounds[2][5],(height * 2, height)) , None) # connect to intersection21
    secondCircle4= MapSection(2, pygame.transform.scale(backgrounds[2][6],(height * 2, height)) , secondCircle5)
    secondCircle3= MapSection(2, pygame.transform.scale(backgrounds[2][4],(height * 2, height)) , None) # connect to intersection32
    secondCircle2= MapSection(2, pygame.transform.scale(backgrounds[2][7],(height * 2, height)) , secondCircle3)
    secondCircle1= MapSection(2, pygame.transform.scale(backgrounds[2][3],(height * 2, height)), secondCircle2)

    #first bay
    firstCircle6 = MapSection(1, pygame.transform.scale(backgrounds[1][7],(height * 2, height)), None) #connect to intersection41
    firstCircle5 = MapSection(1, pygame.transform.scale(backgrounds[1][7],(height * 2, height)), firstCircle6) 
    firstCircle4 = MapSection(1, pygame.transform.scale(backgrounds[1][7],(height * 2, height)), None) #connect to intersectionB
    firstCircle3 = MapSection(1, pygame.transform.scale(backgrounds[0][7],(height * 2, height)), firstCircle4)
    firstCircle2 = MapSection(1, pygame.transform.scale(backgrounds[1][3],(height * 2, height)), None) #connect to intersection21
    firstCircle1 = MapSection(1, pygame.transform.scale(backgrounds[1][4],(height * 2, height)), firstCircle2)

    #starting room
    startRoom= MapSection(1, pygame.transform.scale(backgrounds[1][3],(height * 2, height)), firstCircle1, pixelsAdvanced= pygame.display.get_surface().get_height()*2)
    
    #intersections/path choices
    intersection21 = MapSection(1, pygame.transform.scale(backgrounds[5][0],(height * 2, height)), firstCircle3, secondarySection= secondCircle1)
    firstCircle2.nextSection = intersection21
    secondCircle5.nextSection = intersection21

    intersection32 = MapSection(2, pygame.transform.scale(backgrounds[5][1],(height * 2, height)), secondCircle4, secondarySection= thirdCircle1)
    secondCircle3.nextSection = intersection32
    thirdCircle3.nextSection = intersection32

    intersection41 = MapSection(2, pygame.transform.scale(backgrounds[5][2],(height * 2, height)), firstCircle1, secondarySection= fourthCircle1)
    firstCircle6.nextSection = intersection41
    fourthCircle2.nextSection = intersection41

    intersectionB = MapSection(1, pygame.transform.scale(backgrounds[5][3],(height * 2, height)), firstCircle5, secondarySection= bossCircle1)
    firstCircle4.nextSection = intersectionB
    
    return Map([startRoom])
