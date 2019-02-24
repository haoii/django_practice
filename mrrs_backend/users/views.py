from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse, HttpResponseRedirect
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse


LOGIN_MESSAGE = {
    'password_error': '用户名或密码错误，请重试',
    'is_logout': '已退出登陆',
}


def login_view(request):
    if request.method == 'GET':
        next_url = request.GET.get('next')
        if not next_url:
            next_url = reverse('rooms:index')

        context = {'next': next_url}
        message = request.GET.get('message')
        if message:
            context['message'] = LOGIN_MESSAGE[message]

        return render(request, 'users/login.html', context)

    elif request.method == 'POST':
        username = request.POST['user']
        password = request.POST['password']
        next_url = request.POST['next']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(next_url)
        else:
            redirect_url = reverse('users:login') + '?next=' + next_url + '&message=password_error'
            return HttpResponseRedirect(redirect_url)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('users:login') + '?' + 'message=is_logout')



