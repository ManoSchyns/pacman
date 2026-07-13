import pygame


class TextInput:
    def __init__(self, rect: pygame.Rect, screen: pygame.Surface):
        self.screen = screen
        self.text_input = pygame.Rect(rect)
        self.font = pygame.font.SysFont(None, 30)
        self.text = "Your name"
        self.active: bool = False
        self.first_active = True

    # Return false si on doit quitter le prog
    # Return True si non
    def handle_input(self, event: pygame.event.Event) -> bool:

        def check_col() -> bool:
            if self.text_input.collidepoint(event.pos):
                return True
            return False

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = check_col()
        while self.active:
            if self.first_active:
                self.first_active = False
                self.text = ""
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.active = check_col()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                    if event.key == pygame.K_RETURN:
                        self.active = False
                        if self.text == "":
                            self.text = "Your name"
                            self.first_active = True
                            self.draw()
                        return True
                    elif str.isprintable(event.unicode):
                        self.text += event.unicode
                self.draw()
        return True

    def draw(self) -> None:
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
        pygame.display.flip()

    def get_value(self) -> str:
        if self.text == "Your name":
            return ""
        return self.text
