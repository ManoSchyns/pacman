from mazegenerator import MazeGenerator
import pygame as pygame


class Maze:

    def __init__(self, width: int, height: int,
                 cell_size: int, seed: int = 0) -> None:
        self._cell_size = cell_size
        self._width = width
        self._heigth = height
        self._thickness = 5
        self._walls_color = (255, 152, 0)
        self._42_color = (255, 0, 0)
        self._walls: list[pygame.Rect] = []
        self._maze_gen = MazeGenerator(size=(width, height), seed=seed)
        self._maze = self._maze_gen.maze
        self._maze_surface = pygame.Surface((
            width * cell_size + self._thickness,
            height * cell_size + self._thickness))
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
        return int(corridor_size * 0.75)

    # Return les coordonnées du centre
    def get_center_maze(self) -> tuple[int, int]:
        return (self._width * self._cell_size // 2,
                self._heigth * self._cell_size // 2)


if __name__ == "__main__":
    pygame.init()

    """
    screen size:

    Pour la width du lab
    -> La width su screen = width * cell_size + epaisseur des walls
    Pour la heigth su lab
    -> la heigth du screen = height * cell_Size + epaisseur des walls
    """
    cell_size = 30
    width = 15
    height = 17

    # Scrren du jeu
    screen = pygame.display.set_mode((width * cell_size + 5,
                                      height * cell_size + 5))
    clock = pygame.time.Clock()
    running = True

    # Maze + récupération de sa surface
    maze = Maze(width, height, cell_size)
    screen.blit(maze.get_maze_surface(), (0, 0))

    # Centre du lab
    maze_center = maze.get_center_maze()

    # Taille du pacman
    pacman_size = maze.get_pacman_size()
    center = (pacman_size // 2, pacman_size // 2)
    radius = pacman_size // 2

    # Exemple de pacman sans anim
    pacman = pygame.Surface((pacman_size, pacman_size), pygame.SRCALPHA)
    pygame.draw.circle(
        pacman,
        (255, 255, 0),
        center,
        radius
        )
    # set pacman au centre du lab
    pac_man_pos = pacman.get_rect()
    pac_man_pos.center = maze_center
    screen.blit(pacman, pac_man_pos)

    # on affiche
    pygame.display.flip()

    # mouvements du pacman
    pacman_move = (0, 1)
    while running:

        # touches clavier
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    pacman_move = (0, -1)
                if event.key == pygame.K_DOWN:
                    pacman_move = (0, 1)
                if event.key == pygame.K_RIGHT:
                    pacman_move = (1, 0)
                if event.key == pygame.K_LEFT:
                    pacman_move = (-1, 0)

        # test si on est pas dans un wall
        pac_man_pos.x += pacman_move[0]
        pac_man_pos.y += pacman_move[1]
        if maze.check_collisions(pac_man_pos):
            pac_man_pos.x -= pacman_move[0]
            pac_man_pos.y -= pacman_move[1]

        # On supprime ce qu'il y a a l'ecran et on le remet
        screen.fill((0, 0, 0))
        screen.blit(maze.get_maze_surface(), (0, 0))
        screen.blit(pacman, pac_man_pos)
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
