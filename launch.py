import os
import sys
import subprocess
import threading
import json
from datetime import datetime
import tempfile # Import for temporary file operations

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox,
    QGridLayout, QScrollArea, QGraphicsDropShadowEffect, QHBoxLayout, QDialog, QLineEdit,
    QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve, QSize, QRect, QPoint, QTimer
from PyQt5.QtGui import QIcon, QColor, QFont, QPixmap, QImage

# --- Placeholder Game Classes ---
# These are placeholders. In a real application, you'd import your actual game classes.
# The 'type' in games_config.json determines how they are launched.

class BaseGame:
    """A base class for all games, providing common functionality."""
    def __init__(self, name="Unnamed Game"):
        self.name = name

    def run(self):
        """Method to run non-GUI games (e.g., console-based)."""
        print(f"--- Running {self.name} (Non-GUI) ---")
        # Simulate game execution
        import time
        time.sleep(2) # Simulate work
        print(f"--- {self.name} finished. ---")

class QtGameWindow(QMainWindow):
    """A placeholder for a GUI game built with PyQt5."""
    def __init__(self, name="Qt Game"):
        super().__init__()
        self.setWindowTitle(f"{name} - Game")
        self.setGeometry(200, 200, 600, 400)
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #2c3e50, stop:1 #3498db);
            }
            QLabel {
                color: white;
                font-size: 18pt;
                text-align: center;
            }
        """)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        label = QLabel(f"Welcome to {name}!")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        print(f"--- Launched {name} (GUI) ---")

# --- Game Class Mapping (from JSON) ---
# This dictionary will map game names from JSON to their actual Python classes.
# You will need to manually map your game classes here.
GAME_CLASS_MAP = {
    'Aeroblasters': BaseGame,
    'Angry Walls': BaseGame,
    'Arc Dash': BaseGame,
    'Asteroids': BaseGame,
    'Bounce': BaseGame,
    'Car Racing 2d': BaseGame,
    'Cave Story': BaseGame,
    'Connected': BaseGame,
    'Dodgy Walls': BaseGame,
    'Dots & Boxes': BaseGame,
    'Egg Catching Game': BaseGame,
    'Flappy Bird': BaseGame,
    'GhostBusters': BaseGame,
    'Hangman': BaseGame,
    'Hex Dash': BaseGame,
    'HyperTile Dash': BaseGame,
    'Jungle Dash': BaseGame,
    'Level Designer': BaseGame,
    'Memory Puzzle': BaseGame,
    'MineSweeper': BaseGame,
    'Piano Tiles': BaseGame,
    'Picture Sliding Puzzle': BaseGame,
    'Pong': BaseGame,
    'Qircle Rush': BaseGame,
    'Rock Paper Scissor': BaseGame,
    'Rotate Dash': BaseGame,
    'Snake': BaseGame,
    'SpriteSheet Cutter': BaseGame,
    'Tetris': BaseGame,
    'Tic Tac Toe': BaseGame,
    # Example for a GUI game, if you have one:
    # 'MyQtGame': QtGameWindow,
}


class CPGames:
    """Manages the collection of supported games, now loaded from JSON."""
    CONFIG_FILE = 'games_config.json'

    def __init__(self):
        # Display the full path of the config file being used
        self.full_config_path = os.path.abspath(self.CONFIG_FILE)
        QMessageBox.information(None, "Config File Path", f"Attempting to load/save config from: {self.full_config_path}")
        print(f"CPGames initialized. Config file path: {self.full_config_path}")

        self.games_data = self.load_games_config()
        # Map game names to their data for quick lookup
        self.games_by_name = {game['name']: game for game in self.games_data}

    def load_games_config(self):
        """
        Loads game data from the JSON configuration file.
        Raises an exception if the file is not found or is invalid.
        Ensures 'isFavorite' and 'category' fields exist.
        """
        if not os.path.exists(self.CONFIG_FILE):
            # If config file doesn't exist, create a default one
            print(f"Config file '{self.CONFIG_FILE}' not found. Creating a new one with default data.")
            default_games_data = [
                {"name": "Aeroblasters", "description": "A high-flying arcade shooter.", "type": "non_gui", "category": "Shooter", "last_played": None, "isFavorite": False},
                {"name": "Angry Walls", "description": "A challenging puzzle game.", "type": "non_gui", "category": "Puzzle", "last_played": None, "isFavorite": False},
                {"name": "Arc Dash", "description": "A fast-paced reflex game.", "type": "non_gui", "category": "Arcade", "last_played": None, "isFavorite": False},
                {"name": "Asteroids", "description": "Classic arcade action!", "type": "non_gui", "category": "Arcade", "last_played": None, "isFavorite": False},
                {"name": "Bounce", "description": "A physics-based platformer.", "type": "non_gui", "category": "Platformer", "last_played": None, "isFavorite": False},
                {"name": "Car Racing 2d", "description": "Top-down 2D racing.", "type": "non_gui", "category": "Racing", "last_played": None, "isFavorite": False},
                {"name": "Cave Story", "description": "Classic indie adventure.", "type": "non_gui", "category": "Adventure", "last_played": None, "isFavorite": False},
                {"name": "Connected", "description": "Minimalist puzzle game.", "type": "non_gui", "category": "Puzzle", "last_played": None, "isFavorite": False},
                {"name": "Dodgy Walls", "description": "Navigate a treacherous maze.", "type": "non_gui", "category": "Puzzle", "last_played": None, "isFavorite": False},
                {"name": "Dots & Boxes", "description": "Classic pen-and-paper game.", "type": "non_gui", "category": "Board Game", "last_played": None, "isFavorite": False},
                {"name": "Egg Catching Game", "description": "Catch falling eggs!", "type": "non_gui", "category": "Arcade", "last_played": None, "isFavorite": False},
                {"name": "Flappy Bird", "description": "Infamous mobile game.", "type": "non_gui", "category": "Arcade", "last_played": None, "isFavorite": False},
                {"name": "GhostBusters", "description": "Bust ghosts and save the city.", "type": "non_gui", "category": "Action", "last_played": None, "isFavorite": False},
                {"name": "Hangman", "description": "Guess the word letter by letter.", "type": "non_gui", "category": "Word Game", "last_played": None, "isFavorite": False},
                {"name": "Hex Dash", "description": "Navigate a hexagonal maze.", "type": "non_gui", "category": "Arcade", "last_played": None, "isFavorite": False},
                {"name": "HyperTile Dash", "description": "Tap tiles in sequence.", "type": "non_gui", "category": "Puzzle", "last_played": None, "isFavorite": False},
                {"name": "Jungle Dash", "description": "Run, jump, and slide.", "type": "non_gui", "category": "Runner", "last_played": None, "isFavorite": False},
                {"name": "Level Designer", "description": "Design your own game levels.", "type": "non_gui", "category": "Utility", "last_played": None, "isFavorite": False},
                {"name": "Memory Puzzle", "description": "Test your memory skills.", "type": "non_gui", "category": "Puzzle", "last_played": None, "isFavorite": False},
                {"name": "MineSweeper", "description": "Clear the minefield.", "type": "non_gui", "category": "Puzzle", "last_played": None, "isFavorite": False},
                {"name": "Piano Tiles", "description": "Test your finger speed and rhythm.", "type": "non_gui", "category": "Rhythm", "last_played": None, "isFavorite": False},
                {"name": "Picture Sliding Puzzle", "description": "Rearrange scrambled tiles.", "type": "non_gui", "category": "Puzzle", "last_played": None, "isFavorite": False},
                {"name": "Pong", "description": "Original arcade classic.", "type": "non_gui", "category": "Arcade", "last_played": None, "isFavorite": False},
                {"name": "Qircle Rush", "description": "Guide your circle through obstacles.", "type": "non_gui", "category": "Arcade", "last_played": None, "isFavorite": False},
                {"name": "Rock Paper Scissor", "description": "Ultimate decision-making game.", "type": "non_gui", "category": "Casual", "last_played": None, "isFavorite": False},
                {"name": "Rotate Dash", "description": "Rotate the world to guide your character.", "type": "non_gui", "category": "Puzzle", "last_played": None, "isFavorite": False},
                {"name": "Snake", "description": "Retro arcade hit.", "type": "non_gui", "category": "Arcade", "last_played": None, "isFavorite": False},
                {"name": "SpriteSheet Cutter", "description": "Utility tool for sprite sheets.", "type": "non_gui", "category": "Utility", "last_played": None, "isFavorite": False},
                {"name": "Tetris", "description": "Iconic puzzle game.", "type": "non_gui", "category": "Puzzle", "last_played": None, "isFavorite": False},
                {"name": "Tic Tac Toe", "description": "Timeless game of X's and O's.", "type": "non_gui", "category": "Board Game", "last_played": None, "isFavorite": False},
            ]
            self._atomic_save(default_games_data)
            return default_games_data

        try:
            with open(self.CONFIG_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if not isinstance(data, list):
                    raise ValueError("JSON content is not a list. Expected a list of game objects.")
                
                # Ensure all games have 'isFavorite' and 'category' fields
                for game in data:
                    if 'isFavorite' not in game:
                        game['isFavorite'] = False
                    if 'category' not in game:
                        game['category'] = "" # Default to empty string
                return data
        except json.JSONDecodeError as e:
            QMessageBox.critical(None, "Configuration Error", f"Error decoding JSON from '{self.CONFIG_FILE}': {e}. "
                                 "Please check the file for syntax errors or delete it to generate a new one.")
            return [] # Return empty list on error
        except Exception as e:
            QMessageBox.critical(None, "Configuration Error", f"An unexpected error occurred while loading '{self.CONFIG_FILE}': {e}")
            return [] # Return empty list on error

    def _atomic_save(self, data_to_save):
        """
        Saves data to the JSON configuration file using an atomic write.
        This writes to a temporary file and then renames it to prevent data corruption
        in case of write errors or crashes.
        """
        temp_file_path = None
        try:
            # Create a temporary file in the same directory as the config file
            temp_fd, temp_file_path = tempfile.mkstemp(dir=os.path.dirname(self.full_config_path), suffix='.tmp')
            with os.fdopen(temp_fd, 'w', encoding='utf-8') as f:
                json.dump(data_to_save, f, indent=4)
                f.flush()
                os.fsync(f.fileno()) # Ensure data is written to disk

            # Atomically replace the old config file with the new one
            os.replace(temp_file_path, self.full_config_path)
            print(f"Games config saved successfully to {self.full_config_path} using atomic write!")

        except IOError as e:
            QMessageBox.critical(None, "File Save Error", f"Could not save '{self.CONFIG_FILE}'. Please check file permissions. Error: {e}")
            print(f"IOError during atomic save: {e}")
        except Exception as e:
            QMessageBox.critical(None, "File Save Error", f"An unexpected error occurred while saving '{self.CONFIG_FILE}': {e}")
            print(f"General error during atomic save: {e}")
        finally:
            # Clean up the temporary file if it still exists (e.g., if an error occurred before rename)
            if temp_file_path and os.path.exists(temp_file_path):
                os.remove(temp_file_path)
                print(f"Cleaned up temporary file: {temp_file_path}")


    def save_games_config(self):
        """Saves current in-memory game data back to the JSON configuration file."""
        self._atomic_save(self.games_data)


    def reload_games_config(self):
        """Reloads game data from the JSON configuration file into memory."""
        print("Reloading games config from disk...")
        self.games_data = self.load_games_config()
        self.games_by_name = {game['name']: game for game in self.games_data}
        print("Games config reloaded.")


    def get_all_games(self):
        """Returns a list of all game data dictionaries."""
        return self.games_data

    def get_game_by_name(self, game_name):
        """Returns the data dictionary for a specific game name."""
        return self.games_by_name.get(game_name)

    def update_game_last_played(self, game_name):
        """Updates the 'last_played' timestamp for a game."""
        game = self.games_by_name.get(game_name)
        if game:
            game['last_played'] = datetime.now().isoformat()
            self.save_games_config() # Save changes immediately

    def toggle_game_favorite(self, game_name):
        """Toggles the 'isFavorite' status for a game."""
        game = self.games_by_name.get(game_name)
        if game:
            game['isFavorite'] = not game.get('isFavorite', False) # Toggle, default to False
            self.save_games_config() # Save changes immediately

    def get_recently_played_games(self, count=3):
        """Returns a list of recently played games, sorted by last_played."""
        played_games = [g for g in self.games_data if g.get('last_played')]
        # Sort in descending order of last_played timestamp
        played_games.sort(key=lambda x: x['last_played'], reverse=True)
        return played_games[:count]

    def get_favorite_games(self):
        """Returns a list of games marked as favorites."""
        return [g for g in self.games_data if g.get('isFavorite', False)]

    def clear_recently_played_data(self):
        """
        Clears the 'last_played' timestamp for all games by modifying the in-memory
        data directly and then saving it using an atomic write.
        """
        print("Clearing recently played data by modifying in-memory data and saving atomically...")
        # Iterate directly over self.games_data and set last_played to None
        for game in self.games_data:
            if 'last_played' in game:
                game['last_played'] = None
        
        # Save this modified data to the config file using the atomic save method
        self.save_games_config()
        print("Recently played data cleared and config file saved atomically.")


# --- Custom GameCard Widget ---
class GameCard(QWidget):
    """
    A custom widget representing a single game, designed to look like an interactive card.
    It displays an icon and the game name, with visual feedback for hover and selection.
    """
    # Signal emitted when this card is clicked, carrying its game name.
    clicked = pyqtSignal(str)
    # Signal emitted when the favorite button is clicked, carrying game name
    favorite_toggled = pyqtSignal(str)

    # Base directory for icons
    ICONS_DIR = 'icons'
    DEFAULT_ICON_PATH = os.path.join(ICONS_DIR, 'generic_game.png')

    def __init__(self, game_data, parent=None):
        super().__init__(parent)
        self.game_data = game_data
        self.game_name = game_data['name']
        self._is_selected = False # Internal state for selection
        self.setFixedSize(160, 160) # Slightly larger fixed size for icons

        self.main_layout = QGridLayout(self) # Use QGridLayout for the card itself
        self.main_layout.setContentsMargins(5, 5, 5, 5) # Smaller margins
        self.main_layout.setSpacing(0) # No spacing between internal elements

        self.setup_ui()
        self.apply_base_style()
        self.setCursor(Qt.PointingHandCursor) # Change cursor on hover
        
        # Animations for size and shadow glow
        self.size_animation = QPropertyAnimation(self, b"size")
        self.size_animation.setDuration(150) # milliseconds

        self.shadow_animation = QPropertyAnimation(self.graphicsEffect(), b"color")
        self.shadow_animation.setDuration(150)
        self.shadow_animation.setEasingCurve(QEasingCurve.OutQuad)

        # Animation for blur radius (for glow effect)
        self.blur_animation = QPropertyAnimation(self.graphicsEffect(), b"blurRadius")
        self.blur_animation.setDuration(150)
        self.blur_animation.setEasingCurve(QEasingCurve.OutQuad)


    def setup_ui(self):
        """
        Sets up the layout and widgets for the game card (icon, name, and favorite button).
        """
        # Icon Label - now loads from the 'icons' folder
        self.icon_label = QLabel()
        self.icon_label.setAlignment(Qt.AlignCenter)

        # Normalize game name for filename (lowercase, replace spaces with underscores, handle '&')
        filename_game_name = self.game_name.lower().replace(' ', '_').replace('&', 'and')
        icon_filename = f"{filename_game_name}.png"
        icon_path = os.path.join(self.ICONS_DIR, icon_filename)

        if os.path.exists(icon_path):
            pixmap = QPixmap(icon_path)
            self.icon_label.setPixmap(pixmap.scaled(96, 96, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            # Fallback to default icon if specific one not found
            if os.path.exists(self.DEFAULT_ICON_PATH):
                pixmap = QPixmap(self.DEFAULT_ICON_PATH)
                self.icon_label.setPixmap(pixmap.scaled(96, 96, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            else:
                # Ultimate fallback to generic emoji if no image icon is available
                self.icon_label.setText('❓') # Use a question mark emoji
                font = QFont()
                font.setPointSize(40)
                self.icon_label.setFont(font)
                self.icon_label.setStyleSheet("color: white;")

        # Game Name Label
        self.name_label = QLabel(self.game_name.replace('_', ' ').title()) # Format name nicely
        self.name_label.setAlignment(Qt.AlignCenter)
        self.name_label.setWordWrap(True)
        self.name_label.setStyleSheet("""
            color: #FFFFFF; /* Changed to pure white for maximum visibility */
            font-weight: bold;
            font-size: 10pt; /* Slightly smaller to fit */
            font-family: 'Segoe UI', sans-serif;
        """)

        # Favorite button
        self.favorite_button = QPushButton()
        self.favorite_button.setFixedSize(28, 28) # Slightly smaller button
        self.favorite_button.clicked.connect(self._on_favorite_clicked)
        self.favorite_button.setCursor(Qt.PointingHandCursor) # Indicate clickable
        self._update_favorite_icon() # Set initial icon

        # Add widgets to the QGridLayout
        self.main_layout.addWidget(self.favorite_button, 0, 1, Qt.AlignTop | Qt.AlignRight) # Top-right corner
        self.main_layout.addWidget(self.icon_label, 1, 0, 1, 2, Qt.AlignCenter) # Center icon, span 2 columns
        self.main_layout.addWidget(self.name_label, 2, 0, 1, 2, Qt.AlignCenter) # Center name, span 2 columns
        self.main_layout.setRowStretch(0, 1) # Give some stretch to the top row
        self.main_layout.setRowStretch(1, 4) # Give more space to icon row
        self.main_layout.setRowStretch(2, 1) # Give some space to name row
        self.main_layout.setColumnStretch(0, 1) # Allow columns to stretch
        self.main_layout.setColumnStretch(1, 1)


        # Add a subtle drop shadow for a 3D effect
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20) # More blur
        shadow.setXOffset(3)
        shadow.setYOffset(3)
        shadow.setColor(QColor(0, 0, 0, 120)) # Darker, more prominent shadow
        self.setGraphicsEffect(shadow)

    def _update_favorite_icon(self):
        """Updates the favorite button icon based on the game's favorite status."""
        if self.game_data.get('isFavorite', False):
            self.favorite_button.setText("⭐") # Filled star emoji
            self.favorite_button.setToolTip("Remove from Favorites")
        else:
            self.favorite_button.setText("☆") # Outline star emoji
            self.favorite_button.setToolTip("Add to Favorites")
        
        self.favorite_button.setStyleSheet(f"""
            QPushButton {{
                background-color: rgba(0, 0, 0, 0.5);
                border: none;
                border-radius: 14px; /* Half of fixed size for perfect circle */
                color: {'yellow' if self.game_data.get('isFavorite', False) else 'gray'};
                font-size: 16pt; /* Adjust emoji size */
                padding: 0; /* Remove padding from button itself */
            }}
            QPushButton:hover {{
                background-color: rgba(0, 0, 0, 0.7);
            }}
        """)


    def _on_favorite_clicked(self):
        """Emits the favorite_toggled signal."""
        self.favorite_toggled.emit(self.game_name)


    def apply_base_style(self):
        """
        Applies the default (unselected) style to the card.
        This gives a "hollow" appearance with a border.
        """
        self.setStyleSheet("""
            GameCard {
                background-color: rgba(0, 15, 30, 0.6); /* Slightly transparent dark background */
                border: 2px solid #004D99; /* Deep blue border */
                border-radius: 15px; /* More rounded corners */
                margin: 5px;
            }
            GameCard:hover {
                background-color: rgba(0, 83, 156, 0.4); /* Lighter on hover, semi-transparent */
                border: 2px solid #0099FF; /* Brighter blue on hover */
            }
        """)
        # Reset shadow color directly for base style
        self.graphicsEffect().setColor(QColor(0, 0, 0, 120))
        self.graphicsEffect().setBlurRadius(20)


    def apply_selected_style(self):
        """
        Applies the selected style to the card, making it more prominent.
        """
        self.setStyleSheet("""
            GameCard {
                background-color: #0074D9; /* Solid primary blue when selected */
                border: 3px solid #00EEFF; /* Bright, thicker border for selection */
                border-radius: 15px;
                margin: 5px;
            }
            GameCard:hover {
                background-color: #0088FF; /* Slightly different hover when selected */
            }
        """)
        # Set shadow color directly for selected style
        self.graphicsEffect().setColor(QColor(0, 200, 255, 180))
        self.graphicsEffect().setBlurRadius(25) # Slightly more blur when selected


    def set_selected(self, selected):
        """
        Sets the selection state of the card and updates its visual style.
        """
        if self._is_selected == selected:
            return

        self._is_selected = selected
        if self._is_selected:
            self.apply_selected_style()
        else:
            self.apply_base_style()

    def is_selected(self):
        """
        Returns the current selection state of the card.
        """
        return self._is_selected

    def enterEvent(self, event):
        """Animation on mouse hover enter with glow effect."""
        self.size_animation.setStartValue(self.size())
        self.size_animation.setEndValue(QSize(170, 170)) # Slightly enlarge
        self.size_animation.setEasingCurve(QEasingCurve.OutQuad)
        self.size_animation.start()

        # Glow effect: Animate shadow color to a brighter, more transparent color
        self.shadow_animation.setStartValue(self.graphicsEffect().color())
        self.shadow_animation.setEndValue(QColor(0, 255, 255, 220)) # Cyan glow, higher alpha
        self.shadow_animation.start()

        # Animate blur radius for a stronger glow
        self.blur_animation.setStartValue(self.graphicsEffect().blurRadius())
        self.blur_animation.setEndValue(35) # Increased blur
        self.blur_animation.start()

        super().enterEvent(event)

    def leaveEvent(self, event):
        """Animation on mouse hover leave with glow effect reset."""
        self.size_animation.setStartValue(self.size())
        self.size_animation.setEndValue(QSize(160, 160)) # Return to original size
        self.size_animation.setEasingCurve(QEasingCurve.InQuad)
        self.size_animation.start()

        # Reset glow effect: Animate shadow color back to original
        self.shadow_animation.setStartValue(self.graphicsEffect().color())
        self.shadow_animation.setEndValue(QColor(0, 0, 0, 120)) # Original dark shadow
        self.shadow_animation.start()

        # Reset blur radius
        self.blur_animation.setStartValue(self.graphicsEffect().blurRadius())
        self.blur_animation.setEndValue(20) # Original blur
        self.blur_animation.start()

        super().leaveEvent(event)

    def mousePressEvent(self, event):
        """
        Handles mouse press events to emit the clicked signal.
        """
        if event.button() == Qt.LeftButton:
            # Check if the click was on the favorite button
            # We need to map the event position to the button's local geometry
            # This is a common pattern to distinguish clicks on child widgets
            local_pos = self.favorite_button.mapFromParent(event.pos())
            if self.favorite_button.rect().contains(local_pos):
                # The click was on the favorite button, let its handler take over
                pass 
            else:
                # The click was on the card itself, but not the favorite button
                self.clicked.emit(self.game_name)
        super().mousePressEvent(event)


# --- GameInfoDialog Class ---
class GameInfoDialog(QDialog):
    """
    A custom dialog to display information about a selected game.
    Features a fade-in/fade-out effect and can be dismissed.
    Now includes Play Game and Favorite buttons.
    """
    play_game_requested = pyqtSignal(str)
    favorite_toggled = pyqtSignal(str)

    def __init__(self, game_data, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint) # No title bar
        self.setModal(True) # Make it modal to block interaction with main window

        self.game_data = game_data
        self.game_name = game_data['name']
        self.description = game_data['description']
        self.category = game_data.get('category', 'N/A')
        self.is_favorite = game_data.get('isFavorite', False)
        self.last_played = game_data.get('last_played')

        self.old_pos = None # To store the mouse position for dragging

        self.setup_ui()
        self.apply_style()
        self.setup_animation()

    def setup_ui(self):
        """Sets up the layout and widgets for the info dialog."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(15)
        main_layout.setAlignment(Qt.AlignCenter)

        # Game Title
        self.title_label = QLabel(self.game_name.replace('_', ' ').title())
        self.title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.title_label)

        # Category Label
        self.category_label = QLabel(f"Category: {self.category}")
        self.category_label.setAlignment(Qt.AlignCenter)
        self.category_label.setStyleSheet("color: #BBBBBB; font-size: 12pt;")
        main_layout.addWidget(self.category_label)

        # Last Played Label
        if self.last_played:
            try:
                last_played_dt = datetime.fromisoformat(self.last_played)
                self.last_played_label = QLabel(f"Last Played: {last_played_dt.strftime('%Y-%m-%d %H:%M')}")
            except ValueError:
                self.last_played_label = QLabel("Last Played: Invalid Date")
        else:
            self.last_played_label = QLabel("Last Played: Never")
        self.last_played_label.setAlignment(Qt.AlignCenter)
        self.last_played_label.setStyleSheet("color: #BBBBBB; font-size: 12pt;")
        main_layout.addWidget(self.last_played_label)


        # Game Description
        self.description_label = QLabel(self.description)
        self.description_label.setAlignment(Qt.AlignCenter)
        self.description_label.setWordWrap(True)
        main_layout.addWidget(self.description_label)

        # Action Buttons (Play Game, Favorite)
        action_button_layout = QHBoxLayout()
        action_button_layout.setSpacing(15)
        action_button_layout.setAlignment(Qt.AlignCenter)

        self.play_button = QPushButton("Play Game")
        self.play_button.clicked.connect(lambda: self.play_game_requested.emit(self.game_name))
        action_button_layout.addWidget(self.play_button)

        self.favorite_button = QPushButton()
        self.favorite_button.clicked.connect(lambda: self.favorite_toggled.emit(self.game_name))
        action_button_layout.addWidget(self.favorite_button)
        self._update_favorite_button_style() # Set initial style

        main_layout.addLayout(action_button_layout)

        # Close Button
        self.close_button = QPushButton("Got It!")
        self.close_button.clicked.connect(self.close_dialog)
        main_layout.addWidget(self.close_button, alignment=Qt.AlignCenter)

    def _update_favorite_button_style(self):
        """Updates the favorite button's text and style based on is_favorite."""
        if self.is_favorite:
            self.favorite_button.setText("⭐ Favorited")
            self.favorite_button.setStyleSheet("""
                QPushButton {
                    background-color: #FFD700; /* Gold */
                    border: none;
                    border-radius: 15px;
                    padding: 18px 35px;
                    font-size: 16pt;
                    font-weight: bold;
                    color: #333333; /* Dark text for contrast */
                }
                QPushButton:hover {
                    background-color: #E6C200;
                }
                QPushButton:pressed {
                    background-color: #CCAA00;
                }
            """)
        else:
            self.favorite_button.setText("☆ Add to Favorites")
            self.favorite_button.setStyleSheet("""
                QPushButton {
                    background-color: #666666; /* Gray */
                    border: none;
                    border-radius: 15px;
                    padding: 18px 35px;
                    font-size: 16pt;
                    font-weight: bold;
                    color: white;
                }
                QPushButton:hover {
                    background-color: #555555;
                }
                QPushButton:pressed {
                    background-color: #444444;
                }
            """)

    def update_favorite_status(self, new_status):
        """Updates the internal favorite status and refreshes the button style."""
        self.is_favorite = new_status
        self._update_favorite_button_style()


    def apply_style(self):
        """Applies custom styles to the dialog and its widgets."""
        self.setStyleSheet("""
            GameInfoDialog {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1,
                            stop:0 #1A2A3A, stop:1 #2C3A4A); /* Solid, dark gradient background */
                border: 5px solid #00FFFF; /* Thicker, bright cyan border for frame effect */
                border-radius: 20px; /* Rounded corners */
                padding: 35px; /* Increased padding */
            }
            QLabel {
                color: #FFFFFF; /* Pure white text for maximum visibility */
                font-family: 'Segoe UI', sans-serif;
            }
            GameInfoDialog QLabel#title_label { /* Specific style for title */
                font-size: 30pt; /* Even larger title */
                font-weight: bold;
                margin-bottom: 25px; /* More space below title */
            }
            GameInfoDialog QLabel#description_label { /* Specific style for description */
                font-size: 18pt; /* Even larger font size for description */
                line-height: 1.8; /* Increased line height for readability */
                padding: 20px; /* More padding for text */
            }
            QPushButton {
                background-color: #00A3CC;
                border: none;
                border-radius: 15px; /* More rounded button */
                padding: 18px 35px; /* Even larger button */
                font-size: 20pt; /* Larger font on button */
                font-weight: bold;
                color: white;
                margin-top: 30px; /* More space above button */
            }
            QPushButton:hover {
                background-color: #007ACC;
            }
            QPushButton:pressed {
                background-color: #005A90;
            }
        """)
        # Set object names for specific QLabel styling
        self.title_label.setObjectName("title_label")
        self.description_label.setObjectName("description_label")
        # Apply QGraphicsDropShadowEffect here for the dialog itself
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(50) # Even deeper, more prominent shadow
        shadow.setXOffset(0)
        shadow.setYOffset(18)
        shadow.setColor(QColor(0, 0, 0, 220)) # Darker, more prominent shadow
        self.setGraphicsEffect(shadow)


    def setup_animation(self):
        """Sets up the fade-in and fade-out animations, including scale."""
        self.opacity_animation = QPropertyAnimation(self, b"windowOpacity")
        self.opacity_animation.setDuration(300)
        self.opacity_animation.setEasingCurve(QEasingCurve.OutQuad)

        self.size_animation = QPropertyAnimation(self, b"size")
        self.size_animation.setDuration(300)
        self.size_animation.setEasingCurve(QEasingCurve.OutQuad)


    def showEvent(self, event):
        """Called when the dialog is shown. Starts fade-in and scale-in animations."""
        # Store original size and position to animate from/to
        self._original_size = self.size()
        self._original_pos = self.pos()

        # Start smaller and transparent for scale-in effect
        self.resize(self._original_size * 0.8)
        # Fix: Convert QSize to QPoint for addition
        offset_x = (self._original_size.width() - self.size().width()) / 2
        offset_y = (self._original_size.height() - self.size().height()) / 2
        self.move(self._original_pos + QPoint(int(offset_x), int(offset_y))) # Center it as it scales
        self.setWindowOpacity(0.0)

        self.opacity_animation.setStartValue(0.0)
        self.opacity_animation.setEndValue(1.0)
        self.opacity_animation.start()

        self.size_animation.setStartValue(self.size())
        self.size_animation.setEndValue(self._original_size)
        self.size_animation.start()

        super().showEvent(event)

    def close_dialog(self):
        """Starts fade-out and scale-out animations and then closes the dialog."""
        self.opacity_animation.setStartValue(1.0)
        self.opacity_animation.setEndValue(0.0)
        self.opacity_animation.start()

        self.size_animation.setStartValue(self.size())
        self.size_animation.setEndValue(self._original_size * 0.8) # Scale down
        self.size_animation.start()

        # Connect the close to the end of the opacity animation
        self.opacity_animation.finished.connect(self.accept)

    def mousePressEvent(self, event):
        """Allows dragging the dialog."""
        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPos()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """Moves the dialog based on mouse movement."""
        if self.old_pos:
            delta = event.globalPos() - self.old_pos
            self.move(self.pos() + delta)
            self.old_pos = event.globalPos()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """Resets the mouse position on release."""
        self.old_pos = None
        super().mouseReleaseEvent(event)


# --- SettingsDialog Class ---
class SettingsDialog(QDialog):
    """
    A dialog for launcher settings, including clearing recently played games.
    """
    def __init__(self, cp_games_instance, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint) # No title bar
        self.setModal(True)
        self.cp_games = cp_games_instance # Reference to the CPGames instance

        self.setWindowTitle("Settings")
        self.setGeometry(300, 300, 400, 250) # Fixed size for settings dialog

        self.setup_ui()
        self.apply_style()
        self.setup_animation()

    def setup_ui(self):
        """Sets up the layout and widgets for the settings dialog."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        main_layout.setAlignment(Qt.AlignCenter)

        title_label = QLabel("Launcher Settings")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setObjectName("settingsTitle") # Object name for specific styling
        main_layout.addWidget(title_label)

        # Clear Recently Played Button
        self.clear_recent_button = QPushButton("Clear Recently Played")
        self.clear_recent_button.clicked.connect(self._confirm_clear_recently_played)
        main_layout.addWidget(self.clear_recent_button, alignment=Qt.AlignCenter)

        # Close Button
        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.close_dialog)
        main_layout.addWidget(self.close_button, alignment=Qt.AlignCenter)

    def apply_style(self):
        """Applies custom styles to the settings dialog."""
        self.setStyleSheet("""
            SettingsDialog {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1,
                            stop:0 #2C3E50, stop:1 #34495E); /* Darker, professional gradient */
                border: 3px solid #00BFFF; /* Deep sky blue border */
                border-radius: 15px;
            }
            QLabel#settingsTitle {
                color: #FFFFFF;
                font-size: 20pt;
                font-weight: bold;
            }
            QPushButton {
                background-color: #007ACC; /* Blue for action buttons */
                border: none;
                border-radius: 10px;
                padding: 10px 20px;
                font-size: 14pt;
                font-weight: bold;
                color: white;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #005F99;
            }
            QPushButton:pressed {
                background-color: #004A77;
            }
            QPushButton#close_button {
                background-color: #CC3333; /* Red for close/destructive action */
            }
            QPushButton#close_button:hover {
                background-color: #A32A2A;
            }
        """)
        # Apply QGraphicsDropShadowEffect here for the dialog itself
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(25)
        shadow.setXOffset(0)
        shadow.setYOffset(10)
        shadow.setColor(QColor(0, 0, 0, 180))
        self.setGraphicsEffect(shadow)

    def setup_animation(self):
        """Sets up fade-in/out animations for the settings dialog."""
        self.opacity_animation = QPropertyAnimation(self, b"windowOpacity")
        self.opacity_animation.setDuration(200)
        self.opacity_animation.setEasingCurve(QEasingCurve.OutQuad)

    def showEvent(self, event):
        self.setWindowOpacity(0.0)
        self.opacity_animation.setStartValue(0.0)
        self.opacity_animation.setEndValue(1.0)
        self.opacity_animation.start()
        super().showEvent(event)

    def close_dialog(self):
        self.opacity_animation.setStartValue(1.0)
        self.opacity_animation.setEndValue(0.0)
        self.opacity_animation.finished.connect(self.accept)
        self.opacity_animation.start()

    def _confirm_clear_recently_played(self):
        """Shows a confirmation dialog before clearing recently played data."""
        # Use a custom confirmation dialog for consistent styling
        confirm_dialog = CustomMessageBox(
            "Confirm Clear",
            "Are you sure you want to clear all recently played games?",
            self
        )
        if confirm_dialog.exec_() == QMessageBox.Yes:
            self.cp_games.clear_recently_played_data()
            # Signal to the main window to refresh recently played *before* showing the info box
            if isinstance(self.parent(), GameLauncherWindow):
                # Reload config from disk before repopulating UI
                self.parent().cp_games.reload_games_config() 
                self.parent().populate_recently_played()
                self.parent().populate_favorite_games() # Also refresh favorites
                self.parent().populate_game_grid() # Refresh main grid too
                QApplication.processEvents() # Force UI refresh immediately
            QMessageBox.information(self, "Cleared", "Recently played games have been cleared.")


# --- Custom Confirmation Dialog (Replaces QMessageBox for consistency) ---
class CustomMessageBox(QDialog):
    def __init__(self, title, message, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setModal(True)
        self.setWindowTitle(title)

        self.result = QMessageBox.No # Default result

        self.setup_ui(message)
        self.apply_style()

    def setup_ui(self, message):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignCenter)

        msg_label = QLabel(message)
        msg_label.setAlignment(Qt.AlignCenter)
        msg_label.setWordWrap(True)
        msg_label.setObjectName("messageLabel")
        layout.addWidget(msg_label)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        button_layout.setAlignment(Qt.AlignCenter)

        yes_button = QPushButton("Yes")
        yes_button.clicked.connect(self._on_yes)
        button_layout.addWidget(yes_button)

        no_button = QPushButton("No")
        no_button.clicked.connect(self._on_no)
        button_layout.addWidget(no_button)

    def apply_style(self):
        self.setStyleSheet("""
            CustomMessageBox {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1,
                            stop:0 #2C3E50, stop:1 #34495E);
                border: 3px solid #FFD700; /* Gold border for warnings/confirmations */
                border-radius: 15px;
            }
            QLabel#messageLabel {
                color: #FFFFFF;
                font-size: 14pt;
                font-weight: bold;
            }
            QPushButton {
                background-color: #007ACC;
                border: none;
                border-radius: 10px;
                padding: 10px 20px;
                font-size: 12pt;
                font-weight: bold;
                color: white;
            }
            QPushButton:hover {
                background-color: #005F99;
            }
            QPushButton:pressed {
                background-color: #004A77;
            }
        """)
        # Apply QGraphicsDropShadowEffect here for the dialog itself
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(8)
        shadow.setColor(QColor(0, 0, 0, 180))
        self.setGraphicsEffect(shadow)

    def _on_yes(self):
        self.result = QMessageBox.Yes
        self.accept()

    def _on_no(self):
        self.result = QMessageBox.No
        self.reject()

    def exec_(self):
        # Center the dialog relative to its parent or screen
        if self.parent():
            parent_rect = self.parent().geometry()
            self.move(parent_rect.x() + (parent_rect.width() - self.width()) // 2,
                      parent_rect.y() + (parent_rect.height() - self.height()) // 2)
        else:
            screen_rect = QApplication.desktop().screenGeometry()
            self.move((screen_rect.width() - self.width()) // 2,
                      (screen_rect.height() - self.height()) // 2)
        return super().exec_()


# --- Main GameLauncherWindow updated ---
class GameLauncherWindow(QMainWindow):
    """
    The main window for the game launcher, featuring a grid-based selection
    of game cards instead of a dropdown.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Game Launcher")
        # Set the window icon using 'game.ico'
        if os.path.exists("game.ico"):
            self.setWindowIcon(QIcon("game.ico"))
        else:
            # Fallback for demonstration if icon is not present
            print("Warning: 'game.ico' not found. Using a default blank icon.")
            self.setWindowIcon(QIcon(QPixmap(QImage(64, 64, QImage.Format_ARGB32)).scaled(64, 64))) # Blank icon

        self.setGeometry(100, 100, 950, 700) # Increased window size for 5x6 layout
        self.selected_game_card = None # To keep track of the currently selected GameCard widget
        
        # Initialize CPGames and handle potential errors during config loading
        try:
            self.cp_games = CPGames()
        except (FileNotFoundError, ValueError, Exception) as e:
            QMessageBox.critical(self, "Configuration Error", str(e))
            self.cp_games = CPGames() # Initialize with empty data if error occurs
            self.cp_games.games_data = [] # Ensure games_data is empty
            self.cp_games.games_by_name = {} # Ensure games_by_name is empty

        self.game_info_dialog_instance = None # Keep track of the active dialog instance
        self.setup_ui()
        self.populate_game_grid() # Populate the grid with game cards
        self.populate_recently_played() # Initial populate for recently played
        self.populate_favorite_games() # Initial populate for favorites

        # Overall window style with a sophisticated gradient background.
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1,
                            stop:0 #0D1B2A, stop:0.5 #1B263B, stop:1 #2C3E50); /* Darker, more subtle, modern gradient */
            }
            QScrollArea {
                background: transparent;
                border: none;
            }
            QScrollBar:vertical {
                border: none;
                background: #1A2930; /* Darker scrollbar track */
                width: 12px; /* Slightly wider */
                margin: 0px 0px 0px 0px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: #007ACC; /* Vibrant blue handle */
                min-height: 30px; /* Taller handle */
                border-radius: 6px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: none;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
            QLineEdit {
                background-color: #1A2930;
                border: 2px solid #004D99;
                border-radius: 10px;
                padding: 8px 15px;
                color: #F0F0F0;
                font-size: 12pt;
                font-family: 'Segoe UI', sans-serif;
                selection-background-color: #007ACC;
            }
            QLineEdit:focus {
                border: 2px solid #0099FF;
            }
        """)

    def setup_ui(self):
        """
        Sets up the main UI components, including the title, game grid, search bar, and launch button.
        """
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setAlignment(Qt.AlignCenter) # Center content

        # Header Layout (Title + Settings Button)
        header_layout = QHBoxLayout()
        header_layout.addStretch(1) # Push title to center
        
        self.title_label = QLabel("Welcome to the Game Hub!")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("""
            font-family: 'Montserrat', 'Segoe UI', sans-serif; /* Modern, clean font */
            font-size: 36pt; /* Even larger title */
            font-weight: bold;
            color: #F0F0F0; /* Brighter white */
            margin-bottom: 30px; /* More space */
        """)
        # Apply QGraphicsDropShadowEffect for the title label
        title_shadow = QGraphicsDropShadowEffect(self.title_label)
        title_shadow.setBlurRadius(8)
        title_shadow.setXOffset(3)
        title_shadow.setYOffset(3)
        title_shadow.setColor(QColor(0, 0, 0, 180))
        self.title_label.setGraphicsEffect(title_shadow)

        header_layout.addWidget(self.title_label)
        header_layout.addStretch(1) # Push title to center

        self.settings_button = QPushButton("⚙️") # Gear icon for settings
        self.settings_button.setFixedSize(40, 40)
        self.settings_button.setFont(QFont("Segoe UI Emoji", 16))
        self.settings_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 77, 153, 0.7); /* Darker blue, semi-transparent */
                border: 2px solid #00BFFF; /* Bright border */
                border-radius: 20px; /* Fully rounded */
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(0, 100, 200, 0.8);
                border: 2px solid #00FFFF;
            }
            QPushButton:pressed {
                background-color: rgba(0, 50, 100, 0.9);
            }
        """)
        self.settings_button.clicked.connect(self.show_settings_dialog)
        header_layout.addWidget(self.settings_button, alignment=Qt.AlignTop | Qt.AlignRight)
        
        main_layout.addLayout(header_layout)
        main_layout.addSpacing(30)


        # Search Bar
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search for games...")
        self.search_input.textChanged.connect(self.filter_game_cards)
        main_layout.addWidget(self.search_input, alignment=Qt.AlignCenter)
        main_layout.addSpacing(20) # Space below search bar

        # Favorites Section
        self.favorites_label = QLabel("My Favorites:")
        self.favorites_label.setStyleSheet("""
            color: #F0F0F0;
            font-size: 16pt;
            font-weight: bold;
            margin-left: 10px;
            margin-bottom: 10px;
        """)
        main_layout.addWidget(self.favorites_label)

        self.favorites_layout = QHBoxLayout()
        self.favorites_layout.setAlignment(Qt.AlignLeft)
        main_layout.addLayout(self.favorites_layout)
        main_layout.addSpacing(30)

        # Recently Played Section
        self.recently_played_label = QLabel("Recently Played:")
        self.recently_played_label.setStyleSheet("""
            color: #F0F0F0;
            font-size: 16pt;
            font-weight: bold;
            margin-left: 10px;
            margin-bottom: 10px;
        """)
        main_layout.addWidget(self.recently_played_label)

        self.recently_played_layout = QHBoxLayout()
        self.recently_played_layout.setAlignment(Qt.AlignLeft)
        # Placeholder for recently played cards (will be populated dynamically)
        main_layout.addLayout(self.recently_played_layout)
        main_layout.addSpacing(30) # Space below recently played

        # Scrollable area for all game cards
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff) # No horizontal scroll
        self.scroll_area_content = QWidget()
        self.game_grid_layout = QGridLayout(self.scroll_area_content)
        self.game_grid_layout.setAlignment(Qt.AlignHCenter | Qt.AlignTop) # Center items horizontally, align to top
        self.game_grid_layout.setSpacing(25) # More spacing between cards
        self.scroll_area.setWidget(self.scroll_area_content)
        main_layout.addWidget(self.scroll_area)

        # Launch button.
        self.launch_button = QPushButton("Launch Game")
        self.launch_button.setStyleSheet("""
            QPushButton {
                background-color: #00A3CC; /* A cyan-blue */
                border: none;
                border-radius: 15px; /* Even more rounded */
                padding: 18px 35px; /* Even larger padding */
                font-size: 20pt; /* Larger font */
                font-weight: bold;
                color: white;
                margin-top: 40px; /* More space above button */
            }
            QPushButton:hover {
                background-color: #007ACC; /* Darker blue on hover */
            }
            QPushButton:pressed {
                background-color: #005A90; /* Even darker blue on press */
            }
            QPushButton:disabled {
                background-color: #3C4B56; /* Desaturated for disabled state */
                color: #A0A0A0;
            }
        """)
        # Apply QGraphicsDropShadowEffect for the launch button
        launch_button_shadow = QGraphicsDropShadowEffect(self.launch_button)
        launch_button_shadow.setBlurRadius(20)
        launch_button_shadow.setXOffset(0)
        launch_button_shadow.setYOffset(10)
        launch_button_shadow.setColor(QColor(0, 0, 0, 120))
        self.launch_button.setGraphicsEffect(launch_button_shadow)

        self.launch_button.clicked.connect(self.launch_game)
        self.launch_button.setEnabled(False) # Initially disabled until a game is selected
        main_layout.addWidget(self.launch_button, alignment=Qt.AlignCenter) # Center the button

    def _clear_layout(self, layout):
        """Helper function to clear all widgets from a layout."""
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                    widget.deleteLater()
                else:
                    layout_to_clear = item.layout()
                    if layout_to_clear is not None:
                        self._clear_layout(layout_to_clear)
                    else: # It's a spacer item
                        layout.removeItem(item)

    def populate_game_grid(self):
        """
        Populates the QGridLayout with GameCard widgets for all available games.
        """
        self._clear_layout(self.game_grid_layout) # Clear existing cards first

        game_data_list = self.cp_games.get_all_games()
        row = 0
        col = 0
        max_cols = 5 # Number of columns in the grid

        if not game_data_list:
            # Display a message if no games are loaded
            no_games_label = QLabel("No games found. Please check 'games_config.json'.")
            no_games_label.setAlignment(Qt.AlignCenter)
            no_games_label.setStyleSheet("color: #FF6347; font-size: 14pt; font-weight: bold;")
            self.game_grid_layout.addWidget(no_games_label, 0, 0, 1, max_cols, Qt.AlignCenter)
            return # Exit if no games to populate

        for game_data in game_data_list:
            card = GameCard(game_data)
            card.clicked.connect(self.on_game_card_clicked) # Connect card's click signal
            card.favorite_toggled.connect(self.on_game_favorite_toggled) # Connect favorite toggle signal
            self.game_grid_layout.addWidget(card, row, col)
            col += 1
            if col >= max_cols:
                col = 0
                row += 1

        # Adjust column stretch to center items if fewer than max_cols in the last row
        if col > 0:
            for i in range(col, max_cols):
                self.game_grid_layout.setColumnStretch(i, 1) # Stretch empty columns
        
    def populate_recently_played(self):
        """Populates the recently played section."""
        self._clear_layout(self.recently_played_layout) # Clear existing cards

        self.cp_games.reload_games_config() # Ensure latest data
        recently_played_games = self.cp_games.get_recently_played_games(count=3) # Show top 3

        if not recently_played_games:
            self.recently_played_label.setText("No games played recently.")
        else:
            self.recently_played_label.setText("Recently Played:")
            for game_data in recently_played_games:
                card = GameCard(game_data)
                card.setFixedSize(120, 120) # Smaller size for recently played
                # Ensure icon scales correctly for smaller card
                if card.icon_label.pixmap():
                    card.icon_label.setPixmap(card.icon_label.pixmap().scaled(72, 72, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                else: # Fallback for generic emoji
                    font = QFont()
                    font.setPointSize(30) # Smaller font for emoji
                    card.icon_label.setFont(font)
                card.name_label.setStyleSheet("color: #F0F0F0; font-size: 8pt;")
                card.clicked.connect(self.on_game_card_clicked)
                card.favorite_toggled.connect(self.on_game_favorite_toggled) # Connect favorite toggle signal
                self.recently_played_layout.addWidget(card)
            self.recently_played_layout.addStretch(1) # Push cards to the left

    def populate_favorite_games(self):
        """Populates the favorites section."""
        self._clear_layout(self.favorites_layout) # Clear existing cards

        self.cp_games.reload_games_config() # Ensure latest data
        favorite_games = self.cp_games.get_favorite_games()

        if not favorite_games:
            self.favorites_label.setText("No favorite games added yet.")
        else:
            self.favorites_label.setText("My Favorites:")
            # Sort favorites alphabetically for consistent display
            favorite_games.sort(key=lambda x: x['name'].lower()) 
            for game_data in favorite_games:
                card = GameCard(game_data)
                card.setFixedSize(120, 120) # Smaller size for favorites
                if card.icon_label.pixmap():
                    card.icon_label.setPixmap(card.icon_label.pixmap().scaled(72, 72, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                else:
                    font = QFont()
                    font.setPointSize(30)
                    card.icon_label.setFont(font)
                card.name_label.setStyleSheet("color: #F0F0F0; font-size: 8pt;")
                card.clicked.connect(self.on_game_card_clicked)
                card.favorite_toggled.connect(self.on_game_favorite_toggled)
                self.favorites_layout.addWidget(card)
            self.favorites_layout.addStretch(1) # Push cards to the left


    def filter_game_cards(self, text):
        """Filters game cards based on search input."""
        search_text = text.lower()
        for i in range(self.game_grid_layout.count()):
            item = self.game_grid_layout.itemAt(i)
            if item and item.widget():
                card_widget = item.widget()
                if isinstance(card_widget, GameCard):
                    game_name = card_widget.game_name.lower()
                    game_description = card_widget.game_data.get('description', '').lower()
                    game_category = card_widget.game_data.get('category', '').lower()
                    if search_text in game_name or search_text in game_description or search_text in game_category:
                        card_widget.show()
                    else:
                        card_widget.hide()

    def on_game_card_clicked(self, game_name):
        """
        Handles the event when a GameCard is clicked.
        Updates the selection state and enables the launch button, and shows info dialog.
        """
        # Deselect the previously selected card, if any
        if self.selected_game_card:
            self.selected_game_card.set_selected(False)

        # Find the new selected card widget across all layouts
        found_card = None
        # Search main grid
        for i in range(self.game_grid_layout.count()):
            item = self.game_grid_layout.itemAt(i)
            if item and item.widget():
                card_widget = item.widget()
                if isinstance(card_widget, GameCard) and card_widget.game_name == game_name:
                    found_card = card_widget
                    break
        # Search recently played
        if not found_card:
            for i in range(self.recently_played_layout.count()):
                item = self.recently_played_layout.itemAt(i)
                if item and item.widget():
                    card_widget = item.widget()
                    if isinstance(card_widget, GameCard) and card_widget.game_name == game_name:
                        found_card = card_widget
                        break
        # Search favorites
        if not found_card:
            for i in range(self.favorites_layout.count()):
                item = self.favorites_layout.itemAt(i)
                if item and item.widget():
                    card_widget = item.widget()
                    if isinstance(card_widget, GameCard) and card_widget.game_name == game_name:
                        found_card = card_widget
                        break
        
        if found_card:
            self.selected_game_card = found_card
            self.selected_game_card.set_selected(True)
        else:
            print(f"Error: Clicked game card '{game_name}' not found in any layout.")
            self.launch_button.setEnabled(False)
            self.title_label.setText("Welcome to the Game Hub!")
            return


        self.launch_button.setEnabled(True) # Enable launch button once a game is selected
        self.title_label.setText(f"Selected: {game_name.replace('_', ' ').title()} - Ready to Play!") # Update title to show selection

        # --- Game Info Dialog Logic ---
        # Close any existing dialog before opening a new one
        if self.game_info_dialog_instance and self.game_info_dialog_instance.isVisible():
            # Disconnect signals to prevent multiple connections
            try:
                self.game_info_dialog_instance.play_game_requested.disconnect()
                self.game_info_dialog_instance.favorite_toggled.disconnect()
                self.game_info_dialog_instance.opacity_animation.finished.disconnect()
            except TypeError:
                pass # Already disconnected or not connected
            self.game_info_dialog_instance.close() # Directly close the old dialog
            self.game_info_dialog_instance = None # Clear the reference

        game_data = self.cp_games.get_game_by_name(game_name)
        if game_data:
            self._show_new_info_dialog(game_data)
        else:
            QMessageBox.warning(self, "Game Info", "Game information not found.")

    def on_game_favorite_toggled(self, game_name):
        """Handles the favorite toggle signal from a GameCard or GameInfoDialog."""
        self.cp_games.toggle_game_favorite(game_name)
        # Reload all UI sections that display game cards to reflect the change
        self.cp_games.reload_games_config() # Ensure in-memory data is fresh
        self.populate_game_grid()
        self.populate_recently_played()
        self.populate_favorite_games()

        # If the info dialog is open for this game, update its favorite status
        if self.game_info_dialog_instance and self.game_info_dialog_instance.isVisible() and \
           self.game_info_dialog_instance.game_name == game_name:
            updated_game_data = self.cp_games.get_game_by_name(game_name)
            if updated_game_data:
                self.game_info_dialog_instance.update_favorite_status(updated_game_data.get('isFavorite', False))


    def _show_new_info_dialog(self, game_data):
        """Helper to create and show a new game info dialog."""
        self.game_info_dialog_instance = GameInfoDialog(game_data, self)
        
        # Connect signals from the dialog to methods in the main window
        self.game_info_dialog_instance.play_game_requested.connect(self.launch_game_from_dialog)
        self.game_info_dialog_instance.favorite_toggled.connect(self.on_game_favorite_toggled)

        # Center the dialog relative to the main window
        main_window_rect = self.geometry()
        dialog_width = 600
        dialog_height = 450 # Slightly taller for more info
        dialog_x = main_window_rect.x() + (main_window_rect.width() - dialog_width) // 2
        dialog_y = main_window_rect.y() + (main_window_rect.height() - dialog_height) // 2
        self.game_info_dialog_instance.setGeometry(dialog_x, dialog_y, dialog_width, dialog_height)

        self.game_info_dialog_instance.exec_() # Show as modal dialog

    def launch_game_from_dialog(self, game_name):
        """Launches a game when requested from the info dialog."""
        # Find the game card for the given name and simulate a click
        # This ensures the main launch logic (setting selected_game_card, etc.) is followed
        for i in range(self.game_grid_layout.count()):
            item = self.game_grid_layout.itemAt(i)
            if item and item.widget():
                card_widget = item.widget()
                if isinstance(card_widget, GameCard) and card_widget.game_name == game_name:
                    self.on_game_card_clicked(game_name) # Select the card
                    self.launch_game() # Then launch it
                    if self.game_info_dialog_instance:
                        self.game_info_dialog_instance.close_dialog() # Close dialog after launch
                    return
        QMessageBox.warning(self, "Launch Error", f"Could not find game '{game_name}' to launch.")


    def launch_game(self):
        """
        Launches the currently selected game.
        """
        if not self.selected_game_card:
            QMessageBox.warning(self, "No Selection", "Please select a game before launching.")
            return

        selected_game_name = self.selected_game_card.game_name
        game_data = self.cp_games.get_game_by_name(selected_game_name)

        if not game_data:
            QMessageBox.warning(self, "Launch Error", f"Game data for '{selected_game_name}' not found.")
            return

        # Update last played timestamp
        self.cp_games.update_game_last_played(selected_game_name)
        self.populate_recently_played() # Refresh recently played section
        # No need to populate_favorite_games here unless playing affects favorite status (which it doesn't)

        game_type = game_data.get('type', 'non_gui') # Default to non_gui if type is missing

        # Show "Launching..." state
        original_button_text = self.launch_button.text()
        self.launch_button.setText("Launching...")
        self.launch_button.setEnabled(False) # Disable button during launch

        # Simulate a small delay for the "Launching..." text to be visible
        QApplication.processEvents() # Process UI events to update button text immediately
        QTimer.singleShot(500, lambda: self._actual_launch_game(selected_game_name, game_type, original_button_text))

    def _actual_launch_game(self, selected_game_name, game_type, original_button_text):
        """Performs the actual game launch after a short delay."""
        if game_type == 'gui' and selected_game_name in GAME_CLASS_MAP and issubclass(GAME_CLASS_MAP[selected_game_name], QWidget):
            game_window = GAME_CLASS_MAP[selected_game_name]()
            game_window.setWindowTitle(f"{selected_game_name.replace('_', ' ').title()} - Game")
            game_window.show()  # Display the game window.
            # Store a reference to the game window to prevent it from being garbage collected
            self.game_window_instance = game_window
        else:
            # For non-GUI games (like Pygame ones or console apps), use a thread to keep the launcher responsive.
            try:
                # Replace spaces with underscores or adjust as per your actual folder names
                game_folder = selected_game_name.replace(' ', '_')
                game_path = os.path.join(os.getcwd(), game_folder)
                main_py_path = os.path.join(game_path, "main.py")

                if not os.path.isdir(game_path):
                    QMessageBox.warning(self, "Game Not Found",
                                        f"Game folder '{game_folder}' not found. "
                                        "Please ensure game folders are in the same directory as the launcher.")
                    return
                if not os.path.exists(main_py_path):
                    QMessageBox.warning(self, "Game Not Found",
                                        f"'main.py' not found in '{game_folder}' folder. "
                                        "Please ensure each game folder contains a 'main.py' file.")
                    return

                def run_non_gui_game():
                    """Helper function to run the non-GUI game in a separate process."""
                    original_cwd = os.getcwd()
                    try:
                        os.chdir(game_path) # Change to game's directory
                        # Use subprocess.Popen without .wait() to keep the launcher responsive.
                        # The console window for the launched game might appear.
                        subprocess.Popen([sys.executable, "main.py"])
                        print(f"--- Launched {selected_game_name}. Check your console/new window for game output. ---")
                    except Exception as e:
                        print(f"Error launching non-GUI game '{selected_game_name}': {e}")
                    finally:
                        os.chdir(original_cwd) # Change back to launcher's directory

                threading.Thread(target=run_non_gui_game, daemon=True).start()
                QMessageBox.information(self, "Game Launched",
                                        f"{selected_game_name.replace('_', ' ').title()} is attempting to launch.")
            except Exception as e:
                QMessageBox.critical(self, "Launch Error", f"Could not launch non-GUI game '{selected_game_name}': {e}")
        
        # Reset button state after launch attempt
        self.launch_button.setText(original_button_text)
        self.launch_button.setEnabled(True) # Re-enable after launch attempt

    def show_settings_dialog(self):
        """Shows the settings dialog."""
        settings_dialog = SettingsDialog(self.cp_games, self)
        # Check if the dialog was accepted (closed via close_dialog or accept)
        if settings_dialog.exec_() == QDialog.Accepted:
            # Re-populate recently played games to ensure UI is up-to-date
            # This is a fallback in case direct refresh in settings dialog fails or is missed
            self.populate_recently_played()
            self.populate_favorite_games()
            self.populate_game_grid()


if __name__ == '__main__':
    # Hide the console window on Windows if running as a GUI application.
    if sys.platform.startswith("win"):
        try:
            import ctypes
            ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
        except Exception:
            pass

    app = QApplication(sys.argv)
    launcher = GameLauncherWindow()
    launcher.show()
    sys.exit(app.exec_())
