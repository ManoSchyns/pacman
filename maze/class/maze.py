from mazegenerator import MazeGenerator
import pygame as pygame

class Maze:

	def __init__(self, width, height, cell_size):
		self._cell_size = cell_size
		self._width = width
		self._heigth = height
		self._epaisseur = 5
		self._walls_color = (255, 152, 0)
		self._42_color = (255,0,0)
		self._walls = []
		self._maze_gen = MazeGenerator(size=(width, height))
		self._maze = self._maze_gen.maze
		self._maze_surface = pygame.Surface((width * cell_size + self._epaisseur, height * cell_size + self._epaisseur ))
		self._gen_maze_surface()


	"""
	Dessine le labyrinthe sur une surface.
	Enregistre les collisions dans _walls
	"""
	def _gen_maze_surface(self):

		NORTH = 1
		EAST = 2
		SOUTH = 4
		WEST = 8

		for y in range (self._heigth):
			for x in range(self._width):
				row = y * self._cell_size
				col = x * self._cell_size
				if self._maze[y][x] == 15:
					pygame.draw.rect(self._maze_surface, self._42_color, (col, row, self._cell_size, self._cell_size))
				
				if self._maze[y][x] & NORTH:
					pygame.draw.line(self._maze_surface, self._walls_color, (col, row), (col + self._cell_size, row), self._epaisseur)
					self._walls.append( pygame.Rect(col, row - self._epaisseur // 2, self._cell_size, self._epaisseur))
				if self._maze[y][x] & EAST:
					pygame.draw.line(self._maze_surface, self._walls_color, (col + self._cell_size, row), (col + self._cell_size, row + self._cell_size), self._epaisseur)
					self._walls.append( pygame.Rect(col + self._cell_size - self._epaisseur // 2, row, self._epaisseur, self._cell_size))
				if y == self._heigth - 1 and self._maze[y][x] & SOUTH:
					pygame.draw.line(self._maze_surface, self._walls_color, (col, row + self._cell_size), (col + self._cell_size, row + self._cell_size), self._epaisseur)
					self._walls.append( pygame.Rect(col, row + self._cell_size - self._epaisseur // 2, self._cell_size, self._epaisseur))
				if x == 0 and self._maze[y][x] & WEST:
					pygame.draw.line(self._maze_surface, self._walls_color, (col, row), (col , row + self._cell_size), self._epaisseur)
					self._walls.append( pygame.Rect(col - self._epaisseur // 2, row, self._epaisseur, self._cell_size))

	# Return True si pacman est sur un mur -> collison
	# False si non
	def get_collisions(self, pacman_rect):
		for wall in self._walls:
			if pacman_rect.colliderect(wall):
				return True
		return False

	# Returne l'affichage du lab
	def get_maze_surface(self):
		return self._maze_surface

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
	width = 15
	height = 17
	screen = pygame.display.set_mode((width * cell_size + 5, height * cell_size + 5))
	clock = pygame.time.Clock()
	running = True
	

	maze = Maze(width, height, cell_size)
	screen.blit(maze.get_maze_surface(),(0,0))

	pygame.display.flip()
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
		pygame.display.flip()
		clock.tick(30)
	pygame.quit()