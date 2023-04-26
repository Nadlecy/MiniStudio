# Example file showing a circle moving on screen
import pygame
import math
from player import Player,PlayerBullet
from enemies import Enemy, EnemyBullet
from ui import Menu, ATH
import buttons
from powerUp import *
from map import loadLevel1

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
music_volume = 3
music_volume_display = 3
pygame.mixer.music.load("music/birds_attacks_intro.ogg")
pygame.mixer.music.play()


#creating the player character
skin = 1
thisPlayer=Player(currentSurface=screen, currentVisuals= "player_anim" + str(skin), position = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2))

# creating the first level
level1 = loadLevel1(screen)
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

        
while running:
    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-independent physics.
    dt = clock.tick(60) / 1000

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

    #ATH
    ath.displayLifebar()
    
        
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
    

    #Boosts labels
    ASPBoostLabel = volumeFont.render("ASPBoost = " + str(thisPlayer.shotSpeed), False, (255,255,255))


    #map management
    level1.mapProceed(thisPlayer)

    # music
    pygame.mixer.music.set_volume(music_volume)
    if (pygame.mixer.music.get_busy() == False):
        pygame.mixer.music.load("music/birds_attacks.ogg")
        pygame.mixer.music.play(-1)

    
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
        elif enemy.enemyType == 3:
            for j in range(len(enemy.shotsList)-1,0,-1):
                keeping = enemy.shotsList[j].move(dt)
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
                        collision = EnemyBullet.isCollision(enemy.shotsList[a],thisPlayer.position,screen.get_width()/1.5,screen.get_width()/16)
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
            if enemiesOnScreen[i].enemyType == 0 or 2 or 3 or 4:
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
            elif enemiesOnScreen[i].enemyType == 1:
                if col and elapsed > 1 and thisPlayer.shield == False:
                    enemiesOnScreen[i].hp -= 1
                    thisPlayer.lives -= 1
                    thisPlayer.position.x -= 50
                    thisPlayer.lastHitTime = time.time()
                    print("hp : ", thisPlayer.lives)
                    break
                elif col and elapsed > 1 and thisPlayer.shield == True:
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
    ath.displayLifebar()

    screen.blit(volumeLabel, (30, 70))
    screen.blit(ASPBoostLabel, (30, 1000))
    pygame.display.update()
    # flip() the display to put your work on screen
    pygame.display.flip()

    

pygame.quit()