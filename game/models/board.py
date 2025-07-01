"""Game board model for Wolf and Sheep game"""

from foo import Foo

class GameBoard:
    """Represents the game board and game logic"""

    def __init__(self, size):
        """Initialize the game board

        Args:
            size (int): Board size
        """
        self.size = size
        self.board = [[Foo.EMPTY_CELL for _ in range(size)] for _ in range(size)]

        # Initialize board with starting positions
        self.initialize_board()

    def initialize_board(self):
        """Set up the initial board state"""
        # Clear the board
        for row in range(self.size):
            for col in range(self.size):
                self.board[row][col] = Foo.EMPTY_CELL

        # Set wolf in the center
        wolf_pos = self.size // 2
        self.board[wolf_pos][wolf_pos] = Foo.WOLF

        # Set sheep around the edges
        sheep_count = min(self.size * 2, 12)  # Adjust based on board size
        sheep_placed = 0

        # Place sheep on top edge
        for col in range(self.size):
            if sheep_placed >= sheep_count:
                break
            if col % 2 == 0:  # Alternate columns
                self.board[0][col] = Foo.SHEEP
                sheep_placed += 1

        # Place sheep on bottom edge if needed
        if sheep_placed < sheep_count:
            for col in range(self.size):
                if sheep_placed >= sheep_count:
                    break
                if col % 2 == 1:  # Alternate columns
                    self.board[self.size - 1][col] = Foo.SHEEP
                    sheep_placed += 1

        # Place sheep on left edge if needed
        if sheep_placed < sheep_count:
            for row in range(1, self.size - 1):
                if sheep_placed >= sheep_count:
                    break
                if row % 2 == 0:  # Alternate rows
                    self.board[row][0] = Foo.SHEEP
                    sheep_placed += 1

        # Place sheep on right edge if needed
        if sheep_placed < sheep_count:
            for row in range(1, self.size - 1):
                if sheep_placed >= sheep_count:
                    break
                if row % 2 == 1:  # Alternate rows
                    self.board[row][self.size - 1] = Foo.SHEEP
                    sheep_placed += 1

    def get_cell(self, row, col):
        """Get the content of a cell

        Args:
            row (int): Row index
            col (int): Column index

        Returns:
            int: Cell content (figure type)
        """
        if 0 <= row < self.size and 0 <= col < self.size:
            return self.board[row][col]
        return Foo.NOT_INIT

    def set_cell(self, row, col, figure):
        """Set the content of a cell

        Args:
            row (int): Row index
            col (int): Column index
            figure (int): Figure type to set

        Returns:
            bool: True if successful
        """
        if 0 <= row < self.size and 0 <= col < self.size:
            self.board[row][col] = figure
            return True
        return False

    def is_valid_move(self, row, col, figure):
        """Check if a move is valid

        Args:
            row (int): Destination row
            col (int): Destination column
            figure (int): Figure type making the move

        Returns:
            bool: True if the move is valid
        """
        # Basic checks
        if not (0 <= row < self.size and 0 <= col < self.size):
            return False

        # Destination must be empty
        if self.board[row][col] != Foo.EMPTY_CELL:
            return False

        # Figure-specific move validation
        if figure == Foo.WOLF:
            return self._is_valid_wolf_move(row, col)
        elif figure == Foo.SHEEP:
            return self._is_valid_sheep_move(row, col)

        return False

    def _is_valid_wolf_move(self, dest_row, dest_col):
        """Check if a wolf move is valid

        Args:
            dest_row (int): Destination row
            dest_col (int): Destination column

        Returns:
            bool: True if the move is valid
        """
        # Find wolf position
        wolf_row, wolf_col = self._find_figure(Foo.WOLF)
        if wolf_row == -1:
            return False

        # Wolf can move one step in any direction
        row_diff = abs(dest_row - wolf_row)
        col_diff = abs(dest_col - wolf_col)

        # Check if it's a one-step move (including diagonals)
        return row_diff <= 1 and col_diff <= 1 and (row_diff > 0 or col_diff > 0)

    def _is_valid_sheep_move(self, dest_row, dest_col):
        """Check if a sheep move is valid

        Args:
            dest_row (int): Destination row
            dest_col (int): Destination column

        Returns:
            bool: True if the move is valid
        """
        # Find the sheep that's trying to move
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] == Foo.SHEEP:
                    # Sheep can move one step in any direction
                    row_diff = abs(dest_row - row)
                    col_diff = abs(dest_col - col)

                    # Check if it's a one-step move (including diagonals)
                    if row_diff <= 1 and col_diff <= 1 and (row_diff > 0 or col_diff > 0):
                        return True

        return False

    def make_move(self, row, col, figure):
        """Make a move on the board

        Args:
            row (int): Destination row
            col (int): Destination column
            figure (int): Figure type making the move

        Returns:
            bool: True if the move was successful
        """
        if not self.is_valid_move(row, col, figure):
            return False

        # For wolf, clear previous position
        if figure == Foo.WOLF:
            wolf_row, wolf_col = self._find_figure(Foo.WOLF)
            if wolf_row != -1:
                self.board[wolf_row][wolf_col] = Foo.EMPTY_CELL

        # For sheep, find the sheep that's closest to the destination
        elif figure == Foo.SHEEP:
            sheep_row, sheep_col = self._find_closest_sheep(row, col)
            if sheep_row != -1:
                self.board[sheep_row][sheep_col] = Foo.EMPTY_CELL

        # Set new position
        self.board[row][col] = figure
        return True

    def _find_figure(self, figure):
        """Find the position of a specific figure

        Args:
            figure (int): Figure type to find

        Returns:
            tuple: (row, col) of the figure, or (-1, -1) if not found
        """
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] == figure:
                    return row, col
        return -1, -1

    def _find_closest_sheep(self, dest_row, dest_col):
        """Find the sheep closest to the destination

        Args:
            dest_row (int): Destination row
            dest_col (int): Destination column

        Returns:
            tuple: (row, col) of the closest sheep, or (-1, -1) if not found
        """
        closest_sheep = (-1, -1)
        min_distance = float('inf')

        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] == Foo.SHEEP:
                    # Check if this sheep can move to the destination
                    row_diff = abs(dest_row - row)
                    col_diff = abs(dest_col - col)

                    if row_diff <= 1 and col_diff <= 1 and (row_diff > 0 or col_diff > 0):
                        distance = row_diff + col_diff
                        if distance < min_distance:
                            min_distance = distance
                            closest_sheep = (row, col)

        return closest_sheep

    def get_valid_moves(self, figure):
        """Get all valid moves for a figure

        Args:
            figure (int): Figure type

        Returns:
            list: List of valid moves as (row, col) tuples
        """
        valid_moves = []

        if figure == Foo.WOLF:
            # Find wolf position
            wolf_row, wolf_col = self._find_figure(Foo.WOLF)
            if wolf_row == -1:
                return valid_moves

            # Check all adjacent cells
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue  # Skip current position

                    new_row = wolf_row + dr
                    new_col = wolf_col + dc

                    if (0 <= new_row < self.size and 0 <= new_col < self.size and
                            self.board[new_row][new_col] == Foo.EMPTY_CELL):
                        valid_moves.append((new_row, new_col))

        elif figure == Foo.SHEEP:
            # For sheep, check each sheep's possible moves
            for row in range(self.size):
                for col in range(self.size):
                    if self.board[row][col] == Foo.SHEEP:
                        # Check all adjacent cells
                        for dr in [-1, 0, 1]:
                            for dc in [-1, 0, 1]:
                                if dr == 0 and dc == 0:
                                    continue  # Skip current position

                                new_row = row + dr
                                new_col = col + dc

                                if (0 <= new_row < self.size and 0 <= new_col < self.size and
                                        self.board[new_row][new_col] == Foo.EMPTY_CELL):
                                    valid_moves.append((new_row, new_col))

        return valid_moves
