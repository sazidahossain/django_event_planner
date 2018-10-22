from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    organizer = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    description = models.TextField()
    date=models.DateField()
    time = models.TimeField()
    capacity = models.IntegerField()

    def __str__(self):
        return self.title

class Book(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #seats=
