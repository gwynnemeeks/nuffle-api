"""Team model module"""
from django.db import models

class Team(models.Model):
    """ model for Team """
    team_name = models.CharField(max_length=75)
    coach = models.ForeignKey("Coach", on_delete=models.CASCADE, related_name="teams")
    team_type = models.CharField(max_length=75)
    team_rank = models.IntegerField()
    team_value = models.IntegerField()
    team_rerolls = models.IntegerField()
    fan_factor = models.IntegerField()
    league = models.ForeignKey("League", on_delete=models.CASCADE, related_name="teams")