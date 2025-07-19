import pygame
import pickle
import os
from objects import World, load_level, Button, Player, Portal, game_data, SIZE, WIDTH, HEIGHT

# Initialize Pygame
print("Initializing Pygame...")
pygame.init()
try:
    win = pygame.display.set_mode(SIZE, pygame.SCALED | pygame.FULLSCREEN)
    print("Pygame initialized. Window created.")
except pygame.error as e:
    print(f"Display initialization failed: {e}")
    exit()

clock = pygame.time.Clock()
FPS = 40

tile_size = 16

# Load Images
print("Loading background image...")
try:
    bg = pygame.image.load("Assets/bg.png")
    bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
    print("Background image loaded.")
except pygame.error as e:
    print(f"Failed to load background image: {e}")
    exit()

print("Loading Cave Story title image...")
try:
    cave_story = pygame.image.load("Assets/cave_story.png")
    cave_story = pygame.transform.scale(cave_story, (250, 150))
    print("Cave Story title image loaded.")
except pygame.error as e:
    print(f"Failed to load Cave Story image: {e}")
    exit()

print("Loading game won image...")
try:
    game_won_img = pygame.image.load("Assets/win.png")
    game_won_img = pygame.transform.scale(game_won_img, (250, 150))
    print("Game won image loaded.")
except pygame.error as e:
    print(f"Failed to load game won image: {e}")
    exit()

# Load Sounds
print("Loading music...")
try:
    pygame.mixer.music.load('Sounds/goodbyte_sad-rpg-town.mp3')
    pygame.mixer.music.play(loops=-1)
    print("Music loaded and playing.")
except pygame.error as e:
    print(f"Failed to load music: {e}")
    exit()

print("Loading replay sound effect...")
try:
    replay_fx = pygame.mixer.Sound('Sounds/replay.wav')
    print("Replay sound effect loaded.")
except pygame.error as e:
    print(f"Failed to load replay sound: {e}")
    exit()

# Load Button Images
print("Loading movement button image...")
try:
    move_btn_img = pygame.image.load("Assets/movement.jpeg")
    move_btn_img = pygame.transform.scale(move_btn_img, (80, HEIGHT))
    print("Movement button image loaded.")
except pygame.error as e:
    print(f"Failed to load movement button image: {e}")
    exit()

print("Loading play button image...")
try:
    play_img = pygame.image.load("Assets/play.png")
    play_btn = Button(play_img, (150, 60), WIDTH // 2 - 75, HEIGHT // 2 - 30)
    print("Play button created.")
except pygame.error as e:
    print(f"Failed to load play button image: {e}")
    exit()

print("Loading quit button image...")
try:
    quit_img = pygame.image.load("Assets/quit.png")
    quit_btn = Button(quit_img, (150, 60), WIDTH // 2 - 75, HEIGHT // 2 + 40)
    print("Quit button created.")
except pygame.error as e:
    print(f"Failed to load quit button image: {e}")
    exit()

print("Loading replay button image...")
try:
    replay_img = pygame.image.load("Assets/replay.png")
    replay_btn = Button(replay_img, (40, 40), WIDTH // 2 - 20, HEIGHT // 2 - 50)
    print("Replay button created.")
except pygame.error as e:
    print(f"Failed to load replay button image: {e}")
    exit()

print("Loading sound control images...")
try:
    sound_off_img = pygame.image.load("Assets/sound_off.png")
    sound_on_img = pygame.image.load("Assets/sound_on.png")
    sound_btn = Button(sound_on_img, (40, 40), WIDTH // 2 - 20, HEIGHT // 2 + 10)
    print("Sound buttons created.")
except pygame.error as e:
    print(f"Failed to load sound control images: {e}")
    exit()

# Variables
current_level = 1
MAX_LEVEL = 3
show_keys = True
pressed_keys = [False, False, False, False]  # [Up, Down, Left, Right]

dir_dict = {
    'Up': pygame.Rect(10, HEIGHT // 2 - 80, 60, 50),
    'Down': pygame.Rect(10, HEIGHT // 2 + 30, 60, 50),
    'Left': pygame.Rect(10, HEIGHT // 2 - 20, 60, 20),
    'Right': pygame.Rect(10, HEIGHT // 2, 60, 20)
}

# Groups
print("Sprite groups created.")
diamond_group = pygame.sprite.Group()
spike_group = pygame.sprite.Group()
plant_group = pygame.sprite.Group()
board_group = pygame.sprite.Group()
chain_group = pygame.sprite.Group()
groups = [diamond_group, spike_group, plant_group, board_group, chain_group]

# Load Level Data
print("Attempting to load level 1 data...")
data = load_level(current_level)
if data is None:
    print(f"Warning: Level data for level {current_level} not found. Creating empty world.")
    data = [[0 for _ in range(WIDTH // tile_size)] for _ in range(HEIGHT // tile_size)]
else:
    print(f"Level data loaded/initialized for level {current_level}.")

(player_x, player_y), (portal_x, portal_y) = game_data(current_level)
print(f"Player and portal data for level {current_level} retrieved.")

world = World(win, data, groups)
player = Player(win, (player_x, player_y), world, groups)
portal = Portal(portal_x, portal_y, win)
print("World, Player, and Portal objects created.")

game_started = False
game_over = False
game_won = False
replay_menu = False
sound_on = True
print("Game state variables initialized.")

bgx = 0
bgcounter = 0
bgdx = 1

print("Starting main game loop...")
running = True
while running:
    win.blit(bg, (bgx, 0))
    win.blit(bg, (bgx + WIDTH, 0))  # Second copy for seamless scrolling

    for group in groups:
        group.draw(win)
    world.draw()

    if not game_started:
        win.blit(cave_story, (WIDTH // 2 - cave_story.get_width() // 2, HEIGHT // 2 - cave_story.get_height() // 2 - 50))
        if play_btn.draw(win):
            print("Play button clicked via draw method!")
            game_started = True
        # Additional check for mouse click
        mouse_pos = pygame.mouse.get_pos()
        if play_btn.rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
            print("Play button clicked via mouse check!")
            game_started = True
    elif game_won:
        win.blit(game_won_img, (WIDTH // 2 - game_won_img.get_width() // 2, HEIGHT // 2 - game_won_img.get_height() // 2 - 50))
        if quit_btn.draw(win):
            running = False
        if replay_btn.draw(win):
            game_won = False
            game_started = True
            current_level = 1
            for group in groups:
                group.empty()
            data = load_level(current_level)
            if data is None:
                data = [[0 for _ in range(WIDTH // tile_size)] for _ in range(HEIGHT // tile_size)]
            (player_x, player_y), (portal_x, portal_y) = game_data(current_level)
            world = World(win, data, groups)
            player = Player(win, (player_x, player_y), world, groups)
            portal = Portal(portal_x, portal_y, win)
            replay_fx.play()
    else:
        if show_keys:
            win.blit(move_btn_img, (0, 0))
            bgcounter += 1
            if bgcounter >= 15:
                bgcounter = 0
                bgx += bgdx
                if bgx <= -WIDTH or bgx >= 0:
                    bgdx *= -1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if not game_started and play_btn.rect.collidepoint(pos):
                    print("Play button clicked via event!")
                    game_started = True
                elif show_keys:
                    if dir_dict['Up'].collidepoint(pos):
                        pressed_keys[0] = True
                    elif dir_dict['Down'].collidepoint(pos):
                        pressed_keys[1] = True
                    elif dir_dict['Left'].collidepoint(pos):
                        pressed_keys[2] = True
                    elif dir_dict['Right'].collidepoint(pos):
                        pressed_keys[3] = True
            if event.type == pygame.MOUSEBUTTONUP:
                pressed_keys = [False, False, False, False]
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    running = False
                if event.key == pygame.K_UP:
                    pressed_keys[0] = True
                if event.key == pygame.K_DOWN:
                    pressed_keys[1] = True
                if event.key == pygame.K_LEFT:
                    pressed_keys[2] = True
                if event.key == pygame.K_RIGHT:
                    pressed_keys[3] = True
            if event.type == pygame.KEYUP:
                pressed_keys = [False, False, False, False]

        portal.update()
        if not game_over:
            game_over = player.update(pressed_keys, game_over)
            if game_over:
                show_keys = False
                replay_menu = True

        if player.rect.colliderect(portal.rect):
            if current_level < MAX_LEVEL:
                current_level += 1
                for group in groups:
                    group.empty()
                data = load_level(current_level)
                if data is None:
                    data = [[0 for _ in range(WIDTH // tile_size)] for _ in range(HEIGHT // tile_size)]
                (player_x, player_y), (portal_x, portal_y) = game_data(current_level)
                world = World(win, data, groups)
                player = Player(win, (player_x, player_y), world, groups)
                portal = Portal(portal_x, portal_y, win)
            else:
                show_keys = False
                game_won = True

        if replay_menu:
            if quit_btn.draw(win):
                running = False
            if sound_btn.draw(win):
                sound_on = not sound_on
                sound_btn.update_image(sound_on_img if sound_on else sound_off_img)
                if sound_on:
                    pygame.mixer.music.play(-1)
                else:
                    pygame.mixer.music.stop()
            if replay_btn.draw(win):
                show_keys = True
                replay_menu = False
                game_over = False
                current_level = 1
                for group in groups:
                    group.empty()
                data = load_level(current_level)
                if data is None:
                    data = [[0 for _ in range(WIDTH // tile_size)] for _ in range(HEIGHT // tile_size)]
                (player_x, player_y), (portal_x, portal_y) = game_data(current_level)
                world = World(win, data, groups)
                player = Player(win, (player_x, player_y), world, groups)
                portal = Portal(portal_x, portal_y, win)
                replay_fx.play()

    clock.tick(FPS)
    pygame.display.update()

pygame.quit()