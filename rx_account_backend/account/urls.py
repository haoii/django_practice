from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('customers/', views.customers, name='customers'),
    path('add_customer/', views.add_customer, name='add_customer'),
    path('collect_from_customer/', views.collect_from_customer, name='collect_from_customer'),
    path('collections_from_customer/', views.collections_from_customer, name='collections_from_customer'),
]
