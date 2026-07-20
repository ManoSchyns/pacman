import pygame
from game.classes import Game
from game.classes.menu import MainMenu
from configuration import parse, Config
import sys

SCREEN_WIDTH = 1000
SCREEN_HEIGTH = 1000


if __name__ == "__main__":
    pygame.init()

    config: Config
    args = sys.argv

    if len(args) != 2:
        print("The program must take only ONE argument (A json file)")
        exit()

    config = parse(args[1])

    screen = pygame.display.set_mode((SCREEN_WIDTH,
                                      SCREEN_HEIGTH + 10))
    pygame.display.set_caption("PAC-MAN")
    menu = MainMenu(screen)
    while True:
        action = menu.run()
        if action != "start":
            break
        game = Game(
            config.level_list,
            config.number_pacgum,
            config.points_per_pacgum,
            config.points_per_super_pacgum,
            config.points_per_ghost,
            config.lives,
            "test",
            config.seed, config.level_max_time
        )
        if not game.play(screen):
            break
    pygame.quit()
