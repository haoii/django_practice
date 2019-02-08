from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('submit_post/', views.submit_post, name='submit_post'),
]
