from django.db import models


class TemperatureSensor(models.Model):
    long_name = models.CharField("Displayed name of temperature sensor", max_length=40)
    short_name = models.CharField("Short hand for temperature sensor", max_length=40)
    address = models.CharField("1-wire address of temperature sensor.", max_length=30, unique=True)
    has_power = models.BooleanField("Is power supplied via the power pin?", default=False)
    last_update = models.DateTimeField("Timestamp of the last value", default=None, null=True)
    value = models.FloatField("The current (last) temperature in degrees C.", default=-200)

    def __str__(self):
        return f"{self.long_name}: {self.value:.2f}℃"


class Temperatures(models.Model):
    value = models.FloatField("Temperature in degrees C.")
    timestamp = models.DateTimeField("Timestamp of temperature value", db_index=True)
    sensor = models.ForeignKey(to=TemperatureSensor, on_delete=models.SET_NULL, null=True, db_index=True)
