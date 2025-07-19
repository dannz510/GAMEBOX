import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
import colorsys
import math

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

# Global styling parameters
BORDER_COLOR = (0, 77, 153) # Deep blue, matching launcher theme
BORDER_WIDTH = 4
EMOJI_FONT_SIZE = 80 # Larger font size specifically for emojis (launcher icon)

# Ensure the icons directory exists
os.makedirs(ICONS_DIR, exist_ok=True)

# --- Thematic Icon Data with Modern Colors ---
# Map game names to a primary color hue and a simple shape/concept.
# 'colors' now define a gradient for the background.
# 'shape_color' is for the main graphic.
GAME_THEMES = {
    'Aeroblasters': {'shape': 'plane', 'colors': [(20, 50, 80), (60, 120, 180)], 'shape_color': (150, 200, 255)}, # Deep blue to light blue, metallic plane
    'Angry Walls': {'shape': 'brick_wall', 'colors': [(80, 40, 20), (150, 80, 40)], 'shape_color': (200, 100, 50)}, # Earthy browns, red brick
    'Arc Dash': {'shape': 'lightning_bolt', 'colors': [(50, 50, 0), (200, 200, 0)], 'shape_color': (255, 255, 100)}, # Dark to bright yellow, electric
    'Asteroids': {'shape': 'asteroid', 'colors': [(30, 0, 60), (80, 20, 120)], 'shape_color': (180, 150, 220)}, # Deep space purple, rocky asteroid
    'Bounce': {'shape': 'bouncing_ball', 'colors': [(0, 60, 0), (50, 180, 50)], 'shape_color': (100, 255, 100)}, # Forest to lime green, bouncy ball
    'Car Racing 2d': {'shape': 'race_car', 'colors': [(80, 0, 0), (180, 20, 20)], 'shape_color': (255, 80, 80)}, # Dark to bright red, fast car
    'Cave Story': {'shape': 'cave_entrance', 'colors': [(40, 40, 40), (80, 80, 80)], 'shape_color': (120, 120, 120)}, # Grey to dark grey, stone cave
    'Connected': {'shape': 'chain_link', 'colors': [(60, 0, 90), (120, 40, 160)], 'shape_color': (200, 100, 255)}, # Deep violet, metallic link
    'Dodgy Walls': {'shape': 'hazard_wall', 'colors': [(100, 0, 100), (200, 50, 200)], 'shape_color': (255, 100, 255)}, # Dark to bright magenta, warning
    'Dots & Boxes': {'shape': 'game_grid', 'colors': [(0, 70, 30), (40, 150, 80)], 'shape_color': (100, 200, 150)}, # Dark to light teal, game board
    'Egg Catching Game': {'shape': 'egg', 'colors': [(100, 70, 0), (200, 140, 50)], 'shape_color': (255, 200, 100)}, # Warm orange, golden egg
    'Flappy Bird': {'shape': 'flying_bird', 'colors': [(0, 100, 80), (50, 200, 180)], 'shape_color': (100, 255, 230)}, # Blue-green, soaring bird
    'GhostBusters': {'shape': 'no_ghost', 'colors': [(100, 0, 0), (200, 50, 50)], 'shape_color': (255, 255, 255)}, # Red, white ghost
    'Hangman': {'shape': 'gallows_icon', 'colors': [(40, 40, 80), (80, 80, 160)], 'shape_color': (150, 150, 200)}, # Dark to light blue, stark gallows
    'Hex Dash': {'shape': 'hexagon_path', 'colors': [(60, 0, 120), (120, 50, 200)], 'shape_color': (200, 120, 255)}, # Deep purple, geometric
    'HyperTile Dash': {'shape': 'diamond_tile', 'colors': [(100, 30, 0), (200, 80, 30)], 'shape_color': (255, 150, 80)}, # Burnt orange, sharp edges
    'Jungle Dash': {'shape': 'jungle_leaf', 'colors': [(0, 80, 0), (50, 160, 50)], 'shape_color': (100, 220, 100)}, # Deep green, lush leaf
    'Level Designer': {'shape': 'blueprint', 'colors': [(30, 30, 60), (80, 80, 140)], 'shape_color': (150, 150, 200)}, # Dark blue, technical drawing
    'Memory Puzzle': {'shape': 'matching_squares', 'colors': [(80, 0, 50), (160, 40, 100)], 'shape_color': (220, 100, 180)}, # Deep rose, puzzle pieces
    'MineSweeper': {'shape': 'mine', 'colors': [(50, 0, 0), (120, 30, 30)], 'shape_color': (180, 80, 80)}, # Dark red, explosive
    'Piano Tiles': {'shape': 'piano_keys_icon', 'colors': [(0, 40, 80), (30, 100, 160)], 'shape_color': (200, 200, 200)}, # Dark blue, musical keys
    'Picture Sliding Puzzle': {'shape': 'puzzle_piece', 'colors': [(70, 70, 0), (150, 150, 40)], 'shape_color': (200, 200, 100)}, # Olive green, fragmented image
    'Pong': {'shape': 'pong_paddles', 'colors': [(0, 80, 40), (40, 160, 100)], 'shape_color': (100, 220, 150)}, # Emerald green, classic game
    'Qircle Rush': {'shape': 'concentric_circles_icon', 'colors': [(100, 50, 0), (200, 120, 50)], 'shape_color': (255, 180, 100)}, # Warm orange, target
    'Rock Paper Scissor': {'shape': 'fist_hand', 'colors': [(80, 0, 40), (160, 40, 80)], 'shape_color': (220, 100, 140)}, # Deep pink, hand gesture
    'Rotate Dash': {'shape': 'rotating_arrow', 'colors': [(70, 0, 70), (140, 30, 140)], 'shape_color': (200, 80, 200)}, # Dark purple, dynamic arrow
    'Snake': {'shape': 'snake_icon', 'colors': [(30, 80, 0), (80, 160, 50)], 'shape_color': (150, 220, 100)}, # Bright green, slithering snake
    'SpriteSheet Cutter': {'shape': 'scissors_icon', 'colors': [(0, 80, 100), (40, 160, 200)], 'shape_color': (100, 220, 255)}, # Teal blue, precise cutting
    'Tetris': {'shape': 'tetromino_block', 'colors': [(50, 0, 100), (100, 50, 200)], 'shape_color': (180, 100, 255)}, # Deep indigo, falling blocks
    'Tic Tac Toe': {'shape': 'x_o_grid', 'colors': [(100, 20, 0), (200, 70, 30)], 'shape_color': (255, 120, 80)}, # Burnt orange, classic grid
}


def get_font_path(is_emoji=False):
    """Tries to find a suitable font, prioritizing emoji fonts if requested."""
    font_paths = []
    if is_emoji:
        font_paths.extend([
            '/System/Library/Fonts/Apple Color Emoji.ttc', # macOS
            'C:/Windows/Fonts/seguiemj.ttf', # Windows Segoe UI Emoji
            '/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf', # Linux Noto Color Emoji
            '/usr/share/fonts/opentype/noto/NotoColorEmoji.ttf', # Another common Linux path
        ])
    
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
    return None

def draw_radial_gradient(img, draw, center, radius, start_color, end_color):
    """Draws a radial gradient on the image."""
    width, height = img.size
    max_radius = max(width, height) / 2
    
    # Generate gradient colors
    steps = int(max_radius)
    for i in range(steps):
        r = int(start_color[0] + (end_color[0] - start_color[0]) * i / (steps - 1))
        g = int(start_color[1] + (end_color[1] - start_color[1]) * i / (steps - 1))
        b = int(start_color[2] + (end_color[2] - start_color[2]) * i / (steps - 1))
        color = (r, g, b)
        
        current_radius = int(max_radius * (i + 1) / steps)
        # Draw a filled circle for each step
        draw.ellipse((center[0] - current_radius, center[1] - current_radius,
                      center[0] + current_radius, center[1] + current_radius),
                     fill=color)


# --- Shape Drawing Functions (Enhanced for thematic icons with 3D illusion) ---

def apply_bevel_effect(draw, shape_coords, base_color, highlight_color, shadow_color, width=2):
    """Applies a simple bevel effect to a polygon shape."""
    # Draw highlight (top-left)
    for i in range(width):
        highlight_coords = [(x + i, y + i) for x, y in shape_coords]
        draw.polygon(highlight_coords, outline=highlight_color)
    
    # Draw shadow (bottom-right)
    for i in range(width):
        shadow_coords = [(x - i, y - i) for x, y in shape_coords]
        draw.polygon(shadow_coords, outline=shadow_color)
    
    # Draw base shape
    draw.polygon(shape_coords, fill=base_color)


def draw_plane(d, cx, cy, size, fill, outline):
    # Plane body (main shape)
    body_points = [
        (cx - size * 0.3, cy - size * 0.1),
        (cx + size * 0.4, cy - size * 0.1),
        (cx + size * 0.5, cy),
        (cx + size * 0.4, cy + size * 0.1),
        (cx - size * 0.3, cy + size * 0.1),
        (cx - size * 0.4, cy)
    ]
    
    # Wings
    wing_fill = tuple(min(255, c + 30) for c in fill)
    wing_outline = tuple(max(0, c - 30) for c in outline)

    # Left wing
    d.polygon([
        (cx - size * 0.2, cy - size * 0.1),
        (cx - size * 0.5, cy - size * 0.4),
        (cx - size * 0.4, cy - size * 0.1)
    ], fill=wing_fill, outline=wing_outline, width=1)
    # Right wing
    d.polygon([
        (cx - size * 0.2, cy + size * 0.1),
        (cx - size * 0.5, cy + size * 0.4),
        (cx - size * 0.4, cy + size * 0.1)
    ], fill=wing_fill, outline=wing_outline, width=1)

    # Tail
    d.polygon([
        (cx + size * 0.4, cy - size * 0.1),
        (cx + size * 0.4, cy + size * 0.1),
        (cx + size * 0.6, cy)
    ], fill=wing_fill, outline=wing_outline, width=1)

    # Apply bevel to main body
    apply_bevel_effect(d, body_points, fill, (255,255,255,100), (0,0,0,100))


def draw_brick_wall(d, cx, cy, size, fill, outline):
    brick_width = size // 3
    brick_height = size // 5
    wall_x1 = cx - size // 2
    wall_y1 = cy - size // 2
    
    for r in range(int(size / brick_height)):
        row_offset = (r % 2) * (brick_width // 2)
        for c in range(int(size / brick_width) + 1):
            x1 = wall_x1 + c * brick_width - row_offset
            y1 = wall_y1 + r * brick_height
            x2 = x1 + brick_width
            y2 = y1 + brick_height
            
            # Simulate depth with darker fill for mortar lines
            mortar_color = tuple(max(0, val - 30) for val in fill)
            d.rectangle((x1, y1, x2, y2), fill=fill, outline=mortar_color, width=1)
            # Add subtle highlights/shadows to bricks
            d.line([(x1 + 1, y1 + 1), (x2 - 1, y1 + 1)], fill=(255,255,255,50)) # Top highlight
            d.line([(x1 + 1, y2 - 1), (x2 - 1, y2 - 1)], fill=(0,0,0,50)) # Bottom shadow


def draw_lightning_bolt(d, cx, cy, size, fill, outline):
    points = [
        (cx, cy - size * 0.4),
        (cx + size * 0.15, cy - size * 0.1),
        (cx + size * 0.4, cy - size * 0.2),
        (cx - size * 0.1, cy + size * 0.4),
        (cx - size * 0.25, cy + size * 0.1),
        (cx - size * 0.4, cy + size * 0.2)
    ]
    # Simulate glow effect
    glow_color = tuple(min(255, c + 50) for c in fill) + (100,) # Add alpha for transparency
    d.polygon(points, fill=glow_color, outline=outline, width=0) # Base glow
    
    # Draw main bolt
    apply_bevel_effect(d, points, fill, (255,255,255,150), (0,0,0,150))


def draw_asteroid(d, cx, cy, size, fill, outline):
    points = []
    num_points = random.randint(6, 10)
    for i in range(num_points):
        angle = 2 * math.pi * i / num_points
        radius_variation = random.uniform(0.6, 0.9)
        x = cx + size * 0.4 * radius_variation * math.cos(angle)
        y = cy + size * 0.4 * radius_variation * math.sin(angle)
        points.append((x, y))
    
    # Simulate rocky texture with inner polygons
    inner_fill = tuple(max(0, c - 20) for c in fill)
    d.polygon(points, fill=fill, outline=outline, width=2)
    
    # Add some darker patches for texture
    for _ in range(3):
        patch_points = []
        for _ in range(random.randint(3,5)):
            idx = random.randint(0, len(points) - 1)
            patch_points.append(points[idx])
        if len(patch_points) >= 3:
            d.polygon(patch_points, fill=inner_fill)


def draw_bouncing_ball(d, cx, cy, size, fill, outline):
    ball_radius = size * 0.4
    
    # Simulate sphere with radial gradient
    gradient_steps = 30
    gradient_colors = []
    for i in range(gradient_steps):
        factor = i / (gradient_steps - 1)
        r = int(fill[0] * (1 - factor) + outline[0] * factor)
        g = int(fill[1] * (1 - factor) + outline[1] * factor)
        b = int(fill[2] * (1 - factor) + outline[2] * factor)
        gradient_colors.append((r, g, b))
    
    draw_radial_gradient_sphere(d, (cx, cy), ball_radius, gradient_colors)
    
    # Add a subtle shadow on the ground
    shadow_color = (0, 0, 0, 80) # Semi-transparent black
    shadow_offset = size * 0.1
    d.ellipse((cx - ball_radius * 0.8, cy + ball_radius - shadow_offset,
               cx + ball_radius * 0.8, cy + ball_radius + shadow_offset), fill=shadow_color)


def draw_radial_gradient_sphere(draw, center, radius, colors):
    """Draws a radial gradient to simulate a sphere."""
    for i, color in enumerate(reversed(colors)): # Draw from outer to inner
        current_radius = radius * (i + 1) / len(colors)
        draw.ellipse((center[0] - current_radius, center[1] - current_radius,
                      center[0] + current_radius, center[1] + current_radius),
                     fill=color)


def draw_race_car(d, cx, cy, size, fill, outline):
    body_width = size * 0.7
    body_length = size * 0.4
    
    # Main body with bevel
    body_points = [
        (cx - body_width/2, cy - body_length/2),
        (cx + body_width/2, cy - body_length/2),
        (cx + body_width/2, cy + body_length/2),
        (cx - body_width/2, cy + body_length/2)
    ]
    apply_bevel_effect(d, body_points, fill, (255,255,255,100), (0,0,0,100))
    
    # Cockpit
    cockpit_fill = tuple(max(0, c - 50) for c in fill)
    d.rectangle((cx - body_width*0.2, cy - body_length*0.4, cx + body_width*0.2, cy + body_length*0.1), fill=cockpit_fill, outline=outline, width=1)

    # Wheels (with slight shadow)
    wheel_radius = size * 0.08
    wheel_offset_x = body_width/2 - wheel_radius
    wheel_offset_y = body_length/2 - wheel_radius
    wheel_color = (30, 30, 30)
    
    for x_mult in [-1, 1]:
        for y_mult in [-1, 1]:
            wheel_cx = cx + x_mult * wheel_offset_x
            wheel_cy = cy + y_mult * wheel_offset_y
            # Shadow
            d.ellipse((wheel_cx - wheel_radius + 2, wheel_cy - wheel_radius + 2,
                       wheel_cx + wheel_radius + 2, wheel_cy + wheel_radius + 2), fill=(0,0,0,80))
            d.ellipse((wheel_cx - wheel_radius, wheel_cy - wheel_radius,
                       wheel_cx + wheel_radius, wheel_cy + wheel_radius), fill=wheel_color, outline=outline, width=1)


def draw_cave_entrance(d, cx, cy, size, fill, outline):
    # Arch shape
    arch_points = []
    num_segments = 20
    for i in range(num_segments + 1):
        angle = math.pi * i / num_segments # From 0 to pi (180 degrees)
        x = cx - size // 2 * math.cos(angle)
        y = cy - size // 2 * math.sin(angle)
        arch_points.append((x, y))
    
    # Bottom corners
    arch_points.append((cx + size // 2, cy + size // 2))
    arch_points.append((cx - size // 2, cy + size // 2))

    apply_bevel_effect(d, arch_points, fill, (255,255,255,100), (0,0,0,100))
    
    # Dark interior
    inner_x1 = cx - size // 2 + int(size*0.1)
    inner_y1 = cy + int(size*0.1)
    inner_x2 = cx + size // 2 - int(size*0.1)
    inner_y2 = cy + size // 2
    d.rectangle((inner_x1, inner_y1, inner_x2, inner_y2), fill=(0,0,0), outline=(0,0,0), width=0)


def draw_chain_link(d, cx, cy, size, fill, outline):
    link_radius = size // 4
    link_thickness = int(size * 0.08)
    
    # Draw two links with overlap to simulate connection
    link1_coords = (cx - link_radius * 1.5, cy - link_radius, cx - link_radius * 0.5, cy + link_radius)
    link2_coords = (cx + link_radius * 0.5, cy - link_radius, cx + link_radius * 1.5, cy + link_radius)
    
    # Create temporary images for each link to handle overlap and blending
    temp_img = Image.new('RGBA', ICON_SIZE, (0,0,0,0))
    temp_draw = ImageDraw.Draw(temp_img)
    
    # Draw link 1
    temp_draw.ellipse(link1_coords, outline=fill, width=link_thickness)
    
    # Draw link 2 (offset to simulate overlap)
    temp_draw.ellipse(link2_coords, outline=fill, width=link_thickness)
    
    # Blend them onto the main image
    d.bitmap((0,0), temp_img, fill=fill) # Use fill to apply color to the outline


def draw_hazard_wall(d, cx, cy, size, fill, outline):
    # Yellow and black diagonal stripes
    stripe_width = size // 6
    for i in range(-int(size/stripe_width), int(size/stripe_width) + 1):
        color = (255, 204, 0) if i % 2 == 0 else (0, 0, 0)
        d.line([(0, i * stripe_width), (size, i * stripe_width + size)], fill=color, width=stripe_width * 2)
    
    # Draw a prominent warning sign (e.g., exclamation mark)
    warning_color = (255, 255, 255)
    font_path = get_font_path(is_emoji=False)
    try:
        font = ImageFont.truetype(font_path, int(size * 0.5)) if font_path else ImageFont.load_default()
    except IOError:
        font = ImageFont.load_default()
    
    text = "!"
    bbox = d.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    d.text((cx - text_width/2, cy - text_height/2), text, fill=warning_color, font=font)


def draw_game_grid(d, cx, cy, size, fill, outline):
    grid_spacing = size // 3
    start_x = cx - size // 2
    start_y = cy - size // 2
    
    # Draw grid lines
    for i in range(4):
        d.line([(start_x + i * grid_spacing, start_y), (start_x + i * grid_spacing, start_y + size)], fill=fill, width=2)
        d.line([(start_x, start_y + i * grid_spacing), (start_x + size, start_y + i * grid_spacing)], fill=fill, width=2)
    
    # Add subtle shading to grid cells for depth
    for r in range(3):
        for c in range(3):
            cell_x1 = start_x + c * grid_spacing
            cell_y1 = start_y + r * grid_spacing
            cell_x2 = cell_x1 + grid_spacing
            cell_y2 = cell_y1 + grid_spacing
            
            # Darker shade for bottom-right corner
            d.polygon([
                (cell_x1, cell_y2), (cell_x2, cell_y2), (cell_x2, cell_y1)
            ], fill=tuple(max(0, val - 30) for val in fill))


def draw_egg(d, cx, cy, size, fill, outline):
    egg_coords = (cx - size // 3, cy - size // 2, cx + size // 3, cy + size // 2)
    
    # Simulate egg shell texture with subtle noise
    temp_img = Image.new('RGB', ICON_SIZE, fill)
    temp_draw = ImageDraw.Draw(temp_img)
    temp_draw.ellipse(egg_coords, fill=fill, outline=outline, width=2)
    
    # Add some random pixels for texture
    for _ in range(100):
        x = random.randint(int(egg_coords[0]), int(egg_coords[2]))
        y = random.randint(int(egg_coords[1]), int(egg_coords[3]))
        temp_draw.point((x,y), fill=tuple(max(0, val - random.randint(5,15)) for val in fill))
    
    img_with_egg = Image.alpha_composite(Image.new('RGBA', ICON_SIZE, (0,0,0,0)), temp_img.convert('RGBA'))
    d.bitmap((0,0), img_with_egg, fill=fill)

    # Add a crack
    d.line([(cx - size // 4, cy - size // 8), (cx + size // 4, cy - size // 4)], fill=(200,200,200), width=1)
    d.line([(cx - size // 4, cy - size // 4), (cx + size // 4, cy - size // 8)], fill=(200,200,200), width=1)


def draw_flying_bird(d, cx, cy, size, fill, outline):
    # Simplified bird silhouette with dynamic wings
    body_width = size * 0.4
    body_height = size * 0.25
    wing_span = size * 0.7
    
    # Body (oval)
    d.ellipse((cx - body_width/2, cy - body_height/2, cx + body_width/2, cy + body_height/2), fill=fill, outline=outline, width=2)
    
    # Wings (two polygons for a more dynamic look)
    wing_fill = tuple(min(255, c + 20) for c in fill)
    wing_outline = tuple(max(0, c - 20) for c in outline)

    # Left wing
    d.polygon([
        (cx - body_width/2, cy - body_height/2),
        (cx - wing_span/2, cy - body_height/2 - size * 0.2), # Outer tip up
        (cx - body_width/4, cy - body_height/2 + size * 0.05) # Inner bend down
    ], fill=wing_fill, outline=wing_outline, width=1)
    
    # Right wing
    d.polygon([
        (cx + body_width/2, cy - body_height/2),
        (cx + wing_span/2, cy - body_height/2 - size * 0.2), # Outer tip up
        (cx + body_width/4, cy - body_height/2 + size * 0.05) # Inner bend down
    ], fill=wing_fill, outline=wing_outline, width=1)

    # Small eye
    d.ellipse((cx + body_width*0.1, cy - body_height*0.1, cx + body_width*0.2, cy), fill=(0,0,0))


def draw_no_ghost(d, cx, cy, size, fill, outline):
    # Red circle with diagonal line
    d.ellipse((cx - size // 2, cy - size // 2, cx + size // 2, cy + size // 2), outline=(200,0,0), width=int(size*0.1))
    d.line((cx - size // 2 * 0.7, cy - size // 2 * 0.7, cx + size // 2 * 0.7, cy + size // 2 * 0.7), fill=(200,0,0), width=int(size*0.1))
    
    # Ghost shape (white with subtle shading)
    ghost_fill = (255, 255, 255)
    ghost_outline = (150, 150, 150)
    
    ghost_points = [
        (cx - size * 0.25, cy - size * 0.3),
        (cx + size * 0.25, cy - size * 0.3),
        (cx + size * 0.25, cy + size * 0.1),
        (cx + size * 0.15, cy + size * 0.3),
        (cx, cy + size * 0.2),
        (cx - size * 0.15, cy + size * 0.3),
        (cx - size * 0.25, cy + size * 0.1)
    ]
    
    d.polygon(ghost_points, fill=ghost_fill, outline=ghost_outline, width=1)
    
    # Eyes
    eye_color = (50, 50, 50)
    d.ellipse((cx - size * 0.15, cy - size * 0.15, cx - size * 0.05, cy - size * 0.05), fill=eye_color)
    d.ellipse((cx + size * 0.05, cy - size * 0.15, cx + size * 0.15, cy - size * 0.05), fill=eye_color)


def draw_gallows_icon(d, cx, cy, size, fill, outline):
    # Gallows structure
    wood_color = (139, 69, 19) # Brown
    d.rectangle((cx - size // 4 - 5, cy - size // 2, cx - size // 4 + 5, cy + size // 2), fill=wood_color, outline=outline, width=1) # Vertical post
    d.rectangle((cx - size // 4, cy - size // 2 - 5, cx + size // 4, cy - size // 2 + 5), fill=wood_color, outline=outline, width=1) # Horizontal beam
    d.line([(cx + size // 4 - 5, cy - size // 2), (cx + size // 4 - 5, cy - size // 3)], fill=(100,100,100), width=2) # Rope
    
    # Small head outline
    head_radius = size * 0.08
    d.ellipse((cx + size // 4 - head_radius - 5, cy - size // 3 - head_radius, cx + size // 4 + head_radius - 5, cy - size // 3 + head_radius), outline=(200,200,200), width=1)


def draw_hexagon_path(d, cx, cy, size, fill, outline):
    points = []
    for i in range(6):
        angle_deg = 60 * i - 30
        angle_rad = math.pi / 180 * angle_deg
        points.append((cx + size // 2 * math.cos(angle_rad), cy + size // 2 * math.sin(angle_rad)))
    
    apply_bevel_effect(d, points, fill, (255,255,255,100), (0,0,0,100))
    
    # Inner path/arrow
    path_fill = tuple(min(255, c + 50) for c in fill)
    path_points = [
        (cx - size * 0.1, cy - size * 0.2), (cx + size * 0.1, cy - size * 0.2),
        (cx + size * 0.2, cy), (cx + size * 0.1, cy + size * 0.2),
        (cx - size * 0.1, cy + size * 0.2), (cx - size * 0.2, cy)
    ]
    d.polygon(path_points, fill=path_fill, outline=outline, width=1)


def draw_diamond_tile(d, cx, cy, size, fill, outline):
    diamond_points = [
        (cx, cy - size // 2),
        (cx + size // 2, cy),
        (cx, cy + size // 2),
        (cx - size // 2, cy)
    ]
    apply_bevel_effect(d, diamond_points, fill, (255,255,255,100), (0,0,0,100))
    
    # Inner pattern (e.g., smaller diamond with different color)
    inner_fill = tuple(min(255, c + 50) for c in fill)
    inner_diamond_points = [
        (cx, cy - size // 4),
        (cx + size // 4, cy),
        (cx, cy + size // 4),
        (cx - size // 4, cy)
    ]
    d.polygon(inner_diamond_points, fill=inner_fill, outline=outline, width=1)


def draw_jungle_leaf(d, cx, cy, size, fill, outline):
    # More organic leaf shape
    leaf_points = [
        (cx, cy - size * 0.4),
        (cx + size * 0.3, cy - size * 0.2),
        (cx + size * 0.4, cy + size * 0.1),
        (cx + size * 0.2, cy + size * 0.4),
        (cx, cy + size * 0.3),
        (cx - size * 0.2, cy + size * 0.4),
        (cx - size * 0.4, cy + size * 0.1),
        (cx - size * 0.3, cy - size * 0.2)
    ]
    apply_bevel_effect(d, leaf_points, fill, (255,255,255,80), (0,0,0,80))
    
    # Central vein
    d.line([(cx, cy - size * 0.3), (cx, cy + size * 0.2)], fill=outline, width=1)
    # Side veins
    d.line([(cx - size * 0.15, cy - size * 0.1), (cx - size * 0.05, cy + size * 0.05)], fill=outline, width=1)
    d.line([(cx + size * 0.15, cy - size * 0.1), (cx + size * 0.05, cy + size * 0.05)], fill=outline, width=1)


def draw_blueprint(d, cx, cy, size, fill, outline):
    # Ruler and compass for blueprint
    ruler_fill = tuple(min(255, c + 20) for c in fill)
    d.rectangle((cx - size // 2, cy - size // 8, cx + size // 2, cy + size // 8), fill=ruler_fill, outline=outline, width=2)
    # Markings on ruler
    for i in range(-2, 3):
        d.line([(cx + i * size // 5, cy - size // 8), (cx + i * size // 5, cy + size // 8)], fill=outline, width=1)
    
    # Compass (two lines forming an angle)
    compass_color = (200, 200, 200)
    d.line([(cx - size // 4, cy - size // 4), (cx + size // 4, cy + size // 4)], fill=compass_color, width=2)
    d.line([(cx + size // 4, cy - size // 4), (cx - size // 4, cy + size // 4)], fill=compass_color, width=2)


def draw_matching_squares(d, cx, cy, size, fill, outline):
    square_size = size // 3
    square_fill = tuple(min(255, c + 30) for c in fill)
    
    # Two squares with a subtle gap
    s1_coords = (cx - square_size * 1.5, cy - square_size // 2, cx - square_size // 2, cy + square_size // 2)
    s2_coords = (cx + square_size // 2, cy - square_size // 2, cx + square_size * 1.5, cy + square_size // 2)
    
    d.rectangle(s1_coords, fill=square_fill, outline=outline, width=2)
    d.rectangle(s2_coords, fill=square_fill, outline=outline, width=2)
    
    # Add a subtle glow/shadow to each square
    glow_color = (255,255,255,50)
    shadow_color = (0,0,0,50)
    d.rectangle((s1_coords[0]+1, s1_coords[1]+1, s1_coords[2]-1, s1_coords[1]+2), fill=glow_color)
    d.rectangle((s1_coords[0]+1, s1_coords[3]-2, s1_coords[2]-1, s1_coords[3]-1), fill=shadow_color)
    d.rectangle((s2_coords[0]+1, s2_coords[1]+1, s2_coords[2]-1, s2_coords[1]+2), fill=glow_color)
    d.rectangle((s2_coords[0]+1, s2_coords[3]-2, s2_coords[2]-1, s2_coords[3]-1), fill=shadow_color)


def draw_mine(d, cx, cy, size, fill, outline):
    mine_radius = size * 0.4
    
    # Main body of the mine (sphere-like)
    draw_radial_gradient_sphere(d, (cx, cy), mine_radius, get_gradient_colors(fill, outline, 30))
    
    # Spikes
    spike_length = size * 0.15
    spike_thickness = 2
    for angle_deg in range(0, 360, 45):
        angle_rad = math.radians(angle_deg)
        x1 = cx + mine_radius * math.cos(angle_rad)
        y1 = cy + mine_radius * math.sin(angle_rad)
        x2 = cx + (mine_radius + spike_length) * math.cos(angle_rad)
        y2 = cy + (mine_radius + spike_length) * math.sin(angle_rad)
        d.line([(x1, y1), (x2, y2)], fill=outline, width=spike_thickness)
    
    # Fuse
    fuse_color = (150, 100, 50)
    d.line([(cx, cy - mine_radius), (cx + size * 0.1, cy - mine_radius - size * 0.2)], fill=fuse_color, width=2)


def draw_piano_keys_icon(d, cx, cy, size, fill, outline):
    key_width = size // 5
    key_height = size // 2
    
    # White keys with subtle bevel
    for i in range(-2, 3):
        x = cx + i * key_width - key_width // 2
        key_coords = (x, cy - key_height, x + key_width, cy + key_height)
        apply_bevel_effect(d, [(key_coords[0], key_coords[1]), (key_coords[2], key_coords[1]),
                                (key_coords[2], key_coords[3]), (key_coords[0], key_coords[3])],
                           (255,255,255), (255,255,255,100), (0,0,0,100))
    
    # Black keys (smaller, offset, with bevel)
    black_key_width = key_width // 2
    black_key_height = key_height // 2
    black_key_fill = (50, 50, 50)
    
    black_key_offsets = [-1.5, -0.5, 0.5, 1.5] # Positions relative to center
    for offset_mult in black_key_offsets:
        x = cx + offset_mult * key_width - black_key_width // 2
        black_key_coords = (x, cy - key_height, x + black_key_width, cy - key_height + black_key_height)
        apply_bevel_effect(d, [(black_key_coords[0], black_key_coords[1]), (black_key_coords[2], black_key_coords[1]),
                                (black_key_coords[2], black_key_coords[3]), (black_key_coords[0], black_key_coords[3])],
                           black_key_fill, (255,255,255,80), (0,0,0,80))


def draw_puzzle_piece(d, cx, cy, size, fill, outline):
    piece_size = size * 0.6
    half_piece = piece_size / 2
    notch_size = piece_size / 6

    points = [
        (cx - half_piece, cy - half_piece),
        (cx + half_piece, cy - half_piece),
        (cx + half_piece, cy - notch_size),
        (cx + half_piece + notch_size, cy - notch_size),
        (cx + half_piece + notch_size, cy + notch_size),
        (cx + half_piece, cy + notch_size),
        (cx + half_piece, cy + half_piece),
        (cx - half_piece, cy + half_piece),
        (cx - notch_size, cy + half_piece + notch_size),
        (cx - notch_size, cy + half_piece + notch_size), # This line is redundant, but harmless
        (cx + notch_size, cy + half_piece + notch_size),
        (cx + notch_size, cy + half_piece),
        (cx - half_piece, cy + half_piece)
    ]
    
    apply_bevel_effect(d, points, fill, (255,255,255,100), (0,0,0,100))


def draw_pong_paddles(d, cx, cy, size, fill, outline):
    paddle_width = size // 8
    paddle_height = size // 2
    ball_radius = size // 10
    
    # Paddles with bevel
    paddle1_coords = (cx - size // 2, cy - paddle_height // 2, cx - size // 2 + paddle_width, cy + paddle_height // 2)
    paddle2_coords = (cx + size // 2 - paddle_width, cy - paddle_height // 2, cx + size // 2, cy + paddle_height // 2)
    
    apply_bevel_effect(d, [(paddle1_coords[0], paddle1_coords[1]), (paddle1_coords[2], paddle1_coords[1]),
                            (paddle1_coords[2], paddle1_coords[3]), (paddle1_coords[0], paddle1_coords[3])],
                       fill, (255,255,255,100), (0,0,0,100))
    apply_bevel_effect(d, [(paddle2_coords[0], paddle2_coords[1]), (paddle2_coords[2], paddle2_coords[1]),
                            (paddle2_coords[2], paddle2_coords[3]), (paddle2_coords[0], paddle2_coords[3])],
                       fill, (255,255,255,100), (0,0,0,100))
    
    # Ball with radial gradient
    draw_radial_gradient_sphere(d, (cx, cy), ball_radius, get_gradient_colors(fill, outline, 20))


def draw_concentric_circles_icon(d, cx, cy, size, fill, outline):
    # Multiple concentric circles with depth
    for i in range(3):
        radius = size // 2 - i * (size // 6)
        # Simulate depth by drawing slightly offset circles
        d.ellipse((cx - radius + 1, cy - radius + 1, cx + radius + 1, cy + radius + 1), outline=(0,0,0,80), width=2) # Shadow
        d.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), outline=fill, width=2) # Main circle


def draw_fist_hand(d, cx, cy, size, fill, outline):
    # Simplified fist shape
    fist_points = [
        (cx - size * 0.3, cy - size * 0.2),
        (cx + size * 0.2, cy - size * 0.3),
        (cx + size * 0.4, cy),
        (cx + size * 0.2, cy + size * 0.3),
        (cx - size * 0.3, cy + size * 0.2),
        (cx - size * 0.4, cy)
    ]
    apply_bevel_effect(d, fist_points, fill, (255,255,255,100), (0,0,0,100))
    
    # Knuckle lines
    d.line([(cx - size * 0.1, cy - size * 0.1), (cx + size * 0.1, cy - size * 0.1)], fill=outline, width=1)
    d.line([(cx - size * 0.1, cy), (cx + size * 0.1, cy)], fill=outline, width=1)


def draw_rotating_arrow(d, cx, cy, size, fill, outline):
    # Circular arrow with a sense of motion
    d.arc((cx - size // 2, cy - size // 2, cx + size // 2, cy + size // 2), 0, 270, fill=fill, width=int(size*0.1))
    
    # Arrowhead with bevel
    arrow_tip_x = cx + size // 2 * math.cos(math.radians(270))
    arrow_tip_y = cy + size // 2 * math.sin(math.radians(270))
    arrowhead_points = [
        (arrow_tip_x, arrow_tip_y),
        (arrow_tip_x + size * 0.1, arrow_tip_y - size * 0.1),
        (arrow_tip_x - size * 0.1, arrow_tip_y - size * 0.1)
    ]
    apply_bevel_effect(d, arrowhead_points, fill, (255,255,255,100), (0,0,0,100))


def draw_snake_icon(d, cx, cy, size, fill, outline):
    # Wavy snake body
    points = []
    for i in range(15): # More points for smoother curve
        x = cx - size // 2 + i * (size / 14)
        y = cy + math.sin(i * math.pi / 4) * size // 6
        points.append((x, y))
    d.line(points, fill=fill, width=int(size*0.1), joint="curve")
    
    # Head (more defined)
    head_radius = size * 0.1
    d.ellipse((points[-1][0] - head_radius, points[-1][1] - head_radius,
               points[-1][0] + head_radius, points[-1][1] + head_radius), fill=fill, outline=outline, width=1)
    # Eyes
    eye_color = (0,0,0)
    d.ellipse((points[-1][0] - head_radius/2, points[-1][1] - head_radius/2,
               points[-1][0] - head_radius/4, points[-1][1] - head_radius/4), fill=eye_color)
    d.ellipse((points[-1][0] + head_radius/4, points[-1][1] - head_radius/2,
               points[-1][0] + head_radius/2, points[-1][1] - head_radius/4), fill=eye_color)
    # Tongue
    d.line([(points[-1][0], points[-1][1]), (points[-1][0] + size * 0.08, points[-1][1] + size * 0.08)], fill=(255,0,0), width=1)
    d.line([(points[-1][0], points[-1][1]), (points[-1][0] + size * 0.08, points[-1][1] - size * 0.08)], fill=(255,0,0), width=1)


def draw_scissors_icon(d, cx, cy, size, fill, outline):
    blade_length = size * 0.6
    blade_width = size * 0.1
    
    # Blade 1 with bevel
    blade1_points = [
        (cx - blade_length / 2, cy - blade_width / 2),
        (cx + blade_length / 2, cy - blade_width / 2),
        (cx + blade_length / 2, cy + blade_width / 2),
        (cx - blade_length / 2, cy + blade_width / 2)
    ]
    apply_bevel_effect(d, blade1_points, fill, (255,255,255,100), (0,0,0,100))

    # Blade 2 (rotated with bevel)
    angle = math.radians(45)
    rotated_points = []
    for x, y in blade1_points:
        new_x = cx + (x - cx) * math.cos(angle) - (y - cy) * math.sin(angle)
        new_y = cy + (x - cx) * math.sin(angle) + (y - cy) * math.cos(angle)
        rotated_points.append((new_x, new_y))
    apply_bevel_effect(d, rotated_points, fill, (255,255,255,100), (0,0,0,100))

    # Finger holes (with inner shadow)
    hole_radius = size * 0.1
    hole_color = (0,0,0)
    
    d.ellipse((cx - hole_radius, cy - hole_radius, cx + hole_radius, cy + hole_radius), fill=hole_color, outline=outline, width=1)
    d.ellipse((cx - hole_radius + 2, cy - hole_radius + 2, cx + hole_radius - 2, cy + hole_radius - 2), fill=outline) # Inner highlight


def draw_tetromino_block(d, cx, cy, size, fill, outline):
    block_unit = size // 4
    
    # L-shape tetromino
    blocks = [
        (cx - block_unit * 1.5, cy - block_unit * 0.5, cx - block_unit * 0.5, cy + block_unit * 0.5), # Top-left
        (cx - block_unit * 0.5, cy - block_unit * 0.5, cx + block_unit * 0.5, cy + block_unit * 0.5), # Top-middle
        (cx + block_unit * 0.5, cy - block_unit * 0.5, cx + block_unit * 1.5, cy + block_unit * 0.5), # Top-right
        (cx - block_unit * 1.5, cy + block_unit * 0.5, cx - block_unit * 0.5, cy + block_unit * 1.5)  # Bottom-left
    ]
    
    for block_coords in blocks:
        apply_bevel_effect(d, [(block_coords[0], block_coords[1]), (block_coords[2], block_coords[1]),
                                (block_coords[2], block_coords[3]), (block_coords[0], block_coords[3])],
                           fill, (255,255,255,100), (0,0,0,100))


def draw_x_o_grid(d, cx, cy, size, fill, outline):
    grid_spacing = size // 3
    start_x = cx - size // 2
    start_y = cy - size // 2

    # Grid lines with bevel
    line_color = fill # Use fill color for lines
    d.line([(start_x + grid_spacing, start_y), (start_x + grid_spacing, start_y + size)], fill=line_color, width=2)
    d.line([(start_x + grid_spacing * 2, start_y), (start_x + grid_spacing * 2, start_y + size)], fill=line_color, width=2)
    d.line([(start_x, start_y + grid_spacing), (start_x + size, start_y + grid_spacing)], fill=line_color, width=2)
    d.line([(start_x, start_y + grid_spacing * 2), (start_x + size, start_y + grid_spacing * 2)], fill=line_color, width=2)

    # Draw X and O with bevel
    x_color = (255, 50, 50) # Red
    o_color = (50, 50, 255) # Blue
    
    # X in top-left
    x_cx, x_cy = start_x + grid_spacing // 2, start_y + grid_spacing // 2
    x_offset = grid_spacing // 4
    x_points = [
        (x_cx - x_offset, x_cy - x_offset), (x_cx + x_offset, x_cy + x_offset),
        (x_cx - x_offset, x_cy + x_offset), (x_cx + x_offset, x_cy - x_offset)
    ]
    d.line([(x_cx - x_offset, x_cy - x_offset), (x_cx + x_offset, x_cy + x_offset)], fill=x_color, width=3)
    d.line([(x_cx - x_offset, x_cy + x_offset), (x_cx + x_offset, x_cy - x_offset)], fill=x_color, width=3)

    # O in bottom-right
    o_cx, o_cy = start_x + grid_spacing * 2.5, start_y + grid_spacing * 2.5
    o_radius = grid_spacing // 3
    d.ellipse((o_cx - o_radius, o_cy - o_radius, o_cx + o_radius, o_cy + o_radius), outline=o_color, width=3)


# Map shape names to drawing functions
shape_draw_functions = {
    'plane': draw_plane,
    'brick_wall': draw_brick_wall,
    'lightning_bolt': draw_lightning_bolt,
    'asteroid': draw_asteroid,
    'bouncing_ball': draw_bouncing_ball,
    'race_car': draw_race_car,
    'cave_entrance': draw_cave_entrance,
    'chain_link': draw_chain_link,
    'hazard_wall': draw_hazard_wall,
    'game_grid': draw_game_grid,
    'egg': draw_egg,
    'flying_bird': draw_flying_bird,
    'no_ghost': draw_no_ghost,
    'gallows_icon': draw_gallows_icon,
    'hexagon_path': draw_hexagon_path,
    'diamond_tile': draw_diamond_tile,
    'jungle_leaf': draw_jungle_leaf,
    'blueprint': draw_blueprint,
    'matching_squares': draw_matching_squares,
    'mine': draw_mine,
    'piano_keys_icon': draw_piano_keys_icon,
    'puzzle_piece': draw_puzzle_piece,
    'pong_paddles': draw_pong_paddles,
    'concentric_circles_icon': draw_concentric_circles_icon,
    'fist_hand': draw_fist_hand,
    'rotating_arrow': draw_rotating_arrow,
    'snake_icon': draw_snake_icon,
    'scissors_icon': draw_scissors_icon,
    'tetromino_block': draw_tetromino_block,
    'x_o_grid': draw_x_o_grid,
    'default': lambda d, cx, cy, size, fill, outline: d.rectangle((cx - size//3, cy - size//3, cx + size//3, cy + size//3), fill=fill, outline=outline, width=2) # Default square
}


def generate_game_icon(game_name, icon_path):
    """
    Generates a more beautiful and thematic icon for a game.
    """
    try:
        theme = GAME_THEMES.get(game_name, {'shape': 'default', 'colors': [(50,50,50), (100,100,100)], 'shape_color': (150,150,150)})
        start_color = theme['colors'][0]
        end_color = theme['colors'][1]
        shape_type = theme['shape']
        shape_color = theme['shape_color']

        img = Image.new('RGB', ICON_SIZE)
        draw = ImageDraw.Draw(img)

        # Draw a radial gradient background for more depth
        draw_radial_gradient(img, draw, (ICON_SIZE[0]//2, ICON_SIZE[1]//2), ICON_SIZE[0]//2, start_color, end_color)

        # Calculate center for shapes
        center_x, center_y = ICON_SIZE[0] // 2, ICON_SIZE[1] // 2
        shape_size = ICON_SIZE[0] * 0.6 # Size of the central shape

        # Draw thematic shape
        # Pass shape_color as fill and a darker version as outline
        drawing_function = shape_draw_functions.get(shape_type, shape_draw_functions['default'])
        drawing_function(draw, center_x, center_y, shape_size, shape_color, tuple(max(0, c - 50) for c in shape_color))

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

        font_path = get_font_path(is_emoji=False) # Not an emoji font for generic abbreviation
        try:
            font = ImageFont.truetype(font_path, 40) if font_path else ImageFont.load_default() # Use a fixed size for '?'
        except IOError:
            font = ImageFont.load_default()
            print(f"Could not load font for generic icon. Using default Pillow font.")

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
