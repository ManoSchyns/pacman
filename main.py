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
    ret_val: tuple[bool, Config]
    args = sys.argv

    if len(args) != 2:
        print("\nThe program must take only ONE argument (A json file)\n")
        sys.exit(1)

    ret_val = parse(args[1])
    if not ret_val[0]:
        sys.exit(1)

    config = ret_val[1]

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
            config.seed, config.level_max_time
        )
        if not game.play(screen):
            break
    pygame.quit()
