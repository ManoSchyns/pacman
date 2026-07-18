import pygame


class Animation:
    """Anime une liste de frames a cadence fixe, avec ou sans boucle."""

    def __init__(
        self,
        frames: list[pygame.Surface],
        frame_duration: float = 0.12,
        loop: bool = True,
    ) -> None:
        self.frames = frames
        self.frame_duration = frame_duration
        self.loop = loop
        self.elapsed = 0.0
        self.finished = False

    def reset(self) -> None:
        self.elapsed = 0.0
        self.finished = False

    def update(self, dt: float) -> None:
        if self.finished:
            return
        self.elapsed += dt
        if not self.loop and self.frame_index >= len(self.frames) - 1:
            self.finished = True

    @property
    def frame_index(self) -> int:
        index = int(self.elapsed / self.frame_duration)
        if self.loop:
            return index % len(self.frames)
        return min(index, len(self.frames) - 1)

    def current_frame(self) -> pygame.Surface:
        return self.frames[self.frame_index]
