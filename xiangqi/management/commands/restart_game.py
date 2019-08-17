from django.core.management.base import BaseCommand

from xiangqi.models import Game


class Command(BaseCommand):
    help = "Restart game"

    def add_arguments(self, parser):
        parser.add_argument('--game', type=str, help='Game slug', required=True)

    def handle(self, game=None, *args, **kwargs):
        try:
            Game.objects.get(slug=game).move_set.all().delete()
            self.stdout.write(self.style.SUCCESS('Reset Game {}'.format(game)))
        except Game.DoesNotExist as e:
            self.stdout.write(e, self.style.ERROR)
            return
