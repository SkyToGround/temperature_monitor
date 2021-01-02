from django.shortcuts import render, loader, HttpResponse
from django.views.decorators.cache import never_cache
from camera.models import Camera, CameraImage
from temperature_monitor_site.settings import IMAGE_STORAGE_ROOT
from datetime import datetime, timedelta
from django.core.exceptions import FieldError
import pytz
import tzlocal
import json


@never_cache
def show_images(request):
    index_page_template = loader.get_template("show_images.html")
    all_cameras = Camera.objects.all()
    now = datetime.now().utcnow().replace(tzinfo=pytz.utc)
    local_TZ = tzlocal.get_localzone()
    ret_dict = {"cameras": all_cameras, "now":now.astimezone(local_TZ).strftime("%Y-%m-%d, %H:%M:%S")}
    return HttpResponse(index_page_template.render(ret_dict), content_type="text/html")


def get_image(request, image_id):
    current_image_entry = CameraImage.objects.filter(id=image_id).get()
    in_file = open(IMAGE_STORAGE_ROOT + current_image_entry.image_path, "rb")
    image_data = in_file.read()
    in_file.close()
    return HttpResponse(content=image_data, content_type="image/jpeg")


def get_image_id(request, camera_id: int, timestamp: int):
    used_timestamp = datetime.fromtimestamp(timestamp, pytz.utc)
    return HttpResponse(content=str(get_image_id_with_timestamp(camera_id, used_timestamp)), content_type="text/text")


def get_image_id_with_timestamp(camera_id: int, timestamp: datetime):
    camera_images = CameraImage.objects.filter(camera_id=camera_id)
    greater = camera_images.filter(timestamp__gte=timestamp).order_by("timestamp").first()
    less = camera_images.filter(timestamp__lte=timestamp).order_by("-timestamp").first()
    if greater and less:
        used_image = greater if greater.timestamp - timestamp < timestamp - less.timestamp else less
    else:
        used_image = greater or less
    return used_image.id


def get_next_image_id(image_id):
    current_image_entry = CameraImage.objects.filter(id=image_id).get()
    try:
        next_image = CameraImage.objects.filter(camera_id=current_image_entry.camera_id, id_gt=current_image_entry.id).order_by("timestamp").first()
    except FieldError:
        return current_image_entry.id
    if not next_image:
        return current_image_entry.id
    return next_image.id


def get_previous_image_id(image_id):
    current_image_entry = CameraImage.objects.filter(id=image_id).get()
    try:
        previous_image = CameraImage.objects.filter(camera_id=current_image_entry.camera_id, id_lt=current_image_entry.id).order_by("-timestamp").first()
    except FieldError:
        return current_image_entry.id
    if not previous_image:
        return current_image_entry.id
    return previous_image.id


def get_next_image_id_with_offset(image_id: int, time_offset: timedelta):
    current_image_entry = CameraImage.objects.filter(id=image_id).get()
    next_id = get_image_id_with_timestamp(camera_id=current_image_entry.camera_id, timestamp=current_image_entry.timestamp + time_offset)
    if next_id != current_image_entry.id:
        return next_id
    if time_offset >= timedelta(seconds=0):
        return get_next_image_id(image_id)
    return get_previous_image_id(image_id)


def get_offset_image_id(request, image_id: str, offset: str):
    return HttpResponse(content=str(get_next_image_id_with_offset(int(image_id), timedelta(seconds=int(offset)))), content_type="text/json")


def get_timestamp(request, image_id):
    current_image_entry = CameraImage.objects.filter(id=image_id).get()
    local_TZ = tzlocal.get_localzone()
    json_data = {"timestamp": int(current_image_entry.timestamp.timestamp()), "datetime_string":current_image_entry.timestamp.astimezone(local_TZ).strftime("%Y-%m-%d, %H:%M:%S")}
    return HttpResponse(content=json.dumps(json_data), content_type="text/json")
