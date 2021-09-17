import pygame
from pygame import mixer
import random
import math

#init game
pygame.init
pygame.font.init()
pygame.mixer.init()
 

#create screen
screen = pygame.display.set_mode((800,600))


#Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

#Backround
background = pygame.image.load('space.jpg')

#Backround music
mixer.music.load('music.mp3')
mixer.music.play(-1)

#Score
scoreValue = 0
font = pygame.font.Font(None,32)
textX = 10
textY = 10
def showScore(x,y):
    score = font.render("Score : "+str(scoreValue),True,(255,255,255))
    screen.blit(score,(x,y))

#Highscore
try:
    hiscoreFile = open('hiscore.txt',"r")
    hiscore = int(hiscoreFile.read())
    hiscoreFile.close
except FileNotFoundError:
    hiscore = 0
hiscoreX = 10
hiscoreY = 40
def showHiscore(x,y):
    hiscoreText = font.render("Hiscore : "+str(hiscore),True,(255,255,255))
    screen.blit(hiscoreText,(x,y))

#Gameover text
gameoverFont = pygame.font.Font(None,50)
def gameover():
    gameover = gameoverFont.render("GAME OVER. PRESS R TO TRY AGAIN",True,(255,255,255))
    screen.blit(gameover,(85,250))
    global hiscore
    if scoreValue > hiscore:
        hiscoreFile = open("hiscore.txt","w")
        hiscoreFile.write(str(scoreValue))
        hiscoreFile.close
        hiscore = scoreValue

#Movement speeds
playerSpeed = 1.5
enemySpeed = .75
bulletSpeed = 3

#Player
playerImg = pygame.image.load('spaceship.png')
playerX = 370
playerY = 480
playerXOffset = 0
def player(x,y):
    screen.blit(playerImg,(x,y))

#Enemys
enemyImg = pygame.image.load('enemy.png')
enemyX = []
enemyY = []
enemyXOffset = []
enemyYOffset = []
numOfEnemies = 6

for i in range(numOfEnemies):
    enemyX.append(random.randint(0,736))
    enemyY.append(random.randint(0,200))
    enemyXOffset.append(enemySpeed)
    enemyYOffset.append(0)

def enemy(x,y):
    screen.blit(enemyImg,(x,y))

#Bullet

bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletXOffset = 0
bulletYOffset = bulletSpeed
#Ready can fire else wait
bulletIsReady = True
def fireBullet(x,y):
    global bulletIsReady
    bulletIsReady = False
    screen.blit(bulletImg,(x+16,y+10))

def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt( math.pow(enemyX-bulletX,2) + math.pow(enemyY-bulletY,2))#Distance between enemy and bullet
    if distance < 37:#Check if enemy has been hit
        return True
    else:
        return False

#Game loop
running = True
while running:

    ##########
    # EVENTS #
    ##########

    #Looping thru all event in window
    for event in pygame.event.get():
        #Check to see if exit event has occured
        if event.type == pygame.QUIT:
            running = False

        #Check for directional keystroke
        #Check for pressing of key
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                #print("LEFT KEY PRESSED")
                playerXOffset-=playerSpeed
            if event.key == pygame.K_RIGHT:
                #print("RIGHT KEY PRESSED")
                playerXOffset+=playerSpeed
            if event.key == pygame.K_SPACE:
                #Can only fire bullet if bullet is ready
                if bulletIsReady:
                    #Get position of ship when space was pressed
                    bulletSound = mixer.Sound('laser.wav')
                    bulletSound.play()
                    bulletX = playerX
                    fireBullet(bulletX,bulletY)
            if event.key == pygame.K_r:
                for i in range(numOfEnemies):
                    enemyX[i]=(random.randint(0,736))
                    enemyY[i]=(random.randint(0,200))
                    scoreValue = 0

        #Check if releasing key
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                #print("KEY RELEASED")
                playerXOffset = 0
                 
    #################
    # END OF EVENTS #
    #################

    #Backround color in RGB
    screen.fill((0,0,0))
    #Load backround image
    screen.blit(background,(0,0))

    #Movement
    playerX += playerXOffset
    

    #Check if player has passed boundries
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    #Enemy movements
    for i in range(numOfEnemies):
        #Losing condition
        if enemyY[i] >= 410:
            #update hi-score
            for j in range(numOfEnemies):
                #Move enemy out of screen
                enemyY[j] = 2000
            gameover()
            break   

        enemyX[i] += enemyXOffset[i]
        if enemyX[i] <= 0:
            enemyXOffset[i] = enemySpeed
            enemyY[i] += 40
        elif enemyX[i] >= 736:
            enemyXOffset[i] = -enemySpeed
            enemyY[i] += 40
        #Collision
        hasCollided = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if hasCollided:
            explosionSound = mixer.Sound('explosion.wav')
            explosionSound.play()
            bulletY = 480
            bulletIsReady = True
            scoreValue +=1
            enemyX[i] = random.randint(0,736)
            enemyY[i] = random.randint(0,200)
        enemy(enemyX[i],enemyY[i])
    #Check if bullet has left screen
    if bulletY <= 0:
        bulletY = 480
        bulletIsReady = True

    #Draw player on screen
    player(playerX,playerY)
    
    #Check if bullet has been fired
    if not bulletIsReady:
        fireBullet(bulletX,bulletY)
        bulletY -= bulletYOffset
    showScore(textX,textY)
    showHiscore(hiscoreX,hiscoreY)
    pygame.display.update()
