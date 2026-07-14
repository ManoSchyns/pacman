import pygame

from sprietsheet.classes.spritesheet import SpriteSheet


class Ghost:
    START_INDEX = 0
    COLOR = ""
    DIRECTION_ORDER = ["right", "left", "up", "down"]
    FRAMES_PER_DIRECTION = 2
    FRIGHTENED_INDICES = [32, 33]
    EATEN_INDICES = [34, 35]

    def __init__(self, sheet_path: str) -> None:
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
        return type(self).__name__

    def actions(self) -> list[str]:
        return list(self.animations)

    def frames(self, direction: str) -> list[pygame.Surface]:
        return self.animations[direction]
