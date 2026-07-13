import random
import pygame
from .level import Level
from player import Player

class Game:
    """
    A chaque boucle du jeu
    on affiche le level x, on fait augmenter les points,
    le level s'occupe de tout ? Non je pense pas
    """

    def __init__(self, level_list: list[tuple[int, int]],
                 pacgum: int,
                 points_per_pacgum: int,
                 points_per_super_pacgum: int,
                 points_per_ghost: int,
                 lives: int,
                 filename_hight: str,
                 seed: int,
                 level_max_time: int) -> None:

        self.level_list = level_list
        self.points_per_pacgum = points_per_pacgum
        self.points_per_super_pacgum = points_per_super_pacgum
        self.points_per_ghost = points_per_ghost

        self.filename_hight = filename_hight
        self.seed = seed
        self.level_max_time = level_max_time

        self.number_pacgum = pacgum

        self.current_level = 0
        self.player = Player(lives)

    def play(self, screen: pygame.Surface) -> None:
        # lancer le level x, avec une config x
        # Jouer en faisant augmenter les points
        running: bool = True
        while running and self.current_level < 10:
            curr_level_data = self.level_list[self.current_level]

            level = Level(curr_level_data[0], curr_level_data[1],
                          screen, self.seed,
                          self.number_pacgum, self.points_per_pacgum,
                          self.points_per_super_pacgum,
                          self.points_per_ghost,
                          self.level_max_time)

            exit_value = level.play(self.player)
            if exit_value == -1:
                return
            if exit_value == 0:
                running = False
            else:
                self.current_level += 1
            self.seed = random.randint(0, 2**32 - 1)
            level = None
        if self.current_level == 10:
           self.show_end_screen("Well Done !", screen)
        else:
            self.show_end_screen("Game Over", screen)

    def show_end_screen(self, message: str, screen: pygame.Surface):
        screen.fill((0, 0, 0))

        font = pygame.font.Font("game/srcs/ARCADE_I.TTF", 80)
        text = font.render(message, True, (255, 0, 0))
        text_rect = text.get_rect(
            center=(
                screen.get_width() // 2,
                screen.get_height() // 2 - 100
            )
        )
        screen.blit(text, text_rect)

        font = pygame.font.Font("game/srcs/ARCADE_I.TTF", 40)
        text = font.render(f"Your score: {self.player.get_score()}", True, (255, 255, 0))
        text_rect = text.get_rect(
            center=(
                screen.get_width() // 2,
                screen.get_height() // 2
            )
        )
        screen.blit(text, text_rect)

        font = pygame.font.Font("game/srcs/ARCADE_I.TTF", 20)
        text = font.render("Press any key to quit", True, (255, 255, 255))
        text_rect = text.get_rect(
            center=(
                screen.get_width() // 2,
                screen.get_height() // 2 + 150
            )
        )
        screen.blit(text, text_rect)

        pygame.display.flip()
        running: bool = True
        while running:
             for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    running = False

