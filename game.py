import pygame
import sys
from math import *
from button import Button
from playgame import play

pygame.init()

# create screen
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Menu")


BG = pygame.transform.scale(pygame.image.load("assets/Background.jpg"), (width, height))



def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/KnightWarrior-w16n8.otf", size)




def main_menu():
    while True:
        screen.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(110).render("MAIN   MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(400, 120))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Rect.png"), pos=(370, 280),
            text_input="PLAY", font=get_font(80), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Rect.png"), pos=(370, 450),
            text_input="QUIT", font=get_font(80), base_color="#d7fcd4", hovering_color="White")

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        play(height,width,screen)
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        pygame.quit()
                        sys.exit()

        pygame.display.update()


main_menu()