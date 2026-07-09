import pygame

from classes.spritesheet import SpriteSheet


class Pacman:
    DEATH_INDICES = list(range(13))
    LEFT_INDICES = [14, 13]
    UP_INDICES = [19, 20]
    DOWN_INDICES = [21, 22]
    MERGED_DEATH_FRAME = 4

    def __init__(self, sheet_path: str) -> None:
        sheet = SpriteSheet(sheet_path)
        sprites = [image for _, image in sheet.auto_slice()]
        left = [sprites[i] for i in self.LEFT_INDICES]
        right = [
            pygame.transform.flip(frame, True, False) for frame in left
        ]
        up = [sprites[i] for i in self.UP_INDICES]
        down = [sprites[i] for i in self.DOWN_INDICES]
        death = [sprites[i] for i in self.DEATH_INDICES]
        death[self.MERGED_DEATH_FRAME:self.MERGED_DEATH_FRAME + 1] = (
            self._split_merged_frame(death[self.MERGED_DEATH_FRAME])
        )
        self.animations: dict[str, list[pygame.Surface]] = {
            "left": left,
            "right": right,
            "up": up,
            "down": down,
            "death": death,
        }

    def actions(self) -> list[str]:
        return list(self.animations)

    def frames(self, action: str) -> list[pygame.Surface]:
        return self.animations[action]

    @staticmethod
    def _split_merged_frame(
        image: pygame.Surface,
    ) -> list[pygame.Surface]:
        width, height = image.get_size()
        half = width // 2
        return [
            image.subsurface((0, 0, half, height)).copy(),
            image.subsurface((half, 0, width - half, height)).copy(),
        ]
