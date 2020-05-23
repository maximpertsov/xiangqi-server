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
        return Response(serializer.data, status=status.HTTP_200_OK)


class StartingPositionView(PositionView):
    def get_serializer(self, *args, **kwargs):
        data = kwargs["data"].copy()
        data.update(fen=xiangqi.start_fen())
        kwargs.update(data=data)
        return super().get_serializer(*args, **kwargs)
