import pygame, sys
import random
import math
from pygame import mixer

# Initialize pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))


mainClock = pygame.time.Clock()
# Add Backgroundd
background = pygame.image.load("resources/background.png").convert()

# Background sound
mixer.music.load("resources/background.wav")
mixer.music.play(-1)

# Set Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("resources/ufo.png").convert_alpha()
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load("resources/player.png").convert_alpha()
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
enemyNumber = 6
for i in range(enemyNumber):
    enemyImg.append(pygame.image.load("resources/enemy.png").convert_alpha())
    enemyX.append(random.random() * 735)
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(25)

# Bullet
bulletImg = pygame.image.load("resources/bullet.png").convert_alpha()
bulletX = 0
bulletY = 480
bulletY_change = 10
# Ready: Bullet can't be seen
# Fire: Bullet can be seen
bullet_state = "ready"

# score
scoreValue = 0
font = pygame.font.Font("resources/DolphinNormal.ttf", 48)
overFont = pygame.font.Font("resources/DolphinNormal.ttf", 96)

textCoordinates = (10, 10)


def show_score(coordinates):
    score = font.render("Score: " + str(scoreValue), True, (255, 255, 255))
    screen.blit(score, coordinates)


# method to draw the playerObject on the screen
def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow((enemyY - bulletY), 2) + math.pow((enemyX - bulletX), 2)))
    if distance < 27:
        return True
    else:
        return False


def gameOverText():
    overText = overFont.render("GAME OVER ", True, (255, 255, 255))
    screen.blit(overText, (120, 200))


left = False
right = False
# Game Loop until Player presses the close button
while True:
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))
    movement = 0
    if right == True:
        movement += 4
    if left == True:
        movement -= 4
    # iterates through all the event happening inside the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # if Keystroke is pressed check whether it is right key or left key
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_LEFT:
                left = True
            elif event.key == pygame.K_RIGHT:
                right = True
            elif event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletSound = mixer.Sound("resources/laser.wav")
                    bulletSound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                left = False
            if event.key == pygame.K_RIGHT:
                right = False

    playerX += movement
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    for i in range(enemyNumber):
        # Game over
        if enemyY[i] >= 460:
            for j in range(enemyNumber):
                enemyY[j] = 2000
            gameOverText()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0 or enemyX[i] >= 736:
            enemyX_change[i] *= -1
            enemyY[i] += enemyY_change[i]
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        # Collision
        if collision:
            explosionSound = mixer.Sound("resources/explosion.wav")
            explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            scoreValue += 1
            enemyX[i] = random.random() * 736
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bulletY < 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textCoordinates)
    mainClock.tick(60)
    pygame.display.update()
