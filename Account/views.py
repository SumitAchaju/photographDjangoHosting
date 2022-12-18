from rest_framework import viewsets,permissions
from rest_framework.response import Response
from .serializers import UserSerializer,RegisterSerializer,UpdatePassword
from .models import User
from rest_framework.decorators import api_view,permission_classes


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

from .serializers import RegisterSerializer
from rest_framework import generics


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

@api_view(["PATCH"])
@permission_classes([permissions.IsAuthenticated])
def UpdateProfile(request):
    user = User.objects.get(id=request.user.id)
    serilizer = UserSerializer(user,data=request.data,partial=True)
    if "email" in request.data:
        if User.objects.exclude(id=request.user.id).filter(email=request.data["email"]):
            return Response({"status":"email exists"})
    if "profile_image" in request.data:
        if user.profile_image != "profile/default_profile.jpg":
            user.profile_image.delete()
    if serilizer.is_valid():
        serilizer.save()
        return Response({"status":"success"})
    else:
        return Response({"status":"error"})

@api_view(["PATCH"])
@permission_classes([permissions.IsAuthenticated])
def ChangePassword(request):
    user = User.objects.get(id=request.user.id)
    if user.check_password(request.data["current_password"]):
        serilizer = UpdatePassword(user,data=request.data,partial=True)
        if serilizer.is_valid():
            user.set_password(request.data["password"])
            user.save()
            return Response({"status":"success"})
        else:
            return Response({"status":"Invalid_password"})
    else:
        return Response({"status":"wrong_current_password"})