import pygame
from maze.classes import Maze
from pacman.classes import PacmanPlayer
from player import Player


class Level:

    """"
    Un level affiché sur une surface
    Quand on le lance, il faut le mettre sur le screen. On retire tout du sceen
    Et le level passe au premier plan

    Chaque level possede x pacgums qu'on prend depuis le fichier config
    Chaque level possede 4 super pacgums aux 4 coins
    Chaque levle a 4 ghost aux 4 coins
    """
    def __init__(self, width: int, height: int, screen: pygame.Surface,
                 seed: int, number_pacgum: int,
                 points_per_pacgum: int, points_per_super_pacgum: int,
                 points_per_ghost: int, level_max_time: int,
                 curr_level: int, last_level: int) -> None:
        self.screen = screen
        self.maze = Maze(width, height, screen, seed)
        self.maze_surface = self.maze.get_maze_surface()

        self.pacman = PacmanPlayer(self.maze.get_center_maze(),
                                   self.maze.get_pacman_size())

        self.number_pacgum = number_pacgum
        self.number_super_pacgum = 4

        self.points_per_pacgum = points_per_pacgum
        self.points_per_super_pacgum = points_per_super_pacgum
        self.points_per_ghost = points_per_ghost
        self.current_time = level_max_time

        self.start_time = pygame.time.get_ticks()

        self.curr_level = curr_level
        self.last_level = last_level

    """
    Return -1 si le screen doit etre quitté
    Return 0 si le player a perdu
    Return 1 si le lvl est gagné

    Touches:
     Les fleches / autres pour bouger
     espace -> Cheater mode. On passe en mode tricheur
     Appuyer sur espace = passer au niveau suivant
    """
    def play(self, player: Player) -> int:
        clock: pygame.time.Clock = pygame.time.Clock()

        if not self.waiting_screen(player):
            return -1
        while (player.get_lives() > 0 and
               self.number_pacgum > 0 and self.number_super_pacgum > 0
               and self.current_time - self.get_time_s() > 0):

            dt = clock.tick(60)/1000

            # touches clavier
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return -1
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return 1
                    if event.key == pygame.K_ESCAPE:
                        if not self.waiting_screen(player):
                            return -1

            self.pacman.handle_input()

            self.pacman.move(dt)
            if self.maze.check_collisions(self.pacman.rect):
                self.pacman.go_back()

            # if collision avec fantomes -> lives -= 1

            # if collision avec bouboules -> score ++

            # player.increase_score(10)
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.maze.get_maze_surface(), (0, 0))
            self.pacman.draw(self.screen)
            self.show_information(player)

            pygame.display.flip()

            clock.tick(60)

        if player.get_lives() == 0:
            # Animate death ??
            return 0
        if self.current_time - self.get_time_s() <= 0:
            # Animate end of time
            return 0
        return 1

    def waiting_screen(self, player: Player) -> bool:
        """
        Ecran d'attente. Tant que l'utilisateur
        n'appuie pas sur une touche, on attend
        """
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.maze_surface, (0, 0))
        self.pacman.draw(self.screen)
        self.show_information(player)

        font = pygame.font.SysFont(None, 20)

        overlay = pygame.Surface((self.screen.get_width(),
                                  self.screen.get_height()), pygame.SRCALPHA)
        overlay.fill((20, 20, 20, 180))  # RGB + Alpha

        rect = overlay.get_rect(center=self.screen.get_rect().center)
        self.screen.blit(overlay, rect)

        text = font.render("Press any key !", True, (255, 255, 255))
        text_rect = text.get_rect(center=self.maze_surface.get_rect().center)
        self.screen.blit(text, text_rect)

        pygame.display.flip()
        running: bool = True
        while (running):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    return True

        return False

    def show_information(self, player: Player) -> None:
        """
        Affiche les informations en bas du lab
        """
        font = pygame.font.SysFont(None, 20)

        y = self.maze.get_end_surface()

        def put_message(message: str, position: tuple[int, int]):
            """
            Nested fonction pour afficher un message a une
            position donnée
            """
            text = font.render(
                message,
                True,
                (255, 255, 255)
                )
            self.screen.blit(text, position)

        put_message(f"Level: {self.curr_level}/{self.last_level}",
                    (0, y))
        put_message(f"Score : {player.get_score()}",
                    (100, y))
        put_message(f"Lives : {player.get_lives()}",
                    (200, y))
        put_message(f"Time : {self.current_time - self.get_time_s()}",
                    (300, y))

    # return en seconde le temps écoulé depuis le début du niveau
    def get_time_s(self) -> int:
        elapsed_time: int = pygame.time.get_ticks() - self.start_time
        elapsed_time = elapsed_time // 1000
        return elapsed_time


if __name__ == "__main__":
    cell_size = 30
    width = 10
    height = 7

    # Scrren du jeu
    screen = pygame.display.set_mode((width * cell_size + 5,
                                      height * cell_size + 5))
    level = Level(width, height, 42, 10, 0, 0, 0, 100)
    player = Player(3)
    level.play(screen, player)
