import pygame
import random
from config import *


class Pipe():

    def __init__(self, game_display, x, y, pipe_type):
        self.game_display = game_display
        self.state = PIPE_MOVING
        self.pipe_type = pipe_type
        self.img = pygame.image.load(PIPE_FILE)
        self.shape = self.img.get_rect()

        if self.pipe_type == PIPE_UPPER:
            y = y - self.shape.height

        self.set_position(x, y)

    def set_position(self, x, y):
        self.shape.left = x
        self.shape.top = y

    def move_position(self, dx, dy):
        self.shape.centerx += dx
        self.shape.centery += dy

    def draw(self):
        self.game_display.blit(self.img, self.shape)

    def check_off_screen(self):
        if self.shape.right < 0:
            self.state = PIPE_DONE

    def update(self, dt):
        if self.state == PIPE_MOVING:
            self.move_position(-(PIPE_SPEED * dt), 0)
            self.draw()
            self.check_off_screen()


class PipeCollection():
    def __init__(self, game_display):
        self.game_display = game_display
        self.pipes = []

    def add_new_pipe_pair(self, x):
        top_y = random.randint(PIPE_MIN, PIPE_MAX)
        bottom_y = top_y + PIPE_GAP

        pipe_top = Pipe(self.game_display, x, top_y, PIPE_UPPER)
        pipe_bottom = Pipe(self.game_display, x, bottom_y, PIPE_LOWER)

        self.pipes.append(pipe_top)
        self.pipes.append(pipe_bottom)

    def init_game(self):
        self.pipes = []
        placed = PIPE_FIRST

        while placed < DISPLAY_W:
            self.add_new_pipe_pair(placed)
            placed += PIPE_PAIR_GAP

    def update(self, dt):
        last_pipe_pos = 0

        for pipe in self.pipes:
            pipe.update(dt)
            if pipe.pipe_type == PIPE_UPPER and pipe.shape.left > last_pipe_pos:
                last_pipe_pos = pipe.shape.left

        if last_pipe_pos < (DISPLAY_W - PIPE_PAIR_GAP):
            self.add_new_pipe_pair(DISPLAY_W)

        self.pipes = [p for p in self.pipes if p.state == PIPE_MOVING]
