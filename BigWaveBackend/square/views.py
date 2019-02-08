from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.utils import timezone

from .models import SquarePost


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

    latest_posts = SquarePost.objects.order_by('-pub_date')[:5]
    latest_posts = [post_to_dict(p) for p in latest_posts]
    latest_posts_response = {
        'get_time': timezone.now(),
        'latest_posts': latest_posts
    }

    return JsonResponse(latest_posts_response)
