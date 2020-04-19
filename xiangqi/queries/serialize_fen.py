from abc import ABC, abstractmethod

from django.utils.functional import cached_property

from xiangqi.lib.pyffish import xiangqi
from xiangqi.queries.legal_moves import LegalMoves


class BaseSerializeFen(ABC):
    def result(self):
        return {
            "fen": self.fen,
            "gives_check": self.gives_check,
            "legal_moves": self._legal_moves,
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
    def _legal_moves(self):
        return LegalMoves(fen=self.fen).result()


class SerializeFen(BaseSerializeFen):
    def __init__(self, fen):
        self._fen = fen

    @cached_property
    def fen(self):
        return self._fen

    @property
    def gives_check(self):
        return xiangqi.gives_check(self._fen, [])


class SerializeInitialFen(BaseSerializeFen):
    @cached_property
    def fen(self):
        return xiangqi.start_fen()

    @property
    def gives_check(self):
        return False
