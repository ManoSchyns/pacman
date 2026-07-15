from .pacgums import Pacgums
import pygame


class SuperPacgums(Pacgums):

    def __init__(self, xp: int, x: int, y: int, cell_size: int) -> None:
        super().__init__(xp, x, y, cell_size)
        self.radius_ratio = 0.2
        self.radius = int(cell_size * self.radius_ratio)

        self.color_flag = True
        self.timer = 0

    def draw(self, screen: pygame.Surface, dt: int) -> None:
        self.timer += dt

        if self.timer >= 0.5:
            self.timer = 0
            self.color_flag = not self.color_flag

        if self.color_flag:
            self.color = (255, 255, 255)
        else:
            self.color = (128, 128, 128)
        super().draw(screen, dt)
