"""League model module"""
from django.db import models

class League(models.Model):
    """ model for Leagues """
    coach = models.ForeignKey("Coach", on_delete=models.CASCADE)
    league_name = models.CharField(max_length=100)