from game.classes import Game
import pygame

SCREEN_WIDTH = 1000
SCREEN_HEIGTH = 1000

if __name__ == "__main__":
    pygame.init()
    # Scrren du jeu
    screen = pygame.display.set_mode((SCREEN_WIDTH,
                                      SCREEN_HEIGTH + 10))
    level_list = [(15, 17),
                  (20, 21),
                  (30, 30),
                  (27, 10),
                  (10, 10),
                  (26, 27),
                  (26, 17),
                  (3, 4),
                  (5, 7),
                  (10, 10)]
    game = Game(level_list, 30, 0, 0, 0, 3, "heyy", 42, 100)
    game.play(screen)
    pygame.quit()
