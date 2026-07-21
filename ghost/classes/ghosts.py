from .ghost import Ghost


class Blinky(Ghost):
    """Fantôme rouge dont les sprites commencent à l'index 24."""

    START_INDEX = 24
    COLOR = "red"


class Pinky(Ghost):
    """Fantôme rose dont les sprites commencent à l'index 36."""

    START_INDEX = 36
    COLOR = "pink"


class Inky(Ghost):
    """Fantôme cyan dont les sprites commencent à l'index 47."""

    START_INDEX = 47
    COLOR = "cyan"


class Clyde(Ghost):
    """Fantôme orange dont les sprites commencent à l'index 58."""

    START_INDEX = 58
    COLOR = "orange"
