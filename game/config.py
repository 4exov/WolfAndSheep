"""Game configuration settings"""

class GameConfig:
    """Game configuration class that centralizes all settings"""

    # Display settings
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    FPS = 60
    TITLE = "Wolf and Sheep Game"

    # Game settings
    DEFAULT_BOARD_SIZE = 8
    DEFAULT_PLAY_MODE = 'COMPUTER(Sheep) vs WOLF'
    DEFAULT_AI_LEVEL = 3

    def __init__(self):
        """Initialize with default settings"""
        # Display
        self.screen_width = self.SCREEN_WIDTH
        self.screen_height = self.SCREEN_HEIGHT
        self.fps = self.FPS
        self.title = self.TITLE

        # Game
        self.board_size = self.DEFAULT_BOARD_SIZE
        self.play_mode = self.DEFAULT_PLAY_MODE
        self.ai_level = self.DEFAULT_AI_LEVEL

        # Other config values can be added here

    def update(self, **kwargs):
        """Update configuration with provided values"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                print(f"Warning: Unknown configuration option '{key}'")
