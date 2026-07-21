import pygame

from sprietsheet.classes.spritesheet import SpriteSheet


class Pacman:
    """Découpe la spritesheet en animations de Pacman."""

    DEATH_INDICES = list(range(14))
    LEFT_INDICES = [15, 14]
    UP_INDICES = [20, 21]
    DOWN_INDICES = [22, 23]

    def __init__(self, sheet_path: str, size: int) -> None:
        """Charge la spritesheet et construit chaque animation.

        Args:
            sheet_path: chemin vers l'image de la spritesheet.
            size: taille voulue pour chaque frame en pixels.
        """
        sheet = SpriteSheet(sheet_path)
        sprites = [pygame.transform.scale(image, (size, size))
                   for _, image in sheet.auto_slice()]
        left = [sprites[i] for i in self.LEFT_INDICES]
        right = [
            pygame.transform.flip(frame, True, False) for frame in left
        ]
        up = [sprites[i] for i in self.UP_INDICES]
        down = [sprites[i] for i in self.DOWN_INDICES]
        death = [sprites[i] for i in self.DEATH_INDICES]
        self.animations: dict[str, list[pygame.Surface]] = {
            "left": left,
            "right": right,
            "up": up,
            "down": down,
            "death": death,
        }

    def actions(self) -> list[str]:
        """Retourne la liste des noms d'animations disponibles."""
        return list(self.animations)

    def frames(self, action: str) -> list[pygame.Surface]:
        """Retourne les frames de l'animation demandée."""
        return self.animations[action]
