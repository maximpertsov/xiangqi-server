"""
isort:skip_file

Models must be imported here to be detected by Django migrations
"""

from .player import Player
from .game_event import GameEvent
from .draw_event import DrawEvent
from .takeback_event import TakebackEvent
from .game import Game
from .game_request import GameRequest
from .move import Move
