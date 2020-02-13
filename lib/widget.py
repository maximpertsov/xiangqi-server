import rule
import itertools

class Piece(object):
  LABELS = ['GENERAL',
    'ADVISOR',
    'ELEPHANT',
    'HORSE',
    'CHARIOT',
    'CANNON',
    'SOLDIER']

  namemap = {}
  for _id, label in enumerate(LABELS):
    namemap[_id] = label
    locals()[label] = _id

  UISTATE = ['NONE', 'PRESSED', 'SELECTED']
  statemap = {}
  for _id, state in enumerate(UISTATE):
    statemap[_id] = state
    locals()[state] = _id


  def __init__(self, _type, color='red'):
    self._type = _type
    self.color = color
    self.state = self.NONE
    self.rule = getattr(rule, self.label.lower())

  def __repr__(self):
    return '%s: %s, %s' % (self.color, self.label, self.state)

  @property
  def label(self):
    return self.namemap[self._type]

  @property
  def is_selected(self):
    return self.state == self.SELECTED

  def is_enemy(self, another_piece):
    return self.color != another_piece.color

  def is_general(self):
    return self._type == Piece.GENERAL

class Board(object):
  gx = 8  # grid number in x-axis
  gy = 9  # grid number in y-axis
  turn_iter = itertools.cycle(('red', 'black'))

  def __init__(self):
    self.pieces = {}  # { logical tuple : Piece obj } expect each obj has draw method
    self.onInit()

  def onInit(self):
    initpieces = {
        (4,9) : Piece.GENERAL,
        (3,9) : Piece.ADVISOR,
        (5,9) : Piece.ADVISOR,
        (2,9) : Piece.ELEPHANT,
        (6,9) : Piece.ELEPHANT,
        (1,9) : Piece.HORSE,
        (7,9) : Piece.HORSE,
        (0,9) : Piece.CHARIOT,
        (8,9) : Piece.CHARIOT,
        (7,7) : Piece.CANNON,
        (1,7) : Piece.CANNON,
        (0,6) : Piece.SOLDIER,
        (2,6) : Piece.SOLDIER,
        (4,6) : Piece.SOLDIER,
        (6,6) : Piece.SOLDIER,
        (8,6) : Piece.SOLDIER,
        }
    for c, _type in initpieces.iteritems():
      self.pieces[c] = Piece(_type, 'red')
      ix, iy=c
      d = (ix, -iy+self.gy)
      self.pieces[d] = Piece(_type, 'black')

  def move_piece(self, old_lc, new_lc):
    p = self.pieces.pop(old_lc, None)
    if p == None:
      return
    self.pieces[new_lc] = p

  def check_move(self, old_lc, new_lc):
    piece = self.pieces.get(old_lc, None)
    if piece == None:
      return False
    else:
      rules = piece.rule(old_lc, self.pieces)
      return new_lc in rules
