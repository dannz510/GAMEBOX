import math
import pygame
import random

SCREEN = WIDTH, HEIGHT = 288, 512

BLUE = (53, 81, 92)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255) # Added WHITE for consistency

lane_pos = [50, 95, 142, 190]

class Road():
	def __init__(self):
		self.image = pygame.image.load('Assets/road.png')
		self.image = pygame.transform.scale(self.image, (WIDTH-60, HEIGHT))

		self.reset()
		self.move = True

	def update(self, speed):
		if self.move:
			self.y1 += speed
			self.y2 += speed

			if self.y1 >= HEIGHT:
				self.y1 = -HEIGHT
			if self.y2 >= HEIGHT:
				self.y2 = -HEIGHT

	def draw(self, win):
		win.blit(self.image, (self.x, self.y1))
		win.blit(self.image, (self.x, self.y2))

	def reset(self):
		self.x = 30
		self.y1 = 0
		self.y2 = -HEIGHT

class Player(pygame.sprite.Sprite):
	def __init__(self, x, y, type):
		super(Player, self).__init__()
		self.image = pygame.image.load(f'Assets/cars/{type+1}.png')
		self.original_image = pygame.transform.scale(self.image, (48, 82)) # Store original for rotation
		self.image = self.original_image # Current image for blitting
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.speed_x = 5 # Horizontal movement speed
		self.speed_y = 5 # Vertical movement speed

	def update(self, left, right, up, down): # Added up, down parameters
		# Horizontal movement
		if left:
			self.rect.x -= self.speed_x
			if self.rect.x <= 40:
				self.rect.x = 40
		if right:
			self.rect.x += self.speed_x
			if self.rect.right >= 250:
				self.rect.right = 250

		# Vertical movement
		if up:
			self.rect.y -= self.speed_y
			if self.rect.y <= HEIGHT // 2: # Limit upward movement to roughly half screen
				self.rect.y = HEIGHT // 2
		if down:
			self.rect.y += self.speed_y
			if self.rect.bottom >= HEIGHT - 20: # Limit downward movement near bottom
				self.rect.bottom = HEIGHT - 20

		self.mask = pygame.mask.from_surface(self.image)

	def draw(self, win):
		win.blit(self.image, self.rect)

class Obstacle(pygame.sprite.Sprite):
	def __init__(self, type):
		super(Obstacle, self).__init__()
		dx = 0
		self.type = type
		self.wobble_counter = 0 # For side-to-side movement
		self.wobble_amplitude = 1 # How much it wobbles
		self.wobble_frequency = 0.05 # How fast it wobbles

		if type == 1: # Other cars
			ctype = random.randint(1, 8)
			self.image = pygame.image.load(f'Assets/cars/{ctype}.png')
			self.image = pygame.transform.flip(self.image, False, True)
			self.image = pygame.transform.scale(self.image, (48, 82))
			self.original_x = random.choice(lane_pos) + dx # Store original x for wobble
		if type == 2: # Barrel
			self.image = pygame.image.load('Assets/barrel.png')
			self.image = pygame.transform.scale(self.image, (24, 36))
			dx = 10
			self.original_x = random.choice(lane_pos) + dx
		elif type == 3: # Roadblock
			self.image = pygame.image.load('Assets/roadblock.png')
			self.image = pygame.transform.scale(self.image, (50, 25))
			self.original_x = random.choice(lane_pos) + dx

		self.rect = self.image.get_rect()
		self.rect.x = self.original_x
		self.rect.y = -100

	def update(self, speed):
		self.rect.y += speed

		# Add wobble effect for other cars (type 1)
		if self.type == 1:
			self.wobble_counter += self.wobble_frequency
			self.rect.x = self.original_x + self.wobble_amplitude * math.sin(self.wobble_counter)
			# Keep cars within road boundaries
			if self.rect.x < 40:
				self.rect.x = 40
			if self.rect.right > 250:
				self.rect.right = 250


		self.mask = pygame.mask.from_surface(self.image)

	def draw(self, win):
		win.blit(self.image, self.rect)

class Nitro:
	def __init__(self, x, y):
		self.image = pygame.image.load('Assets/nitro.png')
		self.image = pygame.transform.scale(self.image, (42, 42))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

		self.gas = 0
		self.radius = 20
		self.CENTER = self.rect.centerx, self.rect.centery

	def update(self, nitro_on):
		if nitro_on:
			self.gas -= 1
			if self.gas <= -60: # Allow a small negative buffer for quick taps
				self.gas = -60
		else:
			self.gas += 1
			if self.gas >= 359:
				self.gas = 359

	def draw(self, win):
		win.blit(self.image, self.rect)
		if self.gas > 0 and self.gas < 360:
			for i in range(self.gas):
				x = round(self.CENTER[0] + self.radius * math.cos(i * math.pi / 180))
				y = round(self.CENTER[1] + self.radius * math.sin(i * math.pi / 180))
				pygame.draw.circle(win, YELLOW, (x, y), 1)

class Tree(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super(Tree, self).__init__()

		type = random.randint(1, 4)
		self.image = pygame.image.load(f'Assets/trees/{type}.png')
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

	def update(self, speed):
		self.rect.y += speed
		if self.rect.top >= HEIGHT:
			self.kill()

	def draw(self, win):
		win.blit(self.image, self.rect)

class Fuel(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super(Fuel, self).__init__()

		self.image = pygame.image.load('Assets/fuel.png')
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

	def update(self, speed):
		self.rect.y += speed
		if self.rect.top >= HEIGHT:
			self.kill()

	def draw(self, win):
		win.blit(self.image, self.rect)

class Coins(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super(Coins, self).__init__()

		self.images = []
		for i in range(1, 7):
			img = pygame.image.load(f'Assets/Coins/{i}.png')
			self.images.append(img)

		self.counter = 0
		self.index = 0
		self.image = self.images[self.index]
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

	def update(self, speed):
		self.counter += 1
		if self.counter % 5 == 0:
			self.index = (self.index + 1) % len(self.images)

		self.rect.y += speed
		if self.rect.top >= HEIGHT:
			self.kill()

		self.image = self.images[self.index]

	def draw(self, win):
		win.blit(self.image, self.rect)

class Button(pygame.sprite.Sprite):
	def __init__(self, img, scale, x, y):
		super(Button, self).__init__()
		
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
			if pygame.mouse.get_pressed()[0] and not self.clicked:
				action = True
				self.clicked = True

			if not pygame.mouse.get_pressed()[0]:
				self.clicked = False

		win.blit(self.image, self.rect)
		return action