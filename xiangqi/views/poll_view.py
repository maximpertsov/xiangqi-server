from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response

from xiangqi.models import Game


class PollView(RetrieveAPIView):
    queryset = Game.objects.all()
    lookup_field = "slug"

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        return Response({"update_count": instance.event_set.cached_count()})

    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance)
    #     return Response(serializer.data)
