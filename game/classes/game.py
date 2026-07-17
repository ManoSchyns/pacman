import random
from score import Scores
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

        self.font_80 = pygame.font.Font("game/srcs/ARCADE_I.TTF", 80)
        self.font_40 = pygame.font.Font("game/srcs/ARCADE_I.TTF", 40)
        self.font_20 = pygame.font.Font("game/srcs/ARCADE_I.TTF", 20)
        self.font_15 = pygame.font.Font("game/srcs/ARCADE_R.TTF", 15)

    def play(self, screen: pygame.Surface) -> bool:
        # lancer le level x, avec une config x
        # Jouer en faisant augmenter les points
        end_message: str = "Game Over"
        game_random = random.Random()
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
                return False
            if exit_value == 0:
                running = False
            else:
                self.current_level += 1
            self.seed = game_random.randint(0, 2**32 - 1)

        if self.current_level == self.final_level:
            end_message = "Well Done !"

        if not self.show_end_screen(end_message, screen):
            return False
        return True

    """
    Affiche l'écran de fin avec le score du joueur
    et Recupère le nom de l'utilisateur
    """
    def show_end_screen(self, message: str, screen: pygame.Surface) -> bool:
        screen.fill((0, 0, 0))
        validity: tuple[bool, str] = (True, "None")
        clock = pygame.Clock()
        scores = Scores()

        change_flag: bool = True

        text_input = TextInput((screen.get_width() // 2 - 200,
                                screen.get_height() // 2 + 40,
                                400, 40), screen)

        running: bool = True
        while running:
            if change_flag:
                self.end_screen_view(message, screen, validity, text_input)
                change_flag = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        validity = self.player.verify_name()
                        if validity[0]:
                            running = False
                        else:
                            change_flag = True

                exit_input = text_input.handle_input(event)
                if exit_input == -1:
                    return False
                if exit_input == 1:
                    self.player.name = text_input.get_value()
                    validity = self.player.verify_name()
                    change_flag = True
            clock.tick(60)

        if self.player.name is not None:
            scores.add_player_scores(self.player.name,
                                     self.player.get_score())
        scores.export_scores()
        return True

    def end_screen_view(self, message: str, screen: pygame.Surface,
                        validity: tuple[bool, str],
                        text_input: TextInput) -> None:
        screen.fill((0, 0, 0))
        last_padding_y: int = 150

        color: tuple[int, int, int] = (0, 128, 0)
        if "Over" in message:
            color = (255, 0, 0)

        def put_text(font: pygame.Font, text_value: str,
                     colors: tuple[int, int, int],
                     postition: tuple[int, int]) -> None:
            text = font.render(text_value, True, colors)
            text_rect = text.get_rect(
                center=postition
                )
            screen.blit(text, text_rect)

        put_text(self.font_80, message, color, (
                screen.get_width() // 2,
                screen.get_height() // 2 - 100))

        put_text(self.font_40,
                 f"Your score: {self.player.get_score()}",
                 (255, 255, 0), (
                     screen.get_width() // 2,
                     screen.get_height() // 2))

        text_input.draw()

        if not validity[0]:
            put_text(self.font_15, validity[1],
                     (255, 0, 0), (
                     screen.get_width() // 2,
                     screen.get_height() // 2 + 150))
            last_padding_y = 250

        put_text(self.font_20,
                 "Enter your name and press enter\n"
                 "   To return to the main menu",
                 (255, 255, 255), (
                     screen.get_width() // 2,
                     screen.get_height() // 2 + last_padding_y))

        pygame.display.flip()
