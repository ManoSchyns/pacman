import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import pygame  # noqa: E402
from animation import Animation  # noqa: E402
from pacman.classes import Pacman  # noqa: E402

SHEET_PATH = (
    ROOT / "sprietsheet" / "dbc1ie6-95c45f24-9ea6-462e-88bd-15f1a3d6e051.png"
)
WINDOW_SIZE = (480, 420)
BASE_SIZE = 16
SCALE = 8
SECONDS_PER_ACTION = 3.0
BACKGROUND = (25, 25, 35)
BAR_COLOR = (15, 15, 22)
TEXT_COLOR = (230, 230, 230)
ACCENT = (255, 220, 0)


def build_animations(pacman: Pacman) -> dict[str, Animation]:
    return {
        action: Animation(
            [
                pygame.transform.scale_by(frame, SCALE)
                for frame in pacman.frames(action)
            ]
        )
        for action in pacman.actions()
    }


def draw(
    screen: pygame.Surface,
    animation: Animation,
    action: str,
    font: pygame.font.Font,
) -> None:
    screen.fill(BACKGROUND)
    frame = animation.current_frame()
    rect = frame.get_rect(
        center=(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2 - 20)
    )
    screen.blit(frame, rect)
    title = font.render(action.upper(), True, ACCENT)
    screen.blit(title, title.get_rect(center=(WINDOW_SIZE[0] // 2, 40)))
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
    pacman = Pacman(str(SHEET_PATH), BASE_SIZE)
    animations = build_animations(pacman)
    actions = pacman.actions()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Pacman animations")
    font = pygame.font.Font(None, 32)
    clock = pygame.time.Clock()
    current = 0
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
        if timer >= SECONDS_PER_ACTION:
            timer = 0.0
            current = (current + 1) % len(actions)
            animations[actions[current]].reset()
        animation = animations[actions[current]]
        animation.update(dt)
        draw(screen, animation, actions[current], font)
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()
