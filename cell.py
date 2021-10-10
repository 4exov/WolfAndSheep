from foo import Foo


class Cell:
    x = y = -1
    i = j = 0
    border_size = 2
    size = 0
    color = None
    selected = False
    figure = -1  # -1 - empty cell, 1 -  Wolf, 255- Sheep.

    def __init__(self, x, y, i, j, color, size):
        self.color = color
        self.x = x
        self.y = y
        self.i = i
        self.j = j
        self.size = size

    def set_figure(self, figure):
        self.figure = figure

    def is_empty(self):
        if (self.figure == Foo.WOLF) or (self.figure == Foo.SHEEP):
            return False
        return True

    def is_selected(self):
        return self.selected

    def select(self):
        self.selected = True

    def unselect(self):
        self.selected = False
