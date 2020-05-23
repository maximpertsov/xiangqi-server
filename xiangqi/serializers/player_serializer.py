from rest_framework import serializers

from xiangqi.models import Player


class PlayerSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="username")

    class Meta:
        model = Player
        fields = ["name"]
