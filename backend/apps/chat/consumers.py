from channels.db import database_sync_to_async
from djangochannelsrestframework.decorators import action
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer

from .models import ChatModel


class ChatConsumer(GenericAsyncAPIConsumer):
    def __init__(self, *args, **kwargs):
        self.name = None
        self.room_name = None
        super().__init__(*args, **kwargs)

    async def connect(self):
        if not self.scope['user']:
            await self.close()
        await self.accept()
        self.room_name = self.scope['url_route']['kwargs']['room']
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )
        self.name = await self.get_profile_surname()
        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'sender',
                'message': f'{self.name} connected to chat'
            }
        )
        messages = await self.get_last_five_messages()
        for item in reversed(messages):
            await self.sender({
                'message': item['message'],
                'user': item['owner']
            })

    async def sender(self, event):
        await self.send_json(event)

    @action()
    async def send_message(self, data, request_id, action):
        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'sender',
                'message': data,
                'user': self.name,
                'id': request_id,
            }
        )
        await self.save_message_to_db(data, self.scope['user'])

    @database_sync_to_async
    def get_profile_surname(self):
        return self.scope['user'].profile.surname

    @database_sync_to_async
    def save_message_to_db(self, message, user):
        ChatModel.objects.create(message=message, owner=user)

    @database_sync_to_async
    def get_last_five_messages(self):
        return [
            {'message': item.message, 'owner': item.owner.profile.surname}
            for item in ChatModel.objects.order_by('-id')[:5]
        ]
