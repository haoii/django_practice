from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from .models import SquarePost, User


@login_required(login_url='/login')
def index(request):
    data = {'data': 'test data'}
    return JsonResponse(data)

    def post_to_dict(post):
        return {
            'user': {
                'name': post.user.name,
                'portrait_url': post.user.portrait_url
            },
            'text': post.post_text,
            'image_url': post.image_url,
            'votes': post.votes,
            'pub_date': post.pub_date
        }

    latest_posts = SquarePost.objects.order_by('-pub_date')[:40]
    latest_posts = [post_to_dict(p) for p in latest_posts]
    latest_posts_response = {
        'get_time': timezone.now(),
        'latest_posts': latest_posts
    }

    return JsonResponse(latest_posts_response)


def test_login(request):

    user = authenticate(request, username='root', password='1')
    if user is not None:
        login(request, user)
        return JsonResponse({'data': 'test_login success'})
    else:
        return JsonResponse({'data': 'test_login failed'})


def test_logout(request):
    logout(request)
    return JsonResponse({'data': 'test_logout success'})


@csrf_exempt
def submit_post(request):

    post_text = request.POST.get("post_text")
    user = User.objects.get(pk='haogaofeng')
    post = SquarePost(user=user, post_text=post_text, image_url='', votes=0, pub_date=timezone.now())
    post.save()

    image_hex_list = []
    for i in range(3):
        img = request.FILES.get('image-' + str(i), None)
        if not img:
            break
        image_hex_list.append(img)

    if image_hex_list:
        all_image_url = ''
        for i, image_hex in enumerate(image_hex_list):
            image_url = str(post.id) + '-' + str(i) + '.jpg'
            all_image_url += image_url + ';'
            with open('static/square/post_image/' + image_url, 'wb+') as f:
                for chunk in image_hex.chunks():
                    f.write(chunk)

        post.image_url = all_image_url
        post.save()

    response = {'submit_status': 'success'}
    return JsonResponse(response)
