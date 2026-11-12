import pygame
import random
import sys

# --- INITIALIZATION ---
pygame.init()

# Window dimensions matching the 5x6 landscape grid aspect ratio
BOARD_WIDTH = 1050
BOARD_HEIGHT = 750
UI_HEIGHT = 110
SCREEN_WIDTH = BOARD_WIDTH
SCREEN_HEIGHT = BOARD_HEIGHT + UI_HEIGHT

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cat Board Game - 30 Squares")
clock = pygame.time.Clock()

# Fonts
font_large = pygame.font.SysFont("arial", 32, bold=True)
font_medium = pygame.font.SysFont("arial", 22)
font_small = pygame.font.SysFont("arial", 18)

# --- LOAD & SCALE IMAGES ---
try:
    board_img = pygame.image.load("grid-v2-x30-arrows.png").convert()
    board_img = pygame.transform.smoothscale(board_img, (BOARD_WIDTH, BOARD_HEIGHT))
except FileNotFoundError:
    print("Error: 'grid-v2-x30-arrows.png' not found in the script directory.")
    sys.exit()

# Try loading cat_2.jpg, fall back to cat.jpg if needed
cat_filename = "cat_2.jpg"
try:
    cat_raw = pygame.image.load(cat_filename).convert_alpha()
except FileNotFoundError:
    try:
        cat_filename = "cat.jpg"
        cat_raw = pygame.image.load(cat_filename).convert_alpha()
    except FileNotFoundError:
        print("Error: Neither 'cat_2.jpg' nor 'cat.jpg' found in the script directory.")
        sys.exit()

# Scale cat to fit nicely inside a single grid square
CAT_SIZE = (90, 80)
cat_img = pygame.transform.smoothscale(cat_raw, CAT_SIZE)

# Optional: Remove white/light-gray background pixels around the cat
for x in range(CAT_SIZE[0]):
    for y in range(CAT_SIZE[1]):
        r, g, b, a = cat_img.get_at((x, y))
        if r > 215 and g > 215 and b > 215 and abs(r - g) < 10 and abs(g - b) < 10:
            cat_img.set_at((x, y), (255, 255, 255, 0))

# --- BOARD PATH MAPPING ---
MARGIN_X = BOARD_WIDTH * 0.042
MARGIN_Y = BOARD_HEIGHT * 0.058
GRID_W = BOARD_WIDTH - (2 * MARGIN_X)
GRID_H = BOARD_HEIGHT - (2 * MARGIN_Y)
CELL_W = GRID_W / 6
CELL_H = GRID_H / 5

def get_cell_center(row, col):
    """Returns the (x, y) pixel center for a given (row, col) on the 5x6 grid."""
    x = MARGIN_X + (col + 0.5) * CELL_W
    y = MARGIN_Y + (row + 0.5) * CELL_H
    return (int(x), int(y))

# Exact (row, col) path from Square 1 to Square 30 following the new arrows
PATH_COORDS = [
    (4, 5), # 1  (Bottom right)
    (4, 4), # 2
    (4, 3), # 3
    (4, 2), # 4
    (4, 1), # 5
    (4, 0), # 6  (Bottom left)
    (3, 0), # 7  (Row up)
    (3, 1), # 8
    (3, 2), # 9
    (3, 3), # 10
    (3, 4), # 11
    (3, 5), # 12 (Right side)
    (2, 5), # 13 (Row up)
    (2, 4), # 14
    (2, 3), # 15
    (2, 2), # 16
    (2, 1), # 17
    (2, 0), # 18 (Left side)
    (1, 0), # 19 (Row up)
    (1, 1), # 20
    (1, 2), # 21
    (1, 3), # 22
    (1, 4), # 23
    (1, 5), # 24 (Right side)
    (0, 5), # 25 (Top right)
    (0, 4), # 26
    (0, 3), # 27
    (0, 2), # 28
    (0, 1), # 29
    (0, 0), # 30 (Finish - Top left)
]

SQUARE_CENTERS = [get_cell_center(r, c) for r, c in PATH_COORDS]

# --- GAME STATE VARIABLES ---
current_index = 0          # 0 = Square 1, 29 = Square 30
target_index = 0
dice_value = None
is_rolling = False
roll_timer = 0
move_timer = 0
game_won = False

# Button rectangle for rolling the dice
roll_button = pygame.Rect(SCREEN_WIDTH - 240, BOARD_HEIGHT + 25, 200, 60)

def reset_game():
    global current_index, target_index, dice_value, is_rolling, game_won
    current_index = 0
    target_index = 0
    dice_value = None
    is_rolling = False
    game_won = False

def trigger_roll():
    global is_rolling, roll_timer
    if not is_rolling and current_index == target_index and not game_won:
        is_rolling = True
        roll_timer = 18  # Frames of dice rolling animation

# --- MAIN GAME LOOP ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_won:
                    reset_game()
                else:
                    trigger_roll()
            elif event.key == pygame.K_r:
                reset_game()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and roll_button.collidepoint(event.pos):
                if game_won:
                    reset_game()
                else:
                    trigger_roll()

    # --- UPDATE LOGIC ---
    # 1. Dice rolling animation
    if is_rolling:
        dice_value = random.randint(1, 6)
        roll_timer -= 1
        if roll_timer <= 0:
            is_rolling = False
            # Set destination square (capped at square 30 / index 29)
            target_index = min(current_index + dice_value, len(SQUARE_CENTERS) - 1)
            move_timer = 10

    # 2. Step-by-step cat movement along the path
    elif current_index < target_index:
        move_timer -= 1
        if move_timer <= 0:
            current_index += 1
            move_timer = 10  # Delay between hops (frames)
            if current_index == len(SQUARE_CENTERS) - 1:
                game_won = True

    # --- RENDERING ---
    screen.fill((245, 246, 250))

    # Draw the game board
    screen.blit(board_img, (0, 0))

    # Draw the cat centered in its current square
    cat_center = SQUARE_CENTERS[current_index]
    cat_rect = cat_img.get_rect(center=(cat_center[0] + 5, cat_center[1] + 5))
    screen.blit(cat_img, cat_rect)

    # Draw Bottom UI Bar
    pygame.draw.rect(screen, (35, 40, 50), (0, BOARD_HEIGHT, SCREEN_WIDTH, UI_HEIGHT))

    # Status / Dice Text
    square_num = current_index + 1
    if game_won:
        status_text = "🎉 Purr-fect! The cat reached Square 30!"
        sub_text = "Press SPACE, R, or click 'Play Again' to restart."
    elif is_rolling:
        status_text = f"Rolling dice... [ {dice_value} ]"
        sub_text = f"Current Square: {square_num} / 30"
    elif current_index < target_index:
        status_text = f"Rolled a {dice_value}! Moving..."
        sub_text = f"Square: {square_num} -> {target_index + 1}"
    else:
        dice_display = f"Last Roll: {dice_value}  |  " if dice_value else ""
        status_text = f"{dice_display}Current Square: {square_num} of 30"
        sub_text = "Press SPACE or click 'Roll Dice' to move."

    screen.blit(font_large.render(status_text, True, (255, 255, 255)), (35, BOARD_HEIGHT + 18))
    screen.blit(font_small.render(sub_text, True, (180, 190, 205)), (35, BOARD_HEIGHT + 65))

    # Draw Roll / Play Again Button
    btn_color = (46, 204, 113) if game_won else (52, 152, 219)
    if is_rolling or current_index < target_index:
        btn_color = (127, 140, 141)  # Disabled gray while moving

    pygame.draw.rect(screen, btn_color, roll_button, border_radius=10)
    btn_label = "Play Again" if game_won else "Roll Dice"
    label_surf = font_medium.render(btn_label, True, (255, 255, 255))
    screen.blit(label_surf, label_surf.get_rect(center=roll_button.center))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
