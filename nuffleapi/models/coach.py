"""Coach model module"""

from django.db import models
from django.contrib.auth.models import User

class Coach(models.Model):
    """model for the user as coach"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=50)
    leageAdmin = models.BooleanField()