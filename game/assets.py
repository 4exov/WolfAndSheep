"""Asset management system for the game"""

import pygame
import os
from foo import Foo

class AssetManager:
    """Handles loading and caching of game assets"""

    def __init__(self):
        """Initialize the asset manager"""
        # Image cache
        self.images = {}

        # Sound cache
        self.sounds = {}

        # Font cache
        self.fonts = {}

        # Flag to track if assets are loaded
        self.loaded = False

        # Preload essential assets
        self.preload_assets()

    def preload_assets(self):
        """Preload essential game assets"""
        if self.loaded:
            return

        print("Loading assets...")

        # Load menu assets
        self.load_image('menu_bg', Foo.MENU_BG)
        self.load_image('btn_menu', Foo.MENU_BTN)
        self.load_image('btn_reset', Foo.RESET_BTN)

        # Load figure assets
        for figure, path in Foo.IMAGES.items():
            self.load_image(f'figure_{figure}', path)

        # Load UI assets
        self.load_image('avatar_wolf', Foo.AVATAR_WOLF_IMG_URL)
        self.load_image('avatar_sheep', Foo.AVATAR_SHEEP_IMG_URL)
        self.load_image('victory_msg', Foo.VICTORY_MESSAGE)
        self.load_image('skip_turn', Foo.SKIP_TURN_BTN)
        self.load_image('computer_msg', Foo.COMPUTER_MSG)
        self.load_image('player_msg', Foo.PLAYER_MSG)
        self.load_image('set_wolf_msg', Foo.SET_WOLF_MSG)
        self.load_image('alphabet', Foo.ALPHABET_IMG)
        self.load_image('numbers', Foo.NUMBERS_IMG)

        self.loaded = True
        print("Assets loaded successfully!")

    def load_image(self, name, path):
        """Load an image and store it in the cache

        Args:
            name (str): Name/key for the image
            path (str): Path to the image file
        """
        try:
            self.images[name] = pygame.image.load(path)
            # Only print once for menu background
            if path == Foo.MENU_BG:
                print("Successfully loaded menu background")
        except Exception as e:
            print(f"Failed to load image {path}: {e}")
            # Create placeholder
            placeholder = pygame.Surface((64, 64))
            placeholder.fill((255, 0, 255))  # Magenta placeholder
            self.images[name] = placeholder

    def get_image(self, name):
        """Get an image from the cache

        Args:
            name (str): Name/key of the image

        Returns:
            pygame.Surface: The requested image
        """
        if name not in self.images:
            print(f"Warning: Image '{name}' not found in cache")
            # Return placeholder
            placeholder = pygame.Surface((64, 64))
            placeholder.fill((255, 0, 255))  # Magenta placeholder
            return placeholder

        return self.images[name]

    def get_figure_image(self, figure):
        """Get a figure image from the cache

        Args:
            figure (int): Figure type constant

        Returns:
            pygame.Surface: The requested figure image
        """
        return self.get_image(f'figure_{figure}')
