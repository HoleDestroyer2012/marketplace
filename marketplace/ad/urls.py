from django.urls import path
from . import views

urlpatterns = [
    path('ad/add/', views.add_ad, name='add_ad')
]