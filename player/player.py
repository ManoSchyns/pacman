class Player:
    """Représente le joueur avec son nom, son score et ses vies."""

    def __init__(self, lives: int) -> None:
        """Initialise le joueur sans nom, avec un score nul."""
        self.name: str | None = None
        self.score = 0
        self.lives = lives

    def get_lives(self) -> int:
        """Retourne le nombre de vies restantes."""
        return self.lives

    def lose_lives(self) -> None:
        """Retire une vie au joueur."""
        self.lives -= 1

    def increase_score(self, score: int) -> None:
        """Ajoute les points indiqués au score du joueur."""
        self.score += score

    def get_score(self) -> int:
        """Retourne le score actuel du joueur."""
        return self.score

    def show(self) -> None:
        """Affiche le score et les vies du joueur."""
        print(f"Player has score {self.score} and lives: {self.lives}")

    def verify_name(self) -> tuple[bool, str]:
        """Vérifie que le nom du joueur respecte les contraintes.

        Returns:
            Un tuple (validité du nom, message d'erreur associé).
        """

        def is_valid() -> bool:
            """Indique si le nom est alphanumérique ou espace."""
            if self.name is None:
                return False
            return all(caract.isalnum() or caract.isspace()
                       for caract in self.name)

        if self.name is None:
            return (False,
                    "The name must contain between 1 and 10 characters.")
        if not is_valid():
            return (False,
                    "The name must consist of "
                    "alphanumeric characters or spaces.")
        if len(self.name) < 1 or len(self.name) > 10:
            return (False,
                    "The name must contain between 1 and 10 characters.")
        return (True, "All good")
