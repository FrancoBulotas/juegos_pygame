import random
import pygame
from pygame.locals import *
from math import prod

# Constants
NUMBER_OF_LAYERS = 5
STARS_PER_LAYER = (10, 30, 40, 25, 15)
NUM_STARS = sum(STARS_PER_LAYER)
temp = 0
# assignment expressions (walrus operator :=) requires Python >= 3.8
STAR_RANGES = (0, *(temp := temp + v for v in STARS_PER_LAYER))
LAYER_SPEED_DIVISORS = (1, 2, 4, 8, 16)
SCREEN_SIZE = [640, 480]
WHITE = 255, 255, 255
BLACK = 20, 20, 40
LIGHTGRAY = 180, 180, 180
DARKGRAY = 120, 120, 120
BLUE_SHIFTED = 140, 140, 255
RED_SHIFTED = 200, 40, 40
# colors can be repeated
LAYER_COLORS = WHITE, LIGHTGRAY, DARKGRAY, BLUE_SHIFTED, RED_SHIFTED, DARKGRAY, BLUE_SHIFTED, RED_SHIFTED
LEFT = 0
RIGHT = 1

def initStars(screen):
    "Create the starfield"

    # The starfield is represented as a dictionary of x and y values.
    stars = []

    # Create a list of (x,y) coordinates.
    for loop in range(0, NUM_STARS):
        star = [random.randrange(0, screen.get_width() - 1),
                random.randrange(0, screen.get_height() - 1)]
        stars.append(star);

    return stars

def moveStars(screen, stars, start, end, direction):
    "Correct for stars hitting the screen's borders"

    for loop in range(start, end):
        if (direction == LEFT):
            if (stars[loop][0] != 1):
                stars[loop][0] = stars[loop][0] - 1
            else:
                stars[loop][1] = random.randrange(0, screen.get_height() - 1)
                stars[loop][0] = screen.get_width() - 1
        elif (direction == RIGHT):
            if (stars[loop][0] != screen.get_width() - 1):
                stars[loop][0] = stars[loop][0] + 1
            else:
                stars[loop][1] = random.randrange(0, screen.get_height() - 1)
                stars[loop][0] = 1

    return stars

def main():
    "Main starfield code"

    random.seed()

    # Initialize the pygame library.
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE, FULLSCREEN)
    pygame.display.set_caption("Starfield")
    pygame.mouse.set_visible(0)

    # Set the background to black.
    screen.fill(BLACK)

    # Simulation variables.
    delay = 8
    inc = 1
    direction = LEFT

    # Create the starfield.
    stars = initStars(screen)

    # Main loop
    while True:

        # Handle input events.
        event = pygame.event.poll()
        if (event.type == QUIT):
            break
        elif (event.type == KEYDOWN):
            if (event.key == K_ESCAPE):
                break
            elif (event.key == K_UP):
                if (delay >= 2): delay = delay - 1
            elif (event.key == K_DOWN):
                if (delay <= 16): delay = delay + 1
            elif (event.key == K_LEFT):
                direction = LEFT
            elif (event.key == K_RIGHT):
                direction = RIGHT

        # Used to slow down the second and third field.
        # Make sure this variable doesn't get too large.
        # Use divisors to prevent jitter when the modulus rolls over
        inc = (inc + 1) % (prod(LAYER_SPEED_DIVISORS[1:]) * 100)

        # display furthest stars first so nearer stars are not obscured
        for layer in reversed(range(NUMBER_OF_LAYERS)):

            if (inc % LAYER_SPEED_DIVISORS[layer] == 0):

                # Erase the star field in the current layer.
                for loop in range(*STAR_RANGES[layer:layer + 2]):
                    screen.set_at(stars[loop], BLACK)
                    if layer == 0:
                        screen.set_at((stars[loop][0] - 1, stars[loop][1]), BLACK)

                # Checks to see if the field's stars hit the screen border.
                stars = moveStars(screen, stars, *STAR_RANGES[layer: layer + 2], direction)

                # Place current layer stars.
                for loop in range(*STAR_RANGES[layer:layer + 2]):
                    screen.set_at(stars[loop], LAYER_COLORS[layer])
                    # make foreground stars larger/motion-blurred
                    if layer == 0:
                        screen.set_at((stars[loop][0] - 1, stars[loop][1]), LAYER_COLORS[layer])

        # Control the starfield speed.
        pygame.time.delay(delay)

        # Update the screen.
        pygame.display.update()

# Start the program.
if __name__ == '__main__': main()