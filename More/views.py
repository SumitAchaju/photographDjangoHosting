from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import permissions
from datetime import datetime,timezone
from .models import ImprovementSuggestions,FeedBack


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def ImproveSugg(request):
    data = ImprovementSuggestions(user=request.user,suggestion=request.data["sugg"],date=datetime.now().replace(tzinfo=timezone.utc))
    data.save()
    return Response({"status":"success"})

@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def Feedback(request):
    data = FeedBack(user=request.user,feedback=request.data["feedback"],date=datetime.now().replace(tzinfo=timezone.utc))
    data.save()
    return Response({"status":"success"})