from abc import ABC, abstractmethod

from django.utils.functional import cached_property

from xiangqi.lib import pyffish
from xiangqi.queries.legal_moves import LegalMoves


class BaseSerializeMove(ABC):
    def result(self):
        return {
            "fen": self.fen,
            "gives_check": self.gives_check,
            "legal_moves": self._legal_moves,
            "move": self.move_name,
        }

    @property
    @abstractmethod
    def fen(self):
        pass

    @property
    @abstractmethod
    def gives_check(self):
        pass

    @property
    @abstractmethod
    def move_name(self):
        pass

    @property
    def _legal_moves(self):
        return LegalMoves(fen=self.fen).result()


class SerializeMove(BaseSerializeMove):
    def __init__(self, fen, move_name):
        self._fen = fen
        self._move_name = move_name

    @cached_property
    def fen(self):
        return pyffish.get_fen(self._fen, [self._move_name])

    @property
    def gives_check(self):
        return pyffish.gives_check(self._fen, [self._move_name])

    @property
    def move_name(self):
        return self._move_name


class SerializeInitialPlacement(BaseSerializeMove):
    @cached_property
    def fen(self):
        return pyffish.start_fen()

    @property
    def gives_check(self):
        return False

    @property
    def move_name(self):
        return None
