import pygame
import random
import sys

from helper_functions import get_player_count, convert_white_to_transparent, MAX_PLAYER_COUNT

# --- INITIALIZATION ---
pygame.init()

player_count = get_player_count()

# Initial window dimensions matching the 5x6 landscape grid aspect ratio
BOARD_WIDTH = 1050
BOARD_HEIGHT = 750
UI_HEIGHT = 110
SCREEN_WIDTH = BOARD_WIDTH
SCREEN_HEIGHT = BOARD_HEIGHT + UI_HEIGHT

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Cat Board Game")
clock = pygame.time.Clock()

# Fonts (base font sizes)
font_large = pygame.font.SysFont("arial", 32, bold=True)
font_medium = pygame.font.SysFont("arial", 22)
font_small = pygame.font.SysFont("arial", 18)

# --- LOAD & SCALE IMAGES ---
FILE_NAME_BOARD = "grid-v2-x30-arrows.png"
FILE_NAMES_CATS = [
	"cat-orange.jpg",
	"cat-black.jpg",
	"cat-grey.jpg",
	"cat-stripes.jpg"
]

def load_image(file_name):
	try:
		raw = pygame.image.load(file_name).convert_alpha()
	except FileNotFoundError:
		print(f"Error: {file_name} not found in the script directory.")
		sys.exit()
	return raw

board_raw = load_image(FILE_NAME_BOARD)
sprites_raw = []
for i in range(MAX_PLAYER_COUNT):
	sprites_raw.append(load_image(FILE_NAMES_CATS[i]))
	convert_white_to_transparent(sprites_raw[i])

# --- BOARD PATH MAPPING ---
# Exact (row, col) path from Square 1 to Square 30 following the arrows
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

def get_cell_center(row, col, b_width, b_height):
	"""Returns the (x, y) pixel center dynamically based on current board dimensions."""
	margin_x = b_width * 0.042
	margin_y = b_height * 0.058
	grid_w = b_width - (2 * margin_x)
	grid_h = b_height - (2 * margin_y)
	cell_w = grid_w / 6
	cell_h = grid_h / 5

	x = margin_x + (col + 0.5) * cell_w
	y = margin_y + (row + 0.5) * cell_h
	return (int(x), int(y))

# --- GAME STATE VARIABLES ---
current_index = 0
target_index = 0
dice_value = None
is_rolling = False
roll_timer = 0
move_timer = 0
game_won = False

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
		roll_timer = 18

# --- MAIN GAME LOOP ---
running = True
while running:
	current_w, current_h = screen.get_size()

	# Keep board proportional to window width, reserving 110px at bottom for UI
	curr_board_height = max(400, current_h - 110)
	curr_board_width = current_w

	# Rescale board image dynamically to fit current window size
	scaled_board_img = pygame.transform.smoothscale(board_raw, (curr_board_width, curr_board_height))

	# Recalculate cell centers based on current window dimensions
	square_centers = [get_cell_center(r, c, curr_board_width, curr_board_height) for r, c in PATH_COORDS]

	# Dynamic roll button positioning on the UI bar
	roll_button = pygame.Rect(current_w - 240, curr_board_height + 25, 200, 55)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		# Handle window resizing event
		elif event.type == pygame.VIDEORESIZE:
			screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

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
	if is_rolling:
		dice_value = random.randint(1, 6)
		roll_timer -= 1
		if roll_timer <= 0:
			is_rolling = False
			target_index = min(current_index + dice_value, len(square_centers) - 1)
			move_timer = 10

	elif current_index < target_index:
		move_timer -= 1
		if move_timer <= 0:
			current_index += 1
			move_timer = 10
			if current_index == len(square_centers) - 1:
				game_won = True

	# --- RENDERING ---
	screen.fill((245, 246, 250))

	# Draw scaled game board
	screen.blit(scaled_board_img, (0, 0))

	for i in range(player_count):
		# Rescale sprite image proportional to board grid size
		sprite_size_w = int(curr_board_width / 6 * 0.7)
		sprite_size_h = int(curr_board_height / 5 * 0.7)
		scaled_sprite_img = pygame.transform.smoothscale(sprites_raw[i], (max(20, sprite_size_w), max(20, sprite_size_h)))

		# Draw the sprite centered in its current square
		sprite_center = square_centers[current_index]
		sprite_rect = scaled_sprite_img.get_rect(center=sprite_center)
		screen.blit(scaled_sprite_img, sprite_rect)

	# Draw Bottom UI Bar
	ui_height_val = current_h - curr_board_height
	pygame.draw.rect(screen, (35, 40, 50), (0, curr_board_height, current_w, ui_height_val))

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

	screen.blit(font_large.render(status_text, True, (255, 255, 255)), (30, curr_board_height + 15))
	screen.blit(font_small.render(sub_text, True, (180, 190, 205)), (30, curr_board_height + 55))

	# Draw Roll / Play Again Button
	btn_color = (46, 204, 113) if game_won else (52, 152, 219)
	if is_rolling or current_index < target_index:
		btn_color = (127, 140, 141)

	pygame.draw.rect(screen, btn_color, roll_button, border_radius=10)
	btn_label = "Play Again" if game_won else "Roll Dice"
	label_surf = font_medium.render(btn_label, True, (255, 255, 255))
	screen.blit(label_surf, label_surf.get_rect(center=roll_button.center))

	pygame.display.flip()
	clock.tick(60)

pygame.quit()
sys.exit()
