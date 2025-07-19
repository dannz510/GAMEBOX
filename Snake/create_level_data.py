import os
import pickle

# --- Configuration ---
LEVELS_DIR = "Levels"
ROWS = 32 # Matches ROWS in main.py (512 / 16)
COLS = 18 # Matches COLS in main.py (288 / 16)
MAX_LEVEL = 4 # Matches MAX_LEVEL in main.py

# Snake's initial spawn coordinates (center of the grid)
SNAKE_SPAWN_X = COLS // 2
SNAKE_SPAWN_Y = ROWS // 2

# The area around the snake's spawn that must be clear (head + 2 body segments)
# Snake body: [[head_x-2*CELLSIZE, head_y], [head_x-CELLSIZE, head_y], head]
# In grid coordinates: [(spawn_x-2, spawn_y), (spawn_x-1, spawn_y), (spawn_x, spawn_y)]
SNAKE_CLEAR_AREA = [
    (SNAKE_SPAWN_X - 2, SNAKE_SPAWN_Y),
    (SNAKE_SPAWN_X - 1, SNAKE_SPAWN_Y),
    (SNAKE_SPAWN_X, SNAKE_SPAWN_Y)
]

# Ensure the Levels directory exists
os.makedirs(LEVELS_DIR, exist_ok=True)

def create_boxed_level():
    """Creates a simple 'boxed' level with walls around the perimeter,
    ensuring the snake's spawn area is clear."""
    print("Creating 'boxed' level data...")
    # Initialize all cells to -1 (empty space)
    level_data = [[-1 for _ in range(COLS)] for _ in range(ROWS)]

    # Add walls (represented by tile index 0, which becomes 1 in main.py)
    # Top and bottom borders
    for x in range(COLS):
        level_data[0][x] = 0
        level_data[ROWS-1][x] = 0
    # Left and right borders
    for y in range(ROWS):
        level_data[y][0] = 0
        level_data[y][COLS-1] = 0

    # Ensure snake spawn area is clear by explicitly setting it to -1
    for sx, sy in SNAKE_CLEAR_AREA:
        if 0 <= sx < COLS and 0 <= sy < ROWS: # Ensure within bounds
            level_data[sy][sx] = -1

    file_path = os.path.join(LEVELS_DIR, "boxed")
    with open(file_path, 'wb') as f:
        pickle.dump(level_data, f)
    print(f"Successfully created: {file_path}")

def create_arcade_levels():
    """Creates simple placeholder levels for Arcade mode,
    ensuring the snake's spawn area is clear."""
    print("Creating Arcade mode level data...")
    for level_num in range(1, MAX_LEVEL + 1):
        # Initialize all cells to -1 (empty space)
        level_data = [[-1 for _ in range(COLS)] for _ in range(ROWS)]

        # Add some simple obstacles based on level number (tile index 0)
        # Avoid placing obstacles in the snake's initial spawn area
        def is_clear_for_snake(x, y):
            for sx, sy in SNAKE_CLEAR_AREA:
                if x == sx and y == sy:
                    return False
            return True

        if level_num == 1:
            # Simple horizontal line in the upper part of the screen
            for x in range(COLS // 4, COLS - COLS // 4):
                if is_clear_for_snake(x, ROWS // 4):
                    level_data[ROWS // 4][x] = 0 # Tile index 0 (becomes 1 in game)
        elif level_num == 2:
            # Two vertical lines on the sides
            for y in range(ROWS // 4, ROWS - ROWS // 4):
                if is_clear_for_snake(COLS // 4, y):
                    level_data[y][COLS // 4] = 0
                if is_clear_for_snake(COLS - COLS // 4 - 1, y):
                    level_data[y][COLS - COLS // 4 - 1] = 0
        elif level_num == 3:
            # A cross shape, avoiding snake spawn
            for x in range(COLS):
                if is_clear_for_snake(x, ROWS // 3): # Adjusted Y position
                    level_data[ROWS // 3][x] = 0
            for y in range(ROWS):
                if is_clear_for_snake(COLS // 2, y): # Adjusted X position
                    level_data[y][COLS // 2] = 0
        elif level_num == 4:
            # More complex pattern (e.g., a square in the upper-left)
            for y in range(ROWS // 8, ROWS // 8 + 5): # Small square
                for x in range(COLS // 8, COLS // 8 + 5):
                    if is_clear_for_snake(x, y):
                        level_data[y][x] = 0


        file_path = os.path.join(LEVELS_DIR, f"level{level_num}_data")
        with open(file_path, 'wb') as f:
            pickle.dump(level_data, f)
        print(f"Successfully created: {file_path}")

if __name__ == "__main__":
    print("Starting level data generation...")
    create_boxed_level()
    create_arcade_levels()
    print("\nLevel data generation complete!")
    print("You should now have a 'Levels' folder with 'boxed' and 'levelX_data' files.")
    print("You can now try running 'main.py' again.")
