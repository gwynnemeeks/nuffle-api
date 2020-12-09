"""Players model module"""
from django.db import models

class Player(models.Model):
    """ model for Players """
    team = models.ForeignKey("Team", on_delete=models.CASCADE)
    name = models.CharField(max_length=75)
    position = models.CharField(max_length=75)
    movement = models.IntegerField()
    strength = models.IntegerField()
    agility = models.IntegerField()
    armor_value = models.IntegerField()
    skills = models.CharField(max_length=75)
    cost = models.IntegerField()
    history = models.CharField(max_length=75)