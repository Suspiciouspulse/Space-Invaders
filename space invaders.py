import pygame
from pygame import mixer
import random
import math

pygame.init()
screen=pygame.display.set_mode((800,600))

#adding background image
background=pygame.image.load('./assets/background.jpg')

#adding background image
mixer.music.load('./effects/background.wav')
mixer.music.play(-1)

#adding image and title to the title of the application
pygame.display.set_caption("Space Invaders")
icon=pygame.image.load('./assets/ufo.png')
pygame.display.set_icon(icon)

#loading bullet's png and setting the bullet's starting position
bulletImg=pygame.image.load('./assets/bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 3
bullet_state= "ready"

#player
playerImg=pygame.image.load('./assets/spaceship.png')
playerX = 370
playerY = 480
playerX_change = 0


#enemy
enemyImg=[]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]
enemynum=1


#initial score
score = 0
font = pygame.font.Font('freesansbold.ttf',32)
textX=10
textY=10

over_font = pygame.font.Font('freesansbold.ttf',64)

def show_score(x,y):
    scoreString=font.render("Score :" + str(score),True,(255,255,255))
    screen.blit(scoreString,(x,y))

def game_over(x,y):
    over_text=over_font.render("GAME OVER",True,(255,255,255))
    screen.blit(over_text,(200,250))

def player(x,y):
    screen.blit(playerImg,(x,y))

def enemy(x,y, i):
    screen.blit(enemyImg[i],(x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg,(x+16,y+10))

def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2))+(math.pow(enemyY-bulletY,2)))
    if distance < 27:
        return True
    else:
        return False

clock = pygame.time.Clock()

running=True
while running:
    screen.fill((0,0,0))
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -2
            if event.key == pygame.K_RIGHT:
                playerX_change = 2
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound=mixer.Sound('./effects/shooting.wav')
                    bullet_sound.play()
                    bulletX=playerX
                    fire_bullet(bulletX,bulletY)

        if event.type == pygame.KEYUP:
            playerX_change = 0
        

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    

    for i in range(enemynum):
        enemyImg.append(pygame.image.load('./assets/alien.png'))
        enemyX.append(random.randint(0,735))
        enemyY.append(random.randint(50,150))
        enemyX_change.append(0.7) 
        enemyY_change.append(40)

        if enemyY[i] > 440:
            for j in range(enemynum):
                enemyY[j] = 2000
            game_over(200,250)
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] =0.7 + score * 0.1
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] =-0.7 - score * 0.1
            enemyY[i] += enemyY_change[i]

        collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)

        if collision:
            explosion_sound=mixer.Sound('./effects/Explode.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score += 1
            enemyX[i]=random.randint(0,735)
            enemyY[i]=random.randint(50,150)
            if score%4==0:
                enemynum+=1

        enemy(enemyX[i],enemyY[i], i)

    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    
    if bullet_state == "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change

    player(playerX,playerY)
    show_score(textX,textY)
    pygame.display.update()
    clock.tick(60)
