import os
from PIL import Image, ImageDraw, ImageFont
import random

# List of your 30 game names (from CPGames in your launcher)
GAME_NAMES = [
    'Aeroblasters', 'Angry Walls', 'Arc Dash', 'Asteroids', 'Bounce',
    'Car Racing 2d', 'Cave Story', 'Connected', 'Dodgy Walls', 'Dots & Boxes',
    'Egg Catching Game', 'Flappy Bird', 'GhostBusters', 'Hangman', 'Hex Dash',
    'HyperTile Dash', 'Jungle Dash', 'Level Designer', 'Memory Puzzle', 'MineSweeper',
    'Piano Tiles', 'Picture Sliding Puzzle', 'Pong', 'Qircle Rush', 'Rock Paper Scissor',
    'Rotate Dash', 'Snake', 'SpriteSheet Cutter', 'Tetris', 'Tic Tac Toe'
]

# Output directory for icons
ICONS_DIR = 'icons'
LAUNCHER_ICON_NAME = 'game.ico' # Name for the main launcher icon

# Icon dimensions
ICON_SIZE = (128, 128) # Standard size for game icons
LAUNCHER_ICON_SIZE = (256, 256) # Larger for launcher icon

# Text and border colors
TEXT_COLOR = (255, 255, 255) # White text
BORDER_COLOR = (0, 77, 153) # Deep blue, matching launcher theme
BORDER_WIDTH = 4
FONT_SIZE = 60 # Increased font size for emojis
EMOJI_FONT_SIZE = 80 # Larger font size specifically for emojis on game cards

# Ensure the icons directory exists
os.makedirs(ICONS_DIR, exist_ok=True)

# Dictionary mapping game names to specific emojis
# These emojis will be used to generate the game icons.
GAME_EMOJIS = {
    'Aeroblasters': '✈️',
    'Angry Walls': '🧱',
    'Arc Dash': '⚡',
    'Asteroids': '☄️',
    'Bounce': '🏀',
    'Car Racing 2d': '�',
    'Cave Story': '🦇',
    'Connected': '🔗',
    'Dodgy Walls': '🚧',
    'Dots & Boxes': '🎲',
    'Egg Catching Game': '🥚',
    'Flappy Bird': '🐦',
    'GhostBusters': '👻',
    'Hangman': '😩',
    'Hex Dash': '🔷',
    'HyperTile Dash': '💠',
    'Jungle Dash': '🌿',
    'Level Designer': '📐',
    'Memory Puzzle': '🧠',
    'MineSweeper': '💣',
    'Piano Tiles': '🎹',
    'Picture Sliding Puzzle': '🖼️',
    'Pong': '🏓',
    'Qircle Rush': '⭕',
    'Rock Paper Scissor': '✊',
    'Rotate Dash': '🔄',
    'Snake': '🐍',
    'SpriteSheet Cutter': '✂️',
    'Tetris': '🟥',
    'Tic Tac Toe': '❌⭕',
    'default': '🎮' # Default emoji if not found in the list
}


def generate_vibrant_color():
    """Generates a random, vibrant background color."""
    # This function is now less critical for game icons, but kept for potential future use or other elements.
    hue = random.randint(0, 360)
    saturation = random.randint(70, 100) # High saturation
    lightness = random.randint(40, 70)   # Medium lightness
    try:
        import colorsys
        r, g, b = [int(x * 255) for x in colorsys.hls_to_rgb(hue/360, lightness/100, saturation/100)]
        return (r, g, b)
    except ImportError:
        return (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))


def get_font_path(is_emoji=False):
    """Tries to find a suitable font, prioritizing emoji fonts if requested."""
    font_paths = []
    if is_emoji:
        # Prioritize emoji fonts for better rendering on different OS
        font_paths.extend([
            '/System/Library/Fonts/Apple Color Emoji.ttc', # macOS
            'C:/Windows/Fonts/seguiemj.ttf', # Windows Segoe UI Emoji
            '/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf', # Linux Noto Color Emoji
            '/usr/share/fonts/opentype/noto/NotoColorEmoji.ttf', # Another common Linux path
        ])
    
    # General bold fonts as fallback or for non-emoji text
    font_paths.extend([
        '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', # Linux
        '/Library/Fonts/Arial Bold.ttf', # macOS
        'C:/Windows/Fonts/arialbd.ttf', # Windows
        'arialbd.ttf', # Fallback for local directory if available
        'arial.ttf',   # Another common fallback
    ])

    for path in font_paths:
        if os.path.exists(path):
            return path
    print("Warning: No suitable font found. Using default Pillow font (might not render emojis well).")
    return None

def generate_game_icon(game_name, icon_path):
    """
    Generates an icon for a game using a specific emoji on a subtle background.
    """
    try:
        # Use a consistent, subtle dark background for all game icons
        background_color = (25, 25, 40) # Dark blue-grey

        img = Image.new('RGB', ICON_SIZE, background_color)
        draw = ImageDraw.Draw(img)

        # Get the emoji for the game, default to generic if not found
        emoji = GAME_EMOJIS.get(game_name, GAME_EMOJIS['default'])

        # Load an emoji-compatible font
        font_path = get_font_path(is_emoji=True)
        try:
            # Use EMOJI_FONT_SIZE for game icons
            font = ImageFont.truetype(font_path, EMOJI_FONT_SIZE) if font_path else ImageFont.load_default()
        except IOError:
            font = ImageFont.load_default()
            print(f"Could not load emoji font from {font_path}. Using default Pillow font for emoji.")

        # Get text size and position to center it
        # textbbox works better for emoji sizing than textsize
        bbox = draw.textbbox((0, 0), emoji, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        x = (ICON_SIZE[0] - text_width) / 2
        y = (ICON_SIZE[1] - text_height) / 2
        
        # Draw the emoji
        draw.text((x, y), emoji, fill=TEXT_COLOR, font=font)

        # Add a border
        for i in range(BORDER_WIDTH):
            draw.rectangle((i, i, ICON_SIZE[0] - 1 - i, ICON_SIZE[1] - 1 - i), outline=BORDER_COLOR)

        img.save(icon_path, "PNG")
        print(f"Generated icon: {icon_path}")
    except Exception as e:
        print(f"Error generating icon for {game_name}: {e}")

def generate_launcher_icon(output_path):
    """Generates a simple launcher icon with a game controller emoji."""
    try:
        img = Image.new('RGB', LAUNCHER_ICON_SIZE, color = (30, 60, 90)) # Dark blue background
        draw = ImageDraw.Draw(img)

        font_path = get_font_path(is_emoji=True) # Use emoji font for launcher icon
        try:
            font = ImageFont.truetype(font_path, 100) if font_path else ImageFont.load_default()
        except IOError:
            font = ImageFont.load_default()
            print(f"Could not load emoji font for launcher. Using default Pillow font.")


        text = "🎮" # Game controller emoji
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        x = (LAUNCHER_ICON_SIZE[0] - text_width) / 2
        y = (LAUNCHER_ICON_SIZE[1] - text_height) / 2
        draw.text((x, y), text, fill=(255, 255, 255), font=font) # White emoji

        # Save as ICO with multiple sizes for best display across Windows
        img.save(output_path, "ICO", sizes=[(s,s) for s in [16, 24, 32, 48, 64, 128, 256]])
        print(f"Generated launcher icon: {output_path}")
    except Exception as e:
        print(f"Error generating launcher icon: {e}")

def generate_generic_game_icon():
    """Generates a generic fallback icon (a question mark on grey)."""
    try:
        img = Image.new('RGB', ICON_SIZE, color = (50, 50, 50)) # Grey background
        draw = ImageDraw.Draw(img)

        font_path = get_font_path(is_emoji=True) # Use emoji font for generic icon
        font_size = FONT_SIZE # Initialize font_size here
        try:
            font = ImageFont.truetype(font_path, font_size) if font_path else ImageFont.load_default()
        except IOError:
            font = ImageFont.load_default()
            font_size = 40 # Default fallback size if font loading fails
            print(f"Could not load emoji font for generic icon. Using default Pillow font.")

        text = "?" # Question mark
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        x = (ICON_SIZE[0] - text_width) / 2
        y = (ICON_SIZE[1] - text_height) / 2
        draw.text((x, y), text, fill=(200, 200, 200), font=font) # Light grey text

        img.save(os.path.join(ICONS_DIR, "generic_game.png"), "PNG")
        print(f"Generated generic icon: {os.path.join(ICONS_DIR, 'generic_game.png')}")
    except Exception as e:
        print(f"Error generating generic icon: {e}")

if __name__ == "__main__":
    # Generate individual game icons
    for game in GAME_NAMES:
        # Normalize game name for filename (lowercase, replace spaces with underscores, handle '&')
        # This must match the logic in GameCard.setup_ui for icon lookup
        filename_game_name = game.lower().replace(' ', '_').replace('&', 'and')
        icon_filename = f"{filename_game_name}.png"
        icon_path = os.path.join(ICONS_DIR, icon_filename)
        generate_game_icon(game, icon_path)

    # Generate the main launcher icon
    generate_launcher_icon(LAUNCHER_ICON_NAME)

    # Generate the generic fallback game icon
    generate_generic_game_icon()

    print("\nIcon generation complete.")
    print(f"Please ensure '{LAUNCHER_ICON_NAME}' is in the same directory as 'launch.py'.")
    print(f"All game icons are in the '{ICONS_DIR}' folder.")
    print("You can now run your 'launch.py' script.")
