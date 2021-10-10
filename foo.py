class Foo:
    NOT_INIT = -1
    TROUBLE = None

    # Figures
    EMPTY_CELL = -1
    WOLF = 1
    SHEEP = 255

    # Images
    IMAGES = {
        SHEEP: "assets/sheep.png",
        WOLF: "assets/wolf.png",
        EMPTY_CELL: 'assets/empty_figure.png'
    }

    AVATAR_WOLF_IMG_URL = "assets/avatar_wolf.jpg"
    AVATAR_SHEEP_IMG_URL = "assets/avatar_sheep.jpg"
    VICTORY_MESSAGE = "assets/victory_msg.png"
    RESET_BTN = "assets/reset_btn.png"
    MENU_BTN = "assets/menu_btn.png"
    SKIP_TURN_BTN = "assets/skip_turn_msg.png"
    COMPUTER_MSG = "assets/computer_msg.png"
    PLAYER_MSG = "assets/player_msg.png"
    MENU_BG = "assets/menu-bg.jpg"
    SET_WOLF_MSG = "assets/set_wolf_msg.png"
    ALPHABET_IMG = "assets/alphabet-728x28.png"
    NUMBERS_IMG = "assets/numbers-728x28.png"

    # Play modes
    MODE_PLAYER_WOLF_VS_COMPUTER = 'COMPUTER(Sheep) vs WOLF'
    MODE_PLAYER_SHEEP_VS_AI = 'COMPUTER(Wolf) vs SHEEP'
    MODE_PLAYER_VS_PLAYER = ' PLAYER vs PLAYER'
    MODE_AI_VS_AI = 'COMPUTER vs COMPUTER'

    MODE_SET_FIGURE_MANUALLY = 'SetFiguresManually '
    MODE_MATH = 'MathMode'

    PLAY_MODES = {
        MODE_PLAYER_WOLF_VS_COMPUTER: 1,
        MODE_PLAYER_SHEEP_VS_AI: 2,
        MODE_PLAYER_VS_PLAYER: 3,
        MODE_AI_VS_AI: 4
    }

    # Board sizes
    SIZE_6 = 6
    SIZE_8 = 8
    SIZE_10 = 10
    SIZE_12 = 12
    SIZE_4 = 4

    BOARD_SIZES = {
        SIZE_6: 6,
        SIZE_8: 8,
        SIZE_10: 10,
        SIZE_12: 12,
        SIZE_4: 4
    }

    # AI levels
    AI_1 = 1
    AI_2 = 2
    AI_3 = 3
    AI_4 = 4
    AI_5 = 5

    AI_LEVELS = {
        AI_1: 1,
        AI_2: 2,
        AI_3: 3,
        AI_4: 4,
        AI_5: 5
    }

    # Set wolf manually
    SET_WOLF_MANUALLY_YES = 'YES'
    SET_WOLF_MANUALLY_NO = 'NO'

    SET_WOLF_MANUALLY = {
        SET_WOLF_MANUALLY_YES: 1,
        SET_WOLF_MANUALLY_NO: 2
    }

    # Colours
    COLOR_BLACK_NERO = (40, 40, 40)
    BLACK = (0, 0, 0)

    WHITE = (255, 255, 255)
    COLOR_WHITESMOKE = (242, 242, 242)
    COLOR_GHOSTWHITE = (248, 248, 255)

    COLOR_DIMGREY = (105, 105, 105)
    GRAY = (220, 220, 220)

    RED = (255, 33, 24)

    COLOR_GOLD = (204, 51, 0)

    def __init__(self):
        return

    @staticmethod
    def get_figure_image_url(figure):
        return Foo.IMAGES[figure]

    @staticmethod
    def get_options_from_dict(dict, key):
        result = []

        if key is not None and key in dict:
            result.append((str(key), dict[key]))

        for m in dict:
            if m != key:
                result.append((str(m), dict[m]))

        return result
