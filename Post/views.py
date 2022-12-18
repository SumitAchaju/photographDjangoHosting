from rest_framework import permissions,viewsets
from .serializers import PostSerializer,CategorySerializer
from .models import Post,Category,Comment,PostImage
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from Account.models import User
from datetime import datetime,timezone
from Follow.models import Friend

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by("-id")
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def PostCategory(request,pk):
    if int(pk) == 1:
        posts = Post.objects.all().order_by("-id")
    else:
        posts = Post.objects.filter(category=pk).order_by("-id")
    total = len(posts)
    if int(request.query_params.get("level")) < total:
        serializer = PostSerializer(posts,many=True).data[:int(request.query_params.get('level'))]
    else:
        serializer = PostSerializer(posts,many=True).data[:total]

    return Response({"post":serializer,"results":total})

@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def SinglePost(request,pk):
    if request.method == "GET":
        post = Post.objects.get(id=pk)
        serializer = PostSerializer(post,many=False)
        return Response(serializer.data)

@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def AddComment(request,pk):
    if request.method == "POST":
        post = Post.objects.get(id=pk)
        data = request.data
        user = User.objects.get(id=int(data["userid"]))
        comment = data["comment"]
        new_comment = Comment(comment_by=user,comment=comment)
        new_comment.save()
        post.comment.add(new_comment)
        post.save()
        return Response(PostSerializer(post).data)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def DeleteComment(request,pk):
    if request.method == "POST":
        comment = Comment.objects.get(id=pk)
        comment.delete()
        post = Post.objects.get(id=request.data["postid"])
        return Response(PostSerializer(post).data)


@api_view(["GET","POST"])
@permission_classes([permissions.IsAuthenticated])
def PostLikes(request,pk):
    if request.method == "GET":
        post = Post.objects.get(id=pk)
        post.like_by.add(request.user)
        post.save()
        return Response(PostSerializer(post).data)
    if request.method == "POST":
        post = Post.objects.get(id=pk)
        post.like_by.remove(request.user)
        post.save()
        return Response(PostSerializer(post).data)

@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def PostLikesOut(request,pk):
    if request.data["action"] == "like":
        post = Post.objects.get(id=pk)
        post.like_by.add(request.user)
        post.save()
        return Response({"status":"success"})
    elif request.data["action"] == "unlike":
        post = Post.objects.get(id=pk)
        post.like_by.remove(request.user)
        post.save()
        return Response({"status":"success"})
    elif request.data["action"] == "save":
        post = Post.objects.get(id=pk)
        post.saved_by.add(request.user)
        post.save()
        return Response({"status":"success"})
    elif request.data["action"] == "unsave":
        post = Post.objects.get(id=pk)
        post.saved_by.remove(request.user)
        post.save()
        return Response({"status":"success"})


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def UserPost(request,pk):
    posts= Post.objects.filter(user__id=pk).order_by("-id")
    total = len(posts)
    if int(request.query_params.get("level")) < total:
        serializer = PostSerializer(posts,many=True).data[:int(request.query_params.get('level'))]
    else:
        serializer = PostSerializer(posts,many=True).data[:total]

    return Response({"post":serializer,"results":total})

@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def UploadPost(request):
    uploadedpost = Post(user=request.user,caption=request.data["discription"],post_date=datetime.now().replace(tzinfo=timezone.utc))
    uploadedpost.save()
    category = request.data.getlist("category[]")
    if "1" in category:
        for cat in category:
            uploadedpost.category.add(Category.objects.get(id=int(cat)))
    else:
        for cat in category:
            uploadedpost.category.add(Category.objects.get(id=int(cat)))
        uploadedpost.category.add(Category.objects.get(id=1))
    for image in (request.FILES.getlist("images[]")):
        postimage = PostImage(image=image)
        postimage.save()
        uploadedpost.postimage.add(postimage)
    return Response({"status":"success","postid":uploadedpost.id})

@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def UpdatePost(request,pk):
    post = Post.objects.get(id=pk)
    if post.user.id==request.user.id:
        post.caption=request.data["discription"]
        post.save()
        category = request.data["category"]
        if "1" in category:
            for cat in category:
                post.category.add(Category.objects.get(id=int(cat)))
        else:
            for cat in category:
                post.category.add(Category.objects.get(id=int(cat)))
                post.category.add(Category.objects.get(id=1))
        return Response({"status":"success","postid":post.id})
    else:
        return Response({"status":"invalid"})

@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def DeletePost(request,pk):
    post = Post.objects.get(id=pk)
    if post.user.id==request.user.id:
        postdelete = Post.objects.get(id=pk)
        if postdelete.postimage:
            for post in postdelete.postimage.all():
                post.image.delete()
                post.delete()
        if postdelete.comment:
            for com in postdelete.comment.all():
                com.delete()
        postdelete.delete()
        return Response({"status":"success"})
    else:
        return Response({"status":"invalid"})

@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def PostSaved(request):
    posts = Post.objects.filter(saved_by=request.user)
    total = len(posts)
    if int(request.query_params.get("level")) < total:
        serializer = PostSerializer(posts,many=True).data[:int(request.query_params.get('level'))]
    else:
        serializer = PostSerializer(posts,many=True).data[:total]

    return Response({"post":serializer,"results":total})
