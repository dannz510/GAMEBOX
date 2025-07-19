import os
from PIL import Image, ImageDraw, ImageFont

# --- Configuration ---
ASSETS_DIR = "Assets"
BODY_DIR = os.path.join(ASSETS_DIR, "body")
CELLSIZE = 16 # Matches your game's CELLSIZE for snake parts

# Ensure directories exist
os.makedirs(ASSETS_DIR, exist_ok=True)
os.makedirs(BODY_DIR, exist_ok=True)

# --- Colors (RGB) ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
DARK_GREEN = (0, 128, 0)
LIGHT_GREEN = (0, 200, 0)
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)
GOLD = (255, 215, 0)
BROWN = (139, 69, 19) # For tree trunk
FOREST_GREEN = (34, 139, 34) # For tree leaves

# --- Font (adjust path if necessary, or use a default system font) ---
try:
    # Try to load a common font, or specify a path to a .ttf file
    font_path = "arial.ttf" # Common font on Windows
    # On Linux/macOS, you might use "DejaVuSans.ttf" or specify a full path
    # font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    # font_path = "/System/Library/Fonts/Supplemental/Arial.ttf" # Example for macOS
    button_font = ImageFont.truetype(font_path, 16)
    game_over_font = ImageFont.truetype(font_path, 30)
    score_font = ImageFont.truetype(font_path, 18)
except IOError:
    print("Could not load font. Using default PIL font.")
    button_font = ImageFont.load_default()
    game_over_font = ImageFont.load_default()
    score_font = ImageFont.load_default()


# --- Image Generation Functions ---

def create_button_image(text, size=(100, 50), filename="button.png", color=BLUE, text_color=WHITE):
    """Generates a button image with text."""
    img = Image.new('RGBA', size, (0, 0, 0, 0)) # Transparent background
    draw = ImageDraw.Draw(img)

    # Draw rounded rectangle for button background
    radius = 10
    draw.rounded_rectangle([(0, 0), (size[0]-1, size[1]-1)], radius=radius, fill=color, outline=DARK_GRAY, width=2)

    # Add subtle gradient
    for y in range(size[1]):
        alpha = int(255 * (1 - y / size[1]) * 0.3) # Top brighter, bottom darker
        draw.line([(0, y), (size[0], y)], fill=(255, 255, 255, alpha))

    # Draw text
    # Use textbbox for text dimension calculation
    bbox = draw.textbbox((0, 0), text, font=button_font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    text_x = (size[0] - text_width) // 2
    text_y = (size[1] - text_height) // 2
    draw.text((text_x + 1, text_y + 1), text, font=button_font, fill=BLACK) # Shadow
    draw.text((text_x, text_y), text, font=button_font, fill=text_color)

    img.save(os.path.join(ASSETS_DIR, filename))
    print(f"Generated {filename}")

def create_snake_head(direction, size=CELLSIZE, filename="head.png", head_color=DARK_GREEN, eye_color=WHITE, pupil_color=BLACK):
    """Generates a snake head image for a given direction."""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Draw main head shape
    draw.rectangle([(0, 0), (size-1, size-1)], fill=head_color)

    # Add eyes based on direction
    if direction == 'up':
        draw.ellipse([(size*0.2, size*0.2), (size*0.4, size*0.4)], fill=eye_color, outline=pupil_color)
        draw.ellipse([(size*0.6, size*0.2), (size*0.8, size*0.4)], fill=eye_color, outline=pupil_color)
    elif direction == 'down':
        draw.ellipse([(size*0.2, size*0.6), (size*0.4, size*0.8)], fill=eye_color, outline=pupil_color)
        draw.ellipse([(size*0.6, size*0.6), (size*0.8, size*0.8)], fill=eye_color, outline=pupil_color)
    elif direction == 'left':
        draw.ellipse([(size*0.1, size*0.2), (size*0.3, size*0.4)], fill=eye_color, outline=pupil_color)
        draw.ellipse([(size*0.1, size*0.6), (size*0.3, size*0.8)], fill=eye_color, outline=pupil_color)
    elif direction == 'right':
        draw.ellipse([(size*0.7, size*0.2), (size*0.9, size*0.4)], fill=eye_color, outline=pupil_color)
        draw.ellipse([(size*0.7, size*0.6), (size*0.9, size*0.8)], fill=eye_color, outline=pupil_color)

    img.save(os.path.join(BODY_DIR, filename))
    print(f"Generated {filename}")

def create_snake_body(type, size=CELLSIZE, filename="body.png", body_color=LIGHT_GREEN):
    """Generates snake body segments (horizontal, vertical, corners)."""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    if type == 'h_body': # Horizontal
        draw.rectangle([(0, size*0.25), (size-1, size*0.75)], fill=body_color)
        # Add subtle texture/shading
        draw.line([(0, size//2), (size-1, size//2)], fill=DARK_GREEN, width=1)
    elif type == 'v_body': # Vertical
        draw.rectangle([(size*0.25, 0), (size*0.75, size-1)], fill=body_color)
        # Add subtle texture/shading
        draw.line([(size//2, 0), (size//2, size-1)], fill=DARK_GREEN, width=1)
    elif type == 'tl_corner': # Top-left corner (from top to right, or left to down)
        # Draw the L-shape more explicitly
        draw.polygon([(size//2, 0), (size, 0), (size, size//2), (size, size), (0, size), (0, size//2), (size//2, size//2)], fill=body_color)
    elif type == 'tr_corner': # Top-right corner (from top to left, or right to down)
        # Explicit L-shape
        draw.polygon([(0, 0), (size, 0), (size, size//2), (size//2, size//2), (size//2, size), (0, size)], fill=body_color)
    elif type == 'bl_corner': # Bottom-left corner (from bottom to right, or left to up)
        # Explicit L-shape
        draw.polygon([(0, 0), (size//2, 0), (size//2, size//2), (size, size//2), (size, size), (0, size)], fill=body_color)
    elif type == 'br_corner': # Bottom-right corner (from bottom to left, or right to up)
        # Explicit L-shape
        draw.polygon([(0, 0), (size, 0), (size, size), (size//2, size), (size//2, size//2), (0, size//2)], fill=body_color)

    img.save(os.path.join(BODY_DIR, filename))
    print(f"Generated {filename}")

def create_food_image(type, size=16, filename="food.png", food_color=GOLD):
    """Generates a food image."""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    if type == 1: # Apple-like
        draw.ellipse([(0, 0), (size-1, size-1)], fill=RED, outline=DARK_GRAY, width=1)
        draw.line([(size*0.4, size*0.2), (size*0.6, size*0.1)], fill=BROWN, width=1)
        draw.ellipse([(size*0.5, 0), (size*0.7, size*0.2)], fill=FOREST_GREEN) # Leaf
    elif type == 2: # Berry-like
        draw.ellipse([(size*0.1, size*0.1), (size*0.9, size*0.9)], fill=BLUE, outline=DARK_GRAY, width=1)
        draw.ellipse([(size*0.3, size*0.3), (size*0.7, size*0.7)], fill=(0,0,150)) # Inner highlight
    elif type == 3: # Coin-like
        draw.ellipse([(0, 0), (size-1, size-1)], fill=GOLD, outline=BROWN, width=2)
        # Use textbbox for text dimension calculation
        bbox = draw.textbbox((0, 0), "$", font=ImageFont.truetype(font_path, int(size*0.7)))
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        draw.text((size*0.5 - text_width/2, size*0.5 - text_height/2), "$", font=ImageFont.truetype(font_path, int(size*0.7)), fill=BROWN)

    img.save(os.path.join(ASSETS_DIR, filename))
    print(f"Generated {filename}")

def create_tree_image(index, size=(32, 32), filename="tree.png"):
    """Generates a tree image (simple animation frames)."""
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Trunk
    draw.rectangle([(size[0]*0.4, size[1]*0.6), (size[0]*0.6, size[1]*0.9)], fill=BROWN)

    # Leaves (simple cloud shape)
    if index == 0:
        draw.ellipse([(size[0]*0.1, size[1]*0.1), (size[0]*0.9, size[1]*0.7)], fill=FOREST_GREEN)
    elif index == 1:
        draw.ellipse([(size[0]*0.05, size[1]*0.05), (size[0]*0.85, size[1]*0.65)], fill=FOREST_GREEN)
        draw.ellipse([(size[0]*0.2, size[1]*0.15), (size[0]*0.95, size[1]*0.75)], fill=FOREST_GREEN)
    elif index == 2:
        draw.ellipse([(size[0]*0.1, size[1]*0.1), (size[0]*0.9, size[1]*0.7)], fill=FOREST_GREEN)
        draw.ellipse([(size[0]*0.0, size[1]*0.0), (size[0]*0.8, size[1]*0.6)], fill=FOREST_GREEN)
    elif index == 3:
        draw.ellipse([(size[0]*0.15, size[1]*0.15), (size[0]*0.95, size[1]*0.75)], fill=FOREST_GREEN)
        draw.ellipse([(size[0]*0.05, size[1]*0.05), (size[0]*0.85, size[1]*0.65)], fill=FOREST_GREEN)

    img.save(os.path.join(ASSETS_DIR, filename))
    print(f"Generated {filename}")

def create_misc_images(size=(288, 512)): # Removed default color arguments
    """Generates placeholder images for bg, logo, gameover, bar."""
    # Background
    img_bg = Image.new('RGB', size, BLACK) # Use global BLACK
    draw_bg = ImageDraw.Draw(img_bg)
    # Use textbbox for text dimension calculation
    bbox = draw_bg.textbbox((0, 0), "Background", font=score_font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    draw_bg.text((size[0]//2 - text_width//2, size[1]//2 - text_height//2), "Background", font=score_font, fill=WHITE) # Use global WHITE
    img_bg.save(os.path.join(ASSETS_DIR, "bg.png"))
    print("Generated bg.png")

    # Logo
    img_logo = Image.new('RGB', (size[0], size[1]//2), BLACK) # Use global BLACK
    draw_logo = ImageDraw.Draw(img_logo)
    # Use textbbox for text dimension calculation
    bbox = draw_logo.textbbox((0, 0), "SNAKE", font=game_over_font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    draw_logo.text((size[0]//2 - text_width//2, size[1]//4 - text_height//2), "SNAKE", font=game_over_font, fill=GREEN) # Use global GREEN
    img_logo.save(os.path.join(ASSETS_DIR, "logo.jpg"))
    print("Generated logo.jpg")

    # Logo2
    img_logo2 = Image.new('RGB', (size[0], size[1]//2), BLACK) # Use global BLACK
    draw_logo2 = ImageDraw.Draw(img_logo2)
    # Use textbbox for text dimension calculation
    bbox = draw_logo2.textbbox((0, 0), "GAME", font=game_over_font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    draw_logo2.text((size[0]//2 - text_width//2, size[1]//4 - text_height//2), "GAME", font=game_over_font, fill=GREEN) # Use global GREEN
    img_logo2.save(os.path.join(ASSETS_DIR, "logo2.jpg"))
    print("Generated logo2.jpg")

    # Game Over
    img_gameover = Image.new('RGBA', (200, 100), (0, 0, 0, 0))
    draw_go = ImageDraw.Draw(img_gameover)
    draw_go.rounded_rectangle([(0,0), (199,99)], radius=15, fill=RED, outline=WHITE, width=3) # Use global RED, WHITE
    # Use textbbox for text dimension calculation
    bbox = draw_go.textbbox((0, 0), "GAME OVER", font=game_over_font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    draw_go.text((img_gameover.width//2 - text_width//2, 30), "GAME OVER", font=game_over_font, fill=WHITE) # Use global WHITE
    img_gameover.save(os.path.join(ASSETS_DIR, "gameover.png"))
    print("Generated gameover.png")

    # Bar
    img_bar = Image.new('RGB', (100, 10), LIGHT_GREEN) # Use global LIGHT_GREEN
    img_bar.save(os.path.join(ASSETS_DIR, "bar.png"))
    print("Generated bar.png")

def create_tiles(num_tiles=5, size=(16, 16)):
    """Generates simple tile images."""
    TILE_DIR = "Tiles"
    os.makedirs(TILE_DIR, exist_ok=True)

    for i in range(1, num_tiles + 1):
        img = Image.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        if i == 1: # Wall segment 1 (vertical)
            draw.rectangle([(size[0]*0.3, 0), (size[0]*0.7, size[1]-1)], fill=GRAY, outline=DARK_GRAY)
        elif i == 2: # Wall segment 2 (horizontal)
            draw.rectangle([(0, size[1]*0.3), (size[0]-1, size[1]*0.7)], fill=GRAY, outline=DARK_GRAY)
        elif i == 3: # Transparent/empty tile (or special effect)
            draw.ellipse([(size[0]*0.2, size[1]*0.2), (size[0]*0.8, size[1]*0.8)], fill=(200,200,200,100)) # Semi-transparent circle
        elif i == 4: # Block 1
            draw.rectangle([(0,0), (size[0]-1, size[1]-1)], fill=(150, 75, 0), outline=(100, 50, 0), width=1) # Brown block
        elif i == 5: # Block 2
            draw.rectangle([(0,0), (size[0]-1, size[1]-1)], fill=(180, 90, 0), outline=(120, 60, 0), width=1) # Lighter brown block
        
        img.save(os.path.join(TILE_DIR, f"{i}.png"))
        print(f"Generated Tiles/{i}.png")


# --- Main Generation Call ---
if __name__ == "__main__":
    print("Generating game assets...")

    # Generate buttons
    create_button_image("Replay", filename="replay_btn.png")
    create_button_image("Menu", filename="menu_btn.png")

    # Generate snake head images
    create_snake_head('up', filename="uhead.png")
    create_snake_head('down', filename="dhead.png")
    create_snake_head('left', filename="lhead.png")
    create_snake_head('right', filename="rhead.png")

    # Generate snake body segments
    create_snake_body('h_body', filename="h_body.png")
    create_snake_body('v_body', filename="v_body.png")
    create_snake_body('tl_corner', filename="tl_corner.png")
    create_snake_body('tr_corner', filename="tr_corner.png")
    create_snake_body('bl_corner', filename="bl_corner.png")
    create_snake_body('br_corner', filename="br_corner.png")

    # Generate food images
    create_food_image(1, filename="1.png")
    create_food_image(2, filename="2.png")
    create_food_image(3, filename="3.png")

    # Generate tree animation frames
    for i in range(4):
        create_tree_image(i, filename=f"tree{i}.png")

    # Generate miscellaneous images
    # Call create_misc_images without explicit color arguments,
    # as it now uses the globally defined color constants.
    create_misc_images()

    # Generate tile images
    create_tiles()

    print("\nAsset generation complete!")
    print("Please ensure these images are in your 'Assets/' and 'Assets/body/' folders.")
    print("You can now remove the placeholder URLs from your 'main.py' if you wish to use these generated images.")
