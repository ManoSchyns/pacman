import pygame

from .bases import SpriteSheet as SpriteSheetBase


class SpriteSheet(SpriteSheetBase):
    """Planche de sprites capable de se découper toute seule."""

    def __init__(self, filename: str, bg_threshold: int = 40) -> None:
        """Charge la planche et retient le seuil de détection du fond."""
        super().__init__(filename)
        self.filename = filename
        self.bg_threshold = bg_threshold

    def is_background(self, color: pygame.Color) -> bool:
        """Indique si la couleur est assez sombre pour être du fond."""
        r: int = color.r
        g: int = color.g
        b: int = color.b

        return (
            r < self.bg_threshold
            and g < self.bg_threshold
            and b < self.bg_threshold
        )

    def sprite_at(
        self, rectangle: pygame.Rect | tuple[int, int, int, int]
    ) -> pygame.Surface:
        """Extrait le sprite du rectangle et rend son fond transparent."""
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size, pygame.SRCALPHA)
        image.blit(self.sheet, (0, 0), rect)
        for y in range(rect.height):
            for x in range(rect.width):
                if self.is_background(image.get_at((x, y))):
                    image.set_at((x, y), (0, 0, 0, 0))
        return image

    def sprites_at(
        self, rects: list[pygame.Rect] | list[tuple[int, int, int, int]]
    ) -> list[pygame.Surface]:
        """Retourne les sprites des rectangles donnés."""
        return [self.sprite_at(rect) for rect in rects]

    def grid_rects(self, columns: int, rows: int) -> list[pygame.Rect]:
        """Retourne les rectangles d'une grille régulière de sprites."""
        pitch_w = self.sheet.get_width() / columns
        pitch_h = self.sheet.get_height() / rows
        return [
            pygame.Rect(
                round(i * pitch_w),
                round(j * pitch_h),
                round(pitch_w),
                round(pitch_h),
            )
            for j in range(rows)
            for i in range(columns)
        ]

    def load_grid(self, columns: int, rows: int) -> list[pygame.Surface]:
        """Découpe la planche selon une grille de colonnes et lignes."""
        return self.sprites_at(self.grid_rects(columns, rows))

    def find_sprite_rects(self, min_pixels: int = 4) -> list[pygame.Rect]:
        """Détecte le rectangle de chaque sprite de la planche.

        Args:
            min_pixels: taille minimale d'une composante connexe.

        Returns:
            les rectangles fusionnés, découpés et triés en ordre de
            lecture.
        """
        threshold = (self.bg_threshold,) * 3 + (255,)
        mask = pygame.mask.from_threshold(
            self.sheet, (0, 0, 0, 255), threshold
        )
        mask.invert()
        rects = []
        for component in mask.connected_components(min_pixels):
            bounds = component.get_bounding_rects()
            rect = bounds[0]
            for extra in bounds[1:]:
                rect = rect.union(extra)
            rects.append(rect)
        merged = self._merge_overlapping(rects)
        return self._sort_reading_order(self._split_wide_rects(merged))

    def auto_slice(
        self, min_pixels: int = 4
    ) -> list[tuple[pygame.Rect, pygame.Surface]]:
        """Retourne chaque sprite détecté avec son rectangle d'origine."""
        rects = self.find_sprite_rects(min_pixels)
        return [(rect, self.sprite_at(rect)) for rect in rects]

    @staticmethod
    def scale(image: pygame.Surface, factor: float) -> pygame.Surface:
        """Retourne l'image redimensionnée par le facteur donné."""
        return pygame.transform.scale_by(image, factor)

    def _split_wide_rects(
        self, rects: list[pygame.Rect]
    ) -> list[pygame.Rect]:
        """Découpe les rectangles anormalement larges pour leur ligne."""
        if not rects:
            return rects
        widths = sorted(rect.width for rect in rects)
        heights = sorted(rect.height for rect in rects)
        median_width = widths[len(widths) // 2]
        median_height = heights[len(heights) // 2]

        result: list[pygame.Rect] = []
        for rect in rects:
            if (rect.width >= 1.8 * median_width
                    and rect.height <= 1.5 * median_height):
                result.extend(self._split_at_seam(rect))
            else:
                result.append(rect)
        return result

    def _split_at_seam(self, rect: pygame.Rect) -> list[pygame.Rect]:
        """Coupe le rectangle sur sa colonne la plus vide, si possible."""
        third = rect.width // 3
        candidates = range(rect.x + third, rect.x + rect.width - third)
        seam = min(candidates,
                   key=lambda column: self._column_fill(rect, column))
        if self._column_fill(rect, seam) > 2:
            return [rect]
        left = pygame.Rect(rect.x, rect.y, seam - rect.x, rect.height)
        right = pygame.Rect(seam + 1, rect.y,
                            rect.right - seam - 1, rect.height)
        return [left, right]

    def _column_fill(self, rect: pygame.Rect, column: int) -> int:
        """Compte les pixels non vides d'une colonne du rectangle."""
        count = 0
        for y in range(rect.y, rect.y + rect.height):
            if not self.is_background(self.sheet.get_at((column, y))):
                count += 1
        return count

    @staticmethod
    def _merge_overlapping(rects: list[pygame.Rect]) -> list[pygame.Rect]:
        """Fusionne les rectangles qui se chevauchent."""
        merged = True
        while merged:
            merged = False
            result: list[pygame.Rect] = []
            for rect in rects:
                for i, other in enumerate(result):
                    if rect.colliderect(other):
                        result[i] = other.union(rect)
                        merged = True
                        break
                else:
                    result.append(rect)
            rects = result
        return rects

    @staticmethod
    def _sort_reading_order(
        rects: list[pygame.Rect], row_tolerance: int = 8
    ) -> list[pygame.Rect]:
        """Trie les rectangles ligne par ligne, de gauche à droite."""
        ordered: list[pygame.Rect] = []
        remaining = sorted(rects, key=lambda r: int(r.top))
        while remaining:
            row_top = remaining[0].top
            row = [r for r in remaining if r.top - row_top < row_tolerance]
            remaining = remaining[len(row):]
            ordered.extend(sorted(row, key=lambda r: int(r.left)))
        return ordered
