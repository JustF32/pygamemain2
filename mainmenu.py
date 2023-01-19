import pygame, sys
from menubuttons import Button

pygame.init()

SCREEN = pygame.display.set_mode((1024, 896))
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/bg_menu.png")

def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)


def play():
    import main
    exit()


def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        SwordPic = pygame.transform.scale(pygame.image.load('data/S10.png'), (800, 700))
        SCREEN.blit(SwordPic, (50, 50))

        OPTIONS_BACK = Button(image=None, pos=(640, 760),
                              text_input="BACK", font=get_font(75), base_color="Black")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("ESCAPE FROM DARK", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(540, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/play.png"), pos=(340, 250),
                             text_input="PLAY", font=get_font(75), base_color="#d7fcd4")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/options.png"), pos=(340, 400),
                                text_input="CONTROLS", font=get_font(75), base_color="#d7fcd4")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/quit.png"), pos=(340, 550),
                             text_input="QUIT", font=get_font(75), base_color="#d7fcd4")

        SCREEN.blit(MENU_TEXT, MENU_RECT)


        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
                pygame.display.update()

        pygame.display.update()


main_menu()