from gameboard import Gameboard
from cell import Cell
from options import Options
from foo import Foo
import queue
import copy
import time

class Game:
    run_loop = False

    options = None
    reset_options = None

    # Gameboard().
    gb = None

    # All cells here.
    board = []

    # Figures
    wolf = Foo.NOT_INIT
    sheeps = []  # I'm aware of such things

    # Selected figure, cell
    selected_figure = None

    # MATH
    NOT_INITIALIZED = 255
    MIN_VALUE = 0
    MAX_VALUE = 255
    BIG_VALUE = 500

    map = []
    current_position = queue.Queue()
    search_way = queue.Queue()

    possible_moves = [[1, -1], [1, 1], [-1, -1], [-1, 1]]

    def __init__(self):
        self.options = Options()
        self.gb = Gameboard(self.options)

    # Initialization and load data.
    def init_board(self):
        self.board = []
        cell_size = Gameboard.GAMEBOARD_SIZE // self.options.board_size
        self.options.cell_size = cell_size

        line_y = Gameboard.GAMEBOARD_ZERO_Y
        colours = [Foo.COLOR_BLACK_NERO, Foo.COLOR_WHITESMOKE]
        for i in range(self.options.board_size):
            line_cells = []
            line_x = Gameboard.GAMEBOARD_ZERO_X
            for j in range(self.options.board_size):
                sq = Cell(line_x, line_y, i, j, colours[((i + j) % 2)], cell_size)

                # Set Wolf
                if self.options.set_wolf_manually == Foo.SET_WOLF_MANUALLY_NO:
                    wolf_line = 0 if self.options.who_is_top == Foo.WOLF else (self.options.board_size - 1)
                    if i == wolf_line and sq.color == Foo.COLOR_BLACK_NERO and self.wolf == Foo.NOT_INIT:
                        sq.figure = Foo.WOLF
                        self.wolf = sq
                        self.options.is_wolf_position_init = True

                # Set Sheep
                sheep_line = 0 if self.options.who_is_top == Foo.SHEEP else (self.options.board_size - 1)
                if i == (sheep_line) and sq.color == Foo.COLOR_BLACK_NERO:
                    sq.figure = Foo.SHEEP
                    self.sheeps.append(sq)

                line_cells.append(sq)
                line_x += cell_size

            self.board.append(line_cells)
            line_y += cell_size

    # Main loop for game.
    def run_game(self):
        self.run_loop = True
        self.gb.init_menu(self.options)
        while self.run_loop:
            for event in self.gb.pg.event.get():
                if event.type == self.gb.pg.QUIT:
                    self.run_loop = False

                if event.type == self.gb.pg.MOUSEBUTTONDOWN:
                    coordinates = self.gb.pg.mouse.get_pos()
                    x = coordinates[0]
                    y = coordinates[1]

                    if self.on_show_menu(x, y):
                        print('show menu')
                        self.show_menu()

                    if self.on_restart_game(x, y):
                        self.reset_game()

                    if self.options.won == Foo.NOT_INIT and self.options.is_running and self.options.is_init_board:
                        cell = self.get_cell_by_coordinate(x, y)
                        if cell != None:
                            self.on_select(cell)
                        elif self.on_skip_move_area(x, y):
                            self.skip_wolf_move()


            if self.options.is_the_first_run:
                self.gb.show_menu()
                self.options.is_the_first_run = False

            elif self.options.is_running and not self.options.is_init_board:
                self.reset_options = copy.deepcopy(self.options)
                self.init_board()
                self.options.is_init_board = True
                self.gb.draw_board(self.options, self.board, 300)

            elif self.options.is_running and self.options.is_init_board and self.options.is_wolf_position_init:
                self.switch_move_by_mode()

                self.check_victory()
                # win message
                if self.options.won != Foo.NOT_INIT:
                    self.options.is_running = False
                    won_str = ""
                    if self.options.won == Foo.WOLF:
                        won_str = "Wolf won!"
                    elif self.options.won == Foo.SHEEP:
                        won_str = "Sheep won!"
                    self.options.whose_move = Foo.NOT_INIT
                    self.gb.draw_board(self.options, self.board, 0)
                    self.gb.draw_win_message()


        self.gb.pg.quit()

    # Check area skip the wolf move.
    def on_skip_move_area(self, x, y):
        if self.options.won == Foo.NOT_INIT and \
                self.options.whose_move == Foo.WOLF and self.options.is_possible_skip_move_for_wolf and \
                ((self.options.mode == Foo.MODE_PLAYER_VS_PLAYER) or (self.options.mode == Foo.MODE_PLAYER_WOLF_VS_COMPUTER)) and \
                self.options.is_wolf_position_init:
            if (x >= Gameboard.WOLF_AVATAR_X) and (y >= Gameboard.WOLF_AVATAR_Y) and \
                    (x <= Gameboard.WOLF_AVATAR_X + Gameboard.FIGURE_AVATAR_SIZE) and \
                    (y <= Gameboard.WOLF_AVATAR_Y + Gameboard.FIGURE_AVATAR_SIZE):
                return True
        return False

    # Skip wolf move.
    def skip_wolf_move(self):
        self.unselect_figure_cell(self.wolf)
        self.options.whose_move = Foo.SHEEP
        self.gb.draw_board(self.options, self.board, 0)

    # Check area for restart game.
    def on_restart_game(self, x, y):
        if (x >= Gameboard.BTN_RESET_X) and (y >= Gameboard.BTN_RESET_Y) and \
                (x <= Gameboard.BTN_RESET_X + Gameboard.BTN_RESET_WIDTH) and \
                (y <= Gameboard.BTN_RESET_Y + Gameboard.BTN_RESET_HEIGHT):
            return True
        return False

    def clear_self_data(self):
        self.board = []
        self.sheeps = []
        self.wolf = Foo.NOT_INIT
        self.selected_figure = None
        self.map = []
        self.current_position = queue.Queue()
        self.search_way = queue.Queue()

    # Reset game
    def reset_game(self):
        self.options = copy.deepcopy(self.reset_options)
        self.gb.opt = self.options
        self.clear_self_data()

    # Check area for restart game.
    def on_show_menu(self, x, y):
        if (x >= Gameboard.BTN_MENU_X) and (y >= Gameboard.BTN_MENU_Y) and \
                (x <= Gameboard.BTN_MENU_X + Gameboard.BTN_MENU_WIDTH) and \
                (y <= Gameboard.BTN_MENU_Y + Gameboard.BTN_MENU_HEIGHT):
            return True
        return False

    def show_menu(self):
        self.gb.init_menu(self.options)
        self.clear_self_data()
        self.gb.show_menu()




    # Switch move by mode. In accordance with the game mode, we make a move for the player.
    def switch_move_by_mode(self):
        if self.options.mode == Foo.MODE_PLAYER_VS_PLAYER:
            if self.options.whose_move == Foo.WOLF:
                pass

            elif self.options.whose_move == Foo.SHEEP:
                pass

            else:
                return Foo.TROUBLE

        elif self.options.mode == Foo.MODE_PLAYER_SHEEP_VS_AI:
            if self.options.whose_move == Foo.WOLF:
                self.run_AI(self.options.whose_move)

            elif self.options.whose_move == Foo.SHEEP:
                pass

            else:
                return Foo.TROUBLE

        elif self.options.mode == Foo.MODE_PLAYER_WOLF_VS_COMPUTER:
            if self.options.whose_move == Foo.WOLF:
                pass
            elif self.options.whose_move == Foo.SHEEP:
                self.run_AI(self.options.whose_move)
            else:
                return Foo.TROUBLE

        elif self.options.mode == Foo.MODE_AI_VS_AI:
            self.run_AI(self.options.whose_move)
            self.gb.timeout(300)
            # if self.options.whose_move == Foo.WOLF:
            #     pass
            # elif self.options.whose_move == Foo.SHEEP:
            #     pass
            # else:
            #     return Foo.TROUBLE

    # Get cell by (x, y).
    def get_cell_by_coordinate(self, row, col):
        print('({0}, {1})'.format(row, col))
        for i in range(self.options.board_size):
            for j in range(self.options.board_size):
                x = self.board[i][j].x
                y = self.board[i][j].y
                if (row >= x) and (row <= (x + self.options.cell_size)) and (col >= y) and (
                        col <= y + self.options.cell_size):
                    return self.board[i][j]
        return None

    # Select figure.
    def select_figure_cell(self, cell):
        if self.selected_figure is not None:
            self.selected_figure.unselect()
        cell.select()
        self.selected_figure = cell

    # Unselect figure.
    def unselect_figure_cell(self, cell):
        if self.selected_figure is not None:
            self.selected_figure.unselect()
            self.selected_figure = None
        cell.unselect()

    # Event select.
    def on_select(self, cell):
        is_selected = cell.selected
        i = cell.i
        j = cell.j

        # Set wolf manually
        if not self.options.is_wolf_position_init and cell.is_empty() and ((i + j) % 2) == 0:
            cell.figure = Foo.WOLF
            self.wolf = cell
            self.select_figure_cell(cell)
            self.options.is_wolf_position_init = True

            if self.options.is_manually_set_wolf_cancels_move:
                self.skip_wolf_move()

        # Select figure to move(unselect if other figure already selected)
        elif not (cell.is_empty()) and not is_selected and cell.figure == self.options.whose_move:

            if self.selected_figure is not None:
                self.unselect_figure_cell(self.selected_figure)
            self.select_figure_cell(cell)

        # Unselect figure. Target cell already selected.
        elif is_selected:
            self.unselect_figure_cell(cell)

        # Make move
        elif cell.is_empty() and (self.selected_figure is not None) and (self.is_valid_move_from_selected_figure(cell)):
            self.move_selected_figure_to_position(cell)

        self.gb.draw_board(self.options, self.board, 0)

    # TODO: Rewrite this function!
    def is_valid_move_for_player(self, player, from_cell, to_cell):
        from_i = from_cell.i
        from_j = from_cell.j
        to_i = to_cell.i
        to_j = to_cell.j

        if to_cell.is_empty():
            if player == Foo.WOLF:
                if (abs(from_i - to_i) == 1) and (abs(from_j - to_j) == 1):
                    return True
                else:
                    return False
            elif player == Foo.SHEEP:
                from_to_i = to_i - from_i if self.options.who_is_top == Foo.SHEEP else from_i - to_i

                if (from_to_i == 1) and (abs(from_j - to_j) == 1):
                    return True
                return False
        return False

    # TODO: Rewrite this function!
    def is_valid_move_from_selected_figure(self, cell):
        if cell.color is Foo.COLOR_BLACK_NERO and cell.is_empty():
            if self.options.whose_move == Foo.WOLF:
                if self.is_valid_move_for_player(Foo.WOLF, self.selected_figure, cell):
                    return True
                else:
                    return False
            elif self.options.whose_move == Foo.SHEEP:  # sheep
                if self.is_valid_move_for_player(Foo.SHEEP, self.selected_figure, cell):
                    return True
                else:
                    return False
        else:  # white cell
            return Foo.TROUBLE

    # Move figure from to.
    def move_figure(self, cell_from, cell_to):
        figure = self.board[cell_from.i][cell_from.j].figure
        self.board[cell_from.i][cell_from.j].figure = Foo.EMPTY_CELL
        self.board[cell_to.i][cell_to.j].figure = figure
        return True

    # TODO: Rewrite this function!
    def move_selected_figure_to_position(self, cell_to):
        if not self.selected_figure == None:
            print('move_selected_figure_to_position: Move  selected figure: {0}, from ({1}, {2}) to ({3}, {4}).'.format(
                self.selected_figure.figure,
                self.selected_figure.i,
                self.selected_figure.j,
                cell_to.i,
                cell_to.j
            ))
            

            if self.options.whose_move == Foo.WOLF:
                self.move_figure(self.selected_figure, cell_to)
                self.options.whose_move = Foo.SHEEP
                self.wolf = cell_to

            else:
                self.move_figure(self.selected_figure, cell_to)
                self.options.whose_move = Foo.WOLF
                self.update_sheeps(self.selected_figure, cell_to)

            self.unselect_figure_cell(self.selected_figure)

            print('move_selected_figure_to_position: Current move: {0}, Selected figure: {1}).'.format(
                'WOLF' if self.options.whose_move == Foo.WOLF else 'SHEEP',
                'NaN' if self.selected_figure == None else self.selected_figure.figure
            ))

        else:
            print('move_selected_figure_to_position: ERROR - There are not any selected figures.')
            return False

    # TODO: Rewrite this function!
    def update_figures(self):
        wolf_cells = self.get_cells_by_player(Foo.WOLF)

        if len(wolf_cells) > 0:
            self.wolf = wolf_cells[0]

        sheep_cells = self.get_cells_by_player(Foo.SHEEP)
        self.sheeps.clear()
        for sheep in sheep_cells:
            self.sheeps.append(sheep)

    # TODO: Rewrite this function!
    def update_sheeps(self, from_cell, to_cell):
        i = 0
        for sheep in self.sheeps:
            if (sheep.i == from_cell.i) and (sheep.j == from_cell.j):
                self.board[self.sheeps[i].i][self.sheeps[i].j].figure = Foo.EMPTY_CELL
                self.sheeps[i] = to_cell
                return True
            i += 1
        return False

    # TODO: Rewrite this function!
    def get_cells_by_player(self, player):
        cells = []
        for i in range(self.options.board_size):
            for j in range(self.options.board_size):
                if self.board[i][j].figure == player:
                    cells.append(self.board[i][j])
        return cells

    # TODO: Rewrite this function!
    def get_available_moves_for_cell(self, player, cell):
        moves = []
        cells_for_test = []
        i = cell.i
        j = cell.j

        test_moves = [
            {
                'i': i - 1,
                'j': j + 1
            },
            {
                'i': i - 1,
                'j': j - 1
            },
            {
                'i': i + 1,
                'j': j + 1
            },
            {
                'i': i + 1,
                'j': j - 1
            }

        ]
        for move in test_moves:
            k = move['i']
            l = move['j']
            try:
                ca = self.board[k][l]
                cells_for_test.append(ca)

            except IndexError:
                continue

        for c in cells_for_test:
            if self.is_valid_move_for_player(player, cell, c):
                moves.append(c)

        return moves

    # TODO: Rewrite this function!
    def get_available_moves_by_player(self, player):
        if player == Foo.WOLF:
            return self.get_available_moves_for_cell(Foo.WOLF, self.wolf)
        elif player == Foo.SHEEP:
            avlbl_moves = []
            for sheep in self.sheeps:
                moves = self.get_available_moves_for_cell(Foo.SHEEP, sheep)
                for m in moves:
                    avlbl_moves.append(m)
            return avlbl_moves
        else:
            return Foo.TROUBLE


    # Check victory
    def check_victory(self):

        # Wolf victory
        if self.wolf_is_victory():
            self.options.won = Foo.WOLF
            return self.options.won

        # Sheep victory
        if self.wolf_is_lost():
            self.options.won = Foo.SHEEP
            return self.options.won

        # Wolf victory
        sheep_available_moves = self.get_available_moves_by_player(Foo.SHEEP)
        if len(sheep_available_moves) == 0 and self.options.whose_move == Foo.SHEEP:
            self.options.won = Foo.WOLF
            return self.options.won
    def wolf_is_victory(self):
        i = self.wolf.i
        wolf_point = self.options.board_size - 1 if self.options.who_is_top == Foo.WOLF else 0
        if i == wolf_point:
            return True
        else:
            return False

    def wolf_is_lost(self):
        wolf_available_moves = self.get_available_moves_for_cell(Foo.WOLF, self.wolf)
        if len(wolf_available_moves) != 0:
            return False
        else:
            return True


    # _______MATH__________

    # AI move.
    def run_AI(self, player):
        # _______ RUN RESULT MINMAX
        start = time.time()
        best_move = self.min_max(player, 0, - self.BIG_VALUE, self.BIG_VALUE)
        end = time.time()

        print("Minmax operation time is {0}.".format(end - start))
        self.gb.update()
        if self.options.whose_move == Foo.WOLF:

            to_i = self.wolf.i + self.possible_moves[best_move % 4][0]
            to_j = self.wolf.j + self.possible_moves[best_move % 4][1]
            self.select_figure_cell(self.wolf)

            if self.is_can_move(to_i, to_j):
                self.move_selected_figure_to_position(self.board[to_i][to_j])
                self.gb.draw_board(self.options, self.board, 0)
            else:
                print('run_AI: ERROR - move to ({0}, {1}) is impossible. Please make a manual move.  ')

        elif self.options.whose_move == Foo.SHEEP:
            sheep = self.sheeps[best_move//2]
            to_i = sheep.i + self.possible_moves[best_move % 2][0]
            to_j = sheep.j + self.possible_moves[best_move % 2][1]
            self.select_figure_cell(sheep)
            if self.is_can_move(to_i, to_j):
                self.move_selected_figure_to_position(self.board[to_i][to_j])
                self.gb.draw_board(self.options, self.board, 0)
            else:
                print('run_AI: ERROR - move to ({0}, {1}) is impossible. Please make a manual move.  ')
        else:
            print('run_AI: error has happened')

        # function for MATH

    def prepare_map(self):
        self.map.clear()
        for i in range(self.options.board_size):
            tmp_map = []
            for j in range(self.options.board_size):
                tmp_map.append(0)
            self.map.append(tmp_map)

        self.map[self.wolf.i][self.wolf.j] = Foo.WOLF

        cells = self.get_cells_by_player(Foo.SHEEP)
        for cell in cells:
            self.map[cell.i][cell.j] = Foo.SHEEP

        # function for MATH

    def is_can_move(self, i, j):
        if not ((i >= 0) and (j >= 0) and (i < self.options.board_size) and (j < self.options.board_size)):
            return False
        if self.map[i][j] != 0:
            return False
        if self.board[i][j].figure != Foo.EMPTY_CELL:
            return False

        return True

    def temporary_move(self, index, cell_to_i, cell_to_j):
        cell_to = self.board[cell_to_i][cell_to_j]

        if index == 0:
            self.map[self.wolf.i][self.wolf.j] = 0
            self.map[cell_to_i][cell_to_j] = Foo.WOLF
            self.move_figure(self.wolf, cell_to)
            self.wolf = cell_to
        else:
            sheep = self.sheeps[index - 1]
            self.map[sheep.i][sheep.j] = 0
            self.map[cell_to_i][cell_to_j] = Foo.SHEEP
            self.move_figure(sheep, cell_to)
            self.update_sheeps(sheep, cell_to)

        # 0..253 -wolf; 254 - victor sheep

    def min_max(self, player, rec_level, alpha, beta):
        dangerous_wolf_position =False
        if rec_level == 0:
            self.prepare_map()

        is_sheep = True if (player == Foo.SHEEP) else False
        best_move = self.NOT_INITIALIZED

        min_max = self.MIN_VALUE if is_sheep else self.MAX_VALUE;

        result_min_max = self.NOT_INITIALIZED

        if rec_level >= (self.options.ai_level * 2):
            heuristic = self.get_heuristic_eval()
            self.prepare_map()
            return heuristic

        moves_eval_dict = {}

        for i in range(0 if is_sheep else self.options.board_size, self.options.board_size if is_sheep else (self.options.board_size + 4)):
            # self.update_figures()

            cur_figure_indx = (i // 2 + 1) if is_sheep else 0

            cur_figure = self.wolf if cur_figure_indx == 0 else self.sheeps[cur_figure_indx - 1]
            cur_move = self.possible_moves[i % 2 if is_sheep else i % 4]

            back_i = cur_figure.i
            back_j = cur_figure.j


            run_minmax = True
            result_min_max = 0
            if self.is_can_move(cur_figure.i + cur_move[0], cur_figure.j + cur_move[1]):

                self.temporary_move(cur_figure_indx, cur_figure.i + cur_move[0], cur_figure.j + cur_move[1])
                #self.gb.draw_board(self.options, self.board, 800)

                # Don't run minmax if the wolf have last victory move
                if not is_sheep and rec_level == 0 and self.wolf_is_victory():
                    self.temporary_move(cur_figure_indx, back_i, back_j)
                    best_move = i
                    dangerous_wolf_position = True
                    break

                # Don't run minmax if sheep have last victory move
                if is_sheep and rec_level == 0 and self.wolf_is_lost():
                    self.temporary_move(cur_figure_indx, back_i, back_j)
                    best_move = i
                    break

                # Don't commit suicide, dear The Wolf
                if rec_level == 1 and is_sheep and self.wolf_is_lost():
                    result_min_max = self.MAX_VALUE - 1
                    run_minmax = False

                if run_minmax:
                    result_min_max = self.min_max(Foo.WOLF if is_sheep else Foo.SHEEP, rec_level + 1, alpha, beta)

                self.temporary_move(cur_figure_indx, back_i, back_j)
                #self.gb.draw_board(self.options, self.board, 800)

                if rec_level == 0:
                    moves_eval_dict[i] = result_min_max

                if ((result_min_max > min_max) and is_sheep) or (
                        result_min_max <= min_max and player == Foo.WOLF) or best_move == self.NOT_INITIALIZED:
                    min_max = result_min_max
                    best_move = i

                if is_sheep:
                    alpha = alpha if alpha > result_min_max else result_min_max
                else:
                    beta = beta if beta < result_min_max else result_min_max
                if (beta < alpha):
                    break

        if best_move == self.NOT_INITIALIZED:
            heuristic = self.get_heuristic_eval()
            self.prepare_map()
            return heuristic

        # MAKE MOVE!!!
        if (rec_level == 0) and (best_move != self.NOT_INITIALIZED):
            if not is_sheep:
                if not dangerous_wolf_position:
                    sorted_moves =sorted(moves_eval_dict.items(), key=lambda x: (x[1], x[0]))
                    for eval in sorted_moves:
                        if (eval[1] == moves_eval_dict[best_move]) and (eval[0] % 4 in [2, 3]):
                            best_move = eval[0]
                            break
            return best_move

        #print("ThE BEST MOVE IS: ", best_move)
        return min_max

    def get_heuristic_eval(self):
        wolf_point = self.options.board_size - 1 if self.options.who_is_top == Foo.WOLF else 0
        if self.wolf.i == wolf_point:
            return 0

        self.search_way.queue.clear()
        self.search_way.put(self.wolf)

        while not self.search_way.empty():
            cur_cell = self.search_way.get()

            for k in range(4):
                n = cur_cell.i + self.possible_moves[k][0]
                m = cur_cell.j + self.possible_moves[k][1]
                if self.is_can_move(n, m):
                    cell = self.board[n][m]
                    self.map[cell.i][cell.j] = self.map[cur_cell.i][cur_cell.j] + 1
                    self.search_way.put(cell)

        min = self.MAX_VALUE
        for i in range(self.options.board_size//2):
            if (self.map[0][i * 2] > self.MIN_VALUE) and (self.map[0][i * 2] < min):
                min = self.map[0][i * 2]

        return min - 2
