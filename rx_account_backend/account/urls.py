from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('customers/', views.customers, name='customers'),
    path('suppliers/', views.suppliers, name='suppliers'),
    path('material_classes/', views.material_classes, name='material_classes'),
    path('materials/', views.materials, name='materials'),

    path('warehouses/', views.warehouses, name='warehouses'),
    path('warehouse_materials/', views.warehouse_materials, name='warehouse_materials'),

    path('material_orders/', views.material_orders, name='material_orders'),

    path('supplier_detail/<str:supplier_id>/', views.supplier_detail, name='supplier_detail'),
    path('suppliers_by_material/<str:material_name>/', views.suppliers_by_material, name='suppliers_by_material'),

    path('add_customer/', views.add_customer, name='add_customer'),
    path('add_supplier/', views.add_supplier, name='add_supplier'),

    path('add_material_order/', views.add_material_order, name='add_material_order'),

    path('collect_from_customer/', views.collect_from_customer, name='collect_from_customer'),
    path('collections_from_customer/', views.collections_from_customer, name='collections_from_customer'),

]
