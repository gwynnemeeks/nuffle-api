"""EventTeam model module"""
from django.db import models

class EventTeam(models.Model):
    """ model for EventTeam """
    event = models.ForeignKey("Event", on_delete=models.CASCADE)
    team = models.ForeignKey("Team", on_delete=models.CASCADE)