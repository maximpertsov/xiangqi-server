import pytest
from pytest_factoryboy import register

from tests import factories
from xiangqi.queries.move.legal_moves import LegalMoves
from xiangqi.queries.move.serialize_move import SerializeMove

register(factories.GameFactory)
register(factories.PlayerFactory)
register(factories.UserFactory)
register(factories.ParticipantFactory)
register(factories.MoveFactory)


@pytest.fixture
def fen():
    return 'FEN 0'


@pytest.fixture
def new_fen():
    return 'FEN 1'


@pytest.fixture
def new_legal_moves():
    return []


@pytest.mark.django_db
def test_serialize_move(mocker, move, new_fen, new_legal_moves):
    mock_get_fen = mocker.patch(
        'pyffish.get_fen', mocker.MagicMock(return_value=new_fen)
    )
    mock_query_legal_moves = mocker.patch.object(
        LegalMoves, 'result', return_value=new_legal_moves
    )

    assert SerializeMove(fen=fen, move=move).result() == {
        'fen': new_fen,
        'move': move.name,
        'legal_moves': new_legal_moves,
    }
    mock_get_fen.assert_called_once_with('xiangqi', fen, [move.name])
    mock_query_legal_moves.assert_called_once_with()
