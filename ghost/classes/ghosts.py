from .ghost import Ghost


class Blinky(Ghost):
    START_INDEX = 24
    COLOR = "red"


class Pinky(Ghost):
    START_INDEX = 36
    COLOR = "pink"


class Inky(Ghost):
    START_INDEX = 47
    COLOR = "cyan"


class Clyde(Ghost):
    START_INDEX = 58
    COLOR = "orange"
