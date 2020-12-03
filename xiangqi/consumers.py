from channels.generic.websocket import AsyncWebsocketConsumer


class EventConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.game_slug = self.scope["url_route"]["kwargs"]["slug"]
        self.group_name = "game_%s" % self.game_slug
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        event = {"type": "game_event", "message": text_data}
        await self.channel_layer.group_send(self.group_name, event)

    async def game_event(self, event):
        message = event.pop("message", None)
        if not message:
            return
        await self.send(text_data=message)
