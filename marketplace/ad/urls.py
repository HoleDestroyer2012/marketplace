from django.urls import path
from . import views

urlpatterns = [
    path('ad/add/', views.add_ad, name='add_ad'),
    path('ad/<str:pk>/', views.get_ad, name='get_ad'),
    path('ads/', views.get_all_ads, name='get_all_ads'),
    path('upload_ad_images/', views.upload_ad_images, name='upload_ad_images'),
    path('update_ad/<str:pk>/', views.update_ad, name='update_ad'),
]