class Player:

    def __init__(self, lives: int) -> None:
        self.name: str | None = None
        self.score = 0
        self.lives = lives
    
    def get_lives(self):
        return self.lives
    
    def lose_lives(self):
        self.lives -= 1

    def increase_score(self, score):
        self.score += score
    
    def get_score(self):
        return self.score
    
    def show(self):
        print(f"Player has score {self.score} and lives: {self.lives}")