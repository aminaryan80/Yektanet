from django.shortcuts import render

from .models import Advertiser


def index(request):
    context = {
        'advertisers': Advertiser.objects.all()
    }
    return render(request, 'advertiser_management/ads.html', context)
