from abc import ABC, abstractmethod

from django.utils.functional import cached_property

from xiangqi.lib.pyffish import xiangqi
from xiangqi.queries.legal_moves import LegalMoves


class Position:
    def __init__(self, *, fen=None, move_name=None):
        self._move_name = move_name
        self._fen = fen

    @cached_property
    def legal_moves(self):
        return LegalMoves(fen=self.fen).result()

    @cached_property
    def gives_check(self):
        return xiangqi.gives_check(self.fen, [])

    @cached_property
    def fen(self):
        fen = self._fen or xiangqi.start_fen()
        return xiangqi.get_fen(fen, self._moves)

    @cached_property
    def _moves(self):
        return [self._move_name] if self._move_name else []
