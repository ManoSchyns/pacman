import array
from pathlib import Path

import pygame

ROOT = Path(__file__).resolve().parents[1]
SOUND_PATH = ROOT / "assets" / "Pacman Sound Effects.mp3"

# (début, fin) en secondes de chaque effet dans la compilation mp3.
SEGMENTS = [
    (1.51, 1.90),
    (3.86, 7.18),
    (9.60, 12.84),
    (14.60, 17.82),
    (19.40, 24.56),
    (26.48, 28.02),
    (31.14, 31.69),
    (33.80, 36.14),
    (37.40, 40.80),
    (42.82, 46.98),
    (48.64, 53.25),
]

MENU_MUSIC = 4
DEATH = 5
PACGUM = 0
SIREN = 1
SUPER_PACGUM = 6
WAKA = 10
FRIGHTENED = 8
REVIVE = 3
GAME_OVER = 9


def _ensure_mixer() -> None:
    """Initialise le mixeur pygame s'il ne l'est pas déjà."""
    if not pygame.mixer.get_init():
        pygame.mixer.init()


def _samples() -> tuple[array.array, int, int]:
    """Charge la compilation mp3 et retourne ses échantillons bruts.

    Returns:
        les échantillons 16 bits, la fréquence et le nombre de voies.
    """
    _ensure_mixer()
    full = pygame.mixer.Sound(str(SOUND_PATH))
    samples: array.array = array.array("h")
    samples.frombytes(full.get_raw())
    rate, _, channels = pygame.mixer.get_init()
    return samples, rate, channels


def load_effect(index: int, pad: float = 0.05) -> pygame.mixer.Sound:
    """Découpe un seul effet du mp3, prêt à jouer."""
    samples, rate, channels = _samples()
    start, end = SEGMENTS[index]
    frames = int(rate * pad)
    a = max(0, int(start * rate) - frames) * channels
    b = min(len(samples), (int(end * rate) + frames) * channels)
    chunk = array.array("h", samples[a:b])
    return pygame.mixer.Sound(buffer=chunk.tobytes())


def load_effects(pad: float = 0.05) -> list[pygame.mixer.Sound]:
    """Découpe tous les effets du mp3 (utilisé par le viewer)."""
    samples, rate, channels = _samples()
    frames = int(rate * pad)
    sounds = []
    for start, end in SEGMENTS:
        a = max(0, int(start * rate) - frames) * channels
        b = min(len(samples), (int(end * rate) + frames) * channels)
        chunk = array.array("h", samples[a:b])
        sounds.append(pygame.mixer.Sound(buffer=chunk.tobytes()))
    return sounds
