# portal/serializers.py
from rest_framework import serializers
from post_management.models import NewsPost

class NewsPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsPost
        fields = "__all__"
