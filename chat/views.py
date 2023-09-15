from .models import Message
from Account.models import User
from .serializers import MessageSerializer
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from rest_framework.response import Response
from Follow.models import Friend
from Account.serializers import UserSerializer
from rest_framework.decorators import api_view,permission_classes
from channels.layers import get_channel_layer
from channels.consumer import async_to_sync


class ChatMessage(ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        friend_id = self.kwargs["friend_id"]
        friend_user = User.objects.get(id=friend_id)
        query = Message.objects.filter(
            Q(Q(send_user=self.request.user) & Q(receive_user=friend_user))
            | Q(Q(send_user=friend_user) & Q(receive_user=self.request.user))
        ).order_by("send_date")
        return query
    
    def list(self, request, *args, **kwargs):
        messages = self.get_queryset()
        for msg in messages:
            if msg.send_user.id != request.user.id:
                msg.msg_status = 'seen'
                msg.save()
                channel = get_channel_layer()
                async_to_sync(channel.group_send)(f'chat_{self.kwargs["friend_id"]}',{
                "type": "message.seen",
                'msg_id':msg.id,
                'seen':True
                })
                async_to_sync(channel.group_send)(f'chat_{request.user.id}',{
                "type": "message.seen",
                'msg_id':msg.id,
                'seen':True
                })
        serializer = self.get_serializer(messages,many=True)
        return Response(serializer.data)


class LatestMessage(ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        query = Message.objects.filter(
            Q(receive_user=user) | Q(send_user=user)
        ).order_by("send_date")
        return query

    def list(self, request, *args, **kwargs):
        messages = self.get_queryset()
        unique_latest_message = {}
        for message in messages:
            if (
                message.send_user.id == request.user.id
                and message.receive_user.id not in unique_latest_message
            ):
                unique_latest_message[f"{message.receive_user.id}"] = message
            elif message.send_user.id not in unique_latest_message:
                unique_latest_message[f"{message.send_user.id}"] = message
        latest_message = list(unique_latest_message.values())

        my_friend = Friend.objects.get(id=request.user.id)
        new_friend = []
        for friend in my_friend.mutual.all():
            if str(friend.id) not in unique_latest_message:
                new_friend.append(friend)
        for friend in my_friend.following.all():
            if str(friend.id) not in unique_latest_message:
                new_friend.append(friend)
        new_friend_serializer = UserSerializer(new_friend, many=True)
        serializer = self.get_serializer(latest_message, many=True)
        return Response(
            {"latest_message": serializer.data, "friend": new_friend_serializer.data}
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def msg_seen(request,msg_id):
    message = Message.objects.get(id=msg_id)
    message.msg_status = 'seen'
    message.save()
    message_serializer = MessageSerializer(message,many=False)
    return Response(message_serializer.data)

class UnSeenMsg(ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        query = Message.objects.filter(
            Q(receive_user = user) & Q(Q(msg_status='delivered') | Q(msg_status='sent')) 
        ).order_by("send_date")
        return query
    
    def list(self, request, *args, **kwargs):
        message = self.get_queryset()
        unique_latest_message = {}
        for msg in message:
            if msg.send_user.id not in unique_latest_message:
                unique_latest_message[f'{msg.send_user.id}'] = msg

        unique_message = list(unique_latest_message.values())

        msg_serializer = MessageSerializer(unique_message,many=True)

        return Response(msg_serializer.data)