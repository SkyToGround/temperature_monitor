import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'temperature_monitor_site.settings')
import django
django.setup()
from datetime import datetime, timedelta
from camera.models import Camera, CameraImage
import time
import pytz
import requests
from temperature_monitor_site.settings import IMAGE_STORAGE_ROOT

IMAGE_REPEAT_TIME = timedelta(seconds=60)


def main():
    while True:
        start_time = datetime.now().utcnow().replace(tzinfo=pytz.utc)
        cameras = Camera.objects.all()
        for camera in cameras:
            login_credentials = None
            if camera.user is not None and camera.password is not None and len(camera.user) > 0:
                login_credentials = (camera.user, camera.password)
            session = requests.session()
            try:
                img = requests.get(camera.image_address, auth=login_credentials, timeout=10)
            except requests.ConnectTimeout:
                continue
            except requests.ConnectionError:
                continue
            image_time = datetime.now().utcnow().replace(tzinfo=pytz.utc)
            if img.status_code != 200:
                continue
            used_path = f"camera_{camera.id}/{image_time.year}/{image_time.month:02}/{image_time.day:02}/"
            if not os.path.exists(IMAGE_STORAGE_ROOT + used_path):
                os.makedirs(IMAGE_STORAGE_ROOT + used_path)
            file_name = f"{image_time.hour:02}{image_time.minute:02}{image_time.second:02}.jpg"
            out_file = open(IMAGE_STORAGE_ROOT + used_path + file_name, "wb")
            out_file.write(img.content)
            out_file.close()
            camera.last_update = image_time
            camera.last_image = used_path + file_name
            camera.save()
            db_value = CameraImage(camera_id=camera, timestamp=image_time, image_path=used_path + file_name)
            db_value.save()
        end_time = datetime.now().utcnow().replace(tzinfo=pytz.utc)
        if end_time < start_time + IMAGE_REPEAT_TIME:
            time.sleep(((start_time + IMAGE_REPEAT_TIME) - end_time).total_seconds())


if __name__ == '__main__':
    main()
