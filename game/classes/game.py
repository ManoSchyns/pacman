import random
import pygame
from .level import Level
from player import Player
from game.srcs import TextInput


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
        self.final_level = len(level_list)
        self.player = Player(lives)

    def play(self, screen: pygame.Surface) -> None:
        # lancer le level x, avec une config x
        # Jouer en faisant augmenter les points
        running: bool = True
        while running and self.current_level < self.final_level:
            curr_level_data = self.level_list[self.current_level]

            level = Level(curr_level_data[0], curr_level_data[1],
                          screen, self.seed,
                          self.number_pacgum, self.points_per_pacgum,
                          self.points_per_super_pacgum,
                          self.points_per_ghost,
                          self.level_max_time, self.current_level + 1,
                          self.final_level)

            exit_value = level.play(self.player)
            if exit_value == -1:
                return
            if exit_value == 0:
                running = False
            else:
                self.current_level += 1
            self.seed = random.randint(0, 2**32 - 1)
            level = None
        if self.current_level == self.final_level:
            self.show_end_screen("Well Done !", screen)
        else:
            self.show_end_screen("Game Over", screen)

    """
    Affiche l'écran de fin avec le score du joueur
    et Recupère le nom de l'utilisateur
    """
    def show_end_screen(self, message: str, screen: pygame.Surface):
        screen.fill((0, 0, 0))

        color: tuple[int, int, int] = (0, 128, 0)
        if "Over" in message:
            color = (255, 0, 0)

        def put_text(text_value: str, text_size: int,
                     colors: tuple[int, int, int],
                     postition: tuple[int, int]):
            font = pygame.font.Font("game/srcs/ARCADE_I.TTF", text_size)
            text = font.render(text_value, True, colors)
            text_rect = text.get_rect(
                center=postition
                )
            screen.blit(text, text_rect)

        put_text(message, 80, color, (
                screen.get_width() // 2,
                screen.get_height() // 2 - 100))

        put_text(f"Your score: {self.player.get_score()}", 40,
                 (255, 255, 0), (
                     screen.get_width() // 2,
                     screen.get_height() // 2))

        put_text("Enter your name and press enter\n"
                 "   To return to the main menu", 20,
                 (255, 255, 255), (
                     screen.get_width() // 2,
                     screen.get_height() // 2 + 150))

        text_input = TextInput((screen.get_width() // 2 - 200,
                                screen.get_height() // 2 + 40,
                                400, 40), screen)
        text_input.draw()
        pygame.display.flip()
        running: bool = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.player.name = text_input.get_value()
                        if not self.player.name == "":
                            running = False
                if not text_input.handle_input(event):
                    running = False
        print(self.player.name)
