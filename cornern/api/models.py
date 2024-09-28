from __future__ import annotations

import base64
from uuid import uuid4
from zoneinfo import ZoneInfo

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Corner(models.Model):
    class Meta:
        verbose_name = _("Corner")
        verbose_name_plural = _("Corners")

    name = models.CharField(max_length=100)
    description = models.TextField(verbose_name="Beschreibung", null=True, blank=True)
    lat = models.DecimalField(verbose_name="Breitengrad", max_digits=20, decimal_places=18, null=True)
    lon = models.DecimalField(verbose_name="Längengrad", max_digits=20, decimal_places=18, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def _get_last_masurement(self):
        return MeasurementService.get_service().get_intervall(self, 1, "5min", 1)

    @property
    def score(self):
        m = self._get_last_masurement()
        if m:
            return m[0].get("value", 40)
        return 40

    @property
    def price_factor(self):
        m = self._get_last_masurement()
        if m:
            return m[0].get("price_factor", 1)
        return 1


class Sensor(models.Model):
    class Meta:
        verbose_name = _("Sensor")
        verbose_name_plural = _("Sensoren")

    name = models.CharField(max_length=100)
    corner = models.ForeignKey(Corner, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def secret(self):
        return f"Basic {base64.b64encode(f"{self.name}:{self.token}".encode()).decode("utf-8")}"


class Measurement(models.Model):
    class Meta:
        verbose_name = _("Messung")
        verbose_name_plural = _("Messungen")

    value = models.IntegerField(verbose_name="Wert (dBA)")
    prediction = models.FloatField(verbose_name="Vorhersage")
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.timestamp} - Wert: {self.value} dBA"

    @property
    def timestamp(self):
        return self.created_at.astimezone(ZoneInfo("CET")).strftime("%d.%m.%Y %H:%M:%S")


class Feedback(models.Model):
    class Meta:
        verbose_name = _("Feedback")
        verbose_name_plural = _("Feedbacks")

    class LoudnessType(models.TextChoices):
        VERYLOUD = "Sehr laut", _("Sehr laut")
        LOUD = "Laut", _("Laut")
        NEUTRAL = "neutral", _("Neutral")
        QUIET = "leise", _("Leise")
        VERYQUIET = "Sehr leise", _("Sehr leise")

    subject = models.CharField(verbose_name="Thema", max_length=100)
    message = models.TextField(verbose_name="Nachricht")
    corner = models.ForeignKey(Corner, on_delete=models.CASCADE)
    loudness = models.CharField(verbose_name="Lautstärke", choices=LoudnessType)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.timestamp} - Thema: {self.subject}"

    @property
    def timestamp(self):
        return self.created_at.astimezone(ZoneInfo("CET")).strftime("%d.%m.%Y %H:%M:%S")


from .service import MeasurementService  # noqa
