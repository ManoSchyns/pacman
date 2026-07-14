from collections.abc import Callable

DIRECTIONS: dict[str, tuple[int, int]] = {
    "right": (1, 0),
    "left": (-1, 0),
    "up": (0, -1),
    "down": (0, 1),
}

OPPOSITES: dict[str, str] = {
    "right": "left",
    "left": "right",
    "up": "down",
    "down": "up",
}

TURN_TOLERANCE_RATIO = 0.25
EPS = 1e-6


class GridMovement:

    def __init__(self, position: tuple[int, int], cell_size: int,
                 speed: float,
                 is_open: Callable[[tuple[int, int], str], bool],
                 direction: str = "down") -> None:
        self.x = float(position[0])
        self.y = float(position[1])
        self.cell_size = cell_size
        self.speed = speed
        self.is_open = is_open
        self.tolerance = cell_size * TURN_TOLERANCE_RATIO
        self.current_direction = direction
        self.wanted_direction = direction
        self.moving = True

    def request(self, direction: str) -> None:
        self.wanted_direction = direction

    def position(self) -> tuple[int, int]:
        return (round(self.x), round(self.y))

    def cell(self) -> tuple[int, int]:
        return (int(self.x // self.cell_size),
                int(self.y // self.cell_size))

    def at_decision_point(self) -> bool:
        center = self._center(self.cell())
        return (abs(center[0] - self.x) <= self.tolerance
                and abs(center[1] - self.y) <= self.tolerance)

    def update(self, dt: float) -> tuple[int, int]:
        dt = min(dt, 1 / 30)
        self._try_turn()
        if self.moving:
            self._advance(self.speed * dt)
        return self.position()

    def _try_turn(self) -> None:
        wanted = self.wanted_direction
        current = self.current_direction
        if wanted == current:
            return

        if not self.moving:
            if self.is_open(self.cell(), wanted):
                self.current_direction = wanted
                self.moving = True
            return

        if wanted == OPPOSITES[current]:
            self.current_direction = wanted
            return

        cell = self.cell()
        center = self._center(cell)
        if (abs(self._signed_distance(center, current)) <= self.tolerance
                and self.is_open(cell, wanted)):
            self.x, self.y = center
            self.current_direction = wanted

    def _advance(self, step: float) -> None:
        remaining = step
        while remaining > EPS:
            cell = self.cell()
            center = self._center(cell)
            distance = self._signed_distance(center, self.current_direction)

            if distance > EPS:
                travel = min(remaining, distance)
                self._move(travel)
                remaining -= travel
                if remaining > EPS and not self.is_open(
                        cell, self.current_direction):
                    self.x, self.y = center
                    self.moving = False
                    return
            else:
                if not self.is_open(cell, self.current_direction):
                    self.x, self.y = center
                    self.moving = False
                    return
                travel = min(remaining, self.cell_size + distance)
                self._move(travel)
                remaining -= travel

    def _move(self, distance: float) -> None:
        offset_x, offset_y = DIRECTIONS[self.current_direction]
        self.x += offset_x * distance
        self.y += offset_y * distance

    def _center(self, cell: tuple[int, int]) -> tuple[float, float]:
        return (cell[0] * self.cell_size + self.cell_size / 2,
                cell[1] * self.cell_size + self.cell_size / 2)

    def _signed_distance(self, target: tuple[float, float],
                         direction: str) -> float:
        offset_x, offset_y = DIRECTIONS[direction]
        return ((target[0] - self.x) * offset_x
                + (target[1] - self.y) * offset_y)
