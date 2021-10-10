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

        self.alphabet_img = self.pg.image.load(Foo.ALPHABET_IMG).convert_alpha()
        self.numbers_img = self.pg.image.load(Foo.NUMBERS_IMG).convert_alpha()
        self.update()

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
            self.win.blit( self.alphabet_img, (alph_start_x + self.opt.cell_size//3, self.GAMEBOARD_ZERO_Y // 4),
                           (grid_x, 0, self.ALPHABET_CELL_SIZE, self.ALPHABET_CELL_SIZE) )
            self.win.blit(self.alphabet_img, (alph_start_x + self.opt.cell_size // 3,
                                              self.GAMEBOARD_SIZE + self.GAMEBOARD_ZERO_Y + self.GAMEBOARD_ZERO_Y // 4),
                          (grid_x, 0, self.ALPHABET_CELL_SIZE, self.ALPHABET_CELL_SIZE))

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
        img = self.pg.image.load(Foo.AVATAR_SHEEP_IMG_URL).convert_alpha()
        self.win.blit(img, self.pg.rect.Rect(sheep_x + Gameboard.FIGURE_AVATAR_BORDER_SIZE,
                                             sheep_y + Gameboard.FIGURE_AVATAR_BORDER_SIZE,
                                             self.FIGURE_AVATAR_SIZE,
                                             self.FIGURE_AVATAR_SIZE))
        img_url = Foo.PLAYER_MSG if play_mode == Foo.MODE_PLAYER_VS_PLAYER or \
                                    play_mode == Foo.MODE_PLAYER_SHEEP_VS_AI \
            else Foo.COMPUTER_MSG
        img = self.pg.image.load(img_url).convert_alpha()
        self.win.blit(img, self.pg.rect.Rect(sheep_x + Gameboard.FIGURE_AVATAR_BORDER_SIZE,
                                             sheep_y + Gameboard.FIGURE_AVATAR_BORDER_SIZE,
                                             self.IMG_MESSAGE_WIDTH,
                                             self.IMG_MESSAGE_HEIGHT))

        # Wolf border.
        color = border_color if self.opt.whose_move != Foo.WOLF else Foo.COLOR_GOLD
        wolf_x = sheep_x
        wolf_y = Gameboard.GAMEBOARD_ZERO_Y + Gameboard.GAMEBOARD_SIZE - \
                 Gameboard.FIGURE_AVATAR_SIZE - Gameboard.FIGURE_AVATAR_BORDER_SIZE
        self.pg.draw.rect(self.win, color,
                          (wolf_x, wolf_y, avatar_border_size, avatar_border_size),
                          Gameboard.FIGURE_AVATAR_BORDER_SIZE)
        img = self.pg.image.load(Foo.AVATAR_WOLF_IMG_URL).convert_alpha()
        self.win.blit(img, self.pg.rect.Rect(wolf_x + Gameboard.FIGURE_AVATAR_BORDER_SIZE,
                                             wolf_y + Gameboard.FIGURE_AVATAR_BORDER_SIZE,
                                             self.FIGURE_AVATAR_SIZE,
                                             self.FIGURE_AVATAR_SIZE))
        img_url = Foo.PLAYER_MSG if play_mode == Foo.MODE_PLAYER_VS_PLAYER or \
                                    play_mode == Foo.MODE_PLAYER_WOLF_VS_COMPUTER \
            else Foo.COMPUTER_MSG
        img = self.pg.image.load(img_url).convert_alpha()
        self.win.blit(img, self.pg.rect.Rect(wolf_x + Gameboard.FIGURE_AVATAR_BORDER_SIZE,
                                             wolf_y + Gameboard.FIGURE_AVATAR_BORDER_SIZE,
                                             self.IMG_MESSAGE_WIDTH,
                                             self.IMG_MESSAGE_HEIGHT))

        # Buttons border.
        indent = (wolf_y - sheep_y - Gameboard.FIGURE_AVATAR_SIZE) // 10
        button_border_x = sheep_x
        button_border_y = sheep_y + Gameboard.FIGURE_AVATAR_SIZE + indent * 3
        self.pg.draw.rect(self.win, border_color,
                          (button_border_x, button_border_y, avatar_border_size, indent * 4),
                          Gameboard.FIGURE_AVATAR_BORDER_SIZE)

        # Show buttons: RESET and MENU.
        img = self.pg.image.load(Foo.RESET_BTN).convert_alpha()
        self.win.blit(img, self.pg.rect.Rect(button_border_x + 4, button_border_y + 4,
                                             self.BTN_RESET_WIDTH,
                                             self.BTN_RESET_HEIGHT))

        img = self.pg.image.load(Foo.MENU_BTN).convert_alpha()
        self.win.blit(img, self.pg.rect.Rect(button_border_x + 6 + self.BTN_RESET_WIDTH,
                                             button_border_y + 4,
                                             self.BTN_MENU_WIDTH,
                                             self.BTN_MENU_HEIGHT))

        # Show button: skip turn for wolf.
        if self.opt.won == Foo.NOT_INIT and \
                self.opt.whose_move == Foo.WOLF and self.opt.is_possible_skip_move_for_wolf and \
                ((self.opt.mode == Foo.MODE_PLAYER_VS_PLAYER) or (self.opt.mode == Foo.MODE_PLAYER_WOLF_VS_COMPUTER)) \
                and self.opt.is_wolf_position_init:
            img = self.pg.image.load(Foo.SKIP_TURN_BTN).convert_alpha()
            self.win.blit(img, self.pg.rect.Rect(Gameboard.WOLF_VICTORY_MESSAGE_X, Gameboard.WOLF_VICTORY_MESSAGE_Y,
                                                 self.IMG_MESSAGE_WIDTH,
                                                 self.IMG_MESSAGE_HEIGHT))
        elif not self.opt.is_wolf_position_init:
            img = self.pg.image.load(Foo.SET_WOLF_MSG).convert_alpha()
            self.win.blit(img, self.pg.rect.Rect(Gameboard.WOLF_VICTORY_MESSAGE_X, Gameboard.WOLF_VICTORY_MESSAGE_Y,
                                                 self.IMG_MESSAGE_WIDTH,
                                                 self.IMG_MESSAGE_HEIGHT))


        for i in range(options.board_size):
            for j in range(options.board_size):
                self.draw_cell(cells[i][j])
        self.timeout(timeout)
        self.update()

    def draw_cell(self, cell):
        pygame.draw.rect(self.win, cell.color, (cell.x, cell.y, cell.size, cell.size))

        if not (cell.is_empty()):
            img = self.pg.image.load(Foo.get_figure_image_url(cell.figure)).convert_alpha()
            img = pygame.transform.scale(img, (self.opt.cell_size, self.opt.cell_size))
            self.win.blit(img, self.pg.rect.Rect(cell.x + cell.border_size,
                                                 cell.y + cell.border_size,
                                                 cell.size - cell.border_size,
                                                 cell.size - cell.border_size))

        if cell.selected:
            self.pg.draw.rect(self.win, Foo.COLOR_GOLD, (cell.x, cell.y, cell.size, cell.size), cell.border_size)

    # Menu
    def show_menu(self):
        print('gb-show')
        self.menu.mainloop(self.win, bgfun=self.load_menu_bg)


    def set_game_mode(self, value, mode):
        pass

    def set_board_size(self, value, mode):
        pass

    def set_ai_level(self, value, mode):
        pass

    def start_the_game(self):
        self.opt.set_default()
        border_size = self.menu.get_widget('border_size_selector_id', False).get_value()
        self.opt.board_size = border_size[0][1]

        mode = self.menu.get_widget('play_mode_selector_id', False).get_value()
        self.opt.mode = mode[0][0]

        ai_level = self.menu.get_widget('ai_level_selector_id', False).get_value()
        self.opt.ai_level = ai_level[0][1]

        mode = self.menu.get_widget('set_wolf_manually_selector_id', False).get_value()
        self.opt.set_wolf_manually = mode[0][0]

        self.opt.is_running = True
        self.menu.disable()


    def load_menu_bg(self):
        bg_image = self.pg.image.load(Foo.MENU_BG)
        self.win.blit(bg_image, self.pg.rect.Rect(0, 0, self.WIN_WIDTH, self.WIN_HEIGHT))


    def init_menu(self, options):
        menu_theme = pygame_menu.themes.THEME_DARK.copy()
        menu_theme.set_background_color_opacity(0.93)

        self.menu = pygame_menu.Menu(440, 750, 'Menu', center_content=False, theme=menu_theme)

        self.menu.add_button('PLAY', self.start_the_game)

        self.menu.add_selector('Mode:   ',
                               Foo.get_options_from_dict(Foo.PLAY_MODES, options.mode),
                               selector_id='play_mode_selector_id', onchange=self.set_game_mode)
        self.menu.add_selector('Size:            ',
                               Foo.get_options_from_dict(Foo.BOARD_SIZES, options.board_size),
                               selector_id='border_size_selector_id', onchange=self.set_board_size)
        self.menu.add_selector('AI level:           ',
                               Foo.get_options_from_dict(Foo.AI_LEVELS, options.ai_level),
                            selector_id='ai_level_selector_id', onchange=self.set_ai_level)
        self.menu.add_selector('Set wolf:             ',
                               Foo.get_options_from_dict(Foo.SET_WOLF_MANUALLY, options.set_wolf_manually),
                               selector_id='set_wolf_manually_selector_id')

        self.menu.add_button('QUIT', pygame_menu.events.EXIT)

    def draw_win_message(self):
        # self.pg.font.init()
        # game_font = self.pg.font.SysFont('Roboto', 60)
        # textsurface = game_font.render(Gameboard.VICTORY_MESSAGE, False, Foo.RED)
        # self.win.blit(textsurface, (Gameboard.WOLF_VICTORY_MESSAGE_X, Gameboard.WOLF_VICTORY_MESSAGE_Y))
        # self.win.blit(textsurface, (Gameboard.SHEEP_VICTORY_MESSAGE_X, Gameboard.SHEEP_VICTORY_MESSAGE_Y))

        img = self.pg.image.load(Foo.VICTORY_MESSAGE).convert_alpha()
        if self.opt.won == Foo.WOLF:
            self.win.blit(img, self.pg.rect.Rect(Gameboard.WOLF_VICTORY_MESSAGE_X, Gameboard.WOLF_VICTORY_MESSAGE_Y,
                                                 self.IMG_MESSAGE_WIDTH,
                                                 self.IMG_MESSAGE_HEIGHT))
        elif self.opt.won == Foo.SHEEP:
            self.win.blit(img, self.pg.rect.Rect(Gameboard.SHEEP_VICTORY_MESSAGE_X, Gameboard.SHEEP_VICTORY_MESSAGE_Y,
                                                 self.IMG_MESSAGE_WIDTH,
                                                 self.IMG_MESSAGE_HEIGHT))

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
