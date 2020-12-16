import pygame
import random
import math

# pygame init
pygame.init()

# display setup
screen = pygame.display.set_mode((800, 600))

# window caption and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('./Images/Space-Invader-Icon.png')
pygame.display.set_icon(icon)

# background image
background = pygame.image.load('./Images/Space-Invader-Background.png')

# player
playerImg = pygame.image.load('./Images/Space-Invader-Player-Sprite.png')
playerX = 370
playerY = 480
playerX_Change = 0

# enemy

enemyImg = []
enemyX = []
enemyY = []
enemyX_Change = []
enemyY_Change = []
num_enemies = 6
for i in range(num_enemies):
    enemyImg.append(pygame.image.load('./Images/Space-Invader-Enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_Change.append(1)
    enemyY_Change.append(40)

# bullets/lasers
laserImg = pygame.image.load('./Images/Lasers.png')
laserX = 0
laserY = 480
laserX_Change = 0
laserY_Change = 10
laser_state = "ready"

score = 0

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_laser(x, y):
    global laser_state
    laser_state = "fire"
    screen.blit(laserImg, (x+16, y))

def isCollision(enemyX, enemyY,  laserX, laserY):
    distance = math.sqrt((math.pow(enemyX - laserX,2) + math.pow(enemyY - laserY,2)))
    if distance < 27:
        return True
    else:
        return False

# game loop
running = True
while running:
    # background
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    # event listener
    for event in pygame.event.get():
        # quit
        if event.type == pygame.QUIT:
            running = False
        # key pressed
        if event.type == pygame.KEYDOWN:
            # left
            if event.key == pygame.K_LEFT:
                playerX_Change = -3
            # right
            if event.key == pygame.K_RIGHT:
                playerX_Change = 3
            # space
            if event.key == pygame.K_SPACE and laser_state == "ready":
                laserX = playerX
                fire_laser(laserX, laserY)
        # key released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_Change = 0

    # player movement
    playerX += playerX_Change

    #limit movement off screen
    if playerX < 0:
        playerX = 0
    elif playerX > 736:
        playerX = 736

    # enemy movement
    for i in range(num_enemies):
        enemyX[i] += enemyX_Change[i]

        # limit movement off screen
        if enemyX[i] < 0:
            enemyX_Change[i] = 1
            enemyY[i] += enemyY_Change[i]
        elif enemyX[i] > 736:
            enemyX_Change[i] = -1
            enemyY[i] += enemyY_Change[i]

        # collision
        collision = isCollision(enemyX[i], enemyY[i], laserX, laserY)
        if collision:
            laserY = 480
            laser_state = "ready"
            score += 1
            print(score)
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)


    # laser movement
    if laserY <= 0:
        laserY = 480
        laser_state = "ready"

    if laser_state is "fire":
        fire_laser(laserX, laserY)
        laserY -= laserY_Change

    player(playerX, playerY)

    # update
    pygame.display.update()