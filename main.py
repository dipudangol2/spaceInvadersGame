import pygame as p
import random

# Initialize pygame
p.init()

# Create the screen
screen = p.display.set_mode((800, 600))

# Add Backgroundd
background = p.image.load("resources/background.png").convert()

# Set Title and Icon
p.display.set_caption("Space Invaders")
icon = p.image.load("resources/ufo.png").convert_alpha()
p.display.set_icon(icon)

# Player
playerImg = p.image.load("resources/player.png").convert_alpha()
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = p.image.load("resources/enemy.png")
enemyX = random.random() * 736
enemyY = random.randint(50, 150)
enemyX_change = 0.75
enemyY_change = 20

# Bullet
bulletImg = p.image.load("resources/bullet.png").convert_alpha()
bulletX = 0
bulletY = 480
bulletY_change = 2.5
# Ready: Bullet can't be seen
# Fire: Bullet can be seen
bullet_state = "ready"


# method to draw the playerObject on the screen
def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y):
    screen.blit(enemyImg, (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


# Game Loop until Player presses the close button
running = True
while running:
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))
    # iterates through all the event happening inside the window
    for event in p.event.get():
        if event.type == p.QUIT:
            running = False
        # if Keystroke is pressed check whether it is right key or left key
        if event.type == p.KEYDOWN:
            if event.key == p.K_ESCAPE:
                running = False
            if event.key == p.K_LEFT:
                playerX_change = -1
                print("Left arrow is pressed")
            elif event.key == p.K_RIGHT:
                playerX_change = 1
                print("Right arrow is pressed")
            elif event.key == p.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
            else:
                print("Keystroke event")
        if event.type == p.KEYUP:
            if event.key == p.K_LEFT or event.key == p.K_RIGHT:
                playerX_change = 0
                print("Keystroke released")

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    enemyX += enemyX_change
    if enemyX <= 0 or enemyX >= 736:
        enemyX_change *= -1
        enemyY += enemyY_change

    # Bullet Movement
    if bulletY < 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    player(playerX, playerY)
    enemy(enemyX, enemyY)
    p.display.update()
