from django.db import models


class Camera(models.Model):
    name = models.CharField("Name of camera", max_length=40)
    image_address = models.CharField("Address of image to collect", max_length=200, unique=True)
    user = models.CharField("User name for camera", max_length=40, null=True)
    password = models.CharField("Password for camera", max_length=40, null=True)
    last_update = models.DateTimeField("Timestamp of the last image", default=None, null=True)
    last_image = models.CharField("(Partial) path to current image.", max_length=200)

    def __str__(self):
        return self.name


class CameraImage(models.Model):
    camera_id = models.ForeignKey(to=Camera, on_delete=models.SET_NULL, null=True, db_index=True)
    timestamp = models.DateTimeField("Timestamp of the image", default=None, null=True, db_index=True)
    image_path = models.CharField("(Partial) path to image", max_length=200)
