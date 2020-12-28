from django.contrib import admin
from camera.models import CameraImage, Camera


@admin.register(Camera)
class UnitAdmin(admin.ModelAdmin):
    list_display = ("name", "image_address", "last_update", "last_image", "user", "password")


@admin.register(CameraImage)
class UnitAdmin(admin.ModelAdmin):
    list_display = ("camera_id", "timestamp", "image_path")
