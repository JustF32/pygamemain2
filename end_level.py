import pygame, sys, importlib
from menubuttons import Button

pygame.init()

SCREEN = pygame.display.set_mode((1024, 896))
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/bg_menu.png")

def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)


def play():
    #Сюда прописываешь следующий уровень
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill("black")
        exit()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()


def retry():
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill("black")
        import main
        importlib.reload(main)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            pygame.display.update()

def main_menu():
    while True:

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("YOU DIED", True, "red")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))
        #Чтобы изменить размер кнопки нужно изменить картинку в assets
        PLAY_BUTTON = Button(image=pygame.image.load("assets/play.png"), pos=(800, 600),
                             text_input="EXIT", font=get_font(75), base_color="yellow")
        RETRY_BUTTON = Button(image=pygame.image.load("assets/quit.png"), pos=(340, 600),
                             text_input="RETRY", font=get_font(75), base_color="yellow")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, RETRY_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if RETRY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    retry()
                pygame.display.update()
        pygame.display.update()

main_menu()
