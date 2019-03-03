from django.contrib import admin

from .models import Customer, Supplier, CollectionFromCustomer

admin.site.register(Customer)
admin.site.register(Supplier)
admin.site.register(CollectionFromCustomer)
