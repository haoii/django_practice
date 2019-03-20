import datetime
import json

from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.template import loader
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F, Sum

from .models import (Customer, Supplier, CollectionFromCustomer,
                     MaterialFirstClass, MaterialSecondClass, MaterialThirdClass,
                     Material, MaterialSupplierRelationship, MaterialOrder,
                     MaterialOrderDemandItem, MaterialOrderPurchaseItem, Warehouse,
                     WarehouseMaterialRelationship, MaterialInOrderRelationship,
                     WarehouseInMaterialInOrderRelationship, SupplierInMaterialInOrderRelationship,
                     CustomerInOrderRelationship, MaterialInCustomerInOrderRelationship,
                     WarehouseInOrderRelationship, SupplierInOrderRelationship,
                     MaterialInWarehouseInOrderRelationship, MaterialInSupplierInOrderRelationship)


def index(request):
    return HttpResponse('helloo')


def customers(request):
    def customer_to_dict(customer):
        elapsed_time = timezone.now().date() - customer.sign_date
        remained_duration = customer.duration - elapsed_time.days

        return {
            'name': customer.name,
            'address': customer.address,
            'sign_date': customer.sign_date,
            'duration': customer.duration,
            'remained_duration': remained_duration,
            'phone': customer.phone,

            'area': customer.area,
            'total_price': customer.total_price,
            'price_discount': customer.price_discount,
            'price_received': customer.price_received,
            # 'total_expense': customers_total_expense[customer.address] if customer.address in customers_total_expense else 0,
            # 'expense_paid': customers_expense_paid[customer.address] if customer.address in customers_expense_paid else 0,
            'total_expense': 0,
            'price_received': 0,
        }

    # total_expense = MaterialOrderItem.objects.values('customer__address').annotate(
    #     total=Sum(F('price') * F('quantity')))
    # customers_total_expense = {}
    # for i in total_expense:
    #     customers_total_expense[i['customer__address']] = i['total']
    #
    # expense_paid = MaterialOrderItem.objects.filter(is_paid__exact=True).values('customer__address').annotate(
    #     total=Sum(F('price') * F('quantity')))
    # customers_expense_paid = {}
    # for i in expense_paid:
    #     customers_expense_paid[i['customer__address']] = i['total']

    latest_customers = Customer.objects.order_by('-sign_date')[:40]
    latest_customers = [customer_to_dict(c) for c in latest_customers]
    latest_customers_response = {
        'get_time': timezone.now(),
        'latest_customers': latest_customers
    }

    return JsonResponse(latest_customers_response)


@csrf_exempt
def add_customer(request):

    name = request.POST.get("name")
    address = request.POST.get("address")
    sign_date = request.POST.get("sign_date")
    duration = request.POST.get("duration")
    phone = request.POST.get("phone")
    area = request.POST.get("area")
    total_price = request.POST.get("total_price")
    price_discount = request.POST.get("price_discount")

    try:
        area = float(area)
    except:
        area = 0

    try:
        duration = int(duration)
        total_price = float(total_price)
        price_discount = float(price_discount)
        t = sign_date.split('-')
        sign_date = datetime.date(int(t[0]), int(t[1]), int(t[2]))
    except:
        return HttpResponse('表单数据格式不正确')

    new_customer = Customer(name=name, address=address, sign_date=sign_date, duration=duration,
                            phone=phone, area=area, total_price=total_price, price_discount=price_discount,
                            price_received=1234, total_expense=4500, expense_paid=234.5)
    new_customer.save()
    return HttpResponse('success')


def suppliers(request):
    def supplier_to_dict(supplier):
        return {
            'id': supplier.id,
            'name': supplier.name,
            'address': supplier.address,
            'phone': supplier.phone,

            # 'total_expense': suppliers_total_expense[supplier.name] if supplier.name in suppliers_total_expense else 0,
            # 'expense_paid': suppliers_expense_paid[supplier.name] if supplier.name in suppliers_expense_paid else 0,
            'total_expense': 0,
            'expense_paid': 0,
        }

    # total_expense = MaterialOrderItem.objects.values('supplier__name').annotate(
    #     total=Sum(F('price') * F('quantity')))
    # suppliers_total_expense = {}
    # for i in total_expense:
    #     suppliers_total_expense[i['supplier__name']] = i['total']
    #
    # expense_paid = MaterialOrderItem.objects.filter(is_paid__exact=True).values('supplier__name').annotate(
    #     total=Sum(F('price') * F('quantity')))
    # suppliers_expense_paid = {}
    # for i in expense_paid:
    #     suppliers_expense_paid[i['supplier__name']] = i['total']

    latest_suppliers = Supplier.objects.order_by('-id')[:40]
    latest_suppliers = [supplier_to_dict(c) for c in latest_suppliers]
    latest_suppliers_response = {
        'get_time': timezone.now(),
        'latest_suppliers': latest_suppliers
    }

    return JsonResponse(latest_suppliers_response)


@csrf_exempt
def add_supplier(request):
    name = request.POST.get("name")
    address = request.POST.get("address")
    phone = request.POST.get("phone")

    new_supplier = Supplier(name=name, address=address, phone=phone)
    new_supplier.save()
    return HttpResponse('success')


def collections_from_customer(request):
    def collection_to_dict(collection):
        return {
            'customer': str(collection.customer),
            'amount': collection.amount,
            'collect_date': collection.collect_date,
            'remark': collection.remark,
        }

    latest_collections = CollectionFromCustomer.objects.order_by('-collect_date')[:40]
    latest_collections = [collection_to_dict(c) for c in latest_collections]
    latest_collections_response = {
        'get_time': timezone.now(),
        'latest_collections': latest_collections
    }

    return JsonResponse(latest_collections_response)


@csrf_exempt
def collect_from_customer(request):

    name = request.POST.get("name")
    amount = request.POST.get("amount")
    collect_date = request.POST.get("collect_date")
    remark = request.POST.get("remark")

    try:
        customer_address = name[name.index('(')+1: -1]
        customer = Customer.objects.get(pk=customer_address)
        amount = float(amount)
        t = collect_date.split('-')
        collect_date = datetime.date(int(t[0]), int(t[1]), int(t[2]))
    except:
        return HttpResponse('表单数据格式不正确')

    new_collection = CollectionFromCustomer(customer=customer, amount=amount, collect_date=collect_date, remark=remark)
    new_collection.save()
    customer.price_received += amount
    customer.save()
    return HttpResponse('success')


def material_classes(request):
    data = {}
    first_classes = MaterialFirstClass.objects.all()
    second_classes = MaterialSecondClass.objects.all()
    third_classes = MaterialThirdClass.objects.all()
    for first in first_classes:
        data[str(first.name)] = {}
    for second in second_classes:
        data[str(second.first_class.name)][str(second.name)] = []
    for third in third_classes:
        data[str(third.second_class.first_class.name)][str(third.second_class.name)].append(str(third.name))

    # def parse(data_dict):
    #     if type(data_dict) == list:
    #         return data_dict
    #     data_list = []
    #     for k, v in data_dict.items():
    #         data_list.append({k: parse(v)})
    #     return data_list
    # parsed_data = parse(data)

    parsed_data = []
    for k, v in data.items():
        if len(v) == 0:
            parsed_data.append({k: [{'无': ['无']}]})
        else:
            second = []
            for k2, v2 in v.items():
                if len(v2) == 0:
                    second.append({k2: ['无']})
                else:
                    second.append({k2: v2})
            parsed_data.append({k: second})

    response = {
        'get_time': timezone.now(),
        'material_classes': parsed_data
    }
    return JsonResponse(response)


@csrf_exempt
def materials(request):
    first_class = request.POST.get("first_class")
    second_class = request.POST.get("second_class")
    third_class = request.POST.get("third_class")

    material_class = MaterialThirdClass.objects.get(name__exact=third_class,
                                                    second_class__name__exact=second_class,
                                                    second_class__first_class__name__exact=first_class)

    def material_to_dict(material):
        return {
            'id': material.id,
            'name': material.name,
            'unit': material.unit,
            'description': material.description,

            'total_expense': material.total_expense,
            'total_used_amount': material.total_used_amount,
        }

    all_materials = material_class.material_set.all()
    all_materials = [material_to_dict(c) for c in all_materials]

    all_materials_response = {
        'get_time': timezone.now(),
        'all_materials': all_materials
    }

    return JsonResponse(all_materials_response)


def supplier_detail(request, supplier_id):
    supplier = Supplier.objects.get(pk=supplier_id)
    all_materials = supplier.material_set.all()

    def material_to_dict(material):
        relationship = MaterialSupplierRelationship.objects.get(supplier=supplier, material=material)

        return {
            'id': material.id,
            'name': material.name,
            'unit': material.unit,
            'description': material.description,

            'price': relationship.price,

            'total_expense': material.total_expense,
            'total_used_amount': material.total_used_amount,
        }

    all_materials = [material_to_dict(c) for c in all_materials]
    all_materials_response = {
        'get_time': timezone.now(),
        'all_materials': all_materials
    }

    return JsonResponse(all_materials_response)


# def material_orders(request):
#     def demand_item_to_dict(item):
#         return {
#             'item_num': item.item_num,
#             'material': item.material.name,
#             'material_unit': item.material.unit,
#             'customer_name': item.customer.name,
#             'customer_address': item.customer.address,
#             'quantity': item.quantity,
#             'remark': item.remark,
#         }
#
#     def purchase_item_to_dict(item):
#         return {
#             'material': item.material.name,
#             'material_unit': item.material.unit,
#             'purchase_type': item.purchase_type,
#             # 'warehouse': item.warehouse.name if item.warehouse else None,
#             # 'supplier': item.supplier.name if item.supplier else None,
#             'from': item.warehouse.name if item.warehouse else item.supplier.name,
#             'quantity': item.quantity,
#             'price': item.price,
#             'is_paid': item.is_paid,
#             'remark': item.remark,
#         }
#
#     def order_to_dict(order):
#         order_demand_items = order.materialorderdemanditem_set.all()
#         order_purchase_items = order.materialorderpurchaseitem_set.all()
#         return {
#             'id': order.id,
#             'order_date': order.order_date,
#             'clerk': order.clerk,
#             'remark': order.remark,
#
#             'order_demand_items': [demand_item_to_dict(c) for c in order_demand_items],
#             'order_purchase_items': [purchase_item_to_dict(c) for c in order_purchase_items],
#         }
#
#     latest_material_orders = MaterialOrder.objects.order_by('-order_date')[:40]
#     latest_material_orders = [order_to_dict(c) for c in latest_material_orders]
#     latest_orders_response = {
#         'get_time': timezone.now(),
#         'latest_material_orders': latest_material_orders
#     }
#
#     return JsonResponse(latest_orders_response)


def material_orders(request):

    def get_material_in_supplier_in_order(supplier_in_order):
        material_in_supplier_in_order_set = supplier_in_order.materialinsupplierinorderrelationship_set.all()
        material_in_supplier_in_order_response = {}
        for m in material_in_supplier_in_order_set:
            material_in_supplier_in_order_response[str(m.material)] = {
                'quantity': m.quantity,
                'unit': m.material.unit,
                'price': m.price,
                'remark': m.remark,
            }
        return material_in_supplier_in_order_response

    def get_material_in_warehouse_in_order(warehouse_in_order):
        material_in_warehouse_in_order_set = warehouse_in_order.materialinwarehouseinorderrelationship_set.all()
        material_in_warehouse_in_order_response = {}
        for m in material_in_warehouse_in_order_set:
            material_in_warehouse_in_order_response[str(m.material)] = {
                'quantity': m.quantity,
                'unit': m.material.unit,
                'price': m.price,
                'remark': m.remark,
            }
        return material_in_warehouse_in_order_response

    def get_from_in_order(order):
        warehouse_in_order_set = order.warehouseinorderrelationship_set.all()
        supplier_in_order_set = order.supplierinorderrelationship_set.all()
        from_in_order_response = {}
        for w in warehouse_in_order_set:
            from_in_order_response[str(w.warehouse)] = {
                'is_paid': w.is_paid,
                'expense': w.expense,
                'material_in_from_in_order': get_material_in_warehouse_in_order(w),
            }
        for s in supplier_in_order_set:
            from_in_order_response[str(s.supplier)] = {
                'is_paid': s.is_paid,
                'expense': s.expense,
                'material_in_from_in_order': get_material_in_supplier_in_order(s),
            }
        return from_in_order_response

    def get_from_in_material_in_order(material_in_order):
        warehouse_in_material_in_order = material_in_order.warehouseinmaterialinorderrelationship_set.all()
        supplier_in_material_in_order = material_in_order.supplierinmaterialinorderrelationship_set.all()
        from_in_material_in_order_response = {}
        for w in warehouse_in_material_in_order:
            from_in_material_in_order_response[str(w.warehouse)] = {
                'quantity': w.quantity,
                'price': w.price,
                'is_paid': w.is_paid,
                'remark': w.remark,
            }
        for s in supplier_in_material_in_order:
            from_in_material_in_order_response[str(s.supplier)] = {
                'quantity': s.quantity,
                'price': s.price,
                'is_paid': s.is_paid,
                'remark': s.remark,
            }
        return from_in_material_in_order_response

    def get_material_in_order(order):
        material_in_order_set = order.materialinorderrelationship_set.all()
        material_in_order_response = {}
        for m in material_in_order_set:
            material_in_order_response[str(m.material)] = {
                'quantity': m.quantity,
                'expense': m.expense,
                'unit': m.material.unit,
                'from_in_material_in_order': get_from_in_material_in_order(m),
            }
        return material_in_order_response

    def get_material_in_customer_in_order(customer_in_order):
        material_in_customer_in_order_set = customer_in_order.materialincustomerinorderrelationship_set.all()
        material_in_customer_in_order_response = {}
        for m in material_in_customer_in_order_set:
            material_in_customer_in_order_response[str(m.material)] = {
                'unit': m.material.unit,
                'quantity': m.quantity,
                'remark': m.remark,
                'average_price': m.material_in_order.expense / m.material_in_order.quantity,
                'paid_ratio': m.material_in_order.paid_ratio,
            }
        return material_in_customer_in_order_response

    def get_customer_in_order(order):
        customer_in_order_set = order.customerinorderrelationship_set.all()
        customer_in_order_response = {}
        for c in customer_in_order_set:
            customer_in_order_response[str(c.customer)] = {
                'material_in_customer_in_order': get_material_in_customer_in_order(c),
            }
        return customer_in_order_response

    def order_to_dict(order):
        return {
            'id': order.id,
            'order_date': order.order_date,
            'clerk': order.clerk,
            'remark': order.remark,

            'customer_in_order': get_customer_in_order(order),
            'material_in_order': get_material_in_order(order),
            'from_in_order': get_from_in_order(order),
        }

    latest_material_orders = MaterialOrder.objects.order_by('-order_date')[:40]
    latest_material_orders = [order_to_dict(c) for c in latest_material_orders]
    latest_orders_response = {
        'get_time': timezone.now(),
        'latest_material_orders': latest_material_orders
    }

    return JsonResponse(latest_orders_response)


def suppliers_by_material(request, material_name):
    material = Material.objects.get(name__exact=material_name)
    available_suppliers = material.suppliers.all()
    available_warehouses = material.warehouse_set.all()

    available_from_response = {}

    for w in available_warehouses:
        relationship = WarehouseMaterialRelationship.objects.get(warehouse=w, material=material)
        available_from_response[str(w)] = {
            'type': 'warehouse',
            'price': str(relationship.price),
            'quantity': relationship.quantity,
        }

    for s in available_suppliers:
        relationship = MaterialSupplierRelationship.objects.get(supplier=s, material=material)
        available_from_response[str(s)] = {
            'type': 'supplier',
            'price': str(relationship.price),
        }

    available_suppliers_response = {
        'get_time': timezone.now(),
        'available_from': available_from_response,
    }

    return JsonResponse(available_suppliers_response)


# @csrf_exempt
# def add_material_order(request):
#     order_items = request.POST.get("order_items")
#     order_date = request.POST.get("order_date")
#     remark = request.POST.get("remark")
#     suppliers_paid = request.POST.get("suppliers_paid")
#
#     try:
#         t = order_date.split('-')
#         order_date = datetime.date(int(t[0]), int(t[1]), int(t[2]))
#         order_items = json.loads(order_items)
#         suppliers_paid = json.loads(suppliers_paid)
#     except:
#         return HttpResponse('表单数据格式不正确')
#
#     new_order = MaterialOrder(order_date=order_date, clerk='郝高峰', remark=remark)
#     new_order.save()
#
#     for i, v in enumerate(order_items):
#         material = Material.objects.get(name__exact=v['material'])
#         supplier = Supplier.objects.get(name__exact=v['supplier'])
#         customer_address = v['customer_address'].split('(')
#         customer_address = customer_address[1][:-1]
#         customer = Customer.objects.get(address__exact=customer_address)
#         new_order_item = MaterialOrderItem(order=new_order,
#                                            item_num=i+1,
#                                            material=material,
#                                            supplier=supplier,
#                                            customer=customer,
#                                            quantity=v['quantity'],
#                                            price=v['price'],
#                                            is_paid=suppliers_paid[v['supplier']],
#                                            remark=v['remark'])
#         new_order_item.save()
#
#     return HttpResponse('success')


@csrf_exempt
def add_material_order(request):
    customer_demand_items = request.POST.get("customer_demand_items")
    material_demand_sum = request.POST.get("material_demand_sum")
    order_date = request.POST.get("order_date")
    remark = request.POST.get("remark")
    from_paid = request.POST.get("from_paid")



    try:
        t = order_date.split('-')
        order_date = datetime.date(int(t[0]), int(t[1]), int(t[2]))
        customer_demand_items = json.loads(customer_demand_items)
        material_demand_sum = json.loads(material_demand_sum)
        from_paid = json.loads(from_paid)
    except:
        return HttpResponse('表单数据格式不正确')

    new_order = MaterialOrder(order_date=order_date, clerk='郝高峰', remark=remark)
    new_order.save()

    for material, material_demand in material_demand_sum.items():
        for purchase_item in material_demand['purchase_items']:
            if purchase_item['type'] == 'warehouse' or from_paid[purchase_item['from']]:
                purchase_item['is_paid'] = True
                if 'expense_paid' in material_demand:
                    material_demand['expense_paid'] += purchase_item['price'] * purchase_item['quantity']
                else:
                    material_demand['expense_paid'] = purchase_item['price'] * purchase_item['quantity']
            else:
                purchase_item['is_paid'] = False

    for material_name, material_demand in material_demand_sum.items():
        material = Material.objects.get(name__exact=material_name)
        new_material_in_order = MaterialInOrderRelationship(
            order=new_order,
            material=material,
            quantity=material_demand['quantity'],
            expense=material_demand['expense'],
            paid_ratio=material_demand['expense_paid'] / material_demand['expense']
        )
        new_material_in_order.save()
        material_demand['material_in_order'] = new_material_in_order

        for purchase_item in material_demand['purchase_items']:
            if purchase_item['type'] == 'warehouse':
                warehouse = Warehouse.objects.get(name__exact=purchase_item['from'][:purchase_item['from'].index('(')])
                new_warehouse_in_material_in_order = WarehouseInMaterialInOrderRelationship(
                    material_in_order=new_material_in_order,
                    warehouse=warehouse,
                    quantity=purchase_item['quantity'],
                    price=purchase_item['price'],
                    is_paid=purchase_item['is_paid'],
                    remark=purchase_item['remark']
                )
                new_warehouse_in_material_in_order.save()
            elif purchase_item['type'] == 'supplier':
                supplier = Supplier.objects.get(name__exact=purchase_item['from'])
                new_supplier_in_material_in_order = SupplierInMaterialInOrderRelationship(
                    material_in_order=new_material_in_order,
                    supplier=supplier,
                    quantity=purchase_item['quantity'],
                    price=purchase_item['price'],
                    is_paid=purchase_item['is_paid'],
                    remark=purchase_item['remark']
                )
                new_supplier_in_material_in_order.save()

    for customer_address, customer_demand in customer_demand_items.items():
        customer = Customer.objects.get(address__exact=customer_address[customer_address.index('(')+1:-1])
        new_customer_in_order = CustomerInOrderRelationship(
            order=new_order,
            customer=customer
        )
        new_customer_in_order.save()
        for demand_item in customer_demand:
            material = Material.objects.get(name__exact=demand_item['material'])
            new_material_in_customer_in_order = MaterialInCustomerInOrderRelationship(
                customer_in_order=new_customer_in_order,
                material=material,
                quantity=demand_item['quantity'],
                remark=demand_item['remark'],
                material_in_order=material_demand_sum[demand_item['material']]['material_in_order']
            )
            new_material_in_customer_in_order.save()

    from_purchase_sum = {}
    for material, material_demand in material_demand_sum.items():
        for purchase_item in material_demand['purchase_items']:
            if purchase_item['from'] in from_purchase_sum:
                from_purchase_sum[purchase_item['from']]['expense'] += purchase_item['price'] * purchase_item[
                    'quantity']
                from_purchase_sum[purchase_item['from']]['purchase_items'].append(purchase_item)
            else:
                from_purchase_sum[purchase_item['from']] = {
                    'expense': purchase_item['price'] * purchase_item['quantity'],
                    'purchase_items': [purchase_item],
                    'type': purchase_item['type'],
                }

    for material_from, from_purchase in from_purchase_sum.items():
        if from_purchase['type'] == 'warehouse':
            warehouse = Warehouse.objects.get(name__exact=material_from[:material_from.index('(')])
            new_warehouse_in_order = WarehouseInOrderRelationship(
                order=new_order,
                warehouse=warehouse,
                is_paid=from_paid[material_from],
                expense=from_purchase['expense']
            )
            new_warehouse_in_order.save()

            for purchase_item in from_purchase['purchase_items']:
                material = Material.objects.get(name__exact=purchase_item['material'])
                new_material_in_warehouse_in_order = MaterialInWarehouseInOrderRelationship(
                    warehouse_in_order=new_warehouse_in_order,
                    material=material,
                    quantity=purchase_item['quantity'],
                    price=purchase_item['price'],
                    remark=purchase_item['remark']
                )
                new_material_in_warehouse_in_order.save()

        elif from_purchase['type'] == 'supplier':
            supplier = Supplier.objects.get(name__exact=material_from)
            new_supplier_in_order = SupplierInOrderRelationship(
                order=new_order,
                supplier=supplier,
                is_paid=from_paid[material_from],
                expense=from_purchase['expense']
            )
            new_supplier_in_order.save()

            for purchase_item in from_purchase['purchase_items']:
                material = Material.objects.get(name__exact=purchase_item['material'])
                new_material_in_supplier_in_order = MaterialInSupplierInOrderRelationship(
                    supplier_in_order=new_supplier_in_order,
                    material=material,
                    quantity=purchase_item['quantity'],
                    price=purchase_item['price'],
                    remark=purchase_item['remark']
                )
                new_material_in_supplier_in_order.save()


    print(customer_demand_items)
    print('\n')
    print(material_demand_sum)

    return HttpResponse('success')


def warehouses(request):
    def warehouse_to_dict(warehouse):
        return {
            'name': warehouse.name,
            'address': warehouse.address,
            'remark': warehouse.remark,
        }

    all_warehouses = Warehouse.objects.all()
    all_warehouses = [warehouse_to_dict(c) for c in all_warehouses]
    all_warehouses_response = {
        'get_time': timezone.now(),
        'all_warehouses': all_warehouses
    }

    return JsonResponse(all_warehouses_response)


@csrf_exempt
def warehouse_materials(request):
    first_class = request.POST.get("first_class")
    second_class = request.POST.get("second_class")
    third_class = request.POST.get("third_class")
    warehouse = request.POST.get("warehouse")

    material_class = MaterialThirdClass.objects.get(name__exact=third_class,
                                                    second_class__name__exact=second_class,
                                                    second_class__first_class__name__exact=first_class)
    warehouse = Warehouse.objects.get(name__exact=warehouse)
    all_materials = warehouse.materials.filter(material_class=material_class)

    def material_to_dict(material):
        relationship = WarehouseMaterialRelationship.objects.get(material=material, warehouse=warehouse)

        return {
            'id': material.id,
            'name': material.name,
            'unit': material.unit,
            'description': material.description,

            'price': relationship.price,
            'quantity': relationship.quantity,
        }

    all_materials = [material_to_dict(c) for c in all_materials]

    all_materials_response = {
        'get_time': timezone.now(),
        'all_materials': all_materials
    }

    return JsonResponse(all_materials_response)
