import pygame
from config import *
from pipe import PipeCollection
from bird import BirdCollection


def update_labels(data, title, font, x, y,  game_display):
    label = font.render('{} {}'.format(title, data), 1, DATA_FONT_COLOR)
    game_display.blit(label, (x, y))
    return y


def update_data_labels(dt, game_time, font, game_display, num_i, num_alive):
    y_poz = 10
    gap = 20
    x_poz = 10
    y_poz = update_labels(round(1000/dt, 2), 'FPS',
                          font, x_poz, y_poz + gap, game_display)
    y_poz = update_labels(round(game_time/1000, 2), 'Game Time',
                          font, x_poz, y_poz + gap, game_display)
    y_poz = update_labels(num_i, 'Iteration', font,
                          x_poz, y_poz + gap, game_display)
    y_poz = update_labels(num_alive, 'Alive', font,
                          x_poz, y_poz + gap, game_display)


def run_game():
    pygame.init()
    DISPLAY = pygame.display
    game_display = DISPLAY.set_mode((DISPLAY_W, DISPLAY_H))
    DISPLAY.set_caption('Learn to Fly')

    running = True
    bg_img = pygame.image.load(BG_FILE)
    label_font = pygame.font.SysFont("monospace", DATA_FONT_SIZE)

    clock = pygame.time.Clock()
    game_time = 0
    dt = 0
    num_i = 0

    pipes = PipeCollection(game_display)
    pipes.init_game()
    birds = BirdCollection(game_display)

    while running:

        dt = clock.tick(FPS)
        game_time += dt
        game_display.blit(bg_img, (0, 0))

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    running = False

        pipes.update(dt)
        num_alive = birds.update(dt, pipes.pipes)

        if num_alive == 0: # or (game_time > 10000):
            pipes.init_game()
            game_time = 0
            birds.evolve_population()
            num_i += 1

        update_data_labels(dt, game_time, label_font,
                           game_display, num_i, num_alive)
        DISPLAY.update()


if __name__ == "__main__":
    run_game()
