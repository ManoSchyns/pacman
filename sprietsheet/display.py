import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import pygame  # noqa: E402
from sprietsheet.classes.spritesheet import SpriteSheet  # noqa: E402

WINDOW_WIDTH = 1240
PADDING = 10
SCALE = 3
BAR_HEIGHT = 30
BACKGROUND = (25, 25, 35)
BAR_COLOR = (15, 15, 22)
HIGHLIGHT = (255, 220, 0)
TEXT_COLOR = (230, 230, 230)
DEFAULT_SHEET = (
    Path(__file__).resolve().parent
    / "dbc1ie6-95c45f24-9ea6-462e-88bd-15f1a3d6e051.png"
)

Placed = tuple[pygame.Rect, pygame.Rect, pygame.Surface]


def layout_sprites(
    sprites: list[tuple[pygame.Rect, pygame.Surface]], width: int
) -> tuple[list[Placed], int]:
    """Répartit les sprites en lignes dans la largeur disponible.

    Args:
        sprites: couples (rectangle, image) à afficher.
        width: largeur maximale d'une ligne.

    Returns:
        les sprites placés et la hauteur totale du contenu.
    """
    placed: list[Placed] = []
    x, y = PADDING, PADDING
    row_height = 0
    for rect, image in sprites:
        w = rect.width * SCALE
        h = rect.height * SCALE
        if x + w + PADDING > width:
            x = PADDING
            y += row_height + PADDING
            row_height = 0
        area = pygame.Rect(x, y, w, h)
        placed.append((area, rect, SpriteSheet.scale(image, SCALE)))
        x += w + PADDING
        row_height = max(row_height, h)
    return placed, y + row_height + PADDING


def draw(
    screen: pygame.Surface, placed: list[Placed], font: pygame.font.Font
) -> None:
    """Dessine les sprites et la barre d'infos du sprite survolé."""
    screen.fill(BACKGROUND)
    mouse = pygame.mouse.get_pos()
    hovered: tuple[int, pygame.Rect] | None = None
    for index, (area, rect, image) in enumerate(placed):
        screen.blit(image, area)
        if area.collidepoint(mouse):
            hovered = (index, rect)
            pygame.draw.rect(screen, HIGHLIGHT, area.inflate(6, 6), 1)
    bar = pygame.Rect(
        0, screen.get_height() - BAR_HEIGHT, screen.get_width(), BAR_HEIGHT
    )
    pygame.draw.rect(screen, BAR_COLOR, bar)
    if hovered is not None:
        index, rect = hovered
        text = (
            f"sprite {index}   x={rect.x} y={rect.y}"
            f" w={rect.width} h={rect.height}"
        )
    else:
        text = f"{len(placed)} sprites - survole un sprite pour ses infos"
    label = font.render(text, True, TEXT_COLOR)
    screen.blit(label, (PADDING, bar.y + 8))


def main() -> None:
    """Lance la visionneuse de planche de sprites."""
    path = sys.argv[1] if len(sys.argv) > 1 else str(DEFAULT_SHEET)
    pygame.init()
    pygame.display.set_mode((1, 1), pygame.HIDDEN)
    sheet = SpriteSheet(path)
    placed, content_height = layout_sprites(sheet.auto_slice(), WINDOW_WIDTH)
    screen = pygame.display.set_mode(
        (WINDOW_WIDTH, content_height + BAR_HEIGHT)
    )
    pygame.display.set_caption(f"Spritesheet viewer - {len(placed)} sprites")
    font = pygame.font.Font(None, 22)
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        draw(screen, placed, font)
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


if __name__ == "__main__":
    main()
