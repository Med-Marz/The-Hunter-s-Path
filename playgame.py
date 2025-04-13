import pygame
import sys
import random
from math import *
from pygame import mixer
from button import Button


clock = pygame.time.Clock()

def play(height,width,screen):
    

    # init pygame
    pygame.init()
    clock = pygame.time.Clock()
    # create screen
    #width, height = 800, 600
    #screen = pygame.display.set_mode((width, height))

    # background
    background = pygame.image.load("assets/background.jpg")
    background = pygame.transform.scale(pygame.image.load("assets/background.jpg"), (width, height))


    # background sound
    mixer.music.load("assets/bg-music.mp3")
    mixer.music.play(-1)

    # Function to increase volume
    def increase_volume(step=0.1):
        current_volume = pygame.mixer.music.get_volume()
        new_volume = min(1.0, current_volume + step)
        pygame.mixer.music.set_volume(new_volume)

    # Function to decrease volume
    def decrease_volume(step=0.1):
        current_volume = pygame.mixer.music.get_volume()
        new_volume = max(0.0, current_volume - step)
        pygame.mixer.music.set_volume(new_volume)

    # title and icon
    pygame.display.set_caption("The Hunter's Path")
    icon = pygame.image.load("assets/logo.png")
    pygame.display.set_icon(icon)

    # hunter
    hunterImg = pygame.transform.scale(pygame.image.load("assets/hunter.png"), (64, 64))
    hunterX = 370
    hunterY = 480
    hunterX_change = 0

    def hunter(x, y):
        screen.blit(hunterImg, (x, y))

    # boar
    boarImg = []
    boarX = []
    boarY = []
    boarX_change = []
    boarY_change = []
    num_of_boars = 3

    for i in range(num_of_boars):
        boarImg.append(pygame.transform.scale(pygame.image.load("assets/boar.png"), (64, 64)))
        boarX.append(random.randint(0, 736))
        boarY.append(random.randint(50, 150))
        boarX_change.append(3)
        boarY_change.append(40)

    def boar(x, y, i):
        screen.blit(boarImg[i], (x, y))

    # bullet
    bulletImg = pygame.image.load("assets/bullet.png")
    bulletX = 0
    bulletY = 480
    bulletY_change = 6

    bullet_state = "ready"  # we can't see bullet in screen

  
        

    def fire_bullet(x, y):
        nonlocal bullet_state
        bullet_state = "fire"
        screen.blit(bulletImg, (x + 16, y + 10))

    def isCollision(boarX, boarY, bulletX, bulletY):
        distance = sqrt((bulletX - boarX) ** 2 + (bulletY - boarY) ** 2)
        if distance < 27:
            return True
        else:
            return False

    # score
    score_value = 0
    font = pygame.font.Font("assets/RebellionSquad-ZpprZ.ttf", 28)
    textX = 10
    textY = 10

    def show_score(x, y):
        score = font.render("Score :  " + str(score_value), True, (255, 255, 255))
        screen.blit(score, (x, y))


    # Load all hunter images
    HUNTER_SIZE = (64, 64)
    hunter_images = { 
        'normal': pygame.transform.scale(pygame.image.load("assets/hunter.png"), HUNTER_SIZE), # Original hunter image
        'updated': pygame.transform.scale(pygame.image.load("assets/hunter_updated.png"), HUNTER_SIZE) # Updated hunter image
    }



    # health
    health_value = 100
    health_font = pygame.font.Font("assets/RebellionSquad-ZpprZ.ttf", 28)

    def show_health():
        health = health_font.render("health  :  " + str(health_value), True, (255, 255, 255))
        screen.blit(health, (10, 50))

    # game over text
    over_font = pygame.font.Font("assets/BruceForeverRegular-X3jd2.ttf", 64)

    def game_over_text():
        over_text = over_font.render("GAME OVER !! ", True, (255, 0, 0))
        screen.blit(over_text, (110, 250))

    def respawn(i):
        boarX[i] = random.randint(0, 736)
        boarY[i] = random.randint(50, 150)




    # game loop
    collision = False
    running = True
    game_over = False
    hunter_updated = False  # Flag to track if hunter image has been updated

    while running:
        # screen.fill((red,green,blue))
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    hunterX_change = -5
                if event.key == pygame.K_RIGHT:
                    hunterX_change = 5
                if event.key == pygame.K_SPACE:
                    bullet_sound = mixer.Sound("assets/bull-sound.wav")
                    bullet_sound.play()
                    if bullet_state == "ready":
                        bulletX = hunterX
                        fire_bullet(bulletX, bulletY)
                if event.key == pygame.K_KP_PLUS:
                    increase_volume()
                if event.key == pygame.K_KP_MINUS:
                    decrease_volume()
                if event.key == pygame.K_r and game_over:
                    score_value = 0
                    health_value = 100
                    num_of_boars = 3
                    hunterY = 480
                    for i in range(num_of_boars):
                        respawn(i)
                    game_over = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    hunterX_change = 0





        # Check if score reaches 15 to update hunter image
        if score_value == 15 and not hunter_updated:
            hunter_updated = True
            # Update hunter image
            hunterImg = pygame.transform.scale(pygame.image.load("assets/hunter_updated.png"), HUNTER_SIZE)
            # You may also need to update the hunter function if necessary
            hunter_images['normal'] = hunterImg
            bulletY_change += 2






        # Hunter movement
        hunterX += hunterX_change
        if hunterX <= -64:  # hunterX = 0
            hunterX = width - 64  # hunterX = 0
        elif hunterX >= width:  # hunterX = width -64
            hunterX = 0
        # boar movement

        for i in range(num_of_boars):

            if hunterY + 64 > boarY[i] >= 430 and hunterX <= boarX[i] <= hunterX + 55:
                health_value -= 10
                respawn(i)
                # break

            if  boarY[i] > height - 10:
                respawn(i)


            if health_value == 0:
                for j in range(num_of_boars):
                    boarY[j] = 2000
                game_over_text()
                game_over = True
                break

            boarX[i] += boarX_change[i]
            if boarX[i] <= 0 or boarX[i] >= width - 64:
                boarX_change[i] = -boarX_change[i]
                boarY[i] += boarY_change[i]






            # collision
            if boarY[i] < hunterY - 55:
                collision = isCollision(boarX[i], boarY[i], bulletX, bulletY)
            if collision:
                bullet_sound = mixer.Sound("assets/explosion.wav")
                bullet_sound.play()
                bulletY = 480
                bullet_state = "ready"
                score_value += 1

                if score_value % 3 == 0:
                    # add new boar
                    boarImg.append(pygame.transform.scale(pygame.image.load("assets/boar.png"), (64, 64)))
                    boarX.append(random.randint(0, 736))
                    boarY.append(random.randint(50, 150))
                    boarX_change.append(3)
                    boarY_change.append(40)
                    num_of_boars += 1
                respawn(i)

            boar(boarX[i], boarY[i], i)

        # bullet movement
        if bulletY <= 0:
            bulletY = hunterY
            bullet_state = "ready"

        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

        hunter(hunterX, hunterY)
        show_score(textX, textY)
        show_health()
        pygame.display.update()
        clock.tick(60)