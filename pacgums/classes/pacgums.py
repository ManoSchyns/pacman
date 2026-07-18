import pygame


class Pacgums:

    def __init__(self, xp: int, x: int, y: int, cell_size: int):
        self.xp = xp
        self.rect = pygame.Rect(x - cell_size // 2,
                                y - cell_size // 2,
                                cell_size, cell_size)

        self.radius_ratio = 0.12
        self.color = (255, 255, 255)
        self.radius = int(cell_size * self.radius_ratio)

    def draw(self, screen: pygame.Surface, dt: float) -> None:
        pygame.draw.circle(
            screen,
            self.color,
            self.rect.center,
            self.radius
        )
