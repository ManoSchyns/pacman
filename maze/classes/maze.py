from mazegenerator import MazeGenerator
import pygame as pygame
import random

NORTH: int = 1
EAST: int = 2


class Maze:

    def __init__(self, width: int, height: int,
                 screen: pygame.Surface,
                 seed: int = 0) -> None:

        self._cell_size = min(screen.get_width() // width,
                              (screen.get_height() - 50) // height)
        self._width = width
        self._heigth = height
        self._thickness = 5
        self._walls_color = (255, 152, 0)
        self._42_color = (255, 0, 0)
        self._walls: list[pygame.Rect] = []
        self._maze_gen = MazeGenerator(size=(width, height), seed=seed)
        self._maze = self._maze_gen.maze
        self._maze_surface = pygame.Surface((
            width * self._cell_size + self._thickness,
            height * self._cell_size + self._thickness))
        self._gen_maze_surface()

    """
    Dessine le labyrinthe sur une surface.
    Enregistre les collisions dans _walls
    """
    def _gen_maze_surface(self) -> None:

        NORTH: int = 1
        EAST: int = 2
        SOUTH: int = 4
        WEST: int = 8

        for y in range(self._heigth):
            for x in range(self._width):
                row = y * self._cell_size
                col = x * self._cell_size

                if self._maze[y][x] == 15:
                    pygame.draw.rect(self._maze_surface, self._42_color,
                                     (col, row, self._cell_size,
                                      self._cell_size))

                if self._maze[y][x] & NORTH:
                    pygame.draw.line(self._maze_surface, self._walls_color,
                                     (col, row), (col + self._cell_size, row),
                                     self._thickness)

                    self._walls.append(pygame.Rect
                                       (col, row - self._thickness // 2,
                                        self._cell_size, self._thickness))

                if self._maze[y][x] & EAST:
                    pygame.draw.line(self._maze_surface,
                                     self._walls_color,
                                     (col + self._cell_size, row),
                                     (col + self._cell_size,
                                      row + self._cell_size),
                                     self._thickness)

                    self._walls.append(pygame.Rect
                                       (col + self._cell_size -
                                        self._thickness // 2,
                                        row, self._thickness, self._cell_size))

                if y == self._heigth - 1 and self._maze[y][x] & SOUTH:
                    pygame.draw.line(self._maze_surface,
                                     self._walls_color,
                                     (col, row + self._cell_size),
                                     (col + self._cell_size,
                                      row + self._cell_size),
                                     self._thickness)

                    self._walls.append(pygame.Rect
                                       (col, row + self._cell_size -
                                        self._thickness // 2,
                                        self._cell_size, self._thickness))

                if x == 0 and self._maze[y][x] & WEST:
                    pygame.draw.line(self._maze_surface,
                                     self._walls_color, (col, row),
                                     (col, row + self._cell_size),
                                     self._thickness)

                    self._walls.append(pygame.Rect
                                       (col - self._thickness // 2, row,
                                        self._thickness, self._cell_size))

    # Return True si pacman est sur un mur -> collison
    # False si non
    def check_collisions(self, pacman_rect: pygame.Rect) -> bool:
        for wall in self._walls:
            if pacman_rect.colliderect(wall):
                return True
        return False

    # Returne l'affichage du lab
    def get_maze_surface(self) -> pygame.Surface:
        return self._maze_surface

    # Return en int le  de pacman selon la taille des couloirs
    # Pacman sera un peu plus petit que la taille des couloir *0.8
    def get_pacman_size(self) -> int:
        corridor_size: int = self._cell_size - self._thickness
        return int(corridor_size * 0.7)

    def get_cell_size(self) -> int:
        return self._cell_size

    # Return les coordonnées du centre
    def get_center_maze(self) -> tuple[int, int]:
        x_center: int = self._width // 2
        y_center: int = self._heigth // 2

        while self._maze[y_center][x_center] == 15:
            y_center += 1
        return (x_center * self._cell_size + self._cell_size // 2,
                y_center * self._cell_size + self._cell_size // 2)

    def is_open(self, cell: tuple[int, int], direction: str) -> bool:
        x, y = cell
        if direction == "up":
            target = (x, y - 1)
            blocked = self._wall_bit(x, y, NORTH)
        elif direction == "down":
            target = (x, y + 1)
            blocked = self._wall_bit(x, y + 1, NORTH)
        elif direction == "left":
            target = (x - 1, y)
            blocked = self._wall_bit(x - 1, y, EAST)
        else:
            target = (x + 1, y)
            blocked = self._wall_bit(x, y, EAST)

        target_x, target_y = target
        if not (0 <= target_x < self._width
                and 0 <= target_y < self._heigth):
            return False
        if blocked:
            return False
        return bool(self._maze[target_y][target_x] != 15)

    def _wall_bit(self, x: int, y: int, bit: int) -> bool:
        if not (0 <= x < self._width and 0 <= y < self._heigth):
            return True
        return bool(self._maze[y][x] & bit)

    def get_ghost_spawns(self) -> list[tuple[int, int]]:
        corners = [(0, 0),
                   (self._width - 1, 0),
                   (0, self._heigth - 1),
                   (self._width - 1, self._heigth - 1)]

        spawns: list[tuple[int, int]] = []
        for corner_x, corner_y in corners:
            x, y = self._closest_free_cell(corner_x, corner_y)
            spawns.append((x * self._cell_size + self._cell_size // 2,
                           y * self._cell_size + self._cell_size // 2))
        return spawns

    """
    Return les points de spawn pour les superpacgum
    -> Mis directement dans le coin
    """
    def get_super_pacgums_spawn(self) -> list[int, int]:
        return self.get_ghost_spawns()

    """
    Return  toutes les cellules disponibles
    """
    def get_cell_available(self) -> list[tuple[int, int]]:
        available: list[tuple[int, int]] = []

        to_avoid: list[tuple[int, int]] = self.get_ghost_spawns()
        to_avoid.append(self.get_center_maze())
        to_avoid_2: list[tuple[int, int]] = self.get_super_pacgums_spawn()

        for row in range(self._heigth):
            for col in range(self._width):
                y = row * self._cell_size + self._cell_size // 2
                x = col * self._cell_size + self._cell_size // 2
                if (not (x, y) in to_avoid and not (x, y)
                        in to_avoid_2 and self._maze[row][col] != 15):
                    available.append((x, y))

        return available

    """
    Return les points de spawn des pacgums
    """
    def get_pacgums_spawn(self, number_of_spawn: int) -> list[tuple[int, int]]:
        available: list[tuple[int, int]] = self.get_cell_available()
        random.shuffle(available)
        return available[:number_of_spawn]

    def _closest_free_cell(self, x: int, y: int) -> tuple[int, int]:
        step_x = 1 if x == 0 else -1
        step_y = 1 if y == 0 else -1

        for dist in range(max(self._width, self._heigth)):
            new_x = x + dist * step_x
            if 0 <= new_x < self._width and self._maze[y][new_x] != 15:
                return (new_x, y)

            new_y = y + dist * step_y
            if 0 <= new_y < self._heigth and self._maze[new_y][x] != 15:
                return (x, new_y)
        return (x, y)

    # Return la derniere partie de surface utilisée
    # A partir de ou on peut utiliser les pixel
    def get_end_surface(self) -> int:
        return self._heigth * self._cell_size + self._thickness + 10
