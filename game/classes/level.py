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
    def __init__(self, width: int, height: int, screen, seed: int,
                 number_pacgum: int,
                 points_per_pacgum: int, points_per_super_pacgum: int,
                 points_per_ghost: int, level_max_time: int):
        self.screen = screen
        self.maze = Maze(width, height, screen,seed)
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
    
    """
    Return -1 si le screen doit etre quitté
    Return 0 si le player a perdu
    Return 1 si le lvl est gagné
    """
    def play(self, player) -> int:
        clock = pygame.time.Clock()


        if not self.waiting_screen(player):
            return -1
        while (player.get_lives() > 0 and
               self.number_pacgum > 0 and self.number_super_pacgum > 0
               and self.current_time - self.get_time_s()):

            dt = clock.tick(60)/1000

            # touches clavier
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return -1
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return 1

            self.pacman.handle_input()

            self.pacman.move(dt)
            if self.maze.check_collisions(self.pacman.rect):
                self.pacman.go_back()

            # if collision avec fantomes -> lives -= 1

            # if collision avec bouboules -> score ++

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
    
    def waiting_screen(self, player) -> bool:
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.maze_surface, (0, 0))
        self.pacman.draw(self.screen)
        self.show_information(player)

        font = pygame.font.SysFont(None, 20)

        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        overlay.fill((20, 20, 20, 180))  # RGB + Alpha

        rect = overlay.get_rect(center=self.screen.get_rect().center)
        self.screen.blit(overlay, rect)

        text = font.render("Press any key to start", True, (255, 255, 255))
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

    def show_information(self, player):
        font = pygame.font.SysFont(None, 20)

        y = self.maze.get_end_surface()

        score_text = font.render(
            f"Score : {player.get_score()}",
            True,
            (255, 255, 255)
        )

        lives_text = font.render(
            f"Lives : {player.get_lives()}",
            True,
            (255, 255, 255)
        )

        time_text = font.render(
            f"Time : {self.current_time - self.get_time_s()}",
            True,
            (255, 255, 255)
        )
        self.screen.blit(score_text, (0, y))
        self.screen.blit(lives_text, (100, y))
        self.screen.blit(time_text, (200, y))

    # return en seconde le temps écoulé depuis le début du niveau
    def get_time_s(self):
        elapsed_time = pygame.time.get_ticks() - self.start_time
        elapsed_time = elapsed_time // 1000
        return elapsed_time

if __name__ == "__main__":
    cell_size = 30
    width = 10
    height = 7

    # Scrren du jeu
    screen = pygame.display.set_mode((width * cell_size + 5,
                                      height * cell_size + 5))
    level = Level(width, height, 42, 10, 0, 0 ,0 ,100)
    player = Player(3)
    level.play(screen, player)