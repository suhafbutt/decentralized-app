from django.db import models

class User(models.Model):
  storage_url = models.TextField(unique=True)

class Song(models.Model):
  name = models.TextField()
  link = models.TextField(unique=True)
  thumbnail = models.TextField()
  is_trusted = models.BooleanField(default=True)
  artist = models.ForeignKey("User", on_delete=models.SET_NULL, null=True)
