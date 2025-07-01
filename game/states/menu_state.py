"""Menu state for the game"""

import pygame
from game.states.base_state import BaseState
from foo import Foo

class MenuState(BaseState):
    """Menu state handling the main menu UI and interactions"""

    def __init__(self, engine):
        """Initialize the menu state

        Args:
            engine (GameEngine): Reference to the game engine
        """
        super().__init__(engine)

        # Menu options
        self.options = {
            'play_mode': Foo.MODE_PLAYER_WOLF_VS_COMPUTER,
            'board_size': Foo.SIZE_8,
            'ai_level': Foo.AI_3,
            'set_wolf_manually': Foo.SET_WOLF_MANUALLY_NO
        }

        # Button rectangles for click detection
        self.buttons = {
            'start_game': pygame.Rect(300, 400, 200, 50),
            'mode': pygame.Rect(300, 100, 200, 40),
            'board_size': pygame.Rect(300, 150, 200, 40),
            'ai_level': pygame.Rect(300, 200, 200, 40),
            'set_wolf': pygame.Rect(300, 250, 200, 40)
        }

    def enter(self):
        """Called when entering the menu state"""
        # Make sure assets are loaded
        self.engine.assets.preload_assets()

    def handle_event(self, event):
        """Handle menu events

        Args:
            event (pygame.event.Event): The event to handle
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Get mouse position
            pos = pygame.mouse.get_pos()

            # Check button clicks
            if self.buttons['start_game'].collidepoint(pos):
                # Start the game with current options
                self._start_game()
            elif self.buttons['mode'].collidepoint(pos):
                self._cycle_option('play_mode', Foo.PLAY_MODES)
            elif self.buttons['board_size'].collidepoint(pos):
                self._cycle_option('board_size', Foo.BOARD_SIZES)
            elif self.buttons['ai_level'].collidepoint(pos):
                self._cycle_option('ai_level', Foo.AI_LEVELS)
            elif self.buttons['set_wolf'].collidepoint(pos):
                self._cycle_option('set_wolf_manually', Foo.SET_WOLF_MANUALLY)

    def update(self):
        """Update menu state"""
        # Nothing to update in menu state
        pass

    def render(self, screen):
        """Render the menu

        Args:
            screen (pygame.Surface): The screen surface to render on
        """
        # Draw background
        menu_bg = self.engine.assets.get_image('menu_bg')
        screen.blit(menu_bg, (0, 0))

        # Draw title
        font = pygame.font.Font(None, 48)
        title = font.render("Wolf and Sheep Game", True, Foo.WHITE)
        screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 30))

        # Draw options
        font = pygame.font.Font(None, 32)

        # Play mode
        text = font.render(f"Play Mode: {self.options['play_mode']}", True, Foo.WHITE)
        screen.blit(text, (self.buttons['mode'].x, self.buttons['mode'].y))

        # Board size
        text = font.render(f"Board Size: {self.options['board_size']}x{self.options['board_size']}", True, Foo.WHITE)
        screen.blit(text, (self.buttons['board_size'].x, self.buttons['board_size'].y))

        # AI level
        text = font.render(f"AI Level: {self.options['ai_level']}", True, Foo.WHITE)
        screen.blit(text, (self.buttons['ai_level'].x, self.buttons['ai_level'].y))

        # Set wolf manually
        text = font.render(f"Set Wolf Manually: {self.options['set_wolf_manually']}", True, Foo.WHITE)
        screen.blit(text, (self.buttons['set_wolf'].x, self.buttons['set_wolf'].y))

        # Draw start button
        pygame.draw.rect(screen, Foo.COLOR_GOLD, self.buttons['start_game'])
        text = font.render("Start Game", True, Foo.BLACK)
        screen.blit(text, (self.buttons['start_game'].x + 50, self.buttons['start_game'].y + 15))

    def _cycle_option(self, option_name, options_dict):
        """Cycle through options for a menu item

        Args:
            option_name (str): Name of the option to cycle
            options_dict (dict): Dictionary of available options
        """
        current = self.options[option_name]
        options = list(options_dict.keys())

        # Find index of current option
        if current in options:
            idx = options.index(current)
            # Cycle to next option
            idx = (idx + 1) % len(options)
            self.options[option_name] = options[idx]
        else:
            # If current not found, set to first option
            self.options[option_name] = options[0]

    def _start_game(self):
        """Start the game with current options"""
        # Update game configuration
        self.engine.config.board_size = self.options['board_size']
        self.engine.config.play_mode = self.options['play_mode']
        self.engine.config.ai_level = self.options['ai_level']

        # Initialize gameplay state with current options
        gameplay_state = self.engine.states['gameplay']
        gameplay_state.initialize_game(
            board_size=self.options['board_size'],
            play_mode=self.options['play_mode'],
            ai_level=self.options['ai_level'],
            set_wolf_manually=self.options['set_wolf_manually']
        )

        # Change to gameplay state
        self.engine.change_state('gameplay')
