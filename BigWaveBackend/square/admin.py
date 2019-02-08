from django.contrib import admin

from .models import SquarePost, User

admin.site.register(User)
admin.site.register(SquarePost)
