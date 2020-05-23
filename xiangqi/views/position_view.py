from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from lib.pyffish import xiangqi
from xiangqi.serializers.move_serializer import PositionSerializer


class PositionView(GenericAPIView):
    serializer_class = PositionSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class StartingPositionView(PositionView):
    def get_serializer(self, *args, **kwargs):
        kwargs.update(fen=xiangqi.start_fen())
        return super().get_serializer(*args, **kwargs)
