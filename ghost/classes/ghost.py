import pygame

from sprietsheet.classes.spritesheet import SpriteSheet


class Ghost:
    """Fantôme générique qui découpe ses animations dans le spritesheet."""

    START_INDEX = 0
    COLOR = ""
    DIRECTION_ORDER = ["right", "left", "up", "down"]
    FRAMES_PER_DIRECTION = 2
    FRIGHTENED_INDICES = [32, 33]
    EATEN_INDICES = [34, 35]

    def __init__(self, sheet_path: str) -> None:
        """Charge le spritesheet et construit toutes les animations."""
        sheet = SpriteSheet(sheet_path)
        sprites = [image for _, image in sheet.auto_slice()]
        self.animations: dict[str, list[pygame.Surface]] = {}
        for pair, direction in enumerate(self.DIRECTION_ORDER):
            start = self.START_INDEX + pair * self.FRAMES_PER_DIRECTION
            self.animations[direction] = sprites[
                start:start + self.FRAMES_PER_DIRECTION
            ]
        frightened = [sprites[i] for i in self.FRIGHTENED_INDICES]
        eaten = [sprites[i] for i in self.EATEN_INDICES]
        self.animations["frightened"] = frightened
        self.animations["eaten"] = eaten
        self.animations["revive"] = [
            frightened[0],
            eaten[0],
            frightened[1],
            eaten[1],
        ]

    @property
    def name(self) -> str:
        """Retourne le nom de la classe du fantôme."""
        return type(self).__name__

    def actions(self) -> list[str]:
        """Retourne la liste des animations disponibles."""
        return list(self.animations)

    def frames(self, direction: str) -> list[pygame.Surface]:
        """Retourne les images de l'animation demandée."""
        return self.animations[direction]
