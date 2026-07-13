class Player:

    def __init__(self, lives: int) -> None:
        self.name: str | None = None
        self.score = 0
        self.lives = lives

    def get_lives(self) -> int:
        return self.lives

    def lose_lives(self) -> None:
        self.lives -= 1

    def increase_score(self, score: int) -> None:
        self.score += score

    def get_score(self) -> int:
        return self.score

    def show(self) -> None:
        print(f"Player has score {self.score} and lives: {self.lives}")
