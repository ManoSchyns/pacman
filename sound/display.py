import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import pygame  # noqa: E402
from sound.effects import SEGMENTS, load_effects  # noqa: E402

WINDOW_SIZE = (620, 660)
BACKGROUND = (12, 12, 24)
PANEL = (22, 22, 40)
BAR_COLOR = (15, 15, 22)
TEXT_COLOR = (230, 230, 230)
GREY = (120, 120, 140)
YELLOW = (255, 222, 0)
CYAN = (0, 255, 255)
BLUE = (33, 33, 222)


def draw(screen: pygame.Surface, fonts: dict[str, pygame.font.Font],
         selected: int, playing: int) -> list[pygame.Rect]:
    screen.fill(BACKGROUND)
    title = fonts["title"].render("SOUND EFFECTS", True, YELLOW)
    screen.blit(title, title.get_rect(center=(WINDOW_SIZE[0] // 2, 34)))
    sub = fonts["small"].render(
        "FLECHES / CHIFFRES : choisir    ENTREE : jouer    ESC : quitter",
        True, GREY)
    screen.blit(sub, sub.get_rect(center=(WINDOW_SIZE[0] // 2, 62)))

    rects: list[pygame.Rect] = []
    top = 90
    row_h = 48
    for index, (start, end) in enumerate(SEGMENTS):
        rect = pygame.Rect(30, top + index * row_h, WINDOW_SIZE[0] - 60, 42)
        rects.append(rect)
        is_sel = index == selected
        is_play = index == playing
        pygame.draw.rect(screen, PANEL, rect, border_radius=8)
        if is_sel:
            pygame.draw.rect(screen, YELLOW, rect, 2, border_radius=8)
        if is_play:
            pygame.draw.rect(screen, CYAN, rect, 3, border_radius=8)

        num_color = CYAN if is_play else (YELLOW if is_sel else TEXT_COLOR)
        num = fonts["row"].render(f"#{index:02d}", True, num_color)
        screen.blit(num, (rect.x + 14, rect.centery - num.get_height() // 2))

        info = fonts["small"].render(
            f"{start:5.1f}s  ->  {end:5.1f}s     duree {end - start:.1f}s",
            True, GREY if not is_sel else TEXT_COLOR)
        screen.blit(info, (rect.x + 90,
                           rect.centery - info.get_height() // 2))
        if is_play:
            tag = fonts["small"].render("PLAY", True, CYAN)
            screen.blit(tag, tag.get_rect(
                midright=(rect.right - 16, rect.centery)))

    pygame.draw.rect(screen, BLUE,
                     pygame.Rect(6, 6, WINDOW_SIZE[0] - 12,
                                 WINDOW_SIZE[1] - 12), 2, border_radius=10)
    return rects


def main() -> None:
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Pacman sound effects")
    fonts = {
        "title": pygame.font.Font(None, 44),
        "row": pygame.font.Font(None, 32),
        "small": pygame.font.Font(None, 22),
    }
    sounds = load_effects()
    clock = pygame.time.Clock()
    selected = 0
    playing = -1
    rects: list[pygame.Rect] = []
    channel: pygame.mixer.Channel | None = None

    def play(index: int) -> None:
        nonlocal channel, playing
        if channel is not None:
            channel.stop()
        channel = sounds[index].play()
        playing = index

    running = True
    while running:
        clock.tick(60)
        if channel is not None and not channel.get_busy():
            playing = -1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    selected = (selected + 1) % len(sounds)
                elif event.key in (pygame.K_UP, pygame.K_w):
                    selected = (selected - 1) % len(sounds)
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    play(selected)
                elif pygame.K_0 <= event.key <= pygame.K_9:
                    index = event.key - pygame.K_0
                    if index < len(sounds):
                        selected = index
                        play(index)
            elif (event.type == pygame.MOUSEBUTTONDOWN
                  and event.button == 1):
                for index, rect in enumerate(rects):
                    if rect.collidepoint(event.pos):
                        selected = index
                        play(index)
        rects = draw(screen, fonts, selected, playing)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
