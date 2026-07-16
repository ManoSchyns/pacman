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
    
    def verify_name(self) -> tuple[bool, str]:

        def is_valid() -> bool:
            return all(caract.isalnum() or caract.isspace() for caract in self.name)

        if self.name is None:
            return (False, "The name must contain between 1 and 10 characters.")
        if not is_valid():
            return (False, "The name must consist of alphanumeric characters or spaces.")
        if len(self.name) < 1 or len(self.name) > 10:
            return (False, "The name must contain between 1 and 10 characters.")
        return (True, "All good")
