from django.core.management import call_command
from django.core.management.base import BaseCommand

from xiangqi.models import Game


class Command(BaseCommand):
    help = "Restart game"

    def add_arguments(self, parser):
        parser.add_argument("--game", type=str, help="Game slug", required=True)

    def handle(self, game=None, *args, **kwargs):
        try:
            game = Game.objects.get(slug=game)

            game.move_set.all().delete()
            game.transition_set.all().delete()
            game.event_set.all().delete()

            call_command("clear_cache")
            self.write_success("Reset Game {}".format(game))
        except Game.DoesNotExist as e:
            self.stdout.write(e, self.style.ERROR)
            return

    def write_success(self, message):
        self.stdout.write(self.style.SUCCESS(message))
