DISPLAY_H = 540
DISPLAY_W = 960
FPS = 31

DATA_FONT_SIZE = 18
DATA_FONT_COLOR = (40, 40, 40)

# files
BG_FILE = './assets/BG.png'
PIPE_FILE = './assets/Pipe.png'
BIRD_FILE = './assets/Bird.png'

# pipe
PIPE_SPEED = 70/1000
PIPE_DONE = 'DONE'
PIPE_MOVING = 'MOVING'
PIPE_UPPER = 'UPPER'
PIPE_LOWER = 'LOWER'
PIPE_GAP = 160
# The top pipes max and min end position
PIPE_MIN = 80
PIPE_MAX = 340
PIPE_START_X = DISPLAY_W
PIPE_FIRST = 400
# distance between pairs of pipes
PIPE_PAIR_GAP = 160

# Birdie
BIRD_START_SPEED = -0.32
BIRD_START_X = 200
BIRD_START_Y = 200
BIRD_ALIVE = 'ALIVE'
BIRD_DEAD = 'DEAD'
GRAVITY = 0.001


# ML
GENERATION_SIZE = 4
NNET_INPUTS = 2
NNET_HIDDEN = 5
NNET_OUTPUTS = 1
JUMP_CHANCE = 0.5
# NORMALIZE
MAX_Y_DIFF = DISPLAY_H - PIPE_MIN - PIPE_GAP/2
MIN_Y_DIFF = abs(PIPE_GAP/2 - PIPE_MAX)
NORMALIZE = MAX_Y_DIFF - MIN_Y_DIFF


MUTATION_WEIGHT_MODIFY_CHANCE = 0.25
MUTATION_ARRAY_MIX_PEC = 0.5

MUTATION_CUT_OFF = 0.5
MUTATION_BAD_TO_KEEP = 0.5
MUTATION_MODIFY_CHANCE_LIMIT = 0.5