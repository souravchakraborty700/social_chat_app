# consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import Message, Interest
from channels.db import database_sync_to_async
import logging

logger = logging.getLogger(__name__)

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.interest_id = self.scope['url_route']['kwargs']['interest_id']
        self.room_group_name = f'chat_{self.interest_id}'

        logger.info(f"Connecting to WebSocket room: {self.room_group_name}")

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        logger.info(f"Disconnecting from WebSocket room: {self.room_group_name}")

        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        logger.info(f"WebSocket message received: {text_data}")
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

        logger.info(f"Broadcasting WebSocket message: {message} from {username}")

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
        }))
