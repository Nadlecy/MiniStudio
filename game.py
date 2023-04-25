# Example file showing a circle moving on screen
import pygame
import math
from player import Player,PlayerBullet
from enemies import Enemy, EnemyBullet
from menu import Menu, Button
import buttons
from powerUp import *
from map import GridObjects, MapSection


# Creating a gameState class for game info
class gameState ():
    def __init__(self, Map, currentScrollDirection = "Right"):
        self.Map = Map
        self.currentScrollDirection = currentScrollDirection

class TriggerFunction () :
    def __init__(self,TimeTrigger,function,param):
        self.function = function
        self.TimeTrigger = TimeTrigger
        self.clock = 0
        self.param = param

    def UpdateClock(self,Dt) :
        self.clock += Dt

    def TriggerCheck (self,Dt) :
        self.UpdateClock(Dt)
        if self.TimeTrigger < self.clock:
            self.function(self.param)
            self.clock = 0
    

def spawn_ennemi_1 (enemiesOnScreen):
    enemiesOnScreen.append(Enemy(screen).spawn())


# pygame setup
pygame.init()
#creating a screen
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
clock = pygame.time.Clock()

#menu init
menu = Menu()


#load button images
plus_btn_img = pygame.image.load('image/plus_btn.png')
minus_btn_img = pygame.image.load('image/minus_btn.png')
next_btn_img = pygame.image.load('image/next_btn.png')
last_btn_img = pygame.image.load('image/last_btn.png')

#create button instances
plus_btn = buttons.Button(90, 30, plus_btn_img, 2)
minus_btn = buttons.Button(30, 30, minus_btn_img, 2)
next_btn = buttons.Button(1200, 30, next_btn_img, 2)
last_btn = buttons.Button(1140, 30, last_btn_img, 2)

#Load Music
music_volume = 0.1
music_volume_display = 3
pygame.mixer.music.load("music/birds_attacks_intro.ogg")
pygame.mixer.music.play()

#creating the player character
skin = 1
thisPlayer=Player(currentSurface=screen, currentVisuals= "player_anim" + str(skin), position = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2))


#Text through GUI
volumeFont = pygame.font.SysFont("Times New Roman", 18, True)

#preparing the scrolling screen
bg = pygame.transform.scale(pygame.image.load("image/background2.png"),(screen.get_height() * 4, screen.get_height()))
bg_width = bg.get_width()
scroll = 0
tiles = math.ceil(screen.get_width() / bg_width) +1

#launching the game
running = True
menu_splash_ongoing = True
menu_ongoing = True
dt = 0

#preparing enemy storage list
enemiesOnScreen = []
fonction_spawn = TriggerFunction(2,spawn_ennemi_1,enemiesOnScreen)

#testing map and objects
box = GridObjects("image/testbox.png")
testmap1 = MapSection(None,gridItems=[[box, 1, 2]])
testmap2 = MapSection(testmap1,gridItems=[[box, 1, 2],[box, 4, 2]])
testmap1.nextSection = testmap2
currentSections = [testmap1]

while running:
    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-independent physics.
    dt = clock.tick(60) / 1000

    fonction_spawn.TriggerCheck(dt)

    if menu:
        if menu_splash_ongoing:
            menu.splash_screen(dt)
            if menu.splash_status == 1:
                menu_splash_ongoing = False
            elif menu.splash_status == 2:
                running = False
            continue
        if menu_ongoing:
            menu.menu_screen()
            if menu.home_status == 1:
                menu_ongoing = False
            elif menu.home_status == 2:
                running = False
            continue
        

    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_o:
                if thisPlayer.inventoryBoost["ASPBoost"]> 0:
                    thisPlayer.inventoryBoost["ASPBoost"] -= 1
                    thisPlayer.powerUps.append(ASPBoost(6,thisPlayer))
            elif event.key == pygame.K_p:
                if thisPlayer.inventoryBoost["Shield"]> 0:
                    thisPlayer.inventoryBoost["Shield"] -= 1
                    thisPlayer.powerUps.append(Shield(10,thisPlayer))
            elif event.key == pygame.K_i:
                if thisPlayer.inventoryBoost["Heal"]> 0:
                    thisPlayer.inventoryBoost["Heal"] -= 1
                    if thisPlayer.lives < 3:
                        thisPlayer.powerUps.append(Heal(thisPlayer,1))
                        print(thisPlayer.lives)
            elif event.key == pygame.K_1:
                enemiesOnScreen.append(Enemy(screen).spawn())
            elif event.key == pygame.K_2:
                enemiesOnScreen.append(Enemy(screen, "enemy_anim3", enemyType = 1).spawn())
            elif event.key == pygame.K_ESCAPE:
                menu.menu_pause()
            elif event.key == pygame.K_3:
                enemiesOnScreen.append(Enemy(screen, "enemy_anim2", enemyType = 2).spawn())

    # music
    pygame.mixer.music.set_volume(music_volume)
    if (pygame.mixer.music.get_busy() == False):
        pygame.mixer.music.load("music/birds_attacks.ogg")
        pygame.mixer.music.play(-1)

    # draw scrolling background
    for i in range(0, tiles):
        screen.blit(bg,(i*bg_width+ scroll,0))
    scroll -= screen.get_width()/240
    #scroll reset
    if abs(scroll) > bg_width:
        scroll = 0
    
    # enemies act
    for i in enemiesOnScreen:
        i.ai(thisPlayer,dt)


    # decreases the cooldown on the player's attack
    thisPlayer.currentShotCoolDown -=1

    if thisPlayer.shotsList:
        toDelete=[]
        for i in range(len(thisPlayer.shotsList)):
            keeping = thisPlayer.shotsList[i].move(dt)
            if not keeping:
                toDelete.append(i)
        if toDelete:
            for i in toDelete:
                del thisPlayer.shotsList[i]

    for i in range(len(enemiesOnScreen)):
        enemy = enemiesOnScreen[i]
        enemy.currentShotCoolDown -= 1
        if not enemy.shotsList: continue
        if enemy.enemyType == 2:
            for j in range(len(enemy.shotsList)-1, 0, -1):
                shot = enemy.shotsList[j]
                keeping = True
                if not shot.broken:
                    keeping = shot.move_bis(dt, thisPlayer, enemy)
                else:
                    keeping = shot.move_test(dt)
                if not keeping:
                    del enemy.shotsList[j]
        elif enemy.enemyType == 0:
            for j in range(len(enemy.shotsList)-1,0,-1):
                keeping = enemy.shotsList[j].move(dt)
                if not keeping:
                    del enemy.shotsList[j]

        
    #MOVEMENT
    keys = pygame.key.get_pressed()
    if (keys[pygame.K_z] or keys[pygame.K_UP]) and thisPlayer.position.y > screen.get_height()/9:
        thisPlayer.position.y -= 400 * dt
    if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and thisPlayer.position.y < screen.get_height() - (screen.get_height()/9)*2:
        thisPlayer.position.y += 400 * dt
    if (keys[pygame.K_q] or keys[pygame.K_LEFT]) and thisPlayer.position.x > 0:
        thisPlayer.position.x -= 400 * dt
    if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and thisPlayer.position.x < screen.get_width() - (screen.get_width()/16):
        thisPlayer.position.x += 400 * dt
    if keys[pygame.K_SPACE]:
        thisPlayer.shoot()
        
        
    #Collision    
    for i in range (len(enemiesOnScreen)):
            if thisPlayer.shotsList:
                for a in range (len(thisPlayer.shotsList)):
                    collision = PlayerBullet.isCollision(thisPlayer.shotsList[a],enemiesOnScreen[i].position,80)
                    if collision :
                        thisPlayer.shotsList[a].position.y = screen.get_height()+40
                        enemiesOnScreen[i].hp -= 1
    for i in range (len(enemiesOnScreen)):
            if enemiesOnScreen[i].shotsList:
                for a in range (len(enemiesOnScreen[i].shotsList)):
                    collision = EnemyBullet.isCollision(enemiesOnScreen[i].shotsList[a],thisPlayer.position,80)
                    elapsed = time.time() - thisPlayer.lastHitTime
                    if collision and elapsed >1.5 and thisPlayer.shield == False:
                        enemiesOnScreen[i].shotsList[a].position.y = screen.get_height()+40
                        thisPlayer.position.x -= screen.get_width()/400
                        thisPlayer.lastHitTime = time.time()
                        thisPlayer.lives -= 1
                        print(thisPlayer.lives)
                        break
                    elif collision and elapsed > 1.5 and thisPlayer.shield:
                        enemiesOnScreen[i].shotsList[a].position.y = screen.get_height()+40
                        thisPlayer.shield = False
                        thisPlayer.position.x -= screen.get_width()/400
                        thisPlayer.lastHitTime = time.time()
                        print("hp : ", thisPlayer.lives)
                        print(thisPlayer.shield)
                        break


    for i in range(len(enemiesOnScreen)):
        if thisPlayer:
            col = thisPlayer.Collision(enemiesOnScreen[i].position,80)
            elapsed = time.time() - thisPlayer.lastHitTime
            if enemiesOnScreen[i].enemyType == 0:
                if col and elapsed > 1.5 and thisPlayer.shield == False:
                    thisPlayer.lives -= 1
                    thisPlayer.position.x -= 50
                    thisPlayer.lastHitTime = time.time()
                    print("hp : ", thisPlayer.lives)
                    break
                elif col and elapsed > 1.5 and thisPlayer.shield == True:
                    thisPlayer.shield = False
                    thisPlayer.position.x -= 50
                    thisPlayer.lastHitTime = time.time()
                    print("hp : ", thisPlayer.lives)
                    break
            elif enemiesOnScreen[i].enemyType == 1:
                if col and elapsed > 1.5 and thisPlayer.shield == False:
                    enemiesOnScreen[i].hp -= 1
                    thisPlayer.lives -= 1
                    thisPlayer.position.x -= 50
                    thisPlayer.lastHitTime = time.time()
                    print("hp : ", thisPlayer.lives)
                    break
                elif col and elapsed > 1.5 and thisPlayer.shield == True:
                    enemiesOnScreen[i].hp -= 1
                    thisPlayer.shield = False
                    thisPlayer.position.x -= 50
                    thisPlayer.lastHitTime = time.time()
                    print("hp : ", thisPlayer.lives)
                    break

    if enemiesOnScreen:
        DelEnemies = []
        for i in range(len(enemiesOnScreen)-1,-1,-1):
            if (enemiesOnScreen[i].die()==True):
                DelEnemies.append(i)
                if DelEnemies:
                    del enemiesOnScreen[i]

    for i in range (len(thisPlayer.powerUps)-1,-1,-1):
        power = thisPlayer.powerUps[i]
        power.effect(dt)
        if power.isOver():
            del thisPlayer.powerUps[i]
            print(len(thisPlayer.powerUps))
                    
    #map management
    if currentSections[0].pixelsAdvanced >= screen.get_width() * 2 and len(currentSections) == 2:
        currentSections[0].pixelsAdvanced = 0
        del currentSections[0]
        print(currentSections)
    if currentSections[0].pixelsAdvanced >= screen.get_width() and len(currentSections) == 1:
        currentSections.append(currentSections[0].nextSection)
        print(currentSections)
    for i in currentSections:
        i.loadGrid()

    #BUTTONS

        #VOLUME

        #UP
    if plus_btn.draw(screen):
        if music_volume<0.9:
            music_volume = music_volume + 0.1
            music_volume_display += 1
        print(music_volume)
        #DOWN
    if minus_btn.draw(screen):
        if music_volume>0.1:
            music_volume = music_volume - 0.1
            music_volume_display -= 1
        print(music_volume)
    
    volumeLabel = volumeFont.render("Music = " + str(music_volume_display), False, (0,0,0))
    
    #SKINS
    if next_btn.draw(screen):
        if skin < 6:
            skin+=1
        else:
            skin=1
        thisPlayer=Player(currentSurface=screen, currentVisuals= "player_anim" + str(skin), position = pygame.Vector2(thisPlayer.position,thisPlayer.position))
    if last_btn.draw(screen):
        if skin > 1:
            skin-=1
        else:
            skin=6
        thisPlayer=Player(currentSurface=screen, currentVisuals= "player_anim" + str(skin), position = pygame.Vector2(thisPlayer.position,thisPlayer.position))

    #ANIMATION READER
    thisPlayer.playerAnimate()



    screen.blit(volumeLabel, (30, 70))
    pygame.display.update()
    # flip() the display to put your work on screen
    pygame.display.flip()

    

pygame.quit()