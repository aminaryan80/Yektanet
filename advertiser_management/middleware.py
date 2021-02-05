import re

from django.utils import timezone
from rest_framework.permissions import IsAuthenticated

from advertiser_management.models import Ad, View, Click


def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class ViewAdMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            match = re.match("(?!admin)/advertiser_management/$", request.path)
            if match:
                ads = Ad.objects.all()
                for ad in ads:
                    if ad.approve:
                        view = View.objects.create(ad=ad, time=timezone.now(), ip=get_ip(request))
                        view.save()
        response = self.get_response(request)
        return response


class ClickAdMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            match = re.match("(?!admin)/advertiser_management/click/(\\d+)/$", request.path)
            if match:
                ad = Ad.objects.get(pk=match.group(1))
                click = Click.objects.create(ad=ad, time=timezone.now(), ip=get_ip(request))
                click.save()
        response = self.get_response(request)
        return response
