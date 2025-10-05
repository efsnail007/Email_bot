from django.db import models


class User(models.Model):
    tg_id = models.BigIntegerField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)


class Email(models.Model):
    email = models.EmailField(primary_key=True)
    password = models.CharField(max_length=150)
    last_uuid_seen = models.BigIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
