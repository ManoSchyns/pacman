from dataclasses import replace
from pathlib import Path
import pygame
from ghost.animations import Animation
from pacman.classes.movement import GridMovement
from .brain import ChaseContext, GhostBrain
from .ghost import Ghost

ROOT = Path(__file__).resolve().parents[2]

SHEET_PATH = (
    ROOT / "sprietsheet" / "dbc1ie6-95c45f24-9ea6-462e-88bd-15f1a3d6e051.png"
)


class GhostPlayer:

    def __init__(self, ghost_class: type[Ghost],
                 position: tuple[int, int], size: int,
                 movement: GridMovement | None = None,
                 brain: GhostBrain | None = None) -> None:
        self.ghost = ghost_class(str(SHEET_PATH))
        self.spawn_position = position
        self.movement = movement
        self.brain = brain

        self.animations = {
            action: Animation([
                pygame.transform.scale(frame, (size, size))
                for frame in self.ghost.frames(action)
            ])
            for action in self.ghost.actions()
        }

        if movement is not None:
            self.direction = movement.current_direction
        else:
            self.direction = "right"
        self.animation = self.animations[self.direction]

        self.rect = self.animation.current_frame().get_rect(center=position)

    def update(self, dt: float,
               context: ChaseContext | None = None) -> None:
        if (self.movement is None or self.brain is None
                or context is None):
            self.animation.update(dt)
            return

        own_context = replace(context, ghost_cell=self.movement.cell())
        target_cell = self.brain.target(own_context)
        if self.movement.at_decision_point() or not self.movement.moving:
            choice = self.brain.choose(
                self.movement.cell(),
                self.movement.current_direction,
                self.movement.is_open,
                target_cell,
                force=not self.movement.moving)
            if choice is not None:
                self.movement.request(choice)

        previous = self.movement.current_direction
        self.rect.center = self.movement.update(dt)

        if self.movement.current_direction != previous:
            self.direction = self.movement.current_direction
            self.animation = self.animations[self.direction]
            self.animation.reset()
        self.animation.update(dt)

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(
            self.animation.current_frame(),
            self.rect
        )
