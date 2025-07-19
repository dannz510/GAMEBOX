import pygame
import random

pygame.init()
SCREEN = WIDTH, HEIGHT = 288, 512 # This definition is for context within this file, not the main game window

# Remove or comment out the display setup here as main.py handles it
# info = pygame.display.Info()
# width = info.current_w
# height = info.current_h

# if width >= height:
# 	win = pygame.display.set_mode(SCREEN, pygame.NOFRAME)
# else:
# 	win = pygame.display.set_mode(SCREEN, pygame.NOFRAME | pygame.SCALED | pygame.FULLSCREEN)

clock = pygame.time.Clock()
FPS = 45

# COLORS

RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (54, 69, 79)
c_list = [RED, BLACK, WHITE]

# IMAGES

bg = pygame.image.load("Assets/bg.png")
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT+50)) # Scaling related to this file's SCREEN, not main.py's

egg_bucket = pygame.image.load("Assets/egg_bucket.png")
egg_bucket = pygame.transform.scale(egg_bucket, (120, 80)) # Scaling related to this file's SCREEN, not main.py's

# Remove or comment out this entire game loop as main.py is the primary loop
# running = True
# while running:
# 	win.blit(bg, (0,0))
# 	for event in pygame.event.get():
# 		if event.type == pygame.QUIT:
# 			running = False

# 		if event.type == pygame.KEYDOWN:
# 			if event.key == pygame.K_ESCAPE:
# 				running = False
				
# 	#win.blit(egg_bucket, (WIDTH//2, HEIGHT-120))
				
# 	clock.tick(FPS)
# 	pygame.draw.rect(win, WHITE, (0,0, WIDTH, HEIGHT), 2)
# 	pygame.display.update()
	
# pygame.quit()