from django.urls import path, re_path

from . import views

urlpatterns = [
    path('show_images/', views.show_images),
    path('get_image/<int:image_id>/', views.get_image),
    path('get_timestamp/<int:image_id>/', views.get_timestamp),
    path('get_image_id/<int:camera_id>/<int:timestamp>/', views.get_image_id),
    re_path(r'^get_offset_image_id/(?P<image_id>[0-9]+)/(?P<offset>-?[0-9]+)/$', views.get_offset_image_id),
]