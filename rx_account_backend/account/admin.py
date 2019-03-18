from django.contrib import admin

from .models import (Customer, Supplier, CollectionFromCustomer,
                     MaterialFirstClass, MaterialSecondClass, MaterialThirdClass,
                     Material, MaterialSupplierRelationship, MaterialOrder,
                     MaterialOrderDemandItem, MaterialOrderPurchaseItem, Warehouse,
                     WarehouseMaterialRelationship)

admin.site.register(Customer)
admin.site.register(Supplier)
admin.site.register(CollectionFromCustomer)
admin.site.register(MaterialFirstClass)
admin.site.register(MaterialSecondClass)
admin.site.register(MaterialThirdClass)
admin.site.register(Material)
admin.site.register(MaterialSupplierRelationship)
admin.site.register(MaterialOrder)
admin.site.register(MaterialOrderDemandItem)
admin.site.register(MaterialOrderPurchaseItem)
admin.site.register(Warehouse)
admin.site.register(WarehouseMaterialRelationship)
