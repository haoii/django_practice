from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from .models import SquarePost, User


def index(request):
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

    latest_posts = SquarePost.objects.order_by('-pub_date')[:10]
    latest_posts = [post_to_dict(p) for p in latest_posts]
    latest_posts_response = {
        'get_time': timezone.now(),
        'latest_posts': latest_posts
    }

    return JsonResponse(latest_posts_response)


@csrf_exempt
def submit_post(request):

    post_text = request.POST.get("post_text")
    user = User.objects.get(pk='haogaofeng')
    post = SquarePost(user=user, post_text=post_text, image_url='', votes=0, pub_date=timezone.now())
    post.save()

    file_hex = request.FILES.get("files", None)
    if file_hex:
        image_url = str(post.id) + '-1.jpg'
        with open('static/square/post_image/' + image_url, 'wb+') as f:
            for chunk in file_hex.chunks():
                f.write(chunk)

        post.image_url = image_url
        post.save()

    response = {'submit_status': 'success'}
    return JsonResponse(response)
