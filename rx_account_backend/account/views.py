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

from .models import (Customer, Supplier, CollectionFromCustomer,
                     MaterialFirstClass, MaterialSecondClass, MaterialThirdClass,
                     Material, MaterialSupplierRelationship, MaterialOrder,
                     MaterialOrderItem)


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
            'total_expense': customer.total_expense,
            'expense_paid': customer.expense_paid,
        }

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

            'total_expense': supplier.total_expense,
            'expense_paid': supplier.expense_paid,
        }

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


def material_orders(request):
    def item_to_dict(item):
        return {
            'item_num': item.item_num,
            'material': item.material.name,
            'material_unit': item.material.unit,
            'supplier': item.supplier.name,
            'customer_name': item.customer.name,
            'customer_address': item.customer.address,

            'quantity': item.quantity,
            'price': item.price,
            'is_paid': item.is_paid,
            'remark': item.remark,
        }

    def order_to_dict(order):
        order_items = order.materialorderitem_set.all()
        return {
            'id': order.id,
            'order_date': order.order_date,
            'clerk': order.clerk,
            'remark': order.remark,

            'order_items': [item_to_dict(c) for c in order_items],
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

    def supplier_to_dict(supplier):
        relationship = MaterialSupplierRelationship.objects.get(supplier=supplier, material=material)

        return {
            'name': supplier.name,
            'price': relationship.price,
        }

    available_suppliers = [supplier_to_dict(c) for c in available_suppliers]
    available_suppliers_response = {
        'get_time': timezone.now(),
        'available_suppliers': available_suppliers
    }

    return JsonResponse(available_suppliers_response)


@csrf_exempt
def add_material_order(request):
    order_items = request.POST.get("order_items")
    order_date = request.POST.get("order_date")
    remark = request.POST.get("remark")

    try:
        t = order_date.split('-')
        order_date = datetime.date(int(t[0]), int(t[1]), int(t[2]))
        order_items = json.loads(order_items)
    except:
        return HttpResponse('表单数据格式不正确')

    new_order = MaterialOrder(order_date=order_date, clerk='郝高峰', remark=remark)
    new_order.save()

    for i, v in enumerate(order_items):
        material = Material.objects.get(name__exact=v['material'])
        supplier = Supplier.objects.get(name__exact=v['supplier'])
        customer_address = v['customer_address'].split('(')
        customer_address = customer_address[1][:-1]
        customer = Customer.objects.get(address__exact=customer_address)
        new_order_item = MaterialOrderItem(order=new_order,
                                           item_num=i,
                                           material=material,
                                           supplier=supplier,
                                           customer=customer,
                                           quantity=v['quantity'],
                                           price=v['price'],
                                           is_paid=False,
                                           remark=v['remark'])
        new_order_item.save()

    return HttpResponse('success')
