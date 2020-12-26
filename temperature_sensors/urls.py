from django.urls import path

from . import views

urlpatterns = [
    path('list_sensors/', views.list_sensors),
    path('sensor_values/', views.sensor_values),
]
