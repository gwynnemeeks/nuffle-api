"""EventNote model module"""
from django.db import models

class EventNote(models.Model):
    """ model for EventTeam """
    event = models.ForeignKey("Event", on_delete=models.CASCADE)
    notes = models.CharField(max_length=300)