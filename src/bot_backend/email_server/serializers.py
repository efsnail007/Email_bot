from rest_framework import serializers

from .models import Email, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = User


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        extra_kwargs = {"password": {"write_only": True}}
        model = Email
