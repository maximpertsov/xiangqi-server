from abc import ABC, abstractmethod

import pyffish

from xiangqi.queries.legal_moves import LegalMoves


class BaseSerializeMove(ABC):
    def result(self):
        return {
            "fen": self.fen,
            "gives_check": self.gives_check,
            "legal_moves": self.legal_moves,
            "move": self.move_name,
        }

    @property
    @abstractmethod
    def fen(self):
        pass

    @property
    @abstractmethod
    def legal_moves(self):
        pass

    @property
    @abstractmethod
    def gives_check(self):
        pass

    @property
    @abstractmethod
    def move_name(self):
        pass


class SerializeMove(BaseSerializeMove):
    def __init__(self, fen, move_name):
        self._fen = fen
        self._move_name = move_name

    @property
    def fen(self):
        return pyffish.get_fen("xiangqi", self._fen, [self._move_name])

    @property
    def legal_moves(self):
        return LegalMoves(fen=self._fen, moves=[self._move_name]).result()

    @property
    def gives_check(self):
        return pyffish.gives_check("xiangqi", self._fen, [self._move_name])

    @property
    def move_name(self):
        return self._move_name


class SerializeInitialPlacement(BaseSerializeMove):
    @property
    def fen(self):
        return pyffish.start_fen("xiangqi")

    @property
    def legal_moves(self):
        return LegalMoves(fen=self.fen, moves=[]).result()

    @property
    def gives_check(self):
        return False

    @property
    def move_name(self):
        return None
