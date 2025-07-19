import pygame
import random
from objects import Road, Player, Nitro, Tree, Button, \
					Obstacle, Coins, Fuel

pygame.init()
SCREEN = WIDTH, HEIGHT = 288, 512

info = pygame.display.Info()
width = info.current_w
height = info.current_h

if width >= height:
	win = pygame.display.set_mode(SCREEN, pygame.NOFRAME)
else:
	win = pygame.display.set_mode(SCREEN, pygame.NOFRAME | pygame.SCALED | pygame.FULLSCREEN)

clock = pygame.time.Clock()
FPS = 30 # Keep FPS at 30 for smoother movement and easier speed calculation

lane_pos = [50, 95, 142, 190]

# COLORS **********************************************************************

WHITE = (255, 255, 255)
BLUE = (30, 144,255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 20)
YELLOW = (255, 255, 0) # Added YELLOW for consistency

# FONTS ***********************************************************************

font = pygame.font.SysFont('cursive', 32)
kmh_font = pygame.font.SysFont('arial', 24, bold=True) # New font for km/h display

select_car = font.render('Select Car', True, WHITE)

# IMAGES **********************************************************************

bg = pygame.image.load('Assets/bg.png')

home_img = pygame.image.load('Assets/home.png')
play_img = pygame.image.load('Assets/buttons/play.png')
end_img = pygame.image.load('Assets/end.jpg')
end_img = pygame.transform.scale(end_img, (WIDTH, HEIGHT))
game_over_img = pygame.image.load('Assets/game_over.png')
game_over_img = pygame.transform.scale(game_over_img, (220, 220))
coin_img = pygame.image.load('Assets/coins/1.png')
dodge_img = pygame.image.load('Assets/car_dodge.png')

left_arrow = pygame.image.load('Assets/buttons/arrow.png')
right_arrow = pygame.transform.flip(left_arrow, True, False)

home_btn_img = pygame.image.load('Assets/buttons/home.png')
replay_img = pygame.image.load('Assets/buttons/replay.png')
sound_off_img = pygame.image.load("Assets/buttons/soundOff.png")
sound_on_img = pygame.image.load("Assets/buttons/soundOn.png")

cars = []
car_type = 0
for i in range(1, 9):
	img = pygame.image.load(f'Assets/cars/{i}.png')
	img = pygame.transform.scale(img, (59, 101))
	cars.append(img)

nitro_frames = []
nitro_counter = 0
for i in range(6):
	img = pygame.image.load(f'Assets/nitro/{i}.gif')
	img = pygame.transform.flip(img, False, True)
	img = pygame.transform.scale(img, (18, 36))
	nitro_frames.append(img)

# FUNCTIONS *******************************************************************
def center(image):
	return (WIDTH // 2) - image.get_width() // 2

# BUTTONS *********************************************************************
play_btn = Button(play_img, (100, 34), center(play_img)+10, HEIGHT-80)
la_btn = Button(left_arrow, (32, 42), 40, 180)
ra_btn = Button(right_arrow, (32, 42), WIDTH-60, 180)

home_btn = Button(home_btn_img, (24, 24), WIDTH // 4 - 18, HEIGHT - 80)
replay_btn = Button(replay_img, (36,36), WIDTH // 2  - 18, HEIGHT - 86)
sound_btn = Button(sound_on_img, (24, 24), WIDTH - WIDTH // 4 - 18, HEIGHT - 80)

# SOUNDS **********************************************************************

click_fx = pygame.mixer.Sound('Sounds/click.mp3')
fuel_fx = pygame.mixer.Sound('Sounds/fuel.wav')
start_fx = pygame.mixer.Sound('Sounds/start.mp3')
restart_fx = pygame.mixer.Sound('Sounds/restart.mp3')
coin_fx = pygame.mixer.Sound('Sounds/coin.mp3')
crash_fx = pygame.mixer.Sound('Sounds/crash.mp3') # Added crash sound

pygame.mixer.music.load('Sounds/mixkit-tech-house-vibes-130.mp3')
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(0.6)

# OBJECTS *********************************************************************
road = Road()
nitro = Nitro(WIDTH-80, HEIGHT-80)
p = Player(100, HEIGHT-120, car_type) # Initial player creation

tree_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
fuel_group = pygame.sprite.Group()
obstacle_group = pygame.sprite.Group()

# VARIABLES *******************************************************************
home_page = True
car_page = False
game_page = False
over_page = False

move_left = False
move_right = False
move_up = False # New: for vertical movement
move_down = False # New: for vertical movement
nitro_on = False
sound_on = True

counter = 0
counter_inc = 1
base_speed = 3 # Base speed for the game
boost_speed = 10 # Speed when nitro is active
current_speed = base_speed # Initial current speed
dodged = 0
coins = 0
cfuel = 100

endx, enddx = 0, 0.5
gameovery = -50

running = True
while running:
	win.fill(BLACK)
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
				running = False

			if event.key == pygame.K_LEFT or event.key == pygame.K_a: # A for left
				move_left = True
			if event.key == pygame.K_RIGHT or event.key == pygame.K_d: # D for right
				move_right = True
			if event.key == pygame.K_UP or event.key == pygame.K_w: # W for up
				move_up = True
			if event.key == pygame.K_DOWN or event.key == pygame.K_s: # S for down
				move_down = True

			if event.key == pygame.K_n:
				nitro_on = True

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT or event.key == pygame.K_a:
				move_left = False
			if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
				move_right = False
			if event.key == pygame.K_UP or event.key == pygame.K_w:
				move_up = False
			if event.key == pygame.K_DOWN or event.key == pygame.K_s:
				move_down = False

			if event.key == pygame.K_n:
				nitro_on = False
				current_speed = base_speed # Reset speed when nitro is off
				counter_inc = 1 # Reset counter increment

		if event.type == pygame.MOUSEBUTTONDOWN:
			x, y = event.pos

			if nitro.rect.collidepoint((x, y)):
				nitro_on = True
			else: # Allow mouse click for horizontal movement
				if x <= WIDTH // 2:
					move_left = True
				else:
					move_right = True

		if event.type == pygame.MOUSEBUTTONUP:
			# Reset mouse movement flags
			move_left = False
			move_right = False
			nitro_on = False
			current_speed = base_speed # Reset speed when mouse button released
			counter_inc = 1

	if home_page:
		win.blit(home_img, (0,0))
		counter += 1
		if counter % 60 == 0: # Auto transition after a short delay
			home_page = False
			car_page = True

	if car_page:
		win.blit(select_car, (center(select_car), 80))

		win.blit(cars[car_type], (WIDTH//2-30, 150))
		if la_btn.draw(win):
			car_type -= 1
			click_fx.play()
			if car_type < 0:
				car_type = len(cars) - 1

		if ra_btn.draw(win):
			car_type += 1
			click_fx.play()
			if car_type >= len(cars):
				car_type = 0

		if play_btn.draw(win):
			car_page = False
			game_page = True

			start_fx.play()

			p = Player(100, HEIGHT-120, car_type) # Re-initialize player with chosen car
			counter = 0 # Reset counter for game start

	if over_page:
		win.blit(end_img, (endx, 0))
		endx += enddx
		if endx >= 10 or endx<=-10:
			enddx *= -1

		win.blit(game_over_img, (center(game_over_img), gameovery))
		if gameovery < 16:
			gameovery += 1

		num_coin_img = font.render(f'{coins}', True, WHITE)
		num_dodge_img = font.render(f'{dodged}', True, WHITE)
		distance_img = font.render(f'Distance : {counter/1000:.2f} km', True, WHITE) # Adjusted for counter_inc

		win.blit(coin_img, (80, 240))
		win.blit(dodge_img, (50, 280))
		win.blit(num_coin_img, (180, 250))
		win.blit(num_dodge_img, (180, 300))
		win.blit(distance_img, (center(distance_img), (350)))

		if home_btn.draw(win):
			over_page = False
			home_page = True

			coins = 0
			dodged = 0
			counter = 0
			nitro.gas = 0
			cfuel = 100
			current_speed = base_speed # Reset speed
			counter_inc = 1 # Reset counter increment

			endx, enddx = 0, 0.5
			gameovery = -50

			# Clear groups for next game
			tree_group.empty()
			coin_group.empty()
			fuel_group.empty()
			obstacle_group.empty()

		if replay_btn.draw(win):
			over_page = False
			game_page = True

			coins = 0
			dodged = 0
			counter = 0
			nitro.gas = 0
			cfuel = 100
			current_speed = base_speed # Reset speed
			counter_inc = 1 # Reset counter increment

			endx, enddx = 0, 0.5
			gameovery = -50

			restart_fx.play()

			# Clear groups for next game
			tree_group.empty()
			coin_group.empty()
			fuel_group.empty()
			obstacle_group.empty()

			p = Player(100, HEIGHT-120, car_type) # Re-initialize player for replay

		if sound_btn.draw(win):
			sound_on = not sound_on

			if sound_on:
				sound_btn.update_image(sound_on_img)
				pygame.mixer.music.play(loops=-1)
			else:
				sound_btn.update_image(sound_off_img)
				pygame.mixer.music.stop()

	if game_page:
		win.blit(bg, (0,0))
		road.update(current_speed) # Use current_speed for road movement
		road.draw(win)

		counter += counter_inc # Distance counter
		
		# Display km/h
		# Assuming 1 unit of speed = 10 km/h for a rough estimation
		# Adjust the multiplier (10) based on how fast you want the km/h to feel
		kmh = current_speed * 10
		kmh_text = kmh_font.render(f'{int(kmh)} km/h', True, YELLOW)
		win.blit(kmh_text, (WIDTH - kmh_text.get_width() - 20, 20))


		# Obstacle/item spawning logic (adjusted for current_speed)
		if counter % (60 // (current_speed // base_speed)) == 0: # Faster spawning at higher speeds
			tree = Tree(random.choice([-5, WIDTH-35]), -20)
			tree_group.add(tree)

		if counter % (270 // (current_speed // base_speed)) == 0:
			type = random.choices([1, 2], weights=[6, 4], k=1)[0]
			x = random.choice(lane_pos)+10
			if type == 1:
				count = random.randint(1, 3)
				for i in range(count):
					coin = Coins(x,-100 - (25 * i))
					coin_group.add(coin)
			elif type == 2:
				fuel = Fuel(x, -100)
				fuel_group.add(fuel)
		elif counter % (90 // (current_speed // base_speed)) == 0:
			obs = random.choices([1, 2, 3], weights=[6,2,2], k=1)[0]
			obstacle = Obstacle(obs)
			obstacle_group.add(obstacle)

		if nitro_on and nitro.gas > 0:
			x, y = p.rect.centerx - 8, p.rect.bottom - 10
			win.blit(nitro_frames[nitro_counter], (x, y))
			nitro_counter = (nitro_counter + 1) % len(nitro_frames)

			current_speed = boost_speed # Set speed to boost speed
			if counter_inc == 1: # Only change counter_inc once per boost activation
				counter = 0 # Reset counter to make distance calculation consistent with new speed
				counter_inc = 5 # Faster distance counting when boosting

		elif nitro.gas <= -60: # If nitro is completely depleted
			nitro_on = False # Force nitro off
			current_speed = base_speed
			counter_inc = 1

		else: # If nitro is not on or gas is recovering
			current_speed = base_speed
			counter_inc = 1


		nitro.update(nitro_on)
		nitro.draw(win)
		obstacle_group.update(current_speed) # Pass current_speed to obstacles
		obstacle_group.draw(win)
		tree_group.update(current_speed) # Pass current_speed to trees
		tree_group.draw(win)
		coin_group.update(current_speed) # Pass current_speed to coins
		coin_group.draw(win)
		fuel_group.update(current_speed) # Pass current_speed to fuel
		fuel_group.draw(win)

		p.update(move_left, move_right, move_up, move_down) # Pass vertical movement flags
		p.draw(win)

		if cfuel > 0:
			pygame.draw.rect(win, GREEN, (20, 20, cfuel, 15), border_radius=5)
		pygame.draw.rect(win, WHITE, (20, 20, 100, 15), 2, border_radius=5)
		cfuel -= 0.05 # Fuel depletes slower at base speed, faster at boost speed
		if current_speed == boost_speed:
			cfuel -= 0.15 # Faster depletion when boosting

		# COLLISION DETECTION & KILLS
		for obstacle in obstacle_group:
			if obstacle.rect.y >= HEIGHT:
				if obstacle.type == 1:
					dodged += 1
				obstacle.kill() 

			if pygame.sprite.collide_mask(p, obstacle):
				pygame.draw.rect(win, RED, p.rect, 1) # Highlight collision
				current_speed = 0 # Stop game on collision
				crash_fx.play() # Play crash sound

				game_page = False
				over_page = True

				tree_group.empty()
				coin_group.empty()
				fuel_group.empty()
				obstacle_group.empty()

		if pygame.sprite.spritecollide(p, coin_group, True):
			coins += 1
			coin_fx.play()

		if pygame.sprite.spritecollide(p, fuel_group, True):
			cfuel += 25
			fuel_fx.play()
			if cfuel >= 100:
				cfuel = 100

	pygame.draw.rect(win, BLUE, (0, 0, WIDTH, HEIGHT), 3)
	clock.tick(FPS)
	pygame.display.update()

pygame.quit()