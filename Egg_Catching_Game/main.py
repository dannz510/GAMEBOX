import pygame
import random

from objects import Egg, Basket, Splash, Button, ScoreText, getEggPos, display_score

# Display ***************************************

pygame.init()
SCREEN = WIDTH, HEIGHT = 400, 700  # You can adjust these values as needed
win = pygame.display.set_mode(SCREEN, pygame.RESIZABLE)
xoffset, yoffset = 0, 0 

clock = pygame.time.Clock()
FPS = 45

# Colors ***************************************

WHITE = 255, 255, 255
BLACK = 0, 0, 0

# Fonts ****************************************
pygame.font.init()
score_font = pygame.font.Font('Fonts/PatrickHand-Regular.ttf', 50)
score_font2 = pygame.font.SysFont('Arial',40)
score_font3 = pygame.font.Font('Fonts/PatrickHand-Regular.ttf', 80)

# Music ***************************************
pygame.mixer.music.load('Sounds/music.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(loops=-1)

egg_drop_sound = pygame.mixer.Sound('Sounds/drop.wav')
splash_sound = pygame.mixer.Sound('Sounds/splash.wav')
game_over_sound = pygame.mixer.Sound('Sounds/game_over.wav')

# Objects **************************************
basket = Basket(WIDTH // 2 - 60, HEIGHT - 120, win)

x, y = getEggPos()
e = Egg(x, y, win)
egg_group = pygame.sprite.Group()
egg_group.add(e)

splash_group = pygame.sprite.Group()
score_group = pygame.sprite.Group()

# images **************************************
bg_original = pygame.image.load('Assets/bg.png')
bg = pygame.transform.scale(bg_original, (WIDTH, HEIGHT))

home_original = pygame.image.load('Assets/home.jpg')
home = pygame.transform.scale(home_original, (WIDTH, HEIGHT))

hen_original = pygame.image.load('Assets/hen.png')
hen = pygame.transform.scale(hen_original, (WIDTH, int(hen_original.get_height() * (WIDTH/hen_original.get_width()))))

egg_bucket = pygame.image.load('Assets/egg_bucket.png')
egg_bucket = pygame.transform.scale(egg_bucket, (int(WIDTH * 0.4), int(HEIGHT * 0.1)))

health_egg = pygame.image.load('Assets/egg1.png')
health_egg = pygame.transform.scale(health_egg, (30,40))

leaves_original = pygame.image.load('Assets/leaves.png')
leaves = pygame.transform.scale(leaves_original, (WIDTH, int(leaves_original.get_height() * (WIDTH/leaves_original.get_width()))))

arrow = pygame.image.load('Assets/arrow.png')
larrow = pygame.transform.scale(arrow, (80,80))
rarrow = pygame.transform.flip(larrow, True, False)

close_img = pygame.image.load('Assets/close.png')
close_img = pygame.transform.scale(close_img, (80,80))
restart_img = pygame.image.load('Assets/restart.png')
restart_img = pygame.transform.scale(restart_img, (80,80))

# Buttons **************************************
left_button = Button(larrow, (1,1), WIDTH // 2 - 100, HEIGHT - 85)
right_button = Button(rarrow, (1,1), WIDTH // 2 + 20, HEIGHT - 85)

restart_button = Button(restart_img, (1,1), WIDTH // 2 - restart_img.get_width()//2, HEIGHT //2)
close_button = Button(close_img, (1,1), WIDTH // 2 - close_img.get_width()//2, HEIGHT //2 + 90)

# Game Variables ******************************
health = 5
score = 0
speed = 12
gameStarted = False
gameOver = False

# Movement speed for the basket
basket_speed = 40 # Adjust this value to make the basket move faster or slower

# Game ****************************************

running = True
while running:
	win.fill(BLACK)
	
	for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.VIDEORESIZE: # Handle window resizing
				WIDTH, HEIGHT = event.w, event.h
				win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
				
				# Re-scale all background/static images from their original versions
				bg = pygame.transform.scale(bg_original, (WIDTH, HEIGHT))
				home = pygame.transform.scale(home_original, (WIDTH, HEIGHT))
				hen = pygame.transform.scale(hen_original, (WIDTH, int(hen_original.get_height() * (WIDTH/hen_original.get_width()))))
				leaves = pygame.transform.scale(leaves_original, (WIDTH, int(leaves_original.get_height() * (WIDTH/leaves_original.get_width()))))
				egg_bucket = pygame.transform.scale(egg_bucket, (int(WIDTH * 0.4), int(HEIGHT * 0.1)))

				# Re-position elements based on new WIDTH/HEIGHT
				basket.rect.x = WIDTH // 2 - basket.image.get_width() // 2
				basket.rect.y = HEIGHT - 120
				left_button.rect.x = WIDTH // 2 - 100
				right_button.rect.x = WIDTH // 2 + 20
				left_button.rect.y = HEIGHT - 85
				right_button.rect.y = HEIGHT - 85
				restart_button.rect.x = WIDTH // 2 - restart_img.get_width() // 2
				close_button.rect.x = WIDTH // 2 - close_img.get_width() // 2
				restart_button.rect.y = HEIGHT // 2
				close_button.rect.y = HEIGHT // 2 + 90

			# Handle Keyboard Input for Basket Movement
			if event.type == pygame.KEYDOWN:
				if gameStarted and not gameOver: # Only allow movement when game is active
					if event.key == pygame.K_LEFT or event.key == pygame.K_a:
						basket.rect.x -= basket_speed
					if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
						basket.rect.x += basket_speed
	
	if gameOver:
		win.blit(bg, (0, 0))
		
		score_img = score_font3.render(f'Score : {score}', True, (34, 139, 34))
		score_rect = score_img.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 140))
		win.blit(score_img, score_rect)
		
		win.blit(egg_bucket, (WIDTH // 2 - egg_bucket.get_width() // 2, HEIGHT - 300))
	
		if restart_button.draw(win):
			health = 5
			score = 0
			speed = 12
			gameStarted = True
			gameOver = False

			pygame.mixer.music.play(loops=-1)
			
			x, y = getEggPos()
			e = Egg(x, y, win)
			egg_group.add(e)

		if close_button.draw(win):
			running = False

	else:
		if not gameStarted:
			win.blit(home, (0, 0))
			
			play_button_rect = pygame.Rect(WIDTH // 2 - 60, HEIGHT - 150, 120, 50)
			
			pos = pygame.mouse.get_pos()
			if play_button_rect.collidepoint(pos):
				if pygame.mouse.get_pressed()[0]:
					gameStarted = True
					gameOver = False
	
	if gameStarted:
		win.blit(bg, (0, 0))
		pygame.draw.rect(win, WHITE, (xoffset-10, yoffset-10, WIDTH + 20, HEIGHT + 20), 3)
		
		win.blit(hen, (WIDTH // 2 - hen.get_width() // 2, 50))
		
		img, rect = display_score(score, score_font2, (WIDTH - 150, 10))
		win.blit(img, rect)
		
		for index in range(health):
			win.blit(health_egg, (10 + 40 * index, 15))
			
		win.blit(leaves, (0, int(HEIGHT * 0.2)))
		
		basket.update()
		egg_group.update(speed)
		splash_group.update()
		score_group.update()
		
		for egg in egg_group:
			collision = False
	
			if egg.rect.y >= HEIGHT - 160:
				collision = True
				health -= 1
				splash = Splash(egg.rect.x, egg.rect.y+10, win)
				splash_group.add(splash)
				splash_sound.play()
	
			if basket.check_collision(egg.rect):
				collision = True
				score += 3
				egg_drop_sound.play()
				pos = egg.rect.x, egg.rect.y
				s = ScoreText('+3',  score_font, pos, win)
				score_group.add(s)
			
			if collision:
				egg.kill()
				x, y = getEggPos()
				e = Egg(x, y, win)
				egg_group.add(e)
				
		if health <= 0:
			gameStarted = False
			gameOver = True

			pygame.mixer.music.stop()
			game_over_sound.play()

			egg_group.empty()
			score_group.empty()
			splash_group.empty()
	
		# Keep these button controls as an alternative or if you still want on-screen buttons
		if left_button.draw(win):
				if basket.rect.x >= 0:
					basket.rect.x -= 20
		if right_button.draw(win):
				if basket.rect.right <= WIDTH:
					basket.rect.x += 20
			
		# Ensure basket stays within bounds after key press
		if basket.rect.x < 0:
			basket.rect.x = 0
		if basket.rect.right > WIDTH:
			basket.rect.right = WIDTH
			
	clock.tick(FPS)
	pygame.display.update()
		
pygame.quit()