import pygame
import random
import math
from pygame import mixer

# Initializing Pygame
pygame.init()

# Creating Game Window
screen = pygame.display.set_mode((1600, 900))

# Background Image
background = pygame.image.load('Background.jpg')

# Background Music
mixer.music.load('back music.ogg')
mixer.music.play(-1)

# Title and Icon of Window
# Always Choose 32x32 pixel for icon
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('Icon.png')
pygame.display.set_icon(icon)

# Player Image Loading and Initial Player Position
player_image = pygame.image.load('Spacecraft.png')
player_x = 800
player_y = 700
player_change_in_x = 0
player_change_in_y = 0

# Enemy Image Loading and Initial Position
enemy_image = []
enemy_x = []
enemy_y = []
enemy_change_in_x = []
enemy_change_in_y = []
number_of_enemies = 6
for i in range(number_of_enemies):
    enemy_image .append(pygame.image.load('Ufo.png'))
    enemy_x.append(random.randint(0, 1530))
    enemy_y.append(random.randint(0, 50))
    enemy_change_in_x.append(7)
    enemy_change_in_y.append(40)

# Bullet
bullet_image = pygame.image.load('bullet.png')
bullet_x = 800
bullet_y = 700
bullet_change_in_x = 0
bullet_change_in_y = -15

# Ready state is before fire situation and Fire state is when bullet is released
bullet_state = 'Ready'


def enemy(x, y, n):
    screen.blit(enemy_image[n], (x, y))


def player(x, y):
    screen.blit(player_image, (x, y))


def bullet(x, y):
    global bullet_state, bullet_y
    bullet_state = 'Fire'
    screen.blit(bullet_image, (x + 16, y + 10))
    bullet_y += bullet_change_in_y


def dist(x1, x2, y1, y2):
    distance = math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))
    if distance <= 30:
        return True
    else:
        return False


font2 = pygame.font.Font('GrandHotel-Regular.otf', 150)


def game_over(a, b):
    g_over = font2.render('GAME OVER', True, (0, 0, 0))
    screen.blit(g_over, (a, b))


# Score
score_value = 0
font = pygame.font.Font('Lobster_1.3.otf', 32)
score_x = 10
score_y = 10


def show_score(x, y):
    score = font.render('Score:' + str(score_value), True, (0, 0, 0))
    screen.blit(score, (x, y))


# Maintaining Game Window
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Detecting whether any key is pressed or released
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_change_in_x = -10
                player_change_in_y = 0
            if event.key == pygame.K_RIGHT:
                player_change_in_x = 10
                player_change_in_y = 0

            # Moving Bullet in Straight Line
            if event.key == pygame.K_SPACE:
                if bullet_state == 'Ready':
                    # Adding Laser Sound
                    laser = mixer.Sound('laser.wav')
                    laser.play()
                    bullet_x = player_x
                    bullet(bullet_x, bullet_y)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player_change_in_x = -6
                player_change_in_y = 0
            if event.key == pygame.K_RIGHT:
                player_change_in_x = 6
                player_change_in_y = 0

    # Setting Screen Colour And Updating
    screen.fill((0, 0, 0))

    # Background Image
    screen.blit(background, (0, 0))

    # Setting Boundaries of Screen for Player
    player_x += player_change_in_x
    if player_x <= 0:
        player_x = 0
    elif player_x >= 1536:
        player_x = 1536
    player_y += player_change_in_y
    if player_y <= 0:
        player_y = 0
    elif player_y >= 825:
        player_y = 825

    # Setting Boundaries of Screen for Enemy
    for i in range(number_of_enemies):
        # Game Over
        if enemy_y[i] > 500:
            for j in range(number_of_enemies):
                enemy_y[j] = 10000
            game_over(500, 200)
            break

        enemy_x[i] += enemy_change_in_x[i]
        if enemy_x[i] >= 1536:
            enemy_change_in_x[i] = -7
            enemy_y[i] += enemy_change_in_y[i]
        elif enemy_x[i] <= 0:
            enemy_change_in_x[i] = 7
            enemy_y[i] += enemy_change_in_y[i]

        # Collision
        collision = dist(enemy_x[i], bullet_x, enemy_y[i], bullet_y)
        if collision:
            # Adding Explosion Sound
            explosion = mixer.Sound('explosion.wav')
            explosion.play()
            bullet_y = 700
            bullet_state = 'Ready'
            score_value += 1
            print(score_value)
            enemy_x[i] = random.randint(0, 1600)
            enemy_y[i] = random.randint(0, 50)

        # Calling enemy function
        enemy(enemy_x[i], enemy_y[i], i)

    # Shooting Multiple Bullets
    if bullet_y <= 0:
        bullet_y = 700
        bullet_state = 'Ready'

    # Calling Bullet Function
    if bullet_state == 'Fire':
        bullet(bullet_x, bullet_y)

    # Calling player function
    player(player_x, player_y)

    # Calling Show Score Function
    show_score(score_x, score_y)

    # Updating Screen
    pygame.display.update()
