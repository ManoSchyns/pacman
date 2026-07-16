import pygame
from game.classes import Game
from game.classes.menu import MainMenu

SCREEN_WIDTH = 1000
SCREEN_HEIGTH = 1000

LEVEL_LIST = [(15, 17),
              (20, 21),
              (30, 30),
              (27, 10),
              (10, 10),
              (26, 27),
              (26, 17),
              (3, 4),
              (5, 7),
              (10, 10)]

if __name__ == "__main__":
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH,
                                      SCREEN_HEIGTH + 10))
    pygame.display.set_caption("PAC-MAN")
    menu = MainMenu(screen)
    while True:
        action = menu.run()
        if action != "start":
            break
        game = Game(LEVEL_LIST, 30, 10, 30, 100, 3, "heyy", 42, 90)
        if not game.play(screen):
            break
    pygame.quit()
