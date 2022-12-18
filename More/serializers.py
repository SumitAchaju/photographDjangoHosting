from rest_framework import serializers
from .models import ImprovementSuggestions,FeedBack

class ImprovementSuggestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImprovementSuggestions
        fields = "__all__"

class FeedBackSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedBack
        fields = "__all__"