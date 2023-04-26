import pygame
import math
from player import Player,PlayerBullet
from enemies import Enemy, EnemyBullet
from ui import Menu, ATH
import buttons
from powerUp import *
from map import loadLevel1
from boostObject import *


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
    enemiesOnScreen.append(Enemy(screen,3).spawn())
def spawn_ennemi_2 (enemiesOnScreen):
    enemiesOnScreen.append(Enemy(screen,1, "enemy_anim3", enemyType = 1).spawn())
def spawn_ennemi_3 (enemiesOnScreen):
    enemiesOnScreen.append(Enemy(screen,5, "enemy_anim2", enemyType = 2).spawn())
def spawn_ennemi_4 (enemiesOnScreen):
    enemiesOnScreen.append(Enemy(screen,2, "enemy_anim4", enemyType = 3).spawn())

# pygame setup
pygame.init()

#creating a screen
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
clock = pygame.time.Clock()

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
music_volume = 0.5
music_volume_display = 5
pygame.mixer.music.load("music/ugly_travel.ogg")
pygame.mixer.music.play(-1)
music_order_check = 0

#creating the player character
skin = 1
thisPlayer=Player(currentSurface=screen, currentVisuals= "player_anim" + str(skin), position = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2))

# creating the first level
level1 = loadLevel1()
#menus init
menu = Menu()
ath = ATH(thisPlayer)
#Text through GUI
volumeFont = pygame.font.SysFont("Times New Roman", 18, True)

#launching the game
running = True
menu_splash_ongoing = True
menu_ongoing = True
dt = 0

#preparing enemy storage list
enemiesOnScreen = []
spawn_penguin = TriggerFunction(10,spawn_ennemi_1,enemiesOnScreen)
spawn_hirondelle =TriggerFunction(7,spawn_ennemi_2,enemiesOnScreen)
spawn_poule = TriggerFunction(15,spawn_ennemi_3,enemiesOnScreen)
spawn_pigeon = TriggerFunction(8,spawn_ennemi_4,enemiesOnScreen)

Shield_boost = boosObject(pygame.Vector2(screen.get_width()/2,screen.get_height()/2),screen,Visual="boost_coin_shield",name="Shield")

        
while running:
    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-independent physics.
    dt = clock.tick(60) / 1000  
    #spawn_penguin.TriggerCheck(dt)
    #spawn_hirondelle.TriggerCheck(dt)
    #spawn_poule.TriggerCheck(dt)
    #spawn_pigeon.TriggerCheck(dt)
    #MENU
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
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            
            #Pause menu
            if event.key == pygame.K_ESCAPE:
                print("caca")
                menu.menu_pause()

            #boosts
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

                

            #spawn enemies
            elif event.key == pygame.K_1:
                enemiesOnScreen.append(Enemy(screen,3).spawn())
            elif event.key == pygame.K_2:
                enemiesOnScreen.append(Enemy(screen,1, "enemy_anim3", enemyType = 1).spawn())
            elif event.key == pygame.K_3:
                enemiesOnScreen.append(Enemy(screen,5, "enemy_anim2", enemyType = 2).spawn())
            elif event.key == pygame.K_4:
                enemiesOnScreen.append(Enemy(screen,2, "enemy_anim4", enemyType = 3).spawn())
            elif event.key == pygame.K_5:
                enemiesOnScreen.append(Enemy(screen,2, "boss_idle", enemyType = 4, animationType = "boss_idle").spawn())
                if music_order_check != 2:
                    music_order_check = 2
    #enemy autospawn
    spawn_penguin.TriggerCheck(dt)
    spawn_hirondelle.TriggerCheck(dt)
    spawn_poule.TriggerCheck(dt)
    spawn_pigeon.TriggerCheck(dt)
    
    #Boosts labels
    ASPBoostLabel = volumeFont.render("ASPBoost = " + str(thisPlayer.shotSpeed), False, (255,255,255))

    #map management
    level1.mapProceed(thisPlayer)

    # music
    if music_order_check == 0:
        pygame.mixer.music.load("music/birds_attacks_intro.ogg")
        pygame.mixer.music.play()
        music_order_check = 1

    pygame.mixer.music.set_volume(music_volume)
    if (pygame.mixer.music.get_busy() == False) and music_order_check == 1:
        pygame.mixer.music.load("music/birds_attacks.ogg")
        pygame.mixer.music.play(-1)

    if music_order_check == 2:
        pygame.mixer.music.load("music/No_Boss_Music.ogg")
        pygame.mixer.music.play(-1)
        music_order_check = 3


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

        #Penguin
        if enemy.enemyType == 0:
            for j in range(len(enemy.shotsList)-1,0,-1):
                keeping = enemy.shotsList[j].move_type1(dt)
                if not keeping:
                    del enemy.shotsList[j]

        #Chicken
        elif enemy.enemyType == 2:
            for j in range(len(enemy.shotsList)-1, 0, -1):
                shot = enemy.shotsList[j]
                keeping = True
                if not shot.broken:
                    keeping = shot.move_type2_state1(dt, thisPlayer, enemy)
                else:
                    keeping = shot.move_type2_state2(dt)
                if not keeping:
                    del enemy.shotsList[j]

        #Pigeon
        elif enemy.enemyType == 3:
            for j in range(len(enemy.shotsList)-1,0,-1):
                keeping = enemy.shotsList[j].move_type1(dt)
                if not keeping:
                    del enemy.shotsList[j]

        #Boss
        elif enemy.enemyType == 3:
            for j in range(len(enemy.shotsList)-1,0,-1):
                keeping = enemy.shotsList[j].move_type1(dt)
                if not keeping:
                    del enemy.shotsList[j]

    #MOVEMENT
    keys = pygame.key.get_pressed()
    if (keys[pygame.K_z] or keys[pygame.K_UP]) and thisPlayer.position.y > screen.get_height()/9:
        thisPlayer.position.y -= thisPlayer.speed * dt
    if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and thisPlayer.position.y < screen.get_height() - (screen.get_height()/9)*2:
        thisPlayer.position.y += thisPlayer.speed * dt
    if (keys[pygame.K_q] or keys[pygame.K_LEFT]) and thisPlayer.position.x > 0:
        thisPlayer.position.x -= thisPlayer.speed * dt
    if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and thisPlayer.position.x < screen.get_width() - (screen.get_width()/16):
        thisPlayer.position.x += thisPlayer.speed * dt
    if keys[pygame.K_SPACE]:
        thisPlayer.shoot()
        
    #Collision    
    for i in range (len(enemiesOnScreen)):
            enemy = enemiesOnScreen[i]
            if thisPlayer.shotsList:
                for a in range (len(thisPlayer.shotsList)):  
                    if enemy.enemyType == 4:
                        collision = PlayerBullet.isCollision(thisPlayer.shotsList[a],enemy.position,screen.get_width()/3,screen.get_width()/16)
                    else:
                        collision = PlayerBullet.isCollision(thisPlayer.shotsList[a],enemy.position,screen.get_width()/16,screen.get_width()/16)
                    
                    if collision :
                        thisPlayer.shotsList[a].position.y = screen.get_height()+40
                        enemy.hp -= 1
                        print(enemy.hp)    

    for i in range (len(enemiesOnScreen)):
            enemy = enemiesOnScreen[i]
            if enemy.shotsList:
                for a in range (len(enemy.shotsList)):
                    if enemy.enemyType == 4:
                        collision = EnemyBullet.isCollision(enemy.shotsList[a],thisPlayer.position,screen.get_width()/3,screen.get_width()/16)
                    else:
                        collision = EnemyBullet.isCollision(enemy.shotsList[a],thisPlayer.position,screen.get_width()/16,screen.get_width()/16)
                    elapsed = time.time() - thisPlayer.lastHitTime
                    if collision and elapsed >1 and thisPlayer.shield == False:
                        enemiesOnScreen[i].shotsList[a].position.y = screen.get_height()+40
                        thisPlayer.position.x -= screen.get_width()/400
                        thisPlayer.lastHitTime = time.time()
                        thisPlayer.lives -= 1
                        print(thisPlayer.lives)
                        break
                    elif collision and elapsed > 1 and thisPlayer.shield:
                        enemiesOnScreen[i].shotsList[a].position.y = screen.get_height()+40
                        thisPlayer.shield = False
                        thisPlayer.position.x -= screen.get_width()/400
                        thisPlayer.lastHitTime = time.time()
                        print("hp : ", thisPlayer.lives)
                        print(thisPlayer.shield)
                        break

    for i in range(len(enemiesOnScreen)):
        enemy = enemiesOnScreen[i]
        if thisPlayer:
            if enemy.enemyType == 4:
                col = thisPlayer.Collision(enemy.position,screen.get_width()/3,screen.get_width()/16)
            else:
                col = thisPlayer.Collision(enemy.position,screen.get_width()/16,screen.get_width()/16)
            elapsed = time.time() - thisPlayer.lastHitTime
            if enemiesOnScreen[i].enemyType == 1:
                if col and elapsed > 1 and thisPlayer.shield == False:
                    enemiesOnScreen[i].hp -= 1
                    thisPlayer.lives -= 1
                    thisPlayer.position.x -= 50
                    thisPlayer.lastHitTime = time.time()
                    print(enemiesOnScreen[i])
                    break
                elif col and elapsed > 1 and thisPlayer.shield == True:
                    enemiesOnScreen[i].hp -= 1
                    thisPlayer.shield = False 
                    thisPlayer.position.x -= 50
                    thisPlayer.lastHitTime = time.time()
                    print("hp : ", thisPlayer.lives)
                    break
            else:
                if col and elapsed > 1 and thisPlayer.shield == False:
                    thisPlayer.lives -= 1
                    thisPlayer.position.x -= 50
                    thisPlayer.lastHitTime = time.time()
                    print("hp : ", thisPlayer.lives)
                    break
                elif col and elapsed > 1 and thisPlayer.shield == True:
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
    if thisPlayer.die():
        pygame.quit()
        menu.gameOver()
        

        

    #BUTTONS
    '''
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
    '''
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
    ath.displayLighting()
    ath.displayLifebar()
    ath.displayGadgetbar()
    ath.displayScore()

#    screen.blit(volumeLabel, (30, 70))
    pygame.display.update()
    # flip() the display to put your work on screen
    pygame.display.flip()

pygame.quit()