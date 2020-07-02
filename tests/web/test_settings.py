import channels.layers
from asgiref.sync import async_to_sync


def test_channel_layer():
    channel_name = "test_channel"
    message = {"type": "hello"}

    channel_layer = channels.layers.get_channel_layer()
    async_to_sync(channel_layer.send)(channel_name, message)
    assert async_to_sync(channel_layer.receive)(channel_name) == message
