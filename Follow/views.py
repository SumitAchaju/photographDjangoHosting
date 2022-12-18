from rest_framework import viewsets,permissions
from Follow.models import Friend
from Follow.serializers import AllFriend
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from Post.serializers import PostSerializer
from Post.models import Post
from Account.models import User
from Account.serializers import UserSerializer
from django.db.models import Q

class AllFriendsViewSet(viewsets.ModelViewSet):
    queryset = Friend.objects.all().order_by('-id')
    serializer_class = AllFriend
    permission_classes = [permissions.IsAuthenticated]

@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def UserFriend(request):
    friends = Friend.objects.filter(user=request.user.id).order_by("-id")
    serializer = AllFriend(friends,many=True)
    return Response(serializer.data)

@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def FriendPosts(request):
    friends = Friend.objects.get(user=request.user.id)
    friend_id = [request.user.id]
    for friend in friends.following.all():
        friend_id.append(friend.id)
    for friend in friends.mutual.all():
        friend_id.append(friend.id)
    friend_posts = Post.objects.filter(user__in=list(friend_id)).order_by("-id")
    defaultpost= Post.objects.filter(user__id=2).order_by("-id")
    total = len(friend_posts)
    if total <= 4:
        if request.user.id==2:
            serializer=PostSerializer(friend_posts,many=True).data
        else:
            serializer=[*PostSerializer(friend_posts,many=True).data,*PostSerializer(defaultpost,many=True).data]
        total = len(serializer)
    elif int(request.query_params.get("level")) < total:
        serializer = PostSerializer(friend_posts,many=True).data[:int(request.query_params.get('level'))]
    else:
        serializer = PostSerializer(friend_posts,many=True).data[:total]

    return Response({"post":serializer,"results":total})


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def UserFollowFollowing(request,pk):
    userfriend = Friend.objects.get(user=pk)
    myfriend = Friend.objects.get(user=request.user)
    userfriendserializer = AllFriend(userfriend)
    for friend in userfriendserializer.data['followers']:
        if myfriend.following.filter(id=friend["id"]):
            friend["myfriend_status"] = True
        elif myfriend.mutual.filter(id=friend["id"]):
            friend["myfriend_status"] = True
        else:
            friend["myfriend_status"] = False
    for friend in userfriendserializer.data['following']:
        if myfriend.following.filter(id=friend["id"]):
            friend["myfriend_status"] = True
        elif myfriend.mutual.filter(id=friend["id"]):
            friend["myfriend_status"] = True
        else:
            friend["myfriend_status"] = False
    for friend in userfriendserializer.data['mutual']:
        if myfriend.following.filter(id=friend["id"]):
            friend["myfriend_status"] = True
        elif myfriend.mutual.filter(id=friend["id"]):
            friend["myfriend_status"] = True
        else:
            friend["myfriend_status"] = False


    return Response({"userfriend":userfriendserializer.data})


@api_view(["POST","GET"])
@permission_classes([permissions.IsAuthenticated])
def FriendSuggestion(request):
    if request.method == "GET":
        user = User.objects.exclude(id=request.user.id).order_by("-id")

        mutualfriend = []
        for following in Friend.objects.get(user__id=request.user.id).following.all():
            mutualfriend.append(following)
        for mutual in Friend.objects.get(user__id=request.user.id).mutual.all():
            mutualfriend.append(mutual)

        userdata =UserSerializer(user,many=True).data

        i=0
        for u in user:
            mutual= Friend.objects.get(user__id=u.id)
            for friend in mutualfriend:
                if friend.id == u.id:
                    userdata[i]["myfriend"]=True
                    break
            else:
                userdata[i]["myfriend"]=False
            for friend in mutualfriend:
                if mutual.followers.filter(id=friend.id):
                    userdata[i]["mutual_friend"]=f'{friend.first_name} {friend.last_name}'
                    break
                elif mutual.mutual.filter(id=friend.id):
                    userdata[i]["mutual_friend"]=f'{friend.first_name} {friend.last_name}'
                    break
                else:
                    userdata[i]["mutual_friend"]="no friends"
            else:
                userdata[i]["mutual_friend"]="no friends"

            userdata[i]["followers"] = len(mutual.followers.all())+len(mutual.mutual.all())
            userdata[i]["following"] = len(mutual.following.all())+len(mutual.mutual.all())
            

            i += 1
        return Response({"user":userdata})


    if request.method == "POST":
        user = User.objects.filter(name__icontains=request.data["searchname"]).order_by("-id")
        mutualfriend = []
        for following in Friend.objects.get(user__id=request.user.id).following.all():
            mutualfriend.append(following)
        for mutual in Friend.objects.get(user__id=request.user.id).mutual.all():
            mutualfriend.append(mutual)

        userdata =UserSerializer(user,many=True).data

        i=0
        for u in user:
            mutual= Friend.objects.get(user__id=u.id)
            for friend in mutualfriend:
                if friend.id == u.id:
                    userdata[i]["myfriend"]=True
                    break
            else:
                userdata[i]["myfriend"]=False

            for friend in mutualfriend:
                if mutual.followers.filter(id=friend.id):
                    userdata[i]["mutual_friend"]=f'{friend.first_name} {friend.last_name}'
                    break
                elif mutual.mutual.filter(id=friend.id):
                    userdata[i]["mutual_friend"]=f'{friend.first_name} {friend.last_name}'
                    break
                else:
                    userdata[i]["mutual_friend"]="no friends"
            else:
                userdata[i]["mutual_friend"]="no friends"

            userdata[i]["followers"] = len(mutual.followers.all())+len(mutual.mutual.all())
            userdata[i]["following"] = len(mutual.following.all())+len(mutual.mutual.all())
            

            i += 1
        return Response({"user":userdata})

@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def AddFriend(request,pk):
    myfriend = Friend.objects.get(user__id=request.user.id)
    otherfriend = Friend.objects.get(user__id=pk)
    addedfriend = User.objects.get(id=pk)
    if myfriend.followers.filter(id=pk):
        if otherfriend.following.filter(id=request.user.id):
            otherfriend.following.remove(request.user)
            otherfriend.mutual.add(request.user)
        myfriend.followers.remove(addedfriend)
        myfriend.mutual.add(addedfriend)
    else:
        myfriend.following.add(addedfriend)
        otherfriend.followers.add(request.user)
    return Response({"status":"success"})

@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def RemoveFriend(request,pk):
    myfriend = Friend.objects.get(user__id=request.user.id)
    otherfriend = Friend.objects.get(user__id=pk)
    addedfriend = User.objects.get(id=pk)
    if myfriend.following.filter(id=pk):
        otherfriend.followers.remove(request.user)
        myfriend.following.remove(addedfriend)
    else:
        myfriend.mutual.remove(addedfriend)
        otherfriend.mutual.remove(request.user)
        myfriend.followers.add(addedfriend)
        otherfriend.following.add(request.user)
    return Response({"status":"success"})

    