from config import *
import pygame
import random
from nnet import Nnet
import numpy as np


class Bird():
    def __init__(self, game_display):
        self.game_display = game_display
        self.state = BIRD_ALIVE
        self.img = pygame.image.load(BIRD_FILE)
        self.shape = self.img.get_rect()
        self.speed = 0
        self.fitness = 0
        self.time_alive = 0
        self.nnet = Nnet(NNET_INPUTS, NNET_HIDDEN, NNET_OUTPUTS)
        self.set_position(BIRD_START_X, BIRD_START_Y)

    def reset(self):
        self.speed = 0
        self.time_alive = 0
        self.fitness = 0
        self.state = BIRD_ALIVE
        self.set_position(BIRD_START_X, BIRD_START_Y)

    def set_position(self, x, y):
        self.shape.centerx = x
        self.shape.centery = y

    def get_inputs(self, pipes):
        closest_pipe = DISPLAY_W*2
        bottom_y = 0
        for pipe in pipes:
            if pipe.pipe_type == PIPE_UPPER and pipe.shape.right < closest_pipe and pipe.shape.right > self.shape.left:
                closest_pipe = pipe.shape.right
                bottom_y = pipe.shape.bottom

        dx_pipe_bird = closest_pipe - self.shape.centerx
        dy_bird_pipegap = self.shape.centery - (bottom_y + PIPE_GAP / 2)
        inputs = [
            ((dx_pipe_bird / DISPLAY_W) * 0.99) + 0.01,
            (((dy_bird_pipegap * MIN_Y_DIFF) / NORMALIZE) * 0.99) + 0.01
        ]
        return inputs

    def move(self, dt):
        distance = 0
        new_speed = 0

        # s = ut + 1/2*at**2
        distance = (self.speed*dt) + 0.5 * GRAVITY * (dt ** 2)
        new_speed = self.speed + (GRAVITY * dt)

        self.shape.centery += distance
        self.speed = new_speed

        if self.shape.top < 0:
            self.shape.top = 0
            self.speed = 0

    def jump(self, pipes):
        inputs = self.get_inputs(pipes)
        if JUMP_CHANCE < self.nnet.get_max_value(inputs):
            self.speed = BIRD_START_SPEED

    def draw(self):
        self.game_display.blit(self.img, self.shape)

    def collision_fitness(self, pipe):
        gap_y = 0
        if pipe.pipe_type == PIPE_UPPER:
            gap_y = pipe.shape.bottom + PIPE_GAP / 2
        else:
            gap_y = pipe.shape.top - PIPE_GAP / 2

        self.fitness = -(abs(self.shape.centery - gap_y))

    def check_dead(self, pipes):
        if self.shape.bottom > DISPLAY_H:
            self.state = BIRD_DEAD
        else:
            for pipe in pipes:
                if pipe.shape.colliderect(self.shape):
                    self.state = BIRD_DEAD
                    self.collision_fitness(pipe)
                    break

    def update(self, dt, pipes):
        if self.state == BIRD_ALIVE:
            self.time_alive += dt
            self.move(dt)
            self.draw()
            self.jump(pipes)
            self.check_dead(pipes)

    def create_offspring(bird1, bird2, game_display):
        new_bird = Bird(game_display)
        new_bird.nnet.create_mixed_weights(bird1.nnet, bird2.nnet)
        return new_bird


class BirdCollection():
    def __init__(self, game_display):
        self.game_display = game_display
        self.birds = []
        self.create_new_generation()

    def create_new_generation(self):
        for i in range(0, GENERATION_SIZE):
            self.birds.append(Bird(self.game_display))

    def update(self, dt, pipes):
        num_alive = 0
        for bird in self.birds:
            bird.update(dt, pipes)
            if bird.state == BIRD_ALIVE:
                num_alive += 1
        return num_alive

    def evolve_population(self):

        for b in self.birds:
            b.fitness += b.time_alive * PIPE_SPEED

        self.birds.sort(key=lambda x: x.fitness, reverse=True)

        cut_off = int(len(self.birds) * MUTATION_CUT_OFF)
        print(cut_off)
        good_birds = self.birds[0:cut_off]
        bad_birds = self.birds[cut_off:]
        print('good_birds', good_birds)
        print('bad_birds', bad_birds)
        num_bad_to_take = int(len(self.birds) * MUTATION_BAD_TO_KEEP)

        for b in bad_birds:
            b.nnet.modify_weights()

        new_birds = []

        idx_bad_to_take = np.random.choice(
            np.arange(len(bad_birds)), num_bad_to_take, replace=False)

        for index in idx_bad_to_take:
            new_birds.append(bad_birds[index])

        new_birds.extend(good_birds)

        children_needed = len(self.birds) - len(new_birds)

        while len(new_birds) < len(self.birds):
            idx_to_breed = np.random.choice(np.arange(len(good_birds)), 2, replace=True)

            if idx_to_breed[0] != idx_to_breed[1]:
                new_bird = Bird.create_offspring(
                    good_birds[idx_to_breed[0]], good_birds[idx_to_breed[1]], self.game_display)
                if random.random() < MUTATION_MODIFY_CHANCE_LIMIT:
                    new_bird.nnet.modify_weights()
                new_birds.append(new_bird)

        for b in new_birds:
            b.reset();

        self.birds = new_birds
