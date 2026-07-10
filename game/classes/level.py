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
    def __init__(self, width: int, height: int, seed: int,
                 number_pacgum: int,
                 points_per_pacgum: int, points_per_super_pacgum: int,
                 points_per_ghost: int, level_max_time: int):
        self.maze = Maze(width, height, 30, seed)
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
    def play(self, screen, player) -> int:
        clock = pygame.time.Clock()

        screen.blit(self.maze_surface, (0, 0))

        pygame.display.flip()
        while (player.get_lives() > 0 and
               self.number_pacgum > 0 and self.number_super_pacgum > 0):

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

            screen.fill((0, 0, 0))
            screen.blit(self.maze.get_maze_surface(), (0, 0))
            self.pacman.draw(screen)
            self.show_information(screen, player)

            pygame.display.flip()
            clock.tick(60)

        if player.get_lives() == 0:
            # Animate death ??
            return 0
        return 1
    
    def show_information(self, screen, player):
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
        screen.blit(score_text, (0, y))
        screen.blit(lives_text, (100, y))
        screen.blit(time_text, (200, y))

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