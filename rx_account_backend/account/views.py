import datetime

from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.template import loader
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from .models import Customer


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
