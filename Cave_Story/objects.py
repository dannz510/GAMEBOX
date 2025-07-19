import os
import pickle
import pygame
from pygame.locals import *

SIZE = WIDTH, HEIGHT = 512, 288
TILE_SIZE = 16
ROWS, COLS = HEIGHT // TILE_SIZE, WIDTH // TILE_SIZE

pygame.font.init()
score_font = pygame.font.SysFont('Bauhaus 93', 30)

WHITE = (255, 255, 255)
BLUE = (30, 144, 255)

class World:
    def __init__(self, win, data, groups):
        self.tile_list = []
        self.win = win
        self.groups = groups

        tiles = []
        try:
            for t in sorted(os.listdir('tiles/'), key=lambda s: int(s[:-4])):
                tile = pygame.image.load('tiles/' + t)
                tiles.append(tile)
        except (OSError, pygame.error) as e:
            print(f"Failed to load tiles: {e}")
            tiles = [pygame.Surface((TILE_SIZE, TILE_SIZE)) for _ in range(88)]  # Placeholder tiles

        row_count = 0
        for row in data:
            col_count = 0
            for col in row:
                if col > 0:
                    if col in range(1, 7) or col in range(9, 15) or col in range(17, 23) or col in range(25, 46) or col in range(47, 69):
                        img = tiles[col - 1] if col - 1 < len(tiles) else pygame.Surface((TILE_SIZE, TILE_SIZE))
                        rect = img.get_rect()
                        rect.x = col_count * TILE_SIZE
                        rect.y = row_count * TILE_SIZE
                        self.tile_list.append((img, rect))
                    if col in (81, 82, 83, 84):
                        img = tiles[col - 1] if col - 1 < len(tiles) else pygame.Surface((TILE_SIZE, TILE_SIZE))
                        self.groups[0].add(Diamond(img, col_count * TILE_SIZE, row_count * TILE_SIZE))
                    if col in (72, 80, 87, 88):
                        img = tiles[col - 1] if col - 1 < len(tiles) else pygame.Surface((TILE_SIZE, TILE_SIZE))
                        self.groups[1].add(Spike(img, col_count * TILE_SIZE, row_count * TILE_SIZE))
                    if col in (70, 71, 78, 79):
                        img = tiles[col - 1] if col - 1 < len(tiles) else pygame.Surface((TILE_SIZE, TILE_SIZE))
                        self.groups[2].add(Plant(img, col_count * TILE_SIZE, row_count * TILE_SIZE))
                    if col == 76:
                        img = tiles[col - 1] if col - 1 < len(tiles) else pygame.Surface((TILE_SIZE, TILE_SIZE))
                        self.groups[3].add(Board(img, col_count * TILE_SIZE, row_count * TILE_SIZE))
                    if col in (69, 77, 85):
                        img = tiles[col - 1] if col - 1 < len(tiles) else pygame.Surface((TILE_SIZE, TILE_SIZE))
                        self.groups[4].add(Chain(img, col_count * TILE_SIZE, row_count * TILE_SIZE))
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            self.win.blit(tile[0], tile[1])

def game_data(level):
    if level == 1:
        return (100, 200), (450, 200)
    if level == 2:
        return (50, 200), (400, 50)
    if level == 3:
        return (50, 50), (450, 250)
    return (100, 200), (450, 200)  # Default

class Assets(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        super().__init__()
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Diamond(Assets): pass
class Spike(Assets): pass
class Plant(Assets): pass
class Board(Assets): pass
class Chain(Assets): pass

class Portal:
    def __init__(self, x, y, win):
        self.win = win
        self.im_list = []
        try:
            for i in range(1, 10):
                img = pygame.image.load(f"Assets/portal/{i}.gif")
                img = pygame.transform.scale(img, (24, 24))
                self.im_list.append(img)
        except pygame.error as e:
            print(f"Failed to load portal images: {e}")
            self.im_list = [pygame.Surface((24, 24)) for _ in range(9)]  # Placeholder
        self.rect = self.im_list[0].get_rect()
        self.rect.x = x
        self.rect.y = y
        self.index = 0
        self.cooldown = 2
        self.counter = 0

    def update(self):
        self.counter += 1
        if self.counter >= self.cooldown:
            self.counter = 0
            self.index = (self.index + 1) % len(self.im_list)
        self.win.blit(self.im_list[self.index], self.rect)

# Sound effects
try:
    pygame.mixer.init()
    diamond_fx = pygame.mixer.Sound('Sounds/coin_fx.wav')
    chain_fx = pygame.mixer.Sound('Sounds/chain_fx.mp3')
    death_fx = pygame.mixer.Sound('Sounds/death_fx.wav')
except pygame.error as e:
    print(f"Failed to initialize mixer or load sounds: {e}")

class Player:
    def __init__(self, win, pos, world, groups):
        self.reset(win, pos, world, groups)

    def update(self, pressed_keys, game_over):
        dx = 0
        dy = 0
        walk_cooldown = 5
        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        if pressed_keys[2] and not self.on_chain:
            dx = -self.speed
            self.counter += 1
            self.direction = -1
        elif pressed_keys[3] and not self.on_chain:
            dx = self.speed
            self.counter += 1
            self.direction = 1
        else:
            self.counter = 0
            self.index = 0
            self.image = self.image_left[self.index] if self.direction == -1 else self.image_right[self.index]

        if pressed_keys[0] and not self.jumped and not self.in_air:
            self.vel_y = -9
            self.jumped = True
            self.in_air = True
        if not pressed_keys[0]:
            self.jumped = False

        collide_chain = pygame.sprite.spritecollideany(self, self.groups[4], False)
        if collide_chain:
            self.on_chain = True
            self.in_air = False
            self.vel_y = 0
            self.rect.centerx = collide_chain.rect.centerx
            if pressed_keys[0]:
                dy = -self.speed
                chain_fx.play()
                self.counter += 1
                self.direction = 2
            elif pressed_keys[1]:
                dy = self.speed
                chain_fx.play()
                self.counter += 1
                self.direction = 2
            else:
                self.counter = 0
                self.index = 0
                self.image = self.image_up[self.index]
            if pressed_keys[2]:
                dx = -self.speed * 2
                self.vel_y = -self.speed
                self.on_chain = False
                self.in_air = True
            elif pressed_keys[3]:
                dx = self.speed * 2
                self.vel_y = -self.speed
                self.on_chain = False
                self.in_air = True
        else:
            self.on_chain = False

        if self.counter > walk_cooldown:
            self.counter = 0
            self.index = (self.index + 1) % len(self.image_right)
            self.image = self.image_left[self.index] if self.direction == -1 else self.image_right[self.index] if self.direction == 1 else self.image_up[self.index]

        for tile in self.world.tile_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
                break
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.vel_y > 0:
                    dy = tile[1].top - self.rect.bottom
                    self.vel_y = 0
                    self.in_air = False
                elif self.vel_y < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0
                break
        self.rect.x += dx
        self.rect.y += dy

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            game_over = True

        if pygame.sprite.spritecollide(self, self.groups[0], True):
            diamond_fx.play()
        if pygame.sprite.spritecollide(self, self.groups[1], False):
            death_fx.play()
            game_over = True

        self.win.blit(self.image, self.rect)
        return game_over

    def reset(self, win, pos, world, groups):
        self.win = win
        self.pos = pos
        self.world = world
        self.groups = groups

        self.image_right = []
        self.image_left = []
        self.image_up = []
        try:
            for imindex in range(1, 37):
                img = pygame.image.load(f"Assets/sara/{imindex}.png")
                img = pygame.transform.scale(img, (22, 15))
                if imindex in range(1, 10):
                    self.image_up.append(img)
                if imindex in range(10, 19):
                    self.image_right.append(img)
                if imindex in range(28, 37):
                    self.image_left.append(img)
        except pygame.error as e:
            print(f"Failed to load player images: {e}")
            self.image_up = [pygame.Surface((22, 15)) for _ in range(9)]
            self.image_right = [pygame.Surface((22, 15)) for _ in range(9)]
            self.image_left = [pygame.Surface((22, 15)) for _ in range(9)]

        self.index = 0
        self.counter = 0
        self.speed = 3
        self.image = self.image_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.direction = 1
        self.vel_y = 0
        self.jumped = False
        self.in_air = True
        self.on_chain = False

class Button(pygame.sprite.Sprite):
    def __init__(self, img, scale, x, y):
        super().__init__()
        self.scale = scale
        self.image = pygame.transform.scale(img, self.scale)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def update_image(self, img):
        self.image = pygame.transform.scale(img, self.scale)

    def draw(self, win):
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

def draw_lines(win):
    for row in range(HEIGHT // TILE_SIZE + 1):
        pygame.draw.line(win, WHITE, (0, TILE_SIZE * row), (WIDTH, TILE_SIZE * row), 2)
    for col in range(WIDTH // TILE_SIZE + 1):
        pygame.draw.line(win, WHITE, (TILE_SIZE * col, 0), (TILE_SIZE * col, HEIGHT), 2)

def load_level(level):
    game_level = f'levels/level{level}_data'
    if os.path.exists(game_level):
        try:
            with open(game_level, 'rb') as f:
                return pickle.load(f)
        except Exception as e:
            print(f"Error loading level {level} data: {e}")
            return None
    print(f"Level file {game_level} not found.")
    return None