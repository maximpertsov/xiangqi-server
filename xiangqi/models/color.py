from enum import Enum


class Color(Enum):
    RED = 'red'
    BLACK = 'black'

    @classmethod
    def choices(cls):
        return [(tag, tag.value) for tag in cls]
