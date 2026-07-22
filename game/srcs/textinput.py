import pygame


class TextInput:
    """Champ de saisie de texte affiché sur une surface pygame."""

    def __init__(self, rect: pygame.Rect | tuple[int, int, int, int],
                 screen: pygame.Surface):
        """Initialise le champ de saisie avec sa zone et sa police."""
        self.screen = screen
        self.text_input = pygame.Rect(rect)
        self.font = pygame.font.SysFont(None, 30)
        self.text = "Your name"
        self.active: bool = False
        self.first_active = True

    def handle_input(self, event: pygame.event.Event) -> int:
        """Met à jour le texte saisi à partir d'un évènement pygame.

        Args:
            event: évènement clavier ou souris à traiter.

        Returns:
            1 si le texte a été changé, -1 si sortie, 0 sinon.
        """

        def check_col() -> bool:
            """Retourne True si le clic est dans la zone de saisie."""
            if self.text_input.collidepoint(event.pos):
                return True
            return False

        change: int = 0
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = check_col()
        if self.first_active:
            self.first_active = False
            self.text = ""
        if self.active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                    change = 1
                elif str.isprintable(event.unicode):
                    change = 1
                    self.text += event.unicode
        if self.text == "":
            self.text = "Your name"
            self.first_active = True
        return change

    def draw(self) -> None:
        """Dessine le champ de saisie et son texte à l'écran."""
        pygame.draw.rect(
            self.screen,
            (255, 255, 255),
            self.text_input,
            border_radius=10
        )
        pygame.draw.rect(
            self.screen,
            (255, 255, 255),
            self.text_input,
            2,
            border_radius=10
        )

        text = self.font.render(
            self.text,
            True,
            (100, 100, 100)
            )

        # Centrer le texte dans le rectangle
        text_rect = text.get_rect(
             midleft=(
                 self.text_input.x + 10,
                 self.text_input.centery
                 ))
        self.screen.blit(text, text_rect)

    def get_value(self) -> str:
        """Retourne le texte saisi, ou une chaîne vide si aucun."""
        if self.text == "Your name":
            return ""
        return self.text
