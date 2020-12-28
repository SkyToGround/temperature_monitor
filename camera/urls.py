from django.urls import path

from . import views

urlpatterns = [
    path('show_images/', views.show_images),
    path('get_image/<int:image_id>/', views.get_image),
]