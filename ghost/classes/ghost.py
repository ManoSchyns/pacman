import pygame

from classes.spritesheet import SpriteSheet


class Ghost:
    START_INDEX = 0
    COLOR = ""
    DIRECTION_ORDER = ["right", "left", "up", "down"]
    FRAMES_PER_DIRECTION = 2
    DEAD_INDICES = [31, 32]
    WHITE_INDICES = [33, 34]

    def __init__(self, sheet_path: str) -> None:
        sheet = SpriteSheet(sheet_path)
        sprites = [image for _, image in sheet.auto_slice()]
        self.animations: dict[str, list[pygame.Surface]] = {}
        for pair, direction in enumerate(self.DIRECTION_ORDER):
            start = self.START_INDEX + pair * self.FRAMES_PER_DIRECTION
            self.animations[direction] = sprites[
                start:start + self.FRAMES_PER_DIRECTION
            ]
        dead = [sprites[i] for i in self.DEAD_INDICES]
        white = [sprites[i] for i in self.WHITE_INDICES]
        self.animations["dead"] = dead
        self.animations["revive"] = [
            dead[0],
            white[0],
            dead[1],
            white[1],
        ]

    @property
    def name(self) -> str:
        return type(self).__name__

    def actions(self) -> list[str]:
        return list(self.animations)

    def frames(self, direction: str) -> list[pygame.Surface]:
        return self.animations[direction]
