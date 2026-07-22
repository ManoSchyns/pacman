from .pacgums import Pacgums
from .super_pacgums import SuperPacgums
from maze.classes import Maze
import pygame


class GenPacgums:
    """Gère la création, l'affichage et la collecte des pacgums."""

    def __init__(self, number_pacgums: int, points_per_pacgum: int,
                 points_per_super_pacgum: int,
                 maze: Maze) -> None:
        """Initialise le générateur de pacgums pour un labyrinthe."""
        self.number_pacgums = number_pacgums
        self.number_super_pacgums = 4
        self.points_per_pacgums = points_per_pacgum
        self.points_per_super_pacgums = points_per_super_pacgum

        self.list_pacgums: list[Pacgums | SuperPacgums] = []

        self.maze = maze

    def eat(self, rect: pygame.rect.Rect) -> tuple[int, bool]:
        """Retire le pacgum touché par le rectangle reçu.

        Returns:
            les points gagnés et True si c'était un super pacgum.
        """
        for pacgum in self.list_pacgums:
            if rect.colliderect(pacgum.rect):
                if isinstance(pacgum, SuperPacgums):
                    self.number_super_pacgums -= 1
                else:
                    self.number_pacgums -= 1
                self.list_pacgums.remove(pacgum)
                return (pacgum.xp, isinstance(pacgum, SuperPacgums))
        return (0, False)

    def show(self, surface: pygame.Surface, dt: float) -> None:
        """Dessine tous les pacgums restants sur la surface."""
        for pacgum in self.list_pacgums:
            pacgum.draw(surface, dt)

    def generate(self) -> None:
        """Génère les pacgums et les super pacgums du labyrinthe."""
        self._generate_pacgums()
        self._generate_super_pacgums()

    def _generate_pacgums(self) -> None:
        """Crée les pacgums sur des cases libres tirées au hasard."""
        spawns: list[tuple[int, int]] = self.maze.get_pacgums_spawn(
            self.number_pacgums)

        for spawn in spawns:
            self.list_pacgums.append(Pacgums(self.points_per_pacgums,
                                             spawn[0],
                                             spawn[1],
                                             self.maze.get_cell_size()))

    def _generate_super_pacgums(self) -> None:
        """Crée les super pacgums dans les coins du labyrinthe."""
        spawns: list[tuple[int, int]] = self.maze.get_super_pacgums_spawn()

        for spawn in spawns:
            self.list_pacgums.append(SuperPacgums(
                self.points_per_super_pacgums,
                spawn[0], spawn[1], self.maze.get_cell_size()))
