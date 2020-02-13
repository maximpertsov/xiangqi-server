import widget

class Checker(object):

    def __init__(self, translate = False):
        self.__translate = translate
        self.__board = widget.Board()

    def check_move(self, old , new = None):
        "Checks whether a given move is legal"
        if new == None:
            old, new = old

        return self.__board.check_move(old, new)

    def make_move(self, old, new = None):
        '''Updates the board state, without checking the move's legality'''
        if new == None:
            old, new = old

        self.__board.move_piece(old, new)
