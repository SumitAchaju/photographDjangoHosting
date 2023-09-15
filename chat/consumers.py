import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message
from django.shortcuts import get_object_or_404
from Account.models import User
from .serializers import MessageSerializer

connected_user = {}

class ChatMessage(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name
        user = self.scope['user']
        if user.is_authenticated:
            if self.room_group_name in connected_user:
                connected_user[self.room_group_name].append(user)
            else:
                connected_user[self.room_group_name] = [user]

            # Join room group
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)

            await self.accept()

            await self.change_active_status(user,True)

    async def disconnect(self, close_code):
        # Leave room group
        user = self.scope.get('user')
        if user.is_authenticated:
            if self.room_group_name in connected_user:
                connected_user[self.room_group_name].pop()
            else:
                del connected_user[self.room_group_name]
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
            await self.change_active_status(user,False)

    # Receive message from WebSocket
    async def receive(self, text_data):
        print(text_data)
        text_data_json = json.loads(text_data)
        if "seen" in text_data_json:
            await self.msg_seen(text_data_json['msgId'])
            await self.channel_layer.group_send(
            self.room_group_name,{
                "type": "message.seen",
                'msg_id':text_data_json['msgId'],
                'seen':True
            })
            return

        message_text = text_data_json["message"]
        sender_id = text_data_json["senderId"]

        user = await self.find_user(sender_id)
        if user['sender'] == user['reciever']:
            return
        message = await self.create_message(message_text,user["sender"],user["reciever"])

        if len(connected_user[self.room_group_name])==2:
            await self.msg_delivered(message)

        # Send message to room group
        message_serializer = MessageSerializer(message,many=False).data
        await self.channel_layer.group_send(
            self.room_group_name, { "type": "chat.message",
                                    "id":message_serializer['id'],
                                    "send_user":message_serializer["send_user"] ,
                                    "message_text": message_serializer["message_text"],
                                    "message_img": message_serializer["message_img"],
                                    "message_type": message_serializer["message_type"],
                                    "msg_status": message_serializer["msg_status"],
                                    "receive_user" : message_serializer["receive_user"],
                                    "send_date" : message_serializer["send_date"],
                                    "formated_date":message_serializer['formated_date']})

    # Receive message from room group
    async def chat_message(self, event): 
        id = event["id"]
        message_text = event["message_text"]
        send_user = event['send_user']
        message_img = event['message_img']
        message_type = event['message_type']
        msg_status = event['msg_status']
        receive_user = event['receive_user']
        send_date = event['send_date']
        formated_date = event['formated_date']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({ 
                                    "id":id,
                                    "send_user": send_user ,
                                    "message_text": message_text,
                                    "message_img": message_img,
                                    "message_type": message_type,
                                    "msg_status": msg_status,
                                    "receive_user" : receive_user,
                                    "send_date" : send_date,
                                    "formated_date":formated_date}))
        
    async def message_seen(self, event):
        await self.send(text_data=json.dumps({ 
                "msgId":event['msg_id'],
                "seen":event['seen']}))

    @database_sync_to_async
    def find_user(self,sender_id):
        sender = get_object_or_404(User,id=sender_id)
        reciever = get_object_or_404(User,id=self.room_name)

        return {
            "sender":sender,
            "reciever":reciever
        }
    
    @database_sync_to_async
    def create_message(self,message,sender,reciever):
        message = Message(message_text=message,
                                         send_user=sender,
                                         receive_user=reciever)
        message.save()
        return message
    
    @database_sync_to_async
    def msg_delivered(self,message):
        message.msg_status = 'delivered'
        message.save()

    @database_sync_to_async
    def msg_seen(self,msg_id):
        message = Message.objects.get(id=msg_id)
        message.msg_status = 'seen'
        message.save()

    @database_sync_to_async
    def change_active_status(self,user,status):
        user.active_status = status
        user.save()

