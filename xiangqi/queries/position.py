from abc import ABC, abstractmethod

from django.utils.functional import cached_property

from xiangqi.lib.pyffish import xiangqi
from xiangqi.queries.legal_moves import LegalMoves


class BasePosition(ABC):
    def result(self):
        return {
            "fen": self.fen,
            "gives_check": self._gives_check,
            "legal_moves": self._legal_moves,
        }

    @property
    @abstractmethod
    def fen(self):
        pass

    @property
    def _legal_moves(self):
        return LegalMoves(fen=self.fen).result()

    @property
    def _gives_check(self):
        return xiangqi.gives_check(self.fen, [])


class Position(BasePosition):
    def __init__(self, *, previous_fen, move_name):
        self._move_name = move_name
        self._previous_fen = previous_fen

    @cached_property
    def fen(self):
        return xiangqi.get_fen(self._previous_fen, [self._move_name])


class StartingPosition(BasePosition):
    @cached_property
    def fen(self):
        return xiangqi.start_fen()
