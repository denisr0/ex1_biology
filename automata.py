import pygame
import random

# Set up the window size
cols, rows = 100, 100
cell_size = 8
width, height = cols * cell_size, rows * cell_size

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Wraparound Mode Selection")
font = pygame.font.SysFont("arial", 28)

# --- wraparound selection menu ---
wraparound = None
selecting = True
while selecting:
    screen.fill(WHITE)
    text1 = font.render("Select wraparound mode:", True, BLACK)
    text2 = font.render("Press 0 for NO wraparound", True, BLACK)
    text3 = font.render("Press 1 for WRAPAROUND", True, BLACK)
    screen.blit(text1, (width // 2 - text1.get_width() // 2, height // 2 - 80))
    screen.blit(text2, (width // 2 - text2.get_width() // 2, height // 2 - 30))
    screen.blit(text3, (width // 2 - text3.get_width() // 2, height // 2 + 20))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_0:
                wraparound = False
                selecting = False
            elif event.key == pygame.K_1:
                wraparound = True
                selecting = False

# --- Second menu: grid type selection ---
grid_mode = None
selecting = True
while selecting:
    screen.fill(WHITE)
    text1 = font.render("Select starting pattern:", True, BLACK)
    text2 = font.render("Press 1 for NORMAL run (random)", True, BLACK)
    text3 = font.render("Press 2 for GLIDER", True, BLACK)
    text4 = font.render("Press 3 for INTERESTING", True, BLACK)
    screen.blit(text1, (width // 2 - text1.get_width() // 2, height // 2 - 90))
    screen.blit(text2, (width // 2 - text2.get_width() // 2, height // 2 - 40))
    screen.blit(text3, (width // 2 - text3.get_width() // 2, height // 2 + 10))
    screen.blit(text4, (width // 2 - text4.get_width() // 2, height // 2 + 60))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                grid_mode = "normal"
                selecting = False
            elif event.key == pygame.K_2:
                grid_mode = "glider"
                selecting = False
            elif event.key == pygame.K_3:
                grid_mode = "interesting"
                selecting = False

# --- Third menu: cell alive chance (if normal selected) ---
cell_chance = 0.5  # default

if grid_mode == "normal":
    selecting = True
    while selecting:
        screen.fill(WHITE)
        text1 = font.render("Cell alive chance:", True, BLACK)
        text2 = font.render("Press 1 for 50%", True, BLACK)
        text3 = font.render("Press 2 for 25%", True, BLACK)
        text4 = font.render("Press 3 for 75%", True, BLACK)
        screen.blit(text1, (width // 2 - text1.get_width() // 2, height // 2 - 90))
        screen.blit(text2, (width // 2 - text2.get_width() // 2, height // 2 - 40))
        screen.blit(text3, (width // 2 - text3.get_width() // 2, height // 2 + 10))
        screen.blit(text4, (width // 2 - text4.get_width() // 2, height // 2 + 60))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    cell_chance = 0.5
                    selecting = False
                elif event.key == pygame.K_2:
                    cell_chance = 0.25
                    selecting = False
                elif event.key == pygame.K_3:
                    cell_chance = 0.75
                    selecting = False

# --- Initialize grid ---
def normal_grid():
    return [[1 if random.random() < cell_chance else 0 for _ in range(cols)] for _ in range(rows)]

def glider_grid():
    grid = [[1 for _ in range(cols)] for _ in range(rows)]

    grid[2][6] = 0
    grid[3][7] = 0
    grid[4][7] = 0
    grid[5][6] = 0

    return grid

def glider_grid_no_wraparound():
    grid = [[0 for _ in range(cols)] for _ in range(rows)]

    for y in range(0, rows, 2):
        for x in range(0, cols, 2):
            grid[y][x] = 1
            grid[y + 1][x + 1] = 1

    gx, gy = 10, 10
    grid[gy][gx + 1] = 1
    grid[gy + 1][gx] = 1
    grid[gy + 1][gx + 1] = 0
    grid[gy + 2][gx] = 1
    grid[gy + 2][gx + 1] = 1
    grid[gy + 1][gx + 2] = 1
    grid[gy + 2][gx + 2] = 0
    grid[gy + 3][gx + 1] = 1

    return grid


def interesting_grid():
    grid = [[random.randint(0, 1) for _ in range(cols)] for _ in range(rows)]
    return grid

def interesting_grid_wraparound():
    grid = [[0 for _ in range(cols)] for _ in range(rows)]

    pattern = [
        [1, 1, 0, 0],
        [1, 0, 0, 1],
        [0, 0, 0, 0],
        [0, 1, 0, 1]
    ]

    for y in range(0, rows, 4):
        for x in range(0, cols, 4):
            for dy in range(4):
                for dx in range(4):
                    grid[(y + dy) % rows][(x + dx) % cols] = pattern[dy][dx]

    return grid

def interesting_grid_no_wraparound():
    grid = [[0 for _ in range(cols)] for _ in range(rows)]

    for y in range(0, rows, 2):
        for x in range(0, cols, 2):
            grid[y][x] = 1
            grid[y+1][x+1] = 1

    cx = cols // 2
    cy = rows // 2

    offsets = [-4, 0, 4]

    for dy in offsets:
        y = cy + dy
        x = cx

        if y % 2 != 0:
            y -= 1
        if x % 2 != 0:
            x -= 1

        grid[y][x] = 1
        grid[y][x+1] = 1
        grid[y+1][x] = 1
        grid[y+1][x+1] = 0

    return grid

# Choose grid based on user selection
if grid_mode == "normal":
    grid = normal_grid()
elif grid_mode == "glider" and wraparound == True:
    grid = glider_grid()
elif grid_mode == "glider" and wraparound == False:
    grid = glider_grid_no_wraparound()
elif grid_mode == "interesting" and wraparound == True:
    grid = interesting_grid_wraparound()
elif grid_mode == "interesting" and wraparound == False:
    grid = interesting_grid_no_wraparound()

# --- Drawing ---
def draw_grid():
    screen.fill(WHITE)
    for y in range(rows):
        for x in range(cols):
            color = BLACK if grid[y][x] == 1 else WHITE
            pygame.draw.rect(screen, color, (x * cell_size, y * cell_size, cell_size, cell_size))
    for y in range(0, rows, 2):
        for x in range(0, cols, 2):
            pygame.draw.rect(screen, BLUE, (x * cell_size, y * cell_size, cell_size * 2, cell_size * 2), 1)
    for y in range(0, rows, 2):
        for x in range(0, cols, 2):
            new_x = x - 1
            new_y = y + 1
            for i in range(0, width, 6):
                pygame.draw.line(screen, RED, (i, new_y * cell_size), (i + 3, new_y * cell_size), 2)
                pygame.draw.line(screen, RED, (i, new_y * cell_size + cell_size * 2), (i + 3, new_y * cell_size + cell_size * 2), 2)
            for i in range(0, height, 6):
                pygame.draw.line(screen, RED, (new_x * cell_size, i), (new_x * cell_size, i + 3), 2)
                pygame.draw.line(screen, RED, (new_x * cell_size + cell_size * 2, i), (new_x * cell_size + cell_size * 2, i + 3), 2)
    pygame.display.update()

# --- Rules ---
def apply_rules(generation):
    offset = 0 if generation % 2 == 1 else 1
    for y in range(offset, rows, 2):
        for x in range(offset, cols, 2):

            def get(y_, x_):
                if wraparound:
                    return grid[y_ % rows][x_ % cols]
                if 0 <= y_ < rows and 0 <= x_ < cols:
                    return grid[y_][x_]
                return 0

            block = [
                get(y, x),
                get(y, x + 1),
                get(y + 1, x),
                get(y + 1, x + 1)
            ]
            live_cells = sum(block)

            if live_cells == 2:
                continue

            for dy in range(2):
                for dx in range(2):
                    yy = (y + dy) % rows if wraparound else y + dy
                    xx = (x + dx) % cols if wraparound else x + dx
                    if 0 <= yy < rows and 0 <= xx < cols:
                        grid[yy][xx] = 1 - grid[yy][xx]

            if live_cells == 3:
                y0 = y % rows if wraparound else y
                y1 = (y + 1) % rows if wraparound else y + 1
                x0 = x % cols if wraparound else x
                x1 = (x + 1) % cols if wraparound else x + 1
                if all(0 <= v < rows for v in [y0, y1]) and all(0 <= v < cols for v in [x0, x1]):
                    grid[y0][x0], grid[y1][x0], grid[y0][x1], grid[y1][x1] = \
                        grid[y1][x1], grid[y0][x1], grid[y1][x0], grid[y0][x0]

# --- Main Loop ---
generation = 1
running = True
paused = False

draw_grid()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused

    if not paused and generation < 250:
        apply_rules(generation)
        generation += 1

    draw_grid()
    pygame.display.set_caption(f"Automaton Matrix {generation} - Wraparound: {wraparound}")

pygame.quit()
