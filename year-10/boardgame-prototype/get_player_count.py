def get_player_count():
    while True:
        try:
            # Read input from the terminal
            user_input = input("Enter the player count (number between 1 and 4): ")

            # Attempt to convert the input to an integer
            number = int(user_input)

            # Verify if the number is within the acceptable range
            if 1 <= number <= 4:
                return number
            else:
                print("Invalid range. Please enter a number from 1 to 4.")

        except ValueError:
            # Handle cases where the input is not a valid integer (e.g. letters, symbols)
            print("Invalid input. Please enter a whole number.")
