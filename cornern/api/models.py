from uuid import uuid4

from django.contrib.auth.models import User
from django.db import models


class Corner(models.Model):  # Coor, score
    name = models.CharField(max_length=100)
    description = models.TextField()
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    lon = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Sensor(models.Model):
    name = models.CharField(max_length=100)
    corner = models.ForeignKey(Corner, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Measurement(models.Model):
    value = models.IntegerField()
    prediction = models.FloatField()
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Value: {self.value} - prediction: {self.prediction}"


class Feedback(models.Model):
    class LoudnessType(models.TextChoices):
        VERYLOUD = "Sehr laut"
        LOUD = "Laut"
        NEUTRAL = "neutral"
        QUIET = "leise"
        VERYQUIET = "Sehr leise"

    subject = models.CharField(max_length=100)
    message = models.TextField()
    corner = models.ForeignKey(Corner, on_delete=models.CASCADE)
    loudness = models.CharField(choices=LoudnessType)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject
