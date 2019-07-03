from pygame.locals import *
import pygame
from Maze import Path
import time


class Maze:
    def __init__(self, grid):
        self.M = len(grid[0])
        self.N = len(grid)
        self.maze = grid

    def draw(self, display_surf, image_surf):
        for i in range(len(self.maze)):
            for j in range(len(self.maze[0])):
                if self.maze[i][j] == 1:
                    # display_surf.blit(image_surf, (i * 44, (self.N - j - 1) * 44))
                    display_surf.blit(image_surf, (i * 44, j * 44))

    def draw_path(self, display_surf, path_surf, path):
        for item in path:
            display_surf.blit(path_surf, (item['x']*44, item['y']*44))
            # self._display_surf.blit(self._image_surf, ((path[0]['x']) * 44, path[0]['y'] * 44))
            # self._display_surf.blit(self._end_surf, (path[-1]['x'] * 44, path[-1]['y'] * 44))
            # pygame.display.flip()
            # time.sleep(1)
            # display_surf.blit(path_surf, (item['x']*44, (self.N - item['y'] - 1)*44))


class App:
    windowWidth = 800
    windowHeight = 600
    player = 0

    def __init__(self, grid, search_method, src, dest, h_method):
        self._running = True
        self.done = False
        self._display_surf = None
        self._image_surf = None
        self._block_surf = None
        self._path_surf = None
        self._end_surf = None
        self.grid = grid
        self.M = len(grid[0])
        self.N = len(grid)
        self.maze = Maze(grid)
        self.search_method = search_method
        self.src = src
        self.dest = dest
        self.h_method = h_method

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.windowWidth, self.windowHeight), pygame.HWSURFACE)

        pygame.display.set_caption('AI MAZE')
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
        instance = Path(self.grid, self.h_method,self.search_method)
        path, length = instance.search(self.src, self.dest)
        self.maze.draw_path(self._display_surf, self._path_surf, path)
        # self._display_surf.blit(self._image_surf, ((path[0]['x'])*44, (self.N - path[0]['y']-1)*44))
        # self._display_surf.blit(self._end_surf, (path[-1]['x']*44, (self.N - path[-1]['y']-1)*44))
        self._display_surf.blit(self._image_surf, ((path[0]['x'])*44, path[0]['y']*44))
        self._display_surf.blit(self._end_surf, (path[-1]['x']*44, path[-1]['y']*44))

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

