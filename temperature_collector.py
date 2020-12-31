from datetime import datetime
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'temperature_monitor_site.settings')
import django
django.setup()
import glob
from datetime import datetime, timedelta
from temperature_sensors.models import TemperatureSensor, Temperatures
import time
import pytz

SENSOR_ROOT = "/run/owfs/"
SENSOR_REPEAT_TIME = timedelta(seconds=60)


def main():
    while True:
        start_time = datetime.now().utcnow().replace(tzinfo=pytz.utc)
        known_sensors = glob.glob(SENSOR_ROOT + "/28.*")
        for sensor in known_sensors:
            address = sensor[sensor.rfind("/") + 1:]
            try:
                TemperatureSensor.objects.all().get(address=address)
            except TemperatureSensor.DoesNotExist:
                new_sensor = TemperatureSensor(address=address)
                new_sensor.save()
                new_sensor.long_name = f"Long name {new_sensor.id}"
                new_sensor.short_name = f"short_name_{new_sensor.id}"
                new_sensor.save()
            sensor_with_address = TemperatureSensor.objects.all().get(address=address)
            try:
                with open(f"{sensor}/temperature", 'r') as f:
                    new_value = float(f.read())
                with open(f"{sensor}/power", 'r') as f:
                    is_powered = bool(int(f.read()))
                current_ts = datetime.now().utcnow().replace(tzinfo=pytz.utc)
                db_value = Temperatures(value=new_value, timestamp=current_ts, sensor=sensor_with_address)
                db_value.save()
                sensor_with_address.has_power = is_powered
                sensor_with_address.value = new_value
                sensor_with_address.last_update = current_ts
                sensor_with_address.save()
            except OSError:
                pass
        end_time = datetime.now().utcnow().replace(tzinfo=pytz.utc)
        if end_time < start_time + SENSOR_REPEAT_TIME:
            time.sleep(((start_time + SENSOR_REPEAT_TIME) - end_time).total_seconds())


if __name__ == '__main__':
    main()
