from django.core.management import call_command
from pytest import mark


@mark.django_db
def test_restart_game(game):
    # Smoke test
    call_command("restart_game", slug=game.slug)
    assert True
