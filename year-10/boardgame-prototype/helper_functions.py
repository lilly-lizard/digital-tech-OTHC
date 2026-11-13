MAX_PLAYER_COUNT = 4

def get_player_count():
    while True:
        try:
            # Read input from the terminal
            user_input = input(f"Enter the player count (number between 1 and {MAX_PLAYER_COUNT}): ")

            # Attempt to convert the input to an integer
            number = int(user_input)

            # Verify if the number is within the acceptable range
            if 1 <= number <= MAX_PLAYER_COUNT:
                return number
            else:
                print(f"Invalid range. Please enter a number from 1 to {MAX_PLAYER_COUNT}.")

        except ValueError:
            # Handle cases where the input is not a valid integer (e.g. letters, symbols)
            print("Invalid input. Please enter a whole number.")

# Remove white/light-gray background pixels around the sprite (do this once on raw image)
def convert_white_to_transparent(sprite_raw):
	SPRITE_RAW_SIZE = sprite_raw.get_size()
	for x in range(SPRITE_RAW_SIZE[0]):
	    for y in range(SPRITE_RAW_SIZE[1]):
	        r, g, b, a = sprite_raw.get_at((x, y))
	        if r > 215 and g > 215 and b > 215 and abs(r - g) < 10 and abs(g - b) < 10:
	            sprite_raw.set_at((x, y), (255, 255, 255, 0))
