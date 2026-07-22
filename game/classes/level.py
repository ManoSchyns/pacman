import pygame
import sys
import random
from ghost.classes import (AmbushBrain, Blinky, ChaseContext, Clyde,
                           CowardBrain, FlankBrain, GhostBrain, GhostPlayer,
                           Inky, Pinky)
from maze.classes import Maze
from pacman.classes import PacmanPlayer
from pacman.classes.movement import GridMovement
from player import Player
from pacgums.classes.gen_pacgums import GenPacgums
from sound.mixer import get_mixer
from .pause import PauseMenu

GHOST_BASE_SPEED = 3.0
BLINKY_SPEED_PER_LEVEL = 0.25
BLINKY_MAX_SPEED = 4.5
PINKY_SPEED_PER_LEVEL = 0.05
PINKY_MAX_SPEED = 4.2
PINKY_BASE_RANDOM_TURN = 0.25
PINKY_RANDOM_TURN_DROP_PER_LEVEL = 0.02
PINKY_MIN_RANDOM_TURN = 0.05

BASE_EDIBLE_COOLDOWN = 6
MAX_EDIBLE_COOLDOWN = 10
EDIBLE_COOLDOWN_PER_LEVEL = 0.2


class Level:
    """Un niveau du jeu affiché au premier plan sur une surface.

    Chaque niveau possède un labyrinthe, un nombre de pacgums issu du
    fichier de configuration, quatre super pacgums et quatre fantômes
    placés dans les coins.
    """

    def __init__(self, width: int, height: int, screen: pygame.Surface,
                 seed: int, number_pacgum: int,
                 points_per_pacgum: int, points_per_super_pacgum: int,
                 points_per_ghost: int, level_max_time: int,
                 curr_level: int, last_level: int) -> None:
        """Génère le labyrinthe, les pacgums, Pacman et les fantômes."""
        self.screen = screen

        try:
            self.maze = Maze(width, height, screen, seed)
        except Exception:
            print("Error during maze generation. "
                  "The provided package is non-functional.")
            sys.exit(1)

        self.maze_surface = self.maze.get_maze_surface()

        self.tmp_maze_surface = self.maze_surface
        self.cheater_mode: bool = False
        self.timer_cheater_mode: float = 0.0

        self.pacgums: GenPacgums = GenPacgums(number_pacgum, points_per_pacgum,
                                              points_per_super_pacgum,
                                              self.maze)
        self.pacgums.generate()

        self.pacman: PacmanPlayer | None = None
        self.reset_pacman()

        self.curr_level = curr_level
        self.last_level = last_level

        self.ghosts: list[GhostPlayer] = []
        self.reset_ghosts()

        self.points_per_ghost = points_per_ghost
        self.current_time = level_max_time

        self.mixer = get_mixer()

        self.start_time = pygame.time.get_ticks()
        self.pause_menu: PauseMenu | None = None

    def play(self, player: Player) -> int:
        """Déroule la boucle de jeu du niveau.

        Les flèches déplacent Pacman, espace passe au niveau suivant
        (mode tricheur) et échap met le jeu en pause.

        Args:
            player: joueur dont on suit le score et les vies.

        Returns:
            -2 si le joueur revient au menu depuis la pause, -1 si la
            fenêtre doit être quittée, 0 si le joueur a perdu, 1 si le
            niveau est gagné.
        """
        clock: pygame.time.Clock = pygame.time.Clock()

        if not self.waiting_screen(player):
            return -1

        if self.pacgums is None or self.pacman is None:
            return -1
        try:
            while (player.get_lives() > 0
                   and self.current_time - self.get_time_s() > 0
                   and self.pacgums.number_pacgums > 0):

                self.mixer.update_gameplay(self.ghost_sound_state())
                dt = clock.tick(60)/1000

                if self.cheater_mode:
                    self.maze_with_cheater_mode(dt)

                # touches clavier
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return -1
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE and self.cheater_mode:
                            return 1
                        if event.key == pygame.K_f and self.cheater_mode:
                            self.freeze_ghost()
                        if event.key == pygame.K_c:
                            self.cheater_mode = not self.cheater_mode
                        if event.key == pygame.K_ESCAPE:
                            action = self.open_pause_menu()
                            if action == "quit":
                                return -1
                            if action == "menu":
                                return -2

                self.pacman.handle_input()

                self.pacman.move(dt)

                self.try_eat(player)

                self.screen.fill((0, 0, 0))
                self.screen.blit(self.maze_surface, (0, 0))
                self.pacman.draw(self.screen)
                self.pacgums.show(self.screen, dt)

                pacman_cell = self.pacman.movement.cell()
                blinky_movement = self.ghosts[0].movement
                for ghost in self.ghosts:
                    context = ChaseContext(
                        ghost.is_edible(),
                        pacman_cell,
                        self.pacman.movement.current_direction,
                        blinky_movement.cell() if blinky_movement
                        else pacman_cell)

                    ghost.update(dt, context)
                    ghost.draw(self.screen)

                ret = self.check_col_with_ghost(player)
                if ret <= 0:
                    return ret

                self.show_information(player)

                pygame.display.flip()
            if (self.current_time - self.get_time_s() <= 0
                    or player.get_lives() == 0):
                return 0
            return 1
        finally:
            self.mixer.stop_gameplay()

    def open_pause_menu(self) -> str:
        """Met la partie en pause et retourne le choix du joueur.

        Les chronos du niveau et des fantômes sont décalés de la durée
        de la pause pour ne pas pénaliser le joueur.

        Returns:
            "resume", "menu" ou "quit".
        """
        if self.pacman is None:
            return "quit"
        self.mixer.stop_gameplay()
        if self.pause_menu is None:
            self.pause_menu = PauseMenu(self.screen,
                                        self.pacman.sprite.frames("right"))

        paused_at = pygame.time.get_ticks()
        action = self.pause_menu.run()
        paused_ms = pygame.time.get_ticks() - paused_at

        self.start_time += paused_ms
        for ghost in self.ghosts:
            ghost.start_edible_cooldown += paused_ms
            if ghost.movement is not None:
                ghost.movement.dead_cooldown_start += paused_ms
        return action

    def ghost_sound_state(self) -> str:
        """Retourne l'état sonore de fond des fantômes.

        Returns:
            "revive" pendant le retour au repaire, "frightened" quand
            les fantômes sont vulnérables, "siren" sinon.
        """
        if any(ghost.is_reviving() for ghost in self.ghosts):
            return "revive"
        if any(ghost.is_edible() for ghost in self.ghosts):
            return "frightened"
        return "siren"

    def check_col_with_ghost(self, player: Player) -> int:
        """Vérifie les collisions entre Pacman et les fantômes."""
        for ghost in self.ghosts:
            if ghost is None or self.pacman is None:
                return -1
            elif ghost.rect.colliderect(self.pacman.rect):
                ret = self.coll_with_ghost(player, ghost)
                if ret <= 0:
                    return ret
        return 1

    def coll_with_ghost(self, player: Player, ghost: GhostPlayer) -> int:
        """Gère une collision entre Pacman et un fantôme.

        Args:
            player: joueur qui perd une vie ou gagne des points.
            ghost: fantôme touché par Pacman.

        Returns:
            -1 si la fenêtre doit être quittée, 0 si le joueur n'a plus
            de vie, 1 sinon.
        """
        if ghost.movement is None:
            return -1
        if not ghost.is_edible() and ghost.movement.can_move():
            player.lose_lives()
            if not self.play_death_animation(player):
                return -1
            if player.get_lives() == 0:
                return 0
            self.reset_ghosts()
            self.reset_pacman()
            if not self.waiting_screen(player):
                return -1
        elif ghost.is_edible():
            player.increase_score(self.points_per_ghost)
            ghost.respawn()
            ghost.edible = False
            ghost.movement.speed = ghost.movement.normal_speed
        return 1

    def reset_pacman(self) -> None:
        """Replace Pacman au centre du labyrinthe."""
        cell_size = self.maze.get_cell_size()
        self.pacman = PacmanPlayer(self.maze.get_center_maze(),
                                   self.maze.get_pacman_size(),
                                   cell_size * 4, cell_size,
                                   self.maze.is_open)

    def reset_ghosts(self) -> None:
        """Recrée les quatre fantômes avec leur cerveau et leur vitesse.

        Les vitesses et l'agressivité augmentent avec le niveau courant.
        """
        cell_size = self.maze.get_cell_size()

        blinky_speed = cell_size * min(
            GHOST_BASE_SPEED + BLINKY_SPEED_PER_LEVEL * (self.curr_level - 1),
            BLINKY_MAX_SPEED)
        pinky_speed = cell_size * min(
            GHOST_BASE_SPEED + PINKY_SPEED_PER_LEVEL * (self.curr_level - 1),
            PINKY_MAX_SPEED)
        pinky_random_turn = max(
            PINKY_BASE_RANDOM_TURN
            - PINKY_RANDOM_TURN_DROP_PER_LEVEL * (self.curr_level - 1),
            PINKY_MIN_RANDOM_TURN)

        self.ghosts = []
        for ghost_class, spawn in zip([Blinky, Pinky, Inky, Clyde],
                                      self.maze.get_ghost_spawns()):
            movement = None
            brain: GhostBrain | None = None
            speed = 0.0
            if ghost_class is Blinky:
                brain = GhostBrain()
                speed = blinky_speed
            elif ghost_class is Pinky:
                brain = AmbushBrain(pinky_random_turn)
                speed = pinky_speed
            elif ghost_class is Inky:
                brain = FlankBrain()
                speed = blinky_speed
            elif ghost_class is Clyde:
                corner = (spawn[0] // cell_size, spawn[1] // cell_size)
                brain = CowardBrain(corner)
                speed = pinky_speed
            if brain is not None:
                movement = GridMovement(spawn, cell_size, speed,
                                        self.maze.is_open)
            self.ghosts.append(GhostPlayer(ghost_class, spawn,
                                           self.maze.get_pacman_size(),
                                           movement, brain))

    def try_eat(self, player: Player) -> None:
        """Fait manger un pacgum à Pacman et applique ses effets.

        Le score du joueur augmente et, si c'est un super pacgum, les
        fantômes deviennent vulnérables et ralentissent.
        """
        if self.pacman is None:
            return
        before = self.pacgums.number_pacgums
        data: tuple[int, bool] = self.pacgums.eat(self.pacman.rect)
        player.increase_score(data[0])
        if self.pacgums.number_pacgums < before:
            self.mixer.play_chomp()
        if data[1]:
            self.mixer.play_super()
            for ghost in self.ghosts:
                if ghost.movement is None:
                    return
                if ghost.movement.can_move():
                    ghost.edible = True
                    ghost.edible_cooldown = min(
                        MAX_EDIBLE_COOLDOWN,
                        (BASE_EDIBLE_COOLDOWN +
                         EDIBLE_COOLDOWN_PER_LEVEL *
                         (self.last_level -
                          self.curr_level)))
                    ghost.start_edible_cooldown = pygame.time.get_ticks()

                    ghost.movement.speed = (ghost.movement.normal_speed * 0.6)

    def play_death_animation(self, player: Player) -> bool:
        """Joue l'animation de mort de Pacman jusqu'à sa fin.

        Returns:
            False si la fenêtre a été fermée, True sinon.
        """
        if self.pacman is None:
            return False
        death = self.pacman.animations["death"]
        death.reset()
        self.mixer.play_death()
        clock: pygame.time.Clock = pygame.time.Clock()

        while not death.finished:
            dt = clock.tick(60) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
            death.update(dt)

            self.screen.fill((0, 0, 0))
            self.screen.blit(self.maze.get_maze_surface(), (0, 0))
            self.screen.blit(death.current_frame(), self.pacman.rect)
            self.show_information(player)
            pygame.display.flip()

        pygame.time.wait(500)
        return True

    def waiting_screen(self, player: Player) -> bool:
        """Affiche un écran d'attente jusqu'à l'appui d'une touche.

        Returns:
            False si la fenêtre a été fermée, True sinon.
        """
        if self.pacman is None:
            return False
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.maze_surface, (0, 0))
        self.pacman.draw(self.screen)
        for ghost in self.ghosts:
            ghost.draw(self.screen)
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
        """Affiche les informations de partie sous le labyrinthe."""
        font = pygame.font.SysFont(None, 20)

        y = self.maze.get_end_surface()

        def put_message(message: str, position: tuple[int, int]) -> None:
            """Affiche un message à une position donnée."""
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
        """Retourne le temps écoulé depuis le début du niveau."""
        elapsed_time: int = pygame.time.get_ticks() - self.start_time
        elapsed_time = elapsed_time // 1000
        return elapsed_time

    def freeze_ghost(self) -> None:
        """Permet de bloquer les fantomes sur
        place et desactive leurs collisions"""
        for ghost in self.ghosts:
            if ghost.movement is not None:
                if ghost.movement.dead_cooldown == 99999:
                    ghost.movement.dead_cooldown = 1
                else:
                    ghost.movement.dead_cooldown = 99999

    def maze_with_cheater_mode(self, dt: float) -> None:
        """Change les couleurs du labyrinthe aleatoirement
        lorsque le mode cheater est actif"""
        self.timer_cheater_mode += dt

        if self.timer_cheater_mode >= 1.0:
            self.timer_cheater_mode = 0.0
            r: int = random.randint(0, 255)
            g: int = random.randint(0, 255)
            b: int = random.randint(0, 255)
            self.maze._walls_color = (r, g, b)
            self.maze._gen_maze_surface()
            self.maze_surface = self.maze.get_maze_surface()
