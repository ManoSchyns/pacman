import pygame
from maze.classes import Maze
from pacman.classes import PacmanPlayer

if __name__ == "__main__":

    pygame.init()

    """
    screen size:

    Pour la width du lab
    -> La width su screen = width * cell_size + epaisseur des walls
    Pour la heigth su lab
    -> la heigth du screen = height * cell_Size + epaisseur des walls
    """
    cell_size = 30
    width = 10
    height = 7

    # Scrren du jeu
    screen = pygame.display.set_mode((width * cell_size + 5,
                                      height * cell_size + 5))
    clock = pygame.time.Clock()
    running = True

    # Maze + récupération de sa surface
    maze = Maze(width, height, cell_size)
    screen.blit(maze.get_maze_surface(), (0, 0))
    maze_center = maze.get_center_maze()
    pacman = PacmanPlayer(maze_center, maze.get_pacman_size())

    pygame.display.flip()

    # mouvements du pacman
    pacman_move = (0, 1)
    while running:

        dt = clock.tick(60)/1000
        # touches clavier
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pacman.handle_input()

        pacman.move(dt)
        if maze.check_collisions(pacman.rect):
            pacman.go_back()
        # On supprime ce qu'il y a a l'ecran et on le remet
        screen.fill((0, 0, 0))
        screen.blit(maze.get_maze_surface(), (0, 0))
        pacman.draw(screen)
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
