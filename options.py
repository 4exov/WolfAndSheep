from foo import Foo


class Options:
    who_is_top = Foo.SHEEP
    won = Foo.NOT_INIT
    board_size = Foo.SIZE_8
    cell_size = 90
    mode = Foo.MODE_PLAYER_VS_PLAYER
    ai_level = Foo.AI_2

    whose_move = Foo.NOT_INIT

    is_running = False
    is_init_board = False
    is_show_menu = False
    is_the_first_run = True

    is_wolf_position_init = False
    set_wolf_manually = Foo.SET_WOLF_MANUALLY_NO
    is_possible_skip_move_for_wolf = True
    is_manually_set_wolf_cancels_move = True

    def __init__(self):
        self.set_default()

    def set_default(self):
        self.board_size = Foo.SIZE_8
        self.cell_size = 90
        self.mode = Foo.MODE_PLAYER_WOLF_VS_COMPUTER
        self.ai_level = Foo.AI_2
        self.is_running = False
        self.is_init_board = False
        self.is_show_menu = False
        self.whose_move = Foo.WOLF
        self.won = Foo.NOT_INIT
        self.is_wolf_position_init = False
        self.is_possible_skip_move_for_wolf = True
        self.set_wolf_manually = Foo.SET_WOLF_MANUALLY_NO
