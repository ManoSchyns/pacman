import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "sprietsheet"))

import pygame

from animations.animation import Animation
from classes.ghost import Ghost
from classes.ghosts import Blinky, Clyde, Inky, Pinky

SHEET_PATH = (
    ROOT / "sprietsheet" / "dbc1ie6-95c45f24-9ea6-462e-88bd-15f1a3d6e051.png"
)
WINDOW_SIZE = (480, 420)
SCALE = 8
SECONDS_PER_DIRECTION = 2.0
BACKGROUND = (25, 25, 35)
BAR_COLOR = (15, 15, 22)
TEXT_COLOR = (230, 230, 230)
GHOST_COLORS = {
    "red": (255, 60, 60),
    "pink": (255, 184, 255),
    "cyan": (0, 255, 255),
    "orange": (255, 184, 82),
}


def build_animations(ghost: Ghost) -> dict[str, Animation]:
    return {
        direction: Animation(
            [
                pygame.transform.scale_by(frame, SCALE)
                for frame in ghost.frames(direction)
            ]
        )
        for direction in ghost.actions()
    }


def draw(
    screen: pygame.Surface,
    ghost: Ghost,
    animation: Animation,
    direction: str,
    font: pygame.font.Font,
) -> None:
    screen.fill(BACKGROUND)
    accent = GHOST_COLORS.get(ghost.COLOR, TEXT_COLOR)
    title = font.render(f"{ghost.name} ({ghost.COLOR})", True, accent)
    screen.blit(title, title.get_rect(center=(WINDOW_SIZE[0] // 2, 40)))
    label = font.render(direction.upper(), True, TEXT_COLOR)
    screen.blit(label, label.get_rect(center=(WINDOW_SIZE[0] // 2, 76)))
    frame = animation.current_frame()
    rect = frame.get_rect(
        center=(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2 + 10)
    )
    screen.blit(frame, rect)
    bar = pygame.Rect(0, WINDOW_SIZE[1] - 36, WINDOW_SIZE[0], 36)
    pygame.draw.rect(screen, BAR_COLOR, bar)
    info = font.render(
        f"frame {animation.frame_index + 1}/{len(animation.frames)}",
        True,
        TEXT_COLOR,
    )
    screen.blit(info, (12, bar.y + 9))


def main() -> None:
    pygame.init()
    pygame.display.set_mode((1, 1), pygame.HIDDEN)
    ghosts = [
        Blinky(str(SHEET_PATH)),
        Pinky(str(SHEET_PATH)),
        Inky(str(SHEET_PATH)),
        Clyde(str(SHEET_PATH)),
    ]
    animations = [build_animations(ghost) for ghost in ghosts]
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Ghost animations")
    font = pygame.font.Font(None, 32)
    clock = pygame.time.Clock()
    ghost_index = 0
    direction_index = 0
    timer = 0.0
    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        timer += dt
        if timer >= SECONDS_PER_DIRECTION:
            timer = 0.0
            direction_index += 1
            if direction_index >= len(ghosts[ghost_index].actions()):
                direction_index = 0
                ghost_index = (ghost_index + 1) % len(ghosts)
            current_ghost = ghosts[ghost_index]
            direction = current_ghost.actions()[direction_index]
            animations[ghost_index][direction].reset()
        ghost = ghosts[ghost_index]
        direction = ghost.actions()[direction_index]
        animation = animations[ghost_index][direction]
        animation.update(dt)
        draw(screen, ghost, animation, direction, font)
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()
