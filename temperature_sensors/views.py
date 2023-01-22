from django.template import Context, loader, RequestContext
from django.http import HttpResponse
from django.views.decorators.cache import never_cache

from temperature_sensors.models import TemperatureSensor, TemperatureSensorGroup
import json
import pytz
import tzlocal


@never_cache
def list_sensors(request):
    index_page_template = loader.get_template("list_sensors.html")
    ret_dict = {"groups": [], "loc_list": True}
    all_groups = TemperatureSensorGroup.objects.order_by("order")
    for g in all_groups:
        grouped_sensors = TemperatureSensor.objects.filter(group=g)
        ret_dict["groups"].append({"groupname": g.name, "sensors":grouped_sensors})
    ungrouped_sensors = TemperatureSensor.objects.filter(group=0)
    ret_dict["groups"].append({"groupname": "Övriga", "sensors": ungrouped_sensors})

    return HttpResponse(index_page_template.render(ret_dict), content_type="text/html")


@never_cache
def sensor_values(request):
    all_sensors = TemperatureSensor.objects.all()
    sensor_dict = {}
    local_TZ = tzlocal.get_localzone()
    for CurrentSensor in all_sensors:
        sensor_dict[CurrentSensor.short_name] = {"value": CurrentSensor.temperature, "id": CurrentSensor.id, "timestamp": CurrentSensor.last_update.replace(tzinfo=pytz.utc).astimezone(local_TZ).strftime("%Y-%m-%d %H:%M:%S")}
    ret_str = json.dumps(sensor_dict)
    return HttpResponse(ret_str, content_type="text/text")
