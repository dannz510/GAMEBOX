import pygame
import random
import os # Import os module for path handling

pygame.init()
pygame.mixer.init() # Initialize mixer for sounds

SCREEN = WIDTH, HEIGHT = 288, 512

info = pygame.display.Info()
width = info.current_w
height = info.current_h

if width >= height:
	win = pygame.display.set_mode(SCREEN, pygame.NOFRAME)
else:
	win = pygame.display.set_mode(SCREEN, pygame.NOFRAME | pygame.SCALED | pygame.FULLSCREEN)

clock = pygame.time.Clock()
FPS = 60

# COLORS **********************************************************************

WHITE = (255, 255, 255)
BLUE = (30, 144, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (168, 169, 169)
BLACK = (0, 0, 0) # Added black for drawing lines
LIGHT_GRAY = (200, 200, 200) # For hint box background

# FONTS *************************************************************************

alpha = pygame.font.SysFont("cursive", 21)

# Path to the font file
font_path = os.path.join("Fonts", "Akshar Unicode.ttf")
try:
    hindi = pygame.font.Font(font_path, 18)
except FileNotFoundError:
    print(f"Error: Font file not found at {font_path}. Using default system font.")
    hindi = pygame.font.SysFont("Arial", 18) # Fallback to a common system font
except Exception as e:
    print(f"Error loading font {font_path}: {e}. Using default system font.")
    hindi = pygame.font.SysFont("Arial", 18) # Fallback

msg = alpha.render("Guess the word using the hint below", True, BLUE)

# IMAGES ***********************************************************************

img_list = []
for i in range(7):
    img_path = os.path.join("Assets", f"hangman{i}.png")
    try:
        img = pygame.image.load(img_path)
        img = pygame.transform.scale(img, (100, 103))
        img_list.append(img)
    except pygame.error as e:
        print(f"Error loading hangman image {img_path}: {e}. Please ensure all hangman images (hangman0.png to hangman6.png) are in the 'Assets' folder.")
        # Create a placeholder image if loading fails
        placeholder_img = pygame.Surface((100, 103))
        placeholder_img.fill(RED)
        pygame.draw.rect(placeholder_img, WHITE, placeholder_img.get_rect(), 2)
        text_surface = alpha.render(str(i), True, WHITE)
        placeholder_img.blit(text_surface, (50 - text_surface.get_width() // 2, 50 - text_surface.get_height() // 2))
        img_list.append(placeholder_img)

hangman_logo_path = "hangman_top.png"
try:
    hangman_logo = pygame.image.load(hangman_logo_path)
    hangman_logo = pygame.transform.scale(hangman_logo, (WIDTH - 69, 128))
except pygame.error as e:
    print(f"Error loading hangman logo {hangman_logo_path}: {e}. Please ensure 'hangman_top.png' is in the main directory.")
    # Create a placeholder for the logo
    hangman_logo = pygame.Surface((WIDTH - 69, 128))
    hangman_logo.fill(BLUE)
    logo_text = alpha.render("HANGMAN", True, WHITE)
    hangman_logo.blit(logo_text, (hangman_logo.get_width() // 2 - logo_text.get_width() // 2, hangman_logo.get_height() // 2 - logo_text.get_height() // 2))

# SOUNDS ***********************************************************************

win_fx_path = os.path.join("Sounds", "win.wav")
lose_fx_path = os.path.join("Sounds", "lose.wav")

try:
    win_fx = pygame.mixer.Sound(win_fx_path)
except pygame.error as e:
    print(f"Error loading win sound {win_fx_path}: {e}. Win sound will not play.")
    win_fx = None # Set to None if loading fails

try:
    lose_fx = pygame.mixer.Sound(lose_fx_path)
except pygame.error as e:
    print(f"Error loading lose sound {lose_fx_path}: {e}. Lose sound will not play.")
    lose_fx = None # Set to None if loading fails

# DATA **************************************************************************

word_dict = {}
word_list = [] # Stores words already used in the current game session

words_file_path = "words.txt"
try:
    with open(words_file_path, encoding='utf-8') as file: # Added encoding for broader compatibility
        for line in file.readlines():
            try:
                w, m = line.strip().split(":", 1) # Split only on the first colon
                word_dict[w.strip().upper()] = m.strip() # Store words in uppercase
            except ValueError:
                print(f"Skipping malformed line in words.txt: {line.strip()}")
except FileNotFoundError:
    print(f"Error: {words_file_path} not found. Please create it and add words in 'WORD:HINT' format.")
    # Fallback with some default words if file is missing
    word_dict = {
        "PYTHON": "A popular programming language",
        "JAVASCRIPT": "Language for web browsers",
        "HANGMAN": "The name of this game",
        "COMPUTER": "An electronic device for processing data",
        "KEYBOARD": "Used for typing",
        "MONITOR": "Displays visual output"
    }
except Exception as e:
    print(f"Error reading {words_file_path}: {e}")
    # Fallback in case of other reading errors
    word_dict = {
        "PROGRAM": "A set of instructions for a computer",
        "CODE": "Instructions written in a programming language"
    }

if not word_dict: # If word_dict is still empty, add a last resort fallback
    word_dict = {"HELLO": "A common greeting", "WORLD": "The Earth"}
    print("Warning: No words loaded, using default fallback words.")


def getWord():
    # Filter out words already used
    available_words = [w for w in list(word_dict.keys()) if w not in word_list]
    if not available_words:
        # If all words are used, reset word_list or handle game end
        print("All words used! Resetting word list for new game.")
        word_list.clear() # Clear used words to allow reuse
        available_words = list(word_dict.keys()) # Re-populate available words

    if available_words:
        word = random.choice(available_words)
        meaning = word_dict[word]
        return word, meaning
    else:
        # This case should ideally not be reached if word_list is cleared
        return "ERROR", "No words available"

# Function to wrap text
def wrap_text(text, font, max_width):
    words = text.split(' ')
    lines = []
    current_line = []
    for word in words:
        # Test if adding the next word exceeds the max_width
        if font.size(' '.join(current_line + [word]))[0] < max_width:
            current_line.append(word)
        else:
            # If it exceeds, start a new line with the current word
            lines.append(' '.join(current_line))
            current_line = [word]
    lines.append(' '.join(current_line)) # Add the last line
    return lines

word, meaning = getWord()
word_list.append(word)
guessed = ['' for _ in range(len(word))] # Use _ for unused loop variable

# OBJECTS **********************************************************************

class FadeScreen:
	def __init__(self, w, h, color):
		self.surface = pygame.Surface((w, h))
		self.surface.fill(color)
		self.alpha = 255
		self.surface.set_alpha(self.alpha)
		
	def update(self):
		self.alpha -= 0.8
		if self.alpha < 0:
			self.alpha = 0
		self.surface.set_alpha(self.alpha)
		
	def draw(self, x, y):
		win.blit(self.surface, (x,y))

class Button(pygame.sprite.Sprite):
	def __init__(self, text, x, y, width=30, height=30, text_color=WHITE, border_color=WHITE, bg_color=None):
		super(Button, self).__init__()
		
		self.text = text
		self.text_color = text_color
		self.border_color = border_color
		self.bg_color = bg_color
		
		self.image = alpha.render(self.text, True, self.text_color)
		self.rect = pygame.Rect(x, y, width, height)
		self.clicked = False
		
	def collision(self, pos):
		if pos and not self.clicked:
			if self.rect.collidepoint(pos):
				# For alphabet buttons, change color on click
				if self.text.isalpha():
					self.image = alpha.render(self.text, True, GREEN)
				self.clicked = True
				return True, self.text
		return False
		
	def update(self):
		if self.bg_color:
			pygame.draw.rect(win, self.bg_color, self.rect)
		pygame.draw.rect(win, self.border_color, self.rect, 2)
		win.blit(self.image, (self.rect.centerx - self.image.get_width() // 2, self.rect.centery - self.image.get_height() // 2))
		
	def reset(self):
		self.clicked = False
		self.image = alpha.render(self.text, True, self.text_color)

# Hint Box Class
class HintBox:
    def __init__(self, x, y, width, height, bg_color, border_color, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.bg_color = bg_color
        self.border_color = border_color
        self.font = font
        self.hint_text = ""
        self.visible = False
        self.padding = 10

    def set_hint(self, text):
        self.hint_text = text
        self.visible = True

    def hide(self):
        self.visible = False

    def get_close_button_rect(self):
        # Calculate the close button rect based on the hint box's current position
        close_button_size = 20
        return pygame.Rect(self.rect.right - close_button_size - 5, self.rect.y + 5, close_button_size, close_button_size)

    def draw(self, surface):
        if self.visible:
            # Draw a semi-transparent overlay to dim the background
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150)) # Black with 150 alpha (out of 255)
            surface.blit(overlay, (0, 0))

            pygame.draw.rect(surface, self.bg_color, self.rect, border_radius=10)
            pygame.draw.rect(surface, self.border_color, self.rect, 2, border_radius=10)

            # Wrap and render hint text
            max_text_width = self.rect.width - 2 * self.padding
            wrapped_lines = wrap_text(self.hint_text, self.font, max_text_width)
            
            text_y = self.rect.y + self.padding
            for line in wrapped_lines:
                line_surface = self.font.render(line, True, BLACK)
                line_x = self.rect.x + self.padding + (max_text_width - line_surface.get_width()) // 2
                surface.blit(line_surface, (line_x, text_y))
                text_y += self.font.get_height() + 2 # Line spacing

            # Draw a close button
            close_button_rect = self.get_close_button_rect()
            pygame.draw.circle(surface, RED, close_button_rect.center, close_button_rect.width // 2)
            close_text = alpha.render("X", True, WHITE)
            surface.blit(close_text, (close_button_rect.centerx - close_text.get_width() // 2, close_button_rect.centery - close_text.get_height() // 2))
            

btns = []
for i in range(26):
	text = f"{chr(65+i)}"
	x = 20 + ( i % 7 ) * 36
	y = 330 + (i // 7) * 36
	btns.append(Button(text, x, y))

# Hint button - repositioned to avoid overlapping the word dashes
# Calculate the y-position based on the "Guess the word using the hint below" message
msg_rect = msg.get_rect(center=(WIDTH // 2, 25))
hint_button = Button("HINT", WIDTH // 2 - 30, msg_rect.bottom + 10, 60, 30, BLUE, BLUE, LIGHT_GRAY) # Moved below msg
	
restart_img = alpha.render("RESTART", True, WHITE)
quit_img = alpha.render("QUIT", True, WHITE)

restart_rect = restart_img.get_rect()
restart_rect.x = WIDTH // 2 - restart_img.get_width() // 2 - 40 # Adjusted position
restart_rect.y = 180

quit_rect = quit_img.get_rect()
quit_rect.x = WIDTH // 2 - quit_img.get_width() // 2 + 40 # Adjusted position
quit_rect.y = 180 # Placed next to restart for better layout

# Initialize Hint Box
hint_box_width = WIDTH - 40
hint_box_height = 150
hint_box_x = (WIDTH - hint_box_width) // 2
hint_box_y = (HEIGHT - hint_box_height) // 2
hint_box = HintBox(hint_box_x, hint_box_y, hint_box_width, hint_box_height, LIGHT_GRAY, BLUE, hindi)


# GAME ************************************************************************

lives = 6
score = 0
gameover = False
homepage = True

fadeScreen = FadeScreen(WIDTH, HEIGHT, GRAY)

score_img = alpha.render(f"Score : {score}", True, WHITE)
lives_img = alpha.render(f"Lives : {lives}", True, WHITE)

running = True
while running:
	pos = None
	win.fill(BLACK) # Fill with black initially for clear background
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
				running = False
				
		if event.type == pygame.MOUSEBUTTONDOWN:
			pos = pygame.mouse.get_pos()
            # Check for hint box close button click
			if hint_box.visible:
				close_button_rect = hint_box.get_close_button_rect() # Get the rect
				if close_button_rect.collidepoint(pos):
					hint_box.hide()
			
	if homepage:
		if fadeScreen.alpha > 0: # Check if alpha is greater than 0
			fadeScreen.update()
			fadeScreen.draw(0,0)
			
			# Ensure hangman_logo is not None before setting alpha
			if hangman_logo:
				hangman_logo.set_alpha(int(fadeScreen.alpha)) # Cast to int for set_alpha
				win.blit(hangman_logo, (WIDTH//2 - hangman_logo.get_width() // 2, HEIGHT//2 - hangman_logo.get_height() // 2))
			
		else:
			homepage = False
		
	else:
		win.fill(GRAY)
		
		# Always draw fixed UI elements (backgrounds for score/hint area, and the score/lives text)
		pygame.draw.rect(win, (20,20,20), (0, 0, WIDTH, 90))
		pygame.draw.rect(win, BLUE, (0, 0, WIDTH, 90), 2)
		pygame.draw.rect(win, (20,20,20), (0, HEIGHT//2 + 30, WIDTH, HEIGHT))
		pygame.draw.rect(win, BLUE, (0, HEIGHT//2 + 30, WIDTH, HEIGHT), 2)
		win.blit(score_img, (WIDTH// 2 + score_img.get_width() // 2 + 30, 110))
		win.blit(lives_img, (WIDTH// 2 + lives_img.get_width() // 2 + 30, 130))
		win.blit(msg, (WIDTH // 2 - msg.get_width() // 2, 25)) # "Guess the word..." message

		# Only draw game-specific elements if hint box is NOT visible
		if not hint_box.visible:
			# Render hangman images
			if lives < len(img_list):
				image = img_list[6-lives]
				win.blit(image, (WIDTH // 2 - image.get_width() // 2 - 60, HEIGHT // 2 - image.get_height() // 2 - 100))
			else:
				# Fallback if image list is incomplete (e.g., due to loading errors)
				print("Warning: Not enough hangman images loaded. Displaying placeholder.")
				placeholder_img = pygame.Surface((100, 103))
				placeholder_img.fill(RED)
				pygame.draw.rect(placeholder_img, WHITE, placeholder_img.get_rect(), 2)
				text_surface = alpha.render("?", True, WHITE)
				placeholder_img.blit(text_surface, (50 - text_surface.get_width() // 2, 50 - text_surface.get_height() // 2))
				win.blit(placeholder_img, (WIDTH // 2 - placeholder_img.get_width() // 2 - 60, HEIGHT // 2 - placeholder_img.get_height() // 2 - 100))
			
			# render alphabet buttons
			for btn in btns:
				btn.update()
				collision = btn.collision(pos) 
				if collision and not gameover:
					guessed_char = collision[1]
					if guessed_char in word:
						for i in range(len(word)):
							if word[i] == guessed_char:
								guessed[i] = guessed_char
								
						if '' not in guessed: # Check if all characters are guessed
							word, meaning = getWord()
							guessed = ['' for _ in range(len(word))]
							word_list.append(word)
							if win_fx: # Play sound only if loaded
								win_fx.play()
							score += 1
							
							score_img = alpha.render(f"Score : {score}", True, WHITE)
							
							for btn in btns:
								btn.reset()
					else:
						lives -= 1
						lives_img = alpha.render(f"Lives : {lives}", True, WHITE)
						if lives == 0:
							gameover = True
							if lose_fx: # Play sound only if loaded
								lose_fx.play()
						
			# Render Dash and Characters
			for i in range(len(word)):
				x = WIDTH // 2 - ((18 * len(word)) // 2)
				x1, y1 = (x + 20 * i,HEIGHT // 2)
				x2, y2 = (x + 20 * i + 15, HEIGHT // 2)
				pygame.draw.line(win, BLACK, (x1, y1), (x2, y2), 2) # Use BLACK for lines
				
				if not gameover:
					char = alpha.render(guessed[i], True, WHITE)
				else:
					char = alpha.render(word[i], True, BLUE)
				win.blit(char, (x1 + 3, y1 - 15))
						
			# Render Hint button
			hint_button.update()
			if hint_button.collision(pos) and not gameover:
				hint_box.set_hint(meaning)

		# Draw hint box if visible (always on top of game elements)
		if hint_box.visible:
			hint_box.draw(win)
		
		# Gameover buttons are drawn regardless, but their click logic is affected by hint box visibility
		if gameover:
			# If game is over, hide the hint box so gameover screen is clear
			hint_box.hide() 

			win.blit(restart_img, restart_rect)
			win.blit(quit_img, quit_rect)
			
			pygame.draw.rect(win, RED, (restart_rect.x - 5, restart_rect.y - 5, restart_rect.width + 10, restart_rect.height + 10), 2) # Dynamic size
			pygame.draw.rect(win, RED, (quit_rect.x - 5, quit_rect.y - 5, quit_rect.width + 10, quit_rect.height + 10), 2) # Dynamic size
			
			if pos and restart_rect.collidepoint(*pos):
				score = 0
				lives = 6
				gameover = False
				
				word_list.clear() # Clear word_list for a fresh game
				word, meaning = getWord()
				word_list.append(word)
				guessed = ['' for _ in range(len(word))]
				
				for btn in btns:
					btn.reset()
					
				score_img = alpha.render(f"Score : {score}", True, WHITE)
				lives_img = alpha.render(f"Lives : {lives}", True, WHITE)
				
			if pos and quit_rect.collidepoint(*pos):
				running = False
				
	pygame.draw.rect(win, BLUE, (0,0,WIDTH,HEIGHT), 3)
	clock.tick(FPS)
	pygame.display.update()

pygame.quit()
