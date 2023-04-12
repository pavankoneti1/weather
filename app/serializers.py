from rest_framework import serializers
from .models import *


class WeatherSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    location = serializers.CharField(max_length=20)
    class Meta:
        fields = "__all__"
        Model = WeatherModel



