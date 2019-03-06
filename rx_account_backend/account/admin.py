from django.contrib import admin

from .models import (Customer, Supplier, CollectionFromCustomer,
                     MaterialFirstClass, MaterialSecondClass, MaterialThirdClass,
                     Material, MaterialSupplierRelationship)

admin.site.register(Customer)
admin.site.register(Supplier)
admin.site.register(CollectionFromCustomer)
admin.site.register(MaterialFirstClass)
admin.site.register(MaterialSecondClass)
admin.site.register(MaterialThirdClass)
admin.site.register(Material)
admin.site.register(MaterialSupplierRelationship)
