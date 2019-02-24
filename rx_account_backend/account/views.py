from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import Http404

from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    return HttpResponse('helloo')
