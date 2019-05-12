import json
from sys import argv
from itertools import starmap, chain


def decode_fen_row(i, row):
    result = []
    j = 0
    for ch in row:
        if ch.isdigit():
            j += int(ch)
            continue
        result.append({'code': ch, 'rank': i, 'file': j})
        j += 1
    return result


def decode_fen(fen):
    fen_tokens = fen.split(' ')[0].split('/')
    result = list(chain.from_iterable(starmap(decode_fen_row, enumerate(fen_tokens))))
    return result


if __name__ == '__main__':
    fen = argv[1]
    pieces = decode_fen(fen)
    data = {'pieces': pieces}
    print(json.dumps(data))
