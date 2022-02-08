from random import randint
from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync
from .models import Room, Message
from django.contrib.auth.models import User

class ChatConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.user = None
        self.session = None

    
    def connect(self):
        print('------------- CONNECT FUNCTION --------------------')
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.group_name = f"chat_{self.room_name}"
        # self.session = self.scope['session'].session_key

        # getting the room from the database
        self.room = Room.objects.get(name=self.room_name)
        self.user = self.scope['user']
        self.users_online = len(self.room.get_online_users())
        print('USER', self.user)
        print('CHANNEL NAME: ', self.channel_layer)
        print('SESSION', self.scope['session'].session_key)
        print('PATH', self.scope['path'])
        print(len(self.room.get_online_users()))


        # Joining room group
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

        self.accept()

        # checking if there's any user logged in
        # if self.user.is_authenticated:
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type': 'user_has_joined',
                'user': self.user.username,
            }
        )

            


    def disconnect(self, close_code):
        print('------------- DISCONNECT FUNCTION --------------------')

        # Closing the group
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

        # if there was any user logged
        # if self.user.is_authenticated:
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type': 'user_has_leaved',
                'user': self.user.username
            }
        )
            



    def receive(self, text_data):
        print('------------- RECEIVE FUNCTION --------------------')
        data = json.loads(text_data)
        message = data['message']
        print('data: ', data)
        print('msg: ', message)

        """ Creating new message """
        Message.objects.create(user=self.user, room=self.room, content=message)

        async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'user': self.user.username,
                }
            )
            
        
        

        
    


    def chat_message(self, event):
        print('------------- CHAT MESSAGE FUNCTION --------------------')
        message = event['message'].strip()
        user = event['user']
        print('EVENT ', event)
        print('MESSAGE ', message)
        print('USER ', user)

        # Sending message to WebSocket again
        self.send(text_data=json.dumps({
            'dj-message': 'this is sent by the chat message function',
            'message': message,
            'user': user,
        }))
            

    def user_has_joined(self, event):
        print('------- USER HAS JOINED FUNCTION -----------')
        print('USER WHO JOINED: ', event['user'])
        self.room.join(self.user)


    def user_has_leaved(self, event):
        print('------- USER HAS LEAVED FUNCTION -----------')
        print('USER WHO LEAVED: ', event['user'])
        self.room.leave(self.user)

    