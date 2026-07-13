import pygame
import random
from .level import Level
from player import Player

"""
A chaque boucle du jeu
on affiche le level x, on fait augmenter les points,
le level s'occupe de tout ? Non je pense pas
"""
class Game:

    def __init__(self, level_list: list[tuple[int, int]],
                 pacgum: int,
                 points_per_pacgum: int,
                 points_per_super_pacgum: int,
                 points_per_ghost: int,
                 lives: int,
                 filename_hight: str,
                 seed: int,
                 level_max_time: int):

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

    def play(self, screen):
        # lancer le level x, avec une config x
        # Jouer en faisant augmenter les points
        running = True
        while running and self.current_level < 10:
            curr_level_data = self.level_list[self.current_level]
            
            level = Level(curr_level_data[0], curr_level_data[1], screen, self.seed,
                          self.number_pacgum, self.points_per_pacgum,
                          self.points_per_super_pacgum, self.points_per_ghost,
                          self.level_max_time)

            exit_value = level.play(self.player)
            if exit_value == -1:
                return
            if exit_value == 0:
                running = False
            self.current_level += 1
            self.seed = random.randint(0, 2**32 - 1)
            level = None