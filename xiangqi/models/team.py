from enum import Enum


class Team(Enum):
    RED = 'red'
    BLACK = 'black'

    @classmethod
    def choices(cls):
        return [(tag, tag.value) for tag in cls]
