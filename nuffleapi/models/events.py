"""EventTeam model module"""
from django.db import models

class Event(models.Model):
    """ model for Events """
    day = models.DateField(auto_now=False, auto_now_add=False)
    time = models.TimeField(auto_now=False, auto_now_add=False)
    location = models.CharField(max_length=75)
    final_score = models.CharField(max_length=75)
    event_schedule = models.CharField(max_length=100)
    coach = models.ForeignKey("Coach", on_delete=models.CASCADE)

    @property
    def rsvp(self):
        return self.__rsvp

    @rsvp.setter
    def rsvp(self, value):
        self.__rsvp = value