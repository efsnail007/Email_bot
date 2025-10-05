from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .apps import EmailServerConfig
from .email_reader import EmailReader
from .models import Email, User
from .serializers import EmailSerializer, UserSerializer
from .utils.email_client import ImapClient
from .utils.fernet import encode_password


class UserAPI(APIView):
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailAPI(APIView):
    def get(self, request, tg_id, format=None):
        user = get_object_or_404(User, pk=tg_id)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class EmailAPI(APIView):
    def get(self, request, tg_id, format=None):
        user = get_object_or_404(User, pk=tg_id)
        emails = Email.objects.filter(user=user)
        serializer = EmailSerializer(emails, many=True)
        return Response(serializer.data)

    def post(self, request, tg_id, format=None):
        user = get_object_or_404(User, pk=tg_id)
        email = request.data["email"]
        last_uuid_seen = EmailReader(
            ImapClient, email, request.data["password"]
        ).get_last_uuid_email()
        password = encode_password(EmailServerConfig.fernet, request.data["password"])
        data_serializer = {
            "email": email,
            "password": password,
            "last_uuid_seen": last_uuid_seen,
            "user": user.tg_id,
        }
        serializer = EmailSerializer(data=data_serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailDetailAPI(APIView):
    def get(self, request, tg_id, pk, format=None):
        email = get_object_or_404(Email, user__tg_id=tg_id, pk=pk)
        serializer = EmailSerializer(email)
        return Response(serializer.data)

    def delete(self, request, tg_id, pk, format=None):
        email = get_object_or_404(Email, user__tg_id=tg_id, pk=pk)
        email.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
