from django.urls import path
from . import views

urlpatterns = [
    path('comment/create/', views.create_comment, name='create_comment'),
    path('comment/get/<int:comment_pk>/',
         views.get_comment, name='get_comment'),
    path('comment/update/<int:comment_pk>/',
         views.update_comment, name='update_comment'),
    path('comment/upload_images/<int:comment_pk>/',
         views.upload_images, name='upload_images'),
]
