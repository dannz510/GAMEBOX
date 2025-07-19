import os
import pygame
import pickle
from pygame.locals import *

# SETUP *****************************************
pygame.init()
SCREEN = WIDTH, HEIGHT = 512, 288  # Landscape resolution
try:
    win = pygame.display.set_mode(SCREEN, pygame.NOFRAME)
    pygame.display.set_caption('Connected')
except pygame.error as e:
    print(f"Display initialization failed: {e}")
    exit()

clock = pygame.time.Clock()
FPS = 45

TILE_SIZE = 16
ROWS, COLS = HEIGHT // TILE_SIZE, WIDTH // TILE_SIZE

# Level Variables
NUM_TILES = 88
current_level = 1

# FONTS *****************************************
pygame.font.init()
font = pygame.font.SysFont('Bauhaus 93', 20)

# COLORS ***************************************
WHITE = (255, 255, 255)
BLUE = (30, 144, 255)
RED = (255, 0, 0)

if not os.path.exists('levels/'):
    try:
        os.mkdir('levels/')
        print("Created 'levels' directory.")
    except OSError as e:
        print(f"Failed to create 'levels' directory: {e}")
        exit()

# Images ****************************************
try:
    bg = pygame.image.load("Assets/bg.png")
    bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
except pygame.error as e:
    print(f"Failed to load background image: {e}")
    exit()

# Empty world data
world_data = []
for r in range(ROWS):
    c = [0] * COLS
    world_data.append(c)

# Load tiles
tiles = []
for t in range(1, NUM_TILES + 1):
    try:
        tile = pygame.image.load(f"tiles/{t}.png")
        tiles.append(tile)
    except pygame.error as e:
        print(f"Failed to load tile {t}.png: {e}")
        tiles.append(pygame.Surface((TILE_SIZE, TILE_SIZE)))  # Placeholder

# FUNCTIONS ************************************
def draw_grid(win):
    for r in range(ROWS):
        pygame.draw.line(win, WHITE, (0, TILE_SIZE * r), (WIDTH, TILE_SIZE * r), 2)
    for c in range(COLS):
        pygame.draw.line(win, WHITE, (TILE_SIZE * c, 0), (TILE_SIZE * c, HEIGHT), 2)

def draw_text(text_, color, pos):
    text = font.render(text_, True, color)
    win.blit(text, pos)

def draw_box(r, c):
    t = TILE_SIZE
    pygame.draw.rect(win, BLUE, (c * t, r * t, t, t), 2)

def draw_world():
    for r_index, row in enumerate(world_data):
        for c_index, tile_value in enumerate(row):
            if tile_value > 0:
                win.blit(tiles[tile_value - 1], (c_index * TILE_SIZE, r_index * TILE_SIZE))

# BUTTONS
class Button:
    def __init__(self, pos, image, scale):
        self.image = pygame.transform.scale(image, (30, 16)) if scale else image
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.clicked = False

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                action = True
                self.clicked = True
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
        win.blit(self.image, self.rect)
        return action

# Load button images
try:
    load_img = pygame.image.load('assets/load_btn.png')
    save_img = pygame.image.load('assets/save_btn.png')
    clear_img = pygame.image.load('assets/clear.png')
except pygame.error as e:
    print(f"Failed to load button images: {e}")
    exit()

load_button = Button((WIDTH - 120, HEIGHT - 30), load_img, True)
save_button = Button((WIDTH - 80, HEIGHT - 30), save_img, True)
clear_button = Button((WIDTH - 40, HEIGHT - 30), clear_img, True)

# Tiles
tile_group = []
PALETTE_COLS = 4
tile_display_start_x = (COLS - PALETTE_COLS) * TILE_SIZE
tile_display_start_y = 0

class Tile:
    def __init__(self, pos, image, index):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.clicked = False
        self.index = index

    def update(self):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                action = self.index
                self.clicked = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        win.blit(self.image, self.rect)
        return action

for index, tile_img_asset in enumerate(tiles):
    column = index % PALETTE_COLS
    row = index // PALETTE_COLS
    pos = (tile_display_start_x + column * TILE_SIZE, tile_display_start_y + row * TILE_SIZE)
    t = Tile(pos, tile_img_asset, index + 1)
    tile_group.append(t)

# VARIABLES ************************************
clicked = False
pos = None
r, c = 0, 0

# Main
running = True
while running:
    win.blit(bg, (0, 0))

    selected_tile_index = None
    for tile_btn in tile_group:
        index = tile_btn.update()
        if index:
            selected_tile_index = index

    draw_grid(win)
    draw_world()
    draw_box(r, c)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                running = False
            if event.key == pygame.K_UP:
                r = max(0, r - 1)
            if event.key == pygame.K_DOWN:
                r = min(ROWS - 1, r + 1)
            if event.key == pygame.K_LEFT:
                c = max(0, c - 1)
            if event.key == pygame.K_RIGHT:
                c = min(COLS - 1, c + 1)
            if selected_tile_index is not None:
                world_data[r][c] = selected_tile_index
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if mouse_x < (COLS - PALETTE_COLS) * TILE_SIZE and mouse_y < ROWS * TILE_SIZE:
                r = mouse_y // TILE_SIZE
                c = mouse_x // TILE_SIZE
                if selected_tile_index is not None:
                    world_data[r][c] = selected_tile_index

    if save_button.draw():
        try:
            with open(f'levels/level{current_level}_data', 'wb') as pickle_out:
                pickle.dump(world_data, pickle_out)
            draw_text("Level Saved!", WHITE, (WIDTH - 150, HEIGHT - 100))
            print(f"Level {current_level} saved successfully.")
        except Exception as e:
            print(f"Failed to save level: {e}")
            draw_text("Save Failed!", RED, (WIDTH - 150, HEIGHT - 100))

    if load_button.draw():
        if os.path.exists(f'levels/level{current_level}_data'):
            try:
                with open(f'levels/level{current_level}_data', 'rb') as pickle_in:
                    world_data = pickle.load(pickle_in)
                draw_text("Level Loaded!", WHITE, (WIDTH - 150, HEIGHT - 100))
                print(f"Level {current_level} loaded successfully.")
            except Exception as e:
                print(f"Failed to load level: {e}")
                draw_text("Load Failed!", RED, (WIDTH - 150, HEIGHT - 100))
        else:
            draw_text("No level data found!", RED, (WIDTH - 180, HEIGHT - 100))

    if clear_button.draw():
        world_data[r][c] = 0

    clock.tick(FPS)
    pygame.display.update()

pygame.quit()