from mazegenerator import MazeGenerator
import pygame as pygame


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

    # Return les coordonnées du centre
    def get_center_maze(self) -> tuple[int, int]:
        x_center: int = self._width // 2
        y_center: int = self._heigth // 2

        while self._maze[y_center][x_center] == 15:
            y_center += 1
        return (x_center * self._cell_size + self._cell_size // 2,
                y_center * self._cell_size + self._cell_size // 2)

    # Return la derniere partie de surface utilisée
    # A partir de ou on peut utiliser les pixel
    def get_end_surface(self) -> int:
        return self._heigth * self._cell_size + self._thickness + 10
