from django.shortcuts import render, loader, HttpResponse
from django.views.decorators.cache import never_cache
from camera.models import Camera, CameraImage
from temperature_monitor_site.settings import IMAGE_STORAGE_ROOT
from datetime import datetime
import pytz
import tzlocal


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
