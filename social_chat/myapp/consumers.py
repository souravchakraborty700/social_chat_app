from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import Message, Interest
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.interest_id = self.scope['url_route']['kwargs']['interest_id']
        self.room_group_name = f'chat_{self.interest_id}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = self.scope["user"].username
        user = self.scope["user"]

        # Save message to the database
        interest = await database_sync_to_async(Interest.objects.get)(id=self.interest_id)
        new_message = await database_sync_to_async(Message.objects.create)(
            interest=interest,
            sender=user,
            text=message,
            read=False
        )

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
        }))

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.room_group_name = f'notifications_{self.user.id}'

        # Join notification group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave notification group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        pass

    async def send_notification(self, event):
        notification = event['notification']
        interest_id = event['interest_id']

        # Send notification to WebSocket
        await self.send(text_data=json.dumps({
            'notification': notification,
            'interest_id': interest_id,
        }))
