import pygame
import random
import math
from pygame import mixer

pygame.init()  # to initialize all pygame functions and stuff

# we will create our game window
# it creates a window with height=600, width=800
screen = pygame.display.set_mode((800, 600))
# the problem here is the screen or game window does not stay it vanishes after 1 or 2 seconds

# Set Background image on the screen
background = pygame.image.load('assets/background.jpg')

# Set Background sound
# we need to play this sound long so we use mixer.music
# otherwise we would have used mixer.sound
mixer.music.load('assets/background.wav')
# we need to initialize -1 to loop forever
mixer.music.play(-1)

# set title and icon for the game
pygame.display.set_caption('Space Invaders - Atari Game')
icon = pygame.image.load('assets/icon.png')
pygame.display.set_icon(icon)

# initialise player
player_img = pygame.image.load('assets/player.png')
player_x = 370
player_y = 480
delta_player_x = 0

# initialise enemy
enemy_img = pygame.image.load('assets/enemy.png')
enemy_x = random.randint(0, 736)
enemy_y = random.randint(50, 150)
delta_enemy_x = 0.3
delta_enemy_y = 10

# initialize bullet
ply_bullet_img = pygame.image.load('assets/bullet.png')
ply_bullet_x = 0
ply_bullet_y = 480
delta_ply_bullet_x = 0
delta_ply_bullet_y = 1
ply_bullet_state = 'ready'

# we will place the player on the screen


def player(x, y):
    # we will use blit function to draw the image on the screen
    screen.blit(player_img, (x, y))  # blit means draw


def enemy(x, y):
    # we will use blit function to draw the image on the screen
    screen.blit(enemy_img, (x, y))  # blit means draw


def ply_fire_bullet(x, y):
    global ply_bullet_state
    ply_bullet_state = 'fire'
    screen.blit(ply_bullet_img, (x+16, y+10))


def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt((enemy_x-bullet_x)**2 + (enemy_y-bullet_y)**2)
    if distance < 27:
        return True
    else:
        return False


# Set Game score
score = 0
# 2 args, font name and font size
font = pygame.font.Font('freesansbold.ttf', 32)


def show_score():
    text_pos_x = 10
    text_pos_y = 10
    # we need to render the score before showing it
    # 3 args, statement, boolean, colour(RGB)
    score_banner = font.render('SCORE : ' + str(score), True, (0, 255, 0))
    # show it on screen
    screen.blit(score_banner, (text_pos_x, text_pos_y))


# Game loop
running = True
while running:

    # Fill the screen with a color
    screen.fill((0, 0, 0))  # each value belongs to R G B colors
    # we need to write this important line always inorder to update our screen with whatever changes we made
    # pygame.display.update()

    # Set background
    screen.blit(background, (0, 0))

    # we need to loop through all the events and check for pressing close button
    # if close button is pressed we need to close the screen
    for event in pygame.event.get():  # this line gets a list of events

        if event.type == pygame.QUIT:  # check if close button is pressed
            # stop the game loop
            running = False

        # Move our player using keyboard
        if event.type == pygame.KEYDOWN:  # keydown says that a key in the keyboard is pressed down
            print('A Key Stroke is pressed')
            # conditions to move right or left
            # event.key gives value of the pressed key (key name)
            if event.key == pygame.K_RIGHT:  # k_right specifies that we pressed right arrow key
                print('Right arrow key is pressed')
                delta_player_x = 1
            elif event.key == pygame.K_LEFT:  # k_left specifies that we pressed left arrow key
                print('Left arrow key is pressed')
                delta_player_x = -1
                # Code to fire bullet
            elif event.key == pygame.K_SPACE:
                print('Fire button is pressed')
                if ply_bullet_state == 'ready':
                    print('Fired')
                    ply_bullet_x = player_x
                    ply_bullet_y = player_y
                    bullet_sound = mixer.Sound('assets/fire.wav')
                    bullet_sound.play()
                    ply_fire_bullet(ply_bullet_x, ply_bullet_y)

        elif event.type == pygame.KEYUP:  # keyup says that a key is released after pressing
            print('Key Stroke has been released')
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                delta_player_x = 0
    player_x += delta_player_x

    # set boundary to the player
    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736

    # set enemy mechanics
    if enemy_x <= 0:
        delta_enemy_x = 0.3
        enemy_y += delta_enemy_y
    elif enemy_x >= 736:
        delta_enemy_x = -0.3
        enemy_y += delta_enemy_y
    enemy_x += delta_enemy_x

    # Bullet movement
    if ply_bullet_state == 'fire':
        ply_bullet_y -= delta_ply_bullet_y
        ply_fire_bullet(ply_bullet_x, ply_bullet_y)
    if ply_bullet_y <= 0:
        ply_bullet_y = 480
        ply_bullet_state = 'ready'

    # Collision mechanics
    if is_collision(enemy_x, enemy_y, ply_bullet_x, ply_bullet_y):
        ply_bullet_y = 480
        ply_bullet_state = 'ready'
        # update score
        score += 1
        print('score = ', score)
        # play explosion sound
        buexplosion_sound = mixer.Sound('assets/explosion.wav')
        buexplosion_sound.play()
        # respawn enemy
        enemy_x = random.randint(0, 736)
        enemy_y = random.randint(50, 150)

    # position the player during game
    player(player_x, player_y)
    enemy(enemy_x, enemy_y)
    show_score()
    pygame.display.update()
