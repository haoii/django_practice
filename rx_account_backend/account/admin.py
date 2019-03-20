from django.contrib import admin

from .models import (Customer, Supplier, CollectionFromCustomer,
                     MaterialFirstClass, MaterialSecondClass, MaterialThirdClass,
                     Material, MaterialSupplierRelationship, MaterialOrder,
                     MaterialOrderDemandItem, MaterialOrderPurchaseItem, Warehouse,
                     WarehouseMaterialRelationship, MaterialInOrderRelationship,
                     WarehouseInMaterialInOrderRelationship, SupplierInMaterialInOrderRelationship,
                     CustomerInOrderRelationship, MaterialInCustomerInOrderRelationship,
                     WarehouseInOrderRelationship, SupplierInOrderRelationship,
                     MaterialInWarehouseInOrderRelationship, MaterialInSupplierInOrderRelationship)

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

admin.site.register(MaterialInOrderRelationship)
admin.site.register(WarehouseInMaterialInOrderRelationship)
admin.site.register(SupplierInMaterialInOrderRelationship)
admin.site.register(CustomerInOrderRelationship)
admin.site.register(MaterialInCustomerInOrderRelationship)
admin.site.register(WarehouseInOrderRelationship)
admin.site.register(SupplierInOrderRelationship)
admin.site.register(MaterialInWarehouseInOrderRelationship)
admin.site.register(MaterialInSupplierInOrderRelationship)

