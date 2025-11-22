class Position:
    def __init__(self, index, ln, col=0):
        self.index = index
        self.ln = ln
        self.col = col

    def advance(self, current_char):
        self.index += 1
        if current_char == "\n":
            self.ln += 1
            self.col = 0
        else:
            self.col += 1

    def copy(self):
        return Position(self.index, self.ln, self.col)
