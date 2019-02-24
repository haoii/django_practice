from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse, HttpResponseRedirect
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse


def login_view(request):
    if request.method == 'GET':
        next_url = request.GET.get('next')
        if not next_url:
            next_url = reverse('rooms:index')

        context = {'next': next_url}
        error = request.GET.get('error')
        if error:
            context['error'] = error

        return render(request, 'users/login.html', context)

    elif request.method == 'POST':
        user = authenticate(request, username=request.POST['user'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(request.POST['next'])
        else:
            return HttpResponseRedirect(reverse('users:login') + '?next=' + request.POST['next'] + '&error=1')




