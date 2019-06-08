import json
from itertools import chain, starmap
from sys import argv


def decode_fen_row(i, row):
    result = []
    j = 0
    for ch in row:
        if ch.isdigit():
            j += int(ch)
            continue
        result.append({'name': ch, 'starting_position': '{},{}'.format(i, j)})
        j += 1
    return result


# slots instead of ranks and files
def decode_fen_row2(row):
    result = []
    j = 0
    for ch in row:
        if ch.isdigit():
            k = int(ch)
            result.extend([None] * k)
            j += k
            continue
        result.append(ch)
        j += 1
    return result


def decode_fen(fen):
    fen_tokens = fen.split(' ')[0].split('/')
    result = list(chain.from_iterable(starmap(decode_fen_row, enumerate(fen_tokens))))
    return result


def decode_fen2(fen):
    fen_tokens = fen.split(' ')[0].split('/')
    result = list(chain.from_iterable(map(decode_fen_row2, fen_tokens)))
    return result


if __name__ == '__main__':
    fen = argv[1]
    pieces = decode_fen(fen)

    fixtures = [
        {'model': 'xiangqi.piece', 'pk': i, 'fields': data}
        for i, data in enumerate(pieces, start=1)
    ]

    with open('xiangqi/fixtures/pieces.json', 'w') as f:
        json.dump(fixtures, f)
