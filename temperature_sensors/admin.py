from django.contrib import admin
from temperature_sensors.models import TemperatureSensor, Temperatures, TemperatureSensorGroup


@admin.register(TemperatureSensor)
class UnitAdmin(admin.ModelAdmin):
    list_display = ("long_name", "short_name", "address", "has_power", "last_update", "value")


@admin.register(Temperatures)
class UnitAdmin(admin.ModelAdmin):
    list_display = ("value", "timestamp", "sensor")


@admin.register(TemperatureSensorGroup)
class UnitAdmin(admin.ModelAdmin):
    list_display = ("name", "order")

