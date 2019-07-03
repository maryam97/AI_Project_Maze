from pygame.locals import *
import pygame
from Maze import Path


class Player:

    def __init__(self, x, y):
        self.x = 44 * x
        self.y = 44 * y
        self.speed = 10

    def moveRight(self):
        self.x = self.x + self.speed

    def moveLeft(self):
        self.x = self.x - self.speed

    def moveUp(self):
        self.y = self.y - self.speed

    def moveDown(self):
        self.y = self.y + self.speed


class Maze:
    def __init__(self, grid):
        self.M = len(grid[0])
        self.N = len(grid)
        maze = []
        for row in grid:
            for column in row:
                maze.append(column)

        self.maze = maze

    def draw(self, display_surf, image_surf):
        bx = 0
        by = 0
        for i in range(0, self.M * self.N):
            if self.maze[bx + (by * self.M)] == 1:
                display_surf.blit(image_surf, (bx * 44, by * 44))

            bx = bx + 1
            if bx > self.M - 1:
                bx = 0
                by = by + 1

    def draw_path(self, display_surf, path_surf, path):
        for item in path:
            display_surf.blit(path_surf, (item['x']*44, (self.N-item['y']-1)*44))


class App:
    windowWidth = 800
    windowHeight = 600
    player = 0

    def __init__(self, grid):
        self._running = True
        self.done = False
        self._display_surf = None
        self._image_surf = None
        self._block_surf = None
        self._path_surf = None
        self._end_surf = None
        self.player = Player(8, 3)
        self.grid = grid
        self.M = len(grid[0])
        self.N = len(grid)
        self.maze = Maze(grid)

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.windowWidth, self.windowHeight), pygame.HWSURFACE)

        pygame.display.set_caption('Pygame pythonspot.com example')
        self._running = True
        self._image_surf = pygame.image.load("player.png").convert()
        self._block_surf = pygame.image.load("block.png").convert()
        self._path_surf = pygame.image.load("path.png").convert()
        self._end_surf = pygame.image.load("end.png").convert()

    def on_event(self, event):
        if event.type == QUIT:
            self._running = False

    def on_loop(self):
        pass

    def on_render(self):
        self._display_surf.fill((0, 0, 0))
        self.maze.draw(self._display_surf, self._block_surf)
        a_star = Path(self.grid, "Manhattan")
        path, length = a_star.a_star({'x': 1, 'y': 1}, {'x': 8, 'y': 7})
        self.maze.draw_path(self._display_surf, self._path_surf, path)
        self._display_surf.blit(self._image_surf, ((path[0]['x'])*44, (self.N - path[0]['y']-1)*44))
        self._display_surf.blit(self._end_surf, (path[-1]['x']*44, (self.N - path[-1]['y']-1)*44))
        pygame.display.flip()

    @staticmethod
    def on_cleanup():
        pygame.quit()

    def on_execute(self):

        if self.on_init() == False:
            self._running = False

        while self._running:
            pygame.event.pump()
            keys = pygame.key.get_pressed()

            if keys[K_ESCAPE]:
                self._running = False

            self.on_loop()
            self.on_render()
        self.on_cleanup()

