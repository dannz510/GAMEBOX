import os
import sys
import subprocess
import threading
import json
from datetime import datetime
import tempfile

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox,
    QGridLayout, QScrollArea, QGraphicsDropShadowEffect, QHBoxLayout, QDialog, QLineEdit,
    QSpacerItem, QSizePolicy, QProgressDialog
)
from PyQt5.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve, QSize, QRect, QPoint, QTimer, QThread
from PyQt5.QtGui import QIcon, QColor, QFont, QPixmap, QImage

# --- Placeholder Game Classes ---
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
}


# --- Game Launcher Worker QThread ---
class GameLauncherWorker(QThread):
    launch_started = pyqtSignal(str)
    launch_finished = pyqtSignal(str, bool)

    def __init__(self, game_name, game_type, game_instance=None):
        super().__init__()
        self.game_name = game_name
        self.game_type = game_type
        self.game_instance = game_instance

    def run(self):
        self.launch_started.emit(self.game_name)
        success = False
        try:
            if self.game_type == 'gui' and self.game_instance:
                self.game_instance.show()
                print(f"--- Launched {self.game_name} (GUI) ---")
                import time
                time.sleep(1) # Simulate a short delay for GUI game startup visual effect
                success = True
            elif self.game_type == 'non_gui' and self.game_instance:
                self.game_instance.run() # This will block the worker thread until the non-GUI game finishes.
                success = True
            elif self.game_type == 'executable':
                print(f"--- Launching external executable: {self.game_name} ---")
                # Add actual subprocess.Popen logic here for your executables if needed
                import time
                time.sleep(3) # Simulate external game execution time
                success = True
            else:
                print(f"Unknown game type or no instance for {self.game_name}")
                success = False

        except Exception as e:
            print(f"Error launching {self.game_name}: {e}")
            success = False
        finally:
            self.launch_finished.emit(self.game_name, success)


class CPGames:
    """Manages the collection of supported games, now loaded from JSON."""
    CONFIG_FILE = 'games_config.json'

    def __init__(self):
        self.full_config_path = os.path.abspath(self.CONFIG_FILE)
        print(f"CPGames initialized. Config file path: {self.full_config_path}")

        self.games_data = self.load_games_config()
        self.games_by_name = {game['name']: game for game in self.games_data}

    def load_games_config(self):
        """
        Loads game data from the JSON configuration file.
        Raises an exception if the file is not found or is invalid.
        Ensures 'isFavorite' and 'category' fields exist.
        """
        if not os.path.exists(self.CONFIG_FILE):
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
                {"name": "GhostBusters", "description": "Retro arcade ghost-hunting.", "type": "non_gui", "category": "Arcade", "last_played": None, "isFavorite": False},
                {"name": "Hangman", "description": "Word guessing game.", "type": "non_gui", "category": "Word Game", "last_played": None, "isFavorite": False},
                {"name": "Hex Dash", "description": "A hexagon-based avoidance game.", "type": "non_gui", "category": "Arcade", "last_played": None, "isFavorite": False},
                {"name": "HyperTile Dash", "description": "Fast-paced tile matching.", "type": "non_gui", "category": "Puzzle", "last_played": None, "isFavorite": False},
                {"name": "Jungle Dash", "description": "An endless runner in the jungle.", "type": "non_gui", "category": "Runner", "last_played": None, "isFavorite": False},
                {"name": "Level Designer", "description": "Design your own game levels.", "type": "non_gui", "category": "Tool", "last_played": None, "isFavorite": False},
                {"name": "Memory Puzzle", "description": "Match pairs of cards.", "type": "non_gui", "category": "Puzzle", "last_played": None, "isFavorite": False},
                {"name": "MineSweeper", "description": "Classic logic puzzle game.", "type": "non_gui", "category": "Puzzle", "last_played": None, "isFavorite": False},
                {"name": "Piano Tiles", "description": "Tap the black tiles to the rhythm.", "type": "non_gui", "category": "Music", "last_played": None, "isFavorite": False},
                {"name": "Picture Sliding Puzzle", "description": "Rearrange tiles to form a picture.", "type": "non_gui", "category": "Puzzle", "last_played": None, "isFavorite": False},
                {"name": "Pong", "description": "The original arcade tennis.", "type": "non_gui", "category": "Arcade", "last_played": None, "isFavorite": False},
                {"name": "Qircle Rush", "description": "Navigate a minimalist world.", "type": "non_gui", "category": "Arcade", "last_played": None, "isFavorite": False},
                {"name": "Rock Paper Scissor", "description": "The ultimate decision-making game.", "type": "non_gui", "category": "Casual", "last_played": None, "isFavorite": False},
                {"name": "Rotate Dash", "description": "Rotate the world to survive.", "type": "non_gui", "category": "Arcade", "last_played": None, "isFavorite": False},
                {"name": "Snake", "description": "Classic arcade snake game.", "type": "non_gui", "category": "Arcade", "last_played": None, "isFavorite": False},
                {"name": "SpriteSheet Cutter", "description": "A tool for game developers.", "type": "non_gui", "category": "Tool", "last_played": None, "isFavorite": False},
                {"name": "Tetris", "description": "The classic falling block puzzle.", "type": "non_gui", "category": "Puzzle", "last_played": None, "isFavorite": False},
                {"name": "Tic Tac Toe", "description": "Simple and fun strategy game.", "type": "non_gui", "category": "Board Game", "last_played": None, "isFavorite": False}
            ]
            try:
                with open(self.CONFIG_FILE, 'w', encoding='utf-8') as f:
                    json.dump(default_games_data, f, indent=4)
                print(f"Default '{self.CONFIG_FILE}' created successfully.")
                return default_games_data
            except Exception as e:
                QMessageBox.critical(None, "Error Creating Config", f"Could not create default config file: {e}")
                return []

        try:
            with open(self.CONFIG_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Ensure all games have 'isFavorite' and 'category' fields
                for game in data:
                    game.setdefault('isFavorite', False)
                    game.setdefault('category', 'Uncategorized')
                    game.setdefault('last_played', None) # Ensure this field exists for sorting
                return data
        except FileNotFoundError:
            QMessageBox.critical(None, "Configuration Error", f"Config file not found: {self.CONFIG_FILE}")
            return []
        except json.JSONDecodeError as e:
            QMessageBox.critical(None, "Configuration Error", f"Invalid JSON in config file: {e}")
            return []
        except Exception as e:
            QMessageBox.critical(None, "Configuration Error", f"An unexpected error occurred while loading config: {e}")
            return []

    def save_games_config(self):
        """Saves current game data to the JSON configuration file."""
        try:
            with open(self.CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.games_data, f, indent=4)
            print(f"Config file '{self.CONFIG_FILE}' saved successfully.")
        except Exception as e:
            QMessageBox.critical(None, "Error Saving Config", f"Could not save config file: {e}")

    def get_all_games(self):
        """Returns a list of all games."""
        return self.games_data

    def get_game_by_name(self, name):
        """Returns game data for a given name."""
        return self.games_by_name.get(name)

    def update_game_last_played(self, game_name):
        """Updates the last_played timestamp for a game."""
        game = self.get_game_by_name(game_name)
        if game:
            game['last_played'] = datetime.now().isoformat()
            self.save_games_config()
            print(f"Updated last played for {game_name}")

    def toggle_favorite(self, game_name):
        """Toggles the favorite status of a game."""
        game = self.get_game_by_name(game_name)
        if game:
            game['isFavorite'] = not game['isFavorite']
            self.save_games_config()
            print(f"Toggled favorite for {game_name}. New status: {game['isFavorite']}")
            return game['isFavorite']
        return False


class GameCard(QWidget):
    """A clickable card widget to display game information."""
    game_selected = pyqtSignal(str)

    def __init__(self, game_data, parent=None):
        super().__init__(parent)
        self.game_data = game_data
        self.game_name = game_data['name']
        self.setFixedSize(200, 250) # Fixed size for consistency
        self.apply_style()
        self.setup_ui()
        self.setCursor(Qt.PointingHandCursor) # Indicate clickable

    def apply_style(self):
        self.setStyleSheet(f"""
            GameCard {{
                background-color: #2b2b2b; /* Dark background */
                border: 2px solid #555555; /* Subtle border */
                border-radius: 15px; /* Rounded corners */
                padding: 10px;
                box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.5); /* Soft shadow */
            }}
            GameCard:hover {{
                border: 2px solid #00A3CC; /* Highlight on hover */
            }}
            QLabel {{
                color: #e0e0e0; /* Light text color */
                font-family: 'Segoe UI', sans-serif;
            }}
            QLabel#game_title {{
                font-size: 14pt;
                font-weight: bold;
                text-align: center;
                margin-bottom: 5px;
            }}
            QLabel#game_category {{
                font-size: 10pt;
                color: #aaaaaa;
                text-align: center;
                margin-top: 5px;
            }}
            QPushButton#favorite_button {{
                background-color: transparent;
                border: none;
                padding: 0px;
            }}
            QPushButton#favorite_button:hover {{
                background-color: rgba(255, 255, 255, 0.1);
                border-radius: 5px;
            }}
        """)
        # Add shadow effect
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 150))
        shadow.setOffset(4, 4)
        self.setGraphicsEffect(shadow)

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)

        # Placeholder for game image (could load dynamically)
        self.image_label = QLabel(self)
        # Using a simple icon as a placeholder
        icon_path = os.path.join(os.path.dirname(__file__), "icons", "game_icon.png")
        if os.path.exists(icon_path):
            pixmap = QPixmap(icon_path).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.image_label.setPixmap(pixmap)
        else:
            self.image_label.setText("No Image")
            self.image_label.setAlignment(Qt.AlignCenter)
            self.image_label.setStyleSheet("color: #777; border: 1px dashed #777;")
        self.image_label.setFixedSize(100, 100)
        layout.addWidget(self.image_label, alignment=Qt.AlignCenter)

        self.title_label = QLabel(self.game_name, self)
        self.title_label.setObjectName("game_title")
        self.title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title_label)

        self.category_label = QLabel(self.game_data.get('category', 'N/A'), self)
        self.category_label.setObjectName("game_category")
        self.category_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.category_label)

        spacer = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(spacer)

        # Favorite button
        self.favorite_button = QPushButton(self)
        self.favorite_button.setObjectName("favorite_button")
        self.favorite_button.setFixedSize(28, 28) # Slightly smaller button
        self._update_favorite_icon() # Set initial icon based on favorite status
        self.favorite_button.clicked.connect(self._toggle_favorite)
        layout.addWidget(self.favorite_button, alignment=Qt.AlignRight | Qt.AlignBottom)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.game_selected.emit(self.game_name)
        super().mousePressEvent(event)

    def _toggle_favorite(self):
        """Toggles the favorite status via the CPGames manager and updates icon."""
        is_favorite = self.parent().parent().cp_games.toggle_favorite(self.game_name)
        self.game_data['isFavorite'] = is_favorite # Update local data
        self._update_favorite_icon() # Update button icon
        # Emit signal to notify parent launcher to refresh favorite list
        self.parent().parent().favorite_status_changed.emit()

    def _update_favorite_icon(self):
        """Updates the favorite button icon based on the game's favorite status."""
        star_icon_path = os.path.join(os.path.dirname(__file__), "icons",
                                      "star_filled.png" if self.game_data.get('isFavorite', False) else "star_empty.png")
        if os.path.exists(star_icon_path):
            self.favorite_button.setIcon(QIcon(star_icon_path))
            self.favorite_button.setIconSize(QSize(24, 24))
        else:
            self.favorite_button.setText("★" if self.game_data.get('isFavorite', False) else "☆") # Fallback to text
            self.favorite_button.setFont(QFont("Segoe UI Emoji", 16))


class GameInfoDialog(QDialog):
    """Dialog to display detailed game information and launch options."""
    game_launched = pyqtSignal(str) # Signal to indicate a game was launched
    favorite_toggled = pyqtSignal() # Signal to indicate favorite status changed

    def __init__(self, game_data, cp_games_instance, parent=None):
        super().__init__(parent)
        self.game_data = game_data
        self.cp_games = cp_games_instance
        self.setWindowTitle(game_data['name'])
        self.setFixedSize(600, 700) # Fixed size for the dialog
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground) # For custom border/shadow

        self.apply_style()
        self.setup_ui()

        # Add a shadow effect to the entire dialog
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 0, 0, 200))
        shadow.setOffset(0, 0)
        self.setGraphicsEffect(shadow)

    def apply_style(self):
        """Applies custom styles to the dialog and its widgets."""
        self.setStyleSheet("""
            GameInfoDialog {
                background: qline_gradient(spread:pad, x1:0, y1:0, x2:1, y2:1,
                            stop:0 #1A2A3A, stop:1 #2C3A4A); /* Solid, dark gradient background */
                border: 5px solid #00FFFF; /* Thicker, bright cyan border for frame effect */
                border-radius: 20px; /* Rounded corners */
                padding: 35px; /* Increased padding */
            }
            QLabel {
                color: #FFFFFF; /* Pure white text for maximum visibility */
                font-family: 'Segoe UI', sans-serif;
            }
            GameInfoDialog QLabel#title_label {
                font-size: 30pt; /* Even larger title */
                font-weight: bold;
                margin-bottom: 25px;
            }
            GameInfoDialog QLabel#description_label {
                font-size: 18pt; /* Even larger font size for description */
                line-height: 1.8; /* Increased line height for readability */
                padding: 20px; /* More padding for text */
            }
            QPushButton {
                background-color: #00A3CC;
                border: none;
                border-radius: 15px;
                padding: 18px 35px; /* Even larger button padding */
                font-size: 20pt; /* Larger font on button */
                font-weight: bold;
                color: white;
                margin-top: 30px;
            }
            QPushButton:hover {
                background-color: #007ACC;
            }
            QPushButton:pressed {
                background-color: #005A90;
            }
            QPushButton#favorite_button {
                background-color: #FFD700; /* Gold for favorite */
                color: #333333;
            }
            QPushButton#favorite_button:hover {
                background-color: #FFA500; /* Darker gold on hover */
            }
            QPushButton#favorite_button:pressed {
                background-color: #CC8400; /* Even darker gold */
            }
            QPushButton#close_button {
                background-color: #CC0000; /* Red for close */
            }
            QPushButton#close_button:hover {
                background-color: #990000;
            }
            QPushButton#close_button:pressed {
                background-color: #660000;
            }
        """)

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        # Title
        self.title_label = QLabel(self.game_data['name'])
        self.title_label.setObjectName("title_label")
        self.title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.title_label)

        # Game Description
        self.description_label = QLabel(self.game_data.get('description', 'No description available.'))
        self.description_label.setObjectName("description_label")
        self.description_label.setAlignment(Qt.AlignCenter)
        self.description_label.setWordWrap(True) # Ensure text wraps
        main_layout.addWidget(self.description_label)

        # Spacer to push buttons to the bottom
        main_layout.addStretch(1)

        # Buttons Layout
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(20)

        # Play Button
        self.play_button = QPushButton("Play Game")
        self.play_button.clicked.connect(self._launch_game_and_close)
        buttons_layout.addWidget(self.play_button)

        # Favorite Button
        self.favorite_button = QPushButton()
        self.favorite_button.setObjectName("favorite_button")
        self._update_favorite_button_style() # Set initial state
        self.favorite_button.clicked.connect(self._toggle_favorite_and_update_ui)
        buttons_layout.addWidget(self.favorite_button)

        # Close Button
        self.close_button = QPushButton("Close")
        self.close_button.setObjectName("close_button")
        self.close_button.clicked.connect(self.close_dialog)
        buttons_layout.addWidget(self.close_button)

        main_layout.addLayout(buttons_layout)

    def _launch_game_and_close(self):
        self.game_launched.emit(self.game_data['name']) # Emit signal to main window to launch
        self.accept() # Close the dialog

    def _toggle_favorite_and_update_ui(self):
        """Toggles favorite status and updates button style."""
        is_favorite = self.cp_games.toggle_favorite(self.game_data['name'])
        self.game_data['isFavorite'] = is_favorite # Update local data
        self._update_favorite_button_style()
        self.favorite_toggled.emit() # Notify parent to refresh lists

    def _update_favorite_button_style(self):
        """Updates the favorite button's text and style based on favorite status."""
        if self.game_data.get('isFavorite', False):
            self.favorite_button.setText("Remove Favorite")
            self.favorite_button.setStyleSheet("""
                QPushButton#favorite_button {
                    background-color: #FFD700; /* Gold */
                    color: #333333;
                    border: none;
                    border-radius: 15px;
                    padding: 18px 35px;
                    font-size: 20pt;
                    font-weight: bold;
                }
                QPushButton#favorite_button:hover {
                    background-color: #FFA500;
                }
                QPushButton#favorite_button:pressed {
                    background-color: #CC8400;
                }
            """)
        else:
            self.favorite_button.setText("Add to Favorites")
            self.favorite_button.setStyleSheet("""
                QPushButton#favorite_button {
                    background-color: #00A3CC; /* Original blue */
                    color: white;
                    border: none;
                    border-radius: 15px;
                    padding: 18px 35px;
                    font-size: 20pt;
                    font-weight: bold;
                }
                QPushButton#favorite_button:hover {
                    background-color: #007ACC;
                }
                QPushButton#favorite_button:pressed {
                    background-color: #005A90;
                }
            """)

    def close_dialog(self):
        self.reject() # Close the dialog with a reject status


class SettingsDialog(QDialog):
    """Dialog for application settings."""
    def __init__(self, cp_games_instance, parent=None):
        super().__init__(parent)
        self.cp_games = cp_games_instance
        self.setWindowTitle("Settings")
        self.setFixedSize(400, 300)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.apply_style()
        self.setup_ui()
        self.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=30, color=QColor(0, 0, 0, 200), offset=QPoint(0, 0)))

    def apply_style(self):
        self.setStyleSheet("""
            SettingsDialog {
                background: qline_gradient(spread:pad, x1:0, y1:0, x2:1, y2:1,
                            stop:0 #1A2A3A, stop:1 #2C3A4A);
                border: 5px solid #00FFFF;
                border-radius: 20px;
                padding: 20px;
            }
            QLabel {
                color: #FFFFFF;
                font-family: 'Segoe UI', sans-serif;
                font-size: 16pt;
                margin-bottom: 10px;
            }
            QPushButton {
                background-color: #CC0000; /* Red for destructive actions */
                border: none;
                border-radius: 10px;
                padding: 10px 20px;
                font-size: 14pt;
                font-weight: bold;
                color: white;
                margin-top: 20px;
            }
            QPushButton:hover {
                background-color: #990000;
            }
            QPushButton:pressed {
                background-color: #660000;
            }
            QPushButton#close_button {
                background-color: #00A3CC; /* Blue for general actions */
            }
            QPushButton#close_button:hover {
                background-color: #007ACC;
            }
        """)

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        title_label = QLabel("Settings")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # Clear Recently Played Button
        self.clear_recent_button = QPushButton("Clear Recently Played")
        self.clear_recent_button.clicked.connect(self._clear_recently_played)
        main_layout.addWidget(self.clear_recent_button)

        # Clear All Favorites Button (Optional, implement if needed)
        # self.clear_favorites_button = QPushButton("Clear All Favorites")
        # self.clear_favorites_button.clicked.connect(self._clear_all_favorites)
        # main_layout.addWidget(self.clear_favorites_button)

        main_layout.addStretch(1) # Pushes buttons to top

        # Close Button
        self.close_button = QPushButton("Close")
        self.close_button.setObjectName("close_button")
        self.close_button.clicked.connect(self.close_dialog)
        main_layout.addWidget(self.close_button)

    def _clear_recently_played(self):
        reply = QMessageBox.question(self, "Clear Recently Played",
                                     "Are you sure you want to clear the recently played list?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            for game in self.cp_games.games_data:
                game['last_played'] = None
            self.cp_games.save_games_config()
            QMessageBox.information(self, "Cleared", "Recently played list has been cleared.")
            self.parent().populate_recently_played() # Refresh the main window's list
            self.parent().populate_game_grid() # Refresh main grid
            self.accept() # Close dialog after action

    def close_dialog(self):
        self.accept() # Close the dialog


class ConfirmDialog(QDialog):
    """A custom confirmation dialog."""
    def __init__(self, message, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Confirm")
        self.setFixedSize(350, 150)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.apply_style()
        self.setup_ui(message)
        self.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=30, color=QColor(0, 0, 0, 200), offset=QPoint(0, 0)))

    def apply_style(self):
        self.setStyleSheet("""
            ConfirmDialog {
                background: qline_gradient(spread:pad, x1:0, y1:0, x2:1, y2:1,
                            stop:0 #1A2A3A, stop:1 #2C3A4A);
                border: 3px solid #00FFFF;
                border-radius: 15px;
                padding: 15px;
            }
            QLabel {
                color: #FFFFFF;
                font-family: 'Segoe UI', sans-serif;
                font-size: 14pt;
                text-align: center;
            }
            QPushButton {
                background-color: #00A3CC;
                border: none;
                border-radius: 8px;
                padding: 8px 15px;
                font-size: 12pt;
                font-weight: bold;
                color: white;
            }
            QPushButton:hover {
                background-color: #007ACC;
            }
            QPushButton:pressed {
                background-color: #005A90;
            }
            QPushButton#no_button {
                background-color: #CC0000;
            }
            QPushButton#no_button:hover {
                background-color: #990000;
            }
        """)

    def setup_ui(self, message):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)

        message_label = QLabel(message)
        message_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(message_label)

        button_layout = QHBoxLayout()
        button_layout.addStretch(1)

        self.yes_button = QPushButton("Yes")
        self.yes_button.clicked.connect(self.accept)
        button_layout.addWidget(self.yes_button)

        self.no_button = QPushButton("No")
        self.no_button.setObjectName("no_button")
        self.no_button.clicked.connect(self.reject)
        button_layout.addWidget(self.no_button)

        button_layout.addStretch(1)
        main_layout.addLayout(button_layout)


class GameLauncherWindow(QMainWindow):
    """Main window for the game launcher application."""
    favorite_status_changed = pyqtSignal() # Signal to refresh favorites

    def __init__(self):
        super().__init__()
        self.cp_games = CPGames()
        self.selected_game_name = None # To keep track of the currently selected game
        self.loading_message_box = None # To manage the non-blocking launch message

        self.setWindowTitle("CP Games Launcher")
        self.setGeometry(100, 100, 1200, 800)
        self.apply_style()
        self.setup_ui()

        # Connect the favorite_status_changed signal
        self.favorite_status_changed.connect(self.populate_favorite_games)

    def apply_style(self):
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #1a1a2e, stop:1 #16213e);
                font-family: 'Segoe UI', sans-serif;
            }
            QScrollArea {
                border: none;
            }
            QScrollBar:vertical {
                border: none;
                background: #334455;
                width: 10px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background: #00A3CC;
                border-radius: 5px;
                min-height: 20px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QLabel {
                color: #e0e0e0;
            }
            QLabel#section_title {
                font-size: 20pt;
                font-weight: bold;
                color: #00FFFF; /* Bright cyan for titles */
                margin-bottom: 15px;
            }
            QPushButton {
                background-color: #00A3CC;
                border: none;
                border-radius: 15px;
                padding: 10px 20px;
                font-size: 16pt;
                font-weight: bold;
                color: white;
            }
            QPushButton:hover {
                background-color: #007ACC;
            }
            QPushButton:pressed {
                background-color: #005A90;
            }
            QLineEdit {
                background-color: #334455;
                border: 1px solid #556677;
                border-radius: 10px;
                padding: 8px 15px;
                color: white;
                font-size: 14pt;
            }
            QLineEdit::placeholder {
                color: #aaaaaa;
            }
        """)

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # --- Left Panel: Game List ---
        left_panel = QVBoxLayout()
        left_panel.setSpacing(15)

        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Search games...")
        self.search_input.textChanged.connect(self.filter_games)
        left_panel.addWidget(self.search_input)

        # Game Grid (Scrollable)
        self.game_grid_widget = QWidget()
        self.game_grid_layout = QGridLayout(self.game_grid_widget)
        self.game_grid_layout.setHorizontalSpacing(15)
        self.game_grid_layout.setVerticalSpacing(15)
        self.game_grid_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        self.game_grid_scroll_area = QScrollArea()
        self.game_grid_scroll_area.setWidgetResizable(True)
        self.game_grid_scroll_area.setWidget(self.game_grid_widget)
        left_panel.addWidget(self.game_grid_scroll_area)

        main_layout.addLayout(left_panel, 2) # Takes 2/3 of space

        # --- Right Panel: Details and Categories ---
        right_panel = QVBoxLayout()
        right_panel.setSpacing(20)

        # Settings Button
        self.settings_button = QPushButton(self)
        self.settings_button.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "icons", "settings_icon.png")))
        self.settings_button.setIconSize(QSize(32, 32))
        self.settings_button.setFixedSize(40, 40)
        self.settings_button.setStyleSheet("""
            QPushButton {
                background-color: #334455;
                border-radius: 20px;
                padding: 0px;
            }
            QPushButton:hover {
                background-color: #556677;
            }
        """)
        self.settings_button.clicked.connect(self.show_settings_dialog)
        right_panel.addWidget(self.settings_button, alignment=Qt.AlignRight)

        # Game Details Section
        self.details_label = QLabel("Select a game to see details.", self)
        self.details_label.setObjectName("section_title")
        self.details_label.setAlignment(Qt.AlignCenter)
        right_panel.addWidget(self.details_label)

        # Recently Played Section
        recently_played_title = QLabel("Recently Played")
        recently_played_title.setObjectName("section_title")
        right_panel.addWidget(recently_played_title)

        self.recently_played_layout = QVBoxLayout()
        self.recently_played_layout.setContentsMargins(0, 0, 0, 0)
        self.recently_played_layout.setSpacing(5)
        right_panel.addLayout(self.recently_played_layout)

        # Favorite Games Section
        favorite_games_title = QLabel("Favorite Games")
        favorite_games_title.setObjectName("section_title")
        right_panel.addWidget(favorite_games_title)

        self.favorite_games_layout = QVBoxLayout()
        self.favorite_games_layout.setContentsMargins(0, 0, 0, 0)
        self.favorite_games_layout.setSpacing(5)
        right_panel.addLayout(self.favorite_games_layout)

        right_panel.addStretch(1) # Pushes content to top

        # Launch Button at the bottom right
        self.launch_button = QPushButton("Launch Game")
        self.launch_button.clicked.connect(self.launch_selected_game)
        self.launch_button.setEnabled(False) # Disabled until a game is selected
        right_panel.addWidget(self.launch_button, alignment=Qt.AlignCenter)

        main_layout.addLayout(right_panel, 1) # Takes 1/3 of space

        self.populate_game_grid()
        self.populate_recently_played()
        self.populate_favorite_games()

    def populate_game_grid(self, games_to_display=None):
        """Populates the main game grid with GameCard widgets."""
        # Clear existing cards
        while self.game_grid_layout.count():
            item = self.game_grid_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        if games_to_display is None:
            games_to_display = sorted(self.cp_games.get_all_games(), key=lambda g: g['name'].lower())

        row, col = 0, 0
        for game_data in games_to_display:
            card = GameCard(game_data)
            card.game_selected.connect(self.display_game_details)
            self.game_grid_layout.addWidget(card, row, col)
            col += 1
            if col >= 4: # 4 cards per row
                col = 0
                row += 1

    def filter_games(self, query):
        """Filters games displayed in the grid based on the search query."""
        all_games = self.cp_games.get_all_games()
        if not query:
            self.populate_game_grid(all_games)
            return

        filtered_games = [
            game for game in all_games
            if query.lower() in game['name'].lower() or
               query.lower() in game.get('category', '').lower() or
               query.lower() in game.get('description', '').lower()
        ]
        self.populate_game_grid(filtered_games)

    def display_game_details(self, game_name):
        """Displays detailed information about the selected game."""
        self.selected_game_name = game_name
        self.launch_button.setEnabled(True) # Enable launch button

        game_data = self.cp_games.get_game_by_name(game_name)
        if game_data:
            dialog = GameInfoDialog(game_data, self.cp_games, self)
            dialog.game_launched.connect(self.launch_selected_game) # Connect dialog's launch signal
            dialog.favorite_toggled.connect(self.favorite_status_changed.emit) # Connect to refresh favorites
            dialog.exec_() # Show dialog as modal

            # After dialog closes, update details if the last played time changed
            # (which happens on launch)
            if self.selected_game_name == game_name: # Ensure we're updating for the same game
                updated_game_data = self.cp_games.get_game_by_name(game_name)
                last_played_str = updated_game_data.get('last_played')
                if last_played_str:
                    last_played_dt = datetime.fromisoformat(last_played_str)
                    formatted_time = last_played_dt.strftime("%Y-%m-%d %H:%M:%S")
                    details_text = (f"<h2 style='color: #00FFFF;'>{game_data['name']}</h2>"
                                    f"<p><b>Category:</b> {game_data.get('category', 'N/A')}</p>"
                                    f"<p><b>Last Played:</b> {formatted_time}</p>"
                                    f"<p>{game_data.get('description', 'No description available.')}</p>")
                else:
                    details_text = (f"<h2 style='color: #00FFFF;'>{game_data['name']}</h2>"
                                    f"<p><b>Category:</b> {game_data.get('category', 'N/A')}</p>"
                                    f"<p><b>Last Played:</b> Never</p>"
                                    f"<p>{game_data.get('description', 'No description available.')}</p>")
            self.details_label.setText(details_text)
            self.details_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        else:
            self.details_label.setText(f"<h2>Game '{game_name}' not found.</h2>")
            self.details_label.setAlignment(Qt.AlignCenter)

    def populate_recently_played(self):
        """Populates the 'Recently Played' list."""
        while self.recently_played_layout.count():
            child = self.recently_played_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        recently_played_games = sorted(
            [g for g in self.cp_games.get_all_games() if g['last_played']],
            key=lambda g: datetime.fromisoformat(g['last_played']),
            reverse=True
        )[:5] # Get top 5 most recently played

        if not recently_played_games:
            no_games_label = QLabel("No games played recently.")
            no_games_label.setStyleSheet("color: #aaa;")
            self.recently_played_layout.addWidget(no_games_label)
            return

        for game in recently_played_games:
            game_label = QLabel(game['name'])
            game_label.setStyleSheet("color: #e0e0e0; font-size: 12pt; padding: 2px 0;")
            game_label.setCursor(Qt.PointingHandCursor)
            game_label.mousePressEvent = lambda event, name=game['name']: self.display_game_details(name)
            self.recently_played_layout.addWidget(game_label)

    def populate_favorite_games(self):
        """Populates the 'Favorite Games' list."""
        while self.favorite_games_layout.count():
            child = self.favorite_games_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        favorite_games = [g for g in self.cp_games.get_all_games() if g.get('isFavorite', False)]
        favorite_games.sort(key=lambda g: g['name'].lower()) # Sort alphabetically

        if not favorite_games:
            no_games_label = QLabel("No favorite games added yet.")
            no_games_label.setStyleSheet("color: #aaa;")
            self.favorite_games_layout.addWidget(no_games_label)
            return

        for game in favorite_games:
            game_label = QLabel(game['name'])
            game_label.setStyleSheet("color: #e0e0e0; font-size: 12pt; padding: 2px 0;")
            game_label.setCursor(Qt.PointingHandCursor)
            game_label.mousePressEvent = lambda event, name=game['name']: self.display_game_details(name)
            self.favorite_games_layout.addWidget(game_label)

    def get_game_instance(self, game_name):
        """
        Returns an instance of the game class based on its name.
        """
        game_class = GAME_CLASS_MAP.get(game_name)
        if game_class:
            return game_class(name=game_name)
        return None

    def launch_selected_game(self):
        """
        Initiates the game launch process using a QThread to keep the UI responsive.
        """
        if not self.selected_game_name:
            QMessageBox.warning(self, "No Game Selected", "Please select a game to launch.")
            return

        # Temporarily disable the launch button and change text to indicate loading
        self.original_button_text = self.launch_button.text()
        self.launch_button.setText("Launching...")
        self.launch_button.setEnabled(False)
        
        game_data = self.cp_games.get_game_by_name(self.selected_game_name)
        if not game_data:
            QMessageBox.critical(self, "Launch Error", f"Game data for '{self.selected_game_name}' not found.")
            self._game_launch_completed(self.selected_game_name, False) # Reset UI
            return

        game_type = game_data.get('type')
        game_instance = None
        if game_type in ['non_gui', 'gui']:
            game_instance = self.get_game_instance(self.selected_game_name)
            if not game_instance:
                QMessageBox.critical(self, "Launch Error", f"Could not create instance for '{self.selected_game_name}'.")
                self._game_launch_completed(self.selected_game_name, False) # Reset UI
                return

        # Create and start the worker thread
        self.game_launcher_worker = GameLauncherWorker(self.selected_game_name, game_type, game_instance)
        self.game_launcher_worker.launch_started.connect(self._show_launch_message)
        self.game_launcher_worker.launch_finished.connect(self._game_launch_completed)
        self.game_launcher_worker.start()

    def _show_launch_message(self, game_name):
        """
        Displays a non-blocking loading message box on the main thread.
        """
        if self.loading_message_box is None:
            self.loading_message_box = QMessageBox(self)
            self.loading_message_box.setWindowFlags(Qt.FramelessWindowHint) # Make it frameless
            self.loading_message_box.setModal(False) # Make it non-modal
            self.loading_message_box.setWindowTitle("Launching Game")
            self.loading_message_box.setText(f"Launching {game_name.replace('_', ' ').title()}...")
            self.loading_message_box.setStandardButtons(QMessageBox.NoButton) # No buttons
            self.loading_message_box.show()
            # Center the message box relative to the main window
            parent_rect = self.geometry()
            msg_box_size = self.loading_message_box.sizeHint()
            x = parent_rect.x() + (parent_rect.width() - msg_box_size.width()) / 2
            y = parent_rect.y() + (parent_rect.height() - msg_box_size.height()) / 2
            self.loading_message_box.move(int(x), int(y))

    def _game_launch_completed(self, game_name, success):
        """
        Slot connected to GameLauncherWorker.launch_finished signal.
        Resets UI and updates game status after launch attempt.
        """
        if self.loading_message_box:
            self.loading_message_box.hide()
            self.loading_message_box = None # Clear reference

        # Update last played if successful
        if success:
            self.cp_games.update_game_last_played(game_name)
            self.populate_recently_played() # Refresh recently played section
            self.populate_favorite_games() # Refresh favorites as last played affects order
            self.populate_game_grid() # Refresh main grid in case it's sorted by last played
            # Force update details for the launched game, so 'Last Played' shows updated time
            self.display_game_details(game_name)

        # Reset button state
        if hasattr(self, 'original_button_text'):
            self.launch_button.setText(self.original_button_text)
        else: # Fallback if original_button_text not set
            self.launch_button.setText("Launch Game")
        self.launch_button.setEnabled(True)

        if not success:
            QMessageBox.critical(self, "Launch Failed", f"Failed to launch {game_name.replace('_', ' ').title()}. Please check console for errors.")


    def show_settings_dialog(self):
        """Shows the settings dialog."""
        settings_dialog = SettingsDialog(self.cp_games, self)
        if settings_dialog.exec_() == QDialog.Accepted:
            self.populate_recently_played()
            self.populate_favorite_games()
            self.populate_game_grid()


if __name__ == '__main__':
    if sys.platform.startswith("win"):
        try:
            import ctypes
            ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
        except Exception:
            pass

    app = QApplication(sys.argv)
    # Load custom fonts
    # You might need to adjust paths if fonts are in a different location
    # QFontDatabase.addApplicationFont(":/fonts/seguisb.ttf") # Example for Segoe UI Semibold

    launcher = GameLauncherWindow()
    launcher.show()
    sys.exit(app.exec_())