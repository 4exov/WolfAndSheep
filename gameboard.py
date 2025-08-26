import pygame
import pygame_menu

from foo import Foo


class Gameboard:
    init = False

    pg = None
    win = None
    menu = None
    opt = None


    # Images
    alphabet_img = None
    numbers_img = None
    ALPHABET_CELL_SIZE = 28


    # WINDOW
    win_caption = "Wolf VS Sheep"
    WIN_WIDTH = 1145
    WIN_HEIGHT = 810

    GAMEBOARD_SIZE = 720
    GAMEBOARD_ZERO_X = 45
    GAMEBOARD_ZERO_Y = 45
    GAMEBOARD_BORDER_SIZE = 3

    FIGURE_AVATAR_SIZE = 280
    FIGURE_AVATAR_BORDER_SIZE = 3

    WOLF_AVATAR_X = 810
    WOLF_AVATAR_Y = 485

    VICTORY_MESSAGE = 'Victory!'
    WOLF_VICTORY_MESSAGE_X = 811
    WOLF_VICTORY_MESSAGE_Y = 710
    SHEEP_VICTORY_MESSAGE_X = 811
    SHEEP_VICTORY_MESSAGE_Y = 273

    IMG_MESSAGE_WIDTH = 280
    IMG_MESSAGE_HEIGHT = 55

    BTN_RESET_X = 813
    BTN_RESET_Y = 372
    BTN_RESET_WIDTH = 138
    BTN_RESET_HEIGHT = 56

    BTN_MENU_X = 943
    BTN_MENU_Y = 372
    BTN_MENU_WIDTH = 138
    BTN_MENU_HEIGHT = 56

    def __init__(self, option):
        pygame.init()
        init = True
        self.pg = pygame
        self.opt = option

        self.win = self.pg.display.set_mode((self.WIN_WIDTH, self.WIN_HEIGHT))
        self.pg.display.set_caption(self.win_caption)
        self.win.fill(Foo.COLOR_BLACK_NERO)

        # Try to load images safely
        self.alphabet_img = self.safe_load_image(Foo.ALPHABET_IMG)
        self.numbers_img = self.safe_load_image(Foo.NUMBERS_IMG)
        self.update()

    def safe_load_image(self, path):
        """Safely load an image with fallback for missing DLL issues"""
        try:
            # Try to load with convert_alpha first
            return self.pg.image.load(path).convert_alpha()
        except Exception as e:
            try:
                # Try loading without convert_alpha
                return self.pg.image.load(path)
            except Exception as e2:
                print(f"Failed to load image {path}: {e2}")
                # Create a small surface as placeholder
                surf = self.pg.Surface((30, 30))
                surf.fill((200, 200, 200))
                return surf

    def timeout(self, time):
        self.pg.time.delay(time)

    def update(self):
        self.pg.display.update()

    def set_caption(self, caption):
        self.pg.display.set_caption(caption)

    def draw_board(self, options, cells, timeout):

        self.win.fill(Foo.COLOR_BLACK_NERO)
        play_mode = self.opt.mode

        self.set_caption('{0}   |  MODE: {1}'.format(self.win_caption, self.opt.mode))
        border_color = Foo.GRAY

        # Draw alphabet & Numbers of cells
        alph_start_x = self.GAMEBOARD_ZERO_X
        number_start_y = self.GAMEBOARD_SIZE - self.GAMEBOARD_ZERO_Y
        grid_x = 0
        for i in range(0, self.opt.board_size):
            try:
                self.win.blit( self.alphabet_img, (alph_start_x + self.opt.cell_size//3, self.GAMEBOARD_ZERO_Y // 4),
                               (grid_x, 0, self.ALPHABET_CELL_SIZE, self.ALPHABET_CELL_SIZE) )
                self.win.blit(self.alphabet_img, (alph_start_x + self.opt.cell_size // 3,
                                                  self.GAMEBOARD_SIZE + self.GAMEBOARD_ZERO_Y + self.GAMEBOARD_ZERO_Y // 4),
                              (grid_x, 0, self.ALPHABET_CELL_SIZE, self.ALPHABET_CELL_SIZE))
            except Exception as e:
                # Skip drawing alphabet if there's an error
                print(f"Skipping alphabet: {e}")

            self.win.blit(self.numbers_img, (self.GAMEBOARD_ZERO_X // 4, number_start_y + self.opt.cell_size // 4),
                          (grid_x, 0, self.ALPHABET_CELL_SIZE, self.ALPHABET_CELL_SIZE))

            # self.win.blit(self.numbers_img, ( self.GAMEBOARD_ZERO_X +  self.GAMEBOARD_SIZE,
            #                                   number_start_y + self.opt.cell_size // 4),
            #               (grid_x, 0, self.ALPHABET_CELL_SIZE, self.ALPHABET_CELL_SIZE))


            grid_x += self.ALPHABET_CELL_SIZE
            alph_start_x += self.opt.cell_size
            number_start_y -= self.opt.cell_size


        # Gameboard border
        border_x = Gameboard.GAMEBOARD_ZERO_X - Gameboard.GAMEBOARD_BORDER_SIZE
        border_y = Gameboard.GAMEBOARD_ZERO_Y - Gameboard.GAMEBOARD_BORDER_SIZE
        border_size = Gameboard.GAMEBOARD_SIZE + Gameboard.GAMEBOARD_BORDER_SIZE * 2
        self.pg.draw.rect(self.win, border_color,
                          (border_x, border_y, border_size, border_size),
                          Gameboard.GAMEBOARD_BORDER_SIZE)

        # Sheep border
        color = border_color if self.opt.whose_move != Foo.SHEEP else Foo.COLOR_GOLD
        sheep_x = Gameboard.GAMEBOARD_ZERO_X * 2 + Gameboard.GAMEBOARD_SIZE - Gameboard.FIGURE_AVATAR_BORDER_SIZE
        sheep_y = border_y
        avatar_border_size = Gameboard.FIGURE_AVATAR_SIZE + Gameboard.FIGURE_AVATAR_BORDER_SIZE * 2
        self.pg.draw.rect(self.win, color,
                          (sheep_x, sheep_y, avatar_border_size, avatar_border_size),
                          Gameboard.FIGURE_AVATAR_BORDER_SIZE)
        try:
            img = self.safe_load_image(Foo.AVATAR_SHEEP_IMG_URL)
            self.win.blit(img, self.pg.rect.Rect(sheep_x + Gameboard.FIGURE_AVATAR_BORDER_SIZE,
                                                 sheep_y + Gameboard.FIGURE_AVATAR_BORDER_SIZE,
                                                 self.FIGURE_AVATAR_SIZE,
                                                 self.FIGURE_AVATAR_SIZE))
        except Exception as e:
            # Draw a white sheep placeholder if image loading fails
            sheep_center_x = sheep_x + Gameboard.FIGURE_AVATAR_BORDER_SIZE + self.FIGURE_AVATAR_SIZE // 2
            sheep_center_y = sheep_y + Gameboard.FIGURE_AVATAR_BORDER_SIZE + self.FIGURE_AVATAR_SIZE // 2
            radius = self.FIGURE_AVATAR_SIZE // 3
            self.pg.draw.circle(self.win, (255, 255, 255), (sheep_center_x, sheep_center_y), radius)
            print(f"Using fallback sheep avatar: {e}")
        img_url = Foo.PLAYER_MSG if play_mode == Foo.MODE_PLAYER_VS_PLAYER or \
                                    play_mode == Foo.MODE_PLAYER_SHEEP_VS_AI \
            else Foo.COMPUTER_MSG
        try:
            img = self.safe_load_image(img_url)
            self.win.blit(img, self.pg.rect.Rect(sheep_x + Gameboard.FIGURE_AVATAR_BORDER_SIZE,
                                                 sheep_y + Gameboard.FIGURE_AVATAR_BORDER_SIZE,
                                                 self.IMG_MESSAGE_WIDTH,
                                                 self.IMG_MESSAGE_HEIGHT))
        except Exception as e:
            # Draw text as fallback
            text = "PLAYER" if img_url == Foo.PLAYER_MSG else "COMPUTER"
            font = self.pg.font.SysFont('Arial', 24) if hasattr(self.pg, 'font') and self.pg.font else None
            if font:
                text_surface = font.render(text, True, (255, 255, 255))
                self.win.blit(text_surface, (sheep_x + Gameboard.FIGURE_AVATAR_BORDER_SIZE + 10, 
                                            sheep_y + Gameboard.FIGURE_AVATAR_BORDER_SIZE + 10))
            print(f"Using fallback text: {e}")

        # Wolf border.
        color = border_color if self.opt.whose_move != Foo.WOLF else Foo.COLOR_GOLD
        wolf_x = sheep_x
        wolf_y = Gameboard.GAMEBOARD_ZERO_Y + Gameboard.GAMEBOARD_SIZE - \
                 Gameboard.FIGURE_AVATAR_SIZE - Gameboard.FIGURE_AVATAR_BORDER_SIZE
        self.pg.draw.rect(self.win, color,
                          (wolf_x, wolf_y, avatar_border_size, avatar_border_size),
                          Gameboard.FIGURE_AVATAR_BORDER_SIZE)
        try:
            img = self.safe_load_image(Foo.AVATAR_WOLF_IMG_URL)
            self.win.blit(img, self.pg.rect.Rect(wolf_x + Gameboard.FIGURE_AVATAR_BORDER_SIZE,
                                                 wolf_y + Gameboard.FIGURE_AVATAR_BORDER_SIZE,
                                                 self.FIGURE_AVATAR_SIZE,
                                                 self.FIGURE_AVATAR_SIZE))
        except Exception as e:
            # Draw a red wolf placeholder if image loading fails
            wolf_center_x = wolf_x + Gameboard.FIGURE_AVATAR_BORDER_SIZE + self.FIGURE_AVATAR_SIZE // 2
            wolf_center_y = wolf_y + Gameboard.FIGURE_AVATAR_BORDER_SIZE + self.FIGURE_AVATAR_SIZE // 2
            radius = self.FIGURE_AVATAR_SIZE // 3
            # Wolf is a red triangle
            points = [
                (wolf_center_x, wolf_center_y - radius),  # top
                (wolf_center_x - radius, wolf_center_y + radius),  # bottom left
                (wolf_center_x + radius, wolf_center_y + radius)   # bottom right
            ]
            self.pg.draw.polygon(self.win, (255, 0, 0), points)
            print(f"Using fallback wolf avatar: {e}")
        img_url = Foo.PLAYER_MSG if play_mode == Foo.MODE_PLAYER_VS_PLAYER or \
                                    play_mode == Foo.MODE_PLAYER_WOLF_VS_COMPUTER \
            else Foo.COMPUTER_MSG
        try:
            img = self.safe_load_image(img_url)
            self.win.blit(img, self.pg.rect.Rect(wolf_x + Gameboard.FIGURE_AVATAR_BORDER_SIZE,
                                                 wolf_y + Gameboard.FIGURE_AVATAR_BORDER_SIZE,
                                                 self.IMG_MESSAGE_WIDTH,
                                                 self.IMG_MESSAGE_HEIGHT))
        except Exception as e:
            # Draw text as fallback
            text = "PLAYER" if img_url == Foo.PLAYER_MSG else "COMPUTER"
            font = self.pg.font.SysFont('Arial', 24) if hasattr(self.pg, 'font') and self.pg.font else None
            if font:
                text_surface = font.render(text, True, (255, 255, 255))
                self.win.blit(text_surface, (wolf_x + Gameboard.FIGURE_AVATAR_BORDER_SIZE + 10, 
                                            wolf_y + Gameboard.FIGURE_AVATAR_BORDER_SIZE + 10))
            print(f"Using fallback text: {e}")

        # Buttons border.
        indent = (wolf_y - sheep_y - Gameboard.FIGURE_AVATAR_SIZE) // 10
        button_border_x = sheep_x
        button_border_y = sheep_y + Gameboard.FIGURE_AVATAR_SIZE + indent * 3
        self.pg.draw.rect(self.win, border_color,
                          (button_border_x, button_border_y, avatar_border_size, indent * 4),
                          Gameboard.FIGURE_AVATAR_BORDER_SIZE)

        # Show buttons: RESET and MENU.
        try:
            img = self.safe_load_image(Foo.RESET_BTN)
            self.win.blit(img, self.pg.rect.Rect(button_border_x + 4, button_border_y + 4,
                                                 self.BTN_RESET_WIDTH,
                                                 self.BTN_RESET_HEIGHT))
        except Exception as e:
            # Draw text as fallback
            self.pg.draw.rect(self.win, (100, 100, 100), 
                             (button_border_x + 4, button_border_y + 4, self.BTN_RESET_WIDTH, self.BTN_RESET_HEIGHT))
            font = self.pg.font.SysFont('Arial', 16) if hasattr(self.pg, 'font') and self.pg.font else None
            if font:
                text_surface = font.render("RESET", True, (255, 255, 255))
                self.win.blit(text_surface, (button_border_x + 20, button_border_y + 20))
            print(f"Using fallback reset button: {e}")

        try:
            img = self.safe_load_image(Foo.MENU_BTN)
            self.win.blit(img, self.pg.rect.Rect(button_border_x + 6 + self.BTN_RESET_WIDTH,
                                                 button_border_y + 4,
                                                 self.BTN_MENU_WIDTH,
                                                 self.BTN_MENU_HEIGHT))
        except Exception as e:
            # Draw text as fallback
            self.pg.draw.rect(self.win, (100, 100, 100), 
                             (button_border_x + 6 + self.BTN_RESET_WIDTH, button_border_y + 4, 
                              self.BTN_MENU_WIDTH, self.BTN_MENU_HEIGHT))
            font = self.pg.font.SysFont('Arial', 16) if hasattr(self.pg, 'font') and self.pg.font else None
            if font:
                text_surface = font.render("MENU", True, (255, 255, 255))
                self.win.blit(text_surface, (button_border_x + self.BTN_RESET_WIDTH + 20, button_border_y + 20))
            print(f"Using fallback menu button: {e}")

        # Show button: skip turn for wolf.
        if self.opt.won == Foo.NOT_INIT and \
                self.opt.whose_move == Foo.WOLF and self.opt.is_possible_skip_move_for_wolf and \
                ((self.opt.mode == Foo.MODE_PLAYER_VS_PLAYER) or (self.opt.mode == Foo.MODE_PLAYER_WOLF_VS_COMPUTER)) \
                and self.opt.is_wolf_position_init:
            try:
                img = self.safe_load_image(Foo.SKIP_TURN_BTN)
                self.win.blit(img, self.pg.rect.Rect(Gameboard.WOLF_VICTORY_MESSAGE_X, Gameboard.WOLF_VICTORY_MESSAGE_Y,
                                                     self.IMG_MESSAGE_WIDTH,
                                                     self.IMG_MESSAGE_HEIGHT))
            except Exception as e:
                # Draw text as fallback
                font = self.pg.font.SysFont('Arial', 16) if hasattr(self.pg, 'font') and self.pg.font else None
                if font:
                    text_surface = font.render("SKIP TURN", True, (255, 255, 255))
                    self.win.blit(text_surface, (Gameboard.WOLF_VICTORY_MESSAGE_X + 10, Gameboard.WOLF_VICTORY_MESSAGE_Y + 20))
                print(f"Using fallback skip turn message: {e}")
        elif not self.opt.is_wolf_position_init:
            try:
                img = self.safe_load_image(Foo.SET_WOLF_MSG)
                self.win.blit(img, self.pg.rect.Rect(Gameboard.WOLF_VICTORY_MESSAGE_X, Gameboard.WOLF_VICTORY_MESSAGE_Y,
                                                     self.IMG_MESSAGE_WIDTH,
                                                     self.IMG_MESSAGE_HEIGHT))
            except Exception as e:
                # Draw text as fallback
                font = self.pg.font.SysFont('Arial', 16) if hasattr(self.pg, 'font') and self.pg.font else None
                if font:
                    text_surface = font.render("SET WOLF POSITION", True, (255, 255, 255))
                    self.win.blit(text_surface, (Gameboard.WOLF_VICTORY_MESSAGE_X + 10, Gameboard.WOLF_VICTORY_MESSAGE_Y + 20))
                print(f"Using fallback set wolf message: {e}")


        for i in range(options.board_size):
            for j in range(options.board_size):
                self.draw_cell(cells[i][j])
        self.timeout(timeout)
        self.update()

    def draw_cell(self, cell):
        self.pg.draw.rect(self.win, cell.color, (cell.x, cell.y, cell.size, cell.size))

        if not (cell.is_empty()):
            # Draw a fallback colored shape first
            color = (255, 0, 0) if cell.figure == Foo.WOLF else (255, 255, 255)
            center_x = cell.x + cell.size // 2
            center_y = cell.y + cell.size // 2
            radius = cell.size // 3

            if cell.figure == Foo.WOLF:
                # Wolf is a red triangle
                points = [
                    (center_x, center_y - radius),  # top
                    (center_x - radius, center_y + radius),  # bottom left
                    (center_x + radius, center_y + radius)   # bottom right
                ]
                self.pg.draw.polygon(self.win, color, points)
            else:
                # Sheep is a white circle
                self.pg.draw.circle(self.win, color, (center_x, center_y), radius)

            try:
                # Try loading image with safe_load_image
                img = self.safe_load_image(Foo.get_figure_image_url(cell.figure))
                img = self.pg.transform.scale(img, (self.opt.cell_size - 2*cell.border_size, 
                                                self.opt.cell_size - 2*cell.border_size))
                self.win.blit(img, self.pg.rect.Rect(cell.x + cell.border_size,
                                                 cell.y + cell.border_size,
                                                 cell.size - cell.border_size,
                                                 cell.size - cell.border_size))
            except Exception as e:
                # Already drawn fallback shapes, just log the error
                print(f"Using fallback shape for {cell.figure}: {e}")

        if cell.selected:
            self.pg.draw.rect(self.win, Foo.COLOR_GOLD, (cell.x, cell.y, cell.size, cell.size), cell.border_size)
    # Menu
    def show_menu(self):
        print('gb-show')
        try:
            if self.menu is not None:
                self.menu.mainloop(self.win, bgfun=self.load_menu_bg)
            else:
                # Create a simple fallback menu
                self.win.fill(Foo.COLOR_BLACK_NERO)
                self.pg.draw.rect(self.win, (80, 80, 80),
                                (10, 10, self.WIN_WIDTH - 20, self.WIN_HEIGHT - 20), 3)

                # Draw title
                font = self.pg.font.SysFont('Arial', 48)
                title = font.render('Wolf and Sheep Game', True, (255, 255, 255))
                self.win.blit(title, (self.WIN_WIDTH//2 - 200, 100))

                # Draw instructions
                font = self.pg.font.SysFont('Arial', 24)
                subtitle = font.render('Press any key to start', True, (200, 200, 200))
                self.win.blit(subtitle, (self.WIN_WIDTH//2 - 100, 200))

                self.pg.display.update()

                # Wait for keypress
                waiting = True
                while waiting:
                    for event in self.pg.event.get():
                        if event.type == self.pg.QUIT:
                            self.pg.quit()
                            return
                        if event.type == self.pg.KEYDOWN or event.type == self.pg.MOUSEBUTTONDOWN:
                            waiting = False
                            self.start_the_game()
        except Exception as e:
            print(f"Error showing menu: {e}")


    def set_game_mode(self, value, mode):
        pass

    def set_board_size(self, value, mode):
        pass

    def set_ai_level(self, value, mode):
        pass

    def start_the_game(self):
        self.opt.set_default()
        try:
            if self.menu is not None:
                # Get settings from menu widgets
                border_size = self.menu.get_widget('border_size_selector_id', False).get_value()
                self.opt.board_size = border_size[0][1]

                mode = self.menu.get_widget('play_mode_selector_id', False).get_value()
                self.opt.mode = mode[0][0]

                ai_level = self.menu.get_widget('ai_level_selector_id', False).get_value()
                self.opt.ai_level = ai_level[0][1]

                mode = self.menu.get_widget('set_wolf_manually_selector_id', False).get_value()
                self.opt.set_wolf_manually = mode[0][0]  # 'YES' or 'NO'

                self.menu.disable()
        except Exception as e:
            print(f"Using default settings: {e}")
            # Fallback defaults
            self.opt.board_size = Foo.SIZE_8
            self.opt.mode = Foo.MODE_PLAYER_VS_PLAYER
            self.opt.ai_level = Foo.AI_3
            self.opt.set_wolf_manually = Foo.SET_WOLF_MANUALLY_NO

        # >>> RUN THIS ALWAYS, AFTER values are set <<<
        self.opt.placement_mode = (self.opt.set_wolf_manually == Foo.SET_WOLF_MANUALLY_YES)
        if self.opt.placement_mode:
            self.opt.is_wolf_position_init = False
        else:
            self.opt.is_wolf_position_init = True

        self.opt.is_running = True

    def load_menu_bg(self):
        # Create a fallback gradient background first
        self.win.fill(Foo.COLOR_BLACK_NERO)
        # Add a simple border for visual appeal
        self.pg.draw.rect(self.win, (80, 80, 80),
                        (10, 10, self.WIN_WIDTH - 20, self.WIN_HEIGHT - 20), 3)

        try:
            # Try loading image with safe_load_image
            bg_image = self.safe_load_image(Foo.MENU_BG)
            self.win.blit(bg_image, self.pg.rect.Rect(0, 0, self.WIN_WIDTH, self.WIN_HEIGHT))
#            print("Successfully loaded menu background")
        except Exception as e:
            # Create a more visually appealing fallback background
            for i in range(0, self.WIN_HEIGHT, 10):
                color_value = max(20, 80 - i//10)
                self.pg.draw.rect(self.win, (color_value, color_value, color_value+20),
                                 (0, i, self.WIN_WIDTH, 10))
            print(f"Using fallback background: {e}")
    def init_menu(self, options):
        try:
            import pygame_menu
            menu_theme = pygame_menu.themes.THEME_DARK.copy()
            menu_theme.set_background_color_opacity(0.93)

            # Fixed: Updated parameter order and syntax
            self.menu = pygame_menu.Menu('Menu', 750, 440, theme=menu_theme, center_content=False)

            # Fixed: Changed from add_button to add.button
            self.menu.add.button('PLAY', self.start_the_game)

            # Fixed: Changed from add_selector to add.selector
            self.menu.add.selector('Mode:   ',
                                  Foo.get_options_from_dict(Foo.PLAY_MODES, options.mode),
                                  selector_id='play_mode_selector_id', onchange=self.set_game_mode)
            self.menu.add.selector('Size:            ',
                                  Foo.get_options_from_dict(Foo.BOARD_SIZES, options.board_size),
                                  selector_id='border_size_selector_id', onchange=self.set_board_size)
            self.menu.add.selector('AI level:           ',
                                  Foo.get_options_from_dict(Foo.AI_LEVELS, options.ai_level),
                                  selector_id='ai_level_selector_id', onchange=self.set_ai_level)
            self.menu.add.selector('Set wolf:             ',
                                  Foo.get_options_from_dict(Foo.SET_WOLF_MANUALLY, options.set_wolf_manually),
                                  selector_id='set_wolf_manually_selector_id')

            # Fixed: Changed from add_button to add.button
            self.menu.add.button('QUIT', pygame_menu.events.EXIT)
        except Exception as e:
            print(f"Error creating menu: {e}")
            self.menu = None

    def draw_win_message(self):
        try:
            img = self.safe_load_image(Foo.VICTORY_MESSAGE)
            if self.opt.won == Foo.WOLF:
                self.win.blit(img, self.pg.rect.Rect(Gameboard.WOLF_VICTORY_MESSAGE_X, Gameboard.WOLF_VICTORY_MESSAGE_Y,
                                                     self.IMG_MESSAGE_WIDTH,
                                                     self.IMG_MESSAGE_HEIGHT))
            elif self.opt.won == Foo.SHEEP:
                self.win.blit(img, self.pg.rect.Rect(Gameboard.SHEEP_VICTORY_MESSAGE_X, Gameboard.SHEEP_VICTORY_MESSAGE_Y,
                                                     self.IMG_MESSAGE_WIDTH,
                                                     self.IMG_MESSAGE_HEIGHT))
        except Exception as e:
            # Fallback to text rendering
            self.pg.font.init()
            try:
                game_font = self.pg.font.SysFont('Arial', 32)
                textsurface = game_font.render('VICTORY!', True, Foo.RED)
                if self.opt.won == Foo.WOLF:
                    self.win.blit(textsurface, (Gameboard.WOLF_VICTORY_MESSAGE_X + 20, Gameboard.WOLF_VICTORY_MESSAGE_Y + 10))
                elif self.opt.won == Foo.SHEEP:
                    self.win.blit(textsurface, (Gameboard.SHEEP_VICTORY_MESSAGE_X + 20, Gameboard.SHEEP_VICTORY_MESSAGE_Y + 10))
            except Exception as e2:
                print(f"Could not render victory message: {e2}")

        self.update()

    def show_start_timer(self):
        pass
        # clock = pygame.time.Clock()
        #
        # counter, text = 10, '10'.rjust(3)
        # pygame.time.set_timer(pygame.USEREVENT, 1000)
        # font = pygame.font.SysFont('Consolas', 30)
        #
        # run = True
        # while run:
        #     for e in pygame.event.get():
        #         if e.type == pygame.USEREVENT:
        #             counter -= 1
        #             text = str(counter).rjust(3) if counter > 0 else 'boom!'
        #         if e.type == pygame.QUIT:
        #             run = False
        #
        #     screen.fill((255, 255, 255))
        #     screen.blit(font.render(text, True, (0, 0, 0)), (32, 48))
        #     pygame.display.flip()
        #     clock.tick(60)
