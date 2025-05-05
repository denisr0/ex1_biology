import pygame
import random

cols, rows = 100, 100
cell_size = 10
width, height = cols * cell_size, rows * cell_size
WHITE, BLACK, RED, BLUE = (255, 255, 255), (0, 0, 0), (255, 0, 0), (0, 0, 255)

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Automaton")
font = pygame.font.SysFont("arial", 28)

#this is the normal grid for סעיף 1 based on the chosen percentage
def normal_grid(chance):
    return [[1 if random.random() < chance else 0 for _ in range(cols)] for _ in range(rows)]

# this is the cells for the glider with wraparound
def glider_grid():
    grid = [[1 for _ in range(cols)] for _ in range(rows)]
    grid[48][6] = 0
    grid[49][7] = 0
    grid[50][7] = 0
    grid[51][6] = 0
    return grid

# this is the cells for the glider without wraparound
def glider_grid_no_wraparound():
    grid = [[1 for _ in range(cols)] for _ in range(rows)]
    grid[48][6] = 0
    grid[49][7] = 0
    grid[50][7] = 0
    grid[51][6] = 0
    return grid

# this is the cells for סעיף 3 with wraparound
def interesting_grid_wraparound():
    grid = [[0 for _ in range(cols)] for _ in range(rows)]
    pattern = [[1, 1, 0, 0], [1, 0, 0, 1], [0, 0, 0, 0], [0, 1, 0, 1]]
    for y in range(0, rows, 4):
        for x in range(0, cols, 4):
            for dy in range(4):
                for dx in range(4):
                    grid[(y + dy) % rows][(x + dx) % cols] = pattern[dy][dx]
    return grid

# this is the cells for סעיף 3 without wraparound
def interesting_grid_no_wraparound():
    grid = [[0 for _ in range(cols)] for _ in range(rows)]
    for y in range(0, rows, 2):
        for x in range(0, cols, 2):
            grid[y][x] = 1
            grid[y + 1][x + 1] = 1
    cx, cy = cols // 2, rows // 2
    for dy in [-4, 0, 4]:
        y, x = cy + dy, cx
        y -= y % 2
        x -= x % 2
        grid[y][x] = 1
        grid[y][x+1] = 1
        grid[y+1][x] = 1
    return grid

# here we draw the cells
def draw_grid(grid):
    screen.fill(WHITE)
    for y in range(rows):
        for x in range(cols):
            color = BLACK if grid[y][x] == 1 else WHITE
            pygame.draw.rect(screen, color, (x * cell_size, y * cell_size, cell_size, cell_size))
    # REMOVE the red and blue lines entirely for performance
    pygame.display.update()

# this is where we change the cells based on the given rules of the automata
def apply_rules(grid, wraparound, generation):
    offset = 0 if generation % 2 == 1 else 1
    for y in range(offset, rows, 2):
        for x in range(offset, cols, 2):
            def get(yy, xx):
                if wraparound:
                    return grid[yy % rows][xx % cols]
                if 0 <= yy < rows and 0 <= xx < cols:
                    return grid[yy][xx]
                return 0
            block = [get(y, x), get(y, x + 1), get(y + 1, x), get(y + 1, x + 1)]
            # summing the live cells in the block
            live_cells = sum(block)
            # if 2 live cells we dont change anything
            if live_cells == 2:
                continue
            for dy in range(2):
                for dx in range(2):
                    yy = (y + dy) % rows if wraparound else y + dy
                    xx = (x + dx) % cols if wraparound else x + dx
                    if 0 <= yy < rows and 0 <= xx < cols:
                        grid[yy][xx] = 1 - grid[yy][xx]
            # 3 live cells case - rotating 180 degrees
            if live_cells == 3:
                y0, y1 = y % rows, (y + 1) % rows
                x0, x1 = x % cols, (x + 1) % cols
                grid[y0][x0], grid[y1][x0], grid[y0][x1], grid[y1][x1] = \
                    grid[y1][x1], grid[y0][x1], grid[y1][x0], grid[y0][x0]

# calculating the stability meaning the percantage of changed cells from last generation
def calculate_stability(grid, prev_grid):
    if not prev_grid:
        return 100.0
    unchanged = sum(1 for y in range(rows) for x in range(cols) if grid[y][x] == prev_grid[y][x])
    return (unchanged / (rows * cols)) * 100

# counting live cells for live cells index
def count_live_cells(grid):
    return sum(cell for row in grid for cell in row)

def main_menu():
    while True:
        wraparound = None
        selecting = True
        while selecting:
            screen.fill(WHITE)
            t1 = font.render("Select wraparound mode:", True, BLACK)
            t2 = font.render("Press 0 for NO wraparound", True, BLACK)
            t3 = font.render("Press 1 for WRAPAROUND", True, BLACK)
            t4 = font.render("Press ESC to return to main menu, press SPACE to stop simulation, anytime during run", True, BLACK)
            screen.blit(t1, (width//2 - t1.get_width()//2, height//2 - 110))
            screen.blit(t2, (width//2 - t2.get_width()//2, height//2 - 60))
            screen.blit(t3, (width//2 - t3.get_width()//2, height//2 - 10))
            screen.blit(t4, (width//2 - t4.get_width()//2, height//2 + 40))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                # choosing with wraparound or not
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_0:
                        wraparound = False
                        selecting = False
                    elif event.key == pygame.K_1:
                        wraparound = True
                        selecting = False

        grid_mode = None
        selecting = True
        while selecting:
            screen.fill(WHITE)
            t1 = font.render("Select starting pattern:", True, BLACK)
            t2 = font.render("Press 1 for NORMAL run", True, BLACK)
            t3 = font.render("Press 2 for GLIDER", True, BLACK)
            t4 = font.render("Press 3 for INTERESTING", True, BLACK)
            screen.blit(t1, (width//2 - t1.get_width()//2, height//2 - 90))
            screen.blit(t2, (width//2 - t2.get_width()//2, height//2 - 40))
            screen.blit(t3, (width//2 - t3.get_width()//2, height//2 + 10))
            screen.blit(t4, (width//2 - t4.get_width()//2, height//2 + 60))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                # בחירת סעיפים
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

        cell_chance = 0.5
        if grid_mode == "normal":
            selecting = True
            while selecting:
                screen.fill(WHITE)
                t1 = font.render("Cell alive chance:", True, BLACK)
                t2 = font.render("Press 1 for 50%", True, BLACK)
                t3 = font.render("Press 2 for 25%", True, BLACK)
                t4 = font.render("Press 3 for 75%", True, BLACK)
                screen.blit(t1, (width // 2 - t1.get_width() // 2, height // 2 - 90))
                screen.blit(t2, (width // 2 - t2.get_width() // 2, height // 2 - 40))
                screen.blit(t3, (width // 2 - t3.get_width() // 2, height // 2 + 10))
                screen.blit(t4, (width // 2 - t4.get_width() // 2, height // 2 + 60))
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                    # changing chance based on the choice
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

        if grid_mode == "normal":
            grid = normal_grid(cell_chance)
        elif grid_mode == "glider":
            grid = glider_grid() if wraparound else glider_grid_no_wraparound()
        elif grid_mode == "interesting":
            grid = interesting_grid_wraparound() if wraparound else interesting_grid_no_wraparound()

        # here is the main run of the automaton
        generation = 1
        paused = False
        prev_grid = None
        draw_grid(grid)
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        paused = not paused
                    elif event.key == pygame.K_ESCAPE:
                        return

            if not paused and generation < 250:
                prev_grid_copy = [row[:] for row in grid]
                apply_rules(grid, wraparound, generation)
                generation += 1
                stability = calculate_stability(grid, prev_grid_copy)
                live_cells = count_live_cells(grid)
                draw_grid(grid)
                pygame.display.set_caption(
                    f"Generation {generation} - Wrap: {wraparound} - Stability: {stability:.2f}% - Live: {live_cells}"
                )
                clock.tick(9)


while True:
    main_menu()
