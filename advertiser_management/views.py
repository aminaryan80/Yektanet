from datetime import timedelta

from django.db.models import Count
from django.db.models.functions import TruncHour
from django.shortcuts import render, get_object_or_404
from django.views.generic import RedirectView, CreateView, DetailView, ListView, TemplateView
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.views import APIView

from .forms import CreateNewAdForm
from .models import Advertiser, Ad, Click, View


class AdsView(TemplateView, APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        context = {
            'advertisers': Advertiser.objects.all()
        }
        return render(request, 'advertiser_management/ads.html', context)


class ClickTaskView(RedirectView):
    pattern_name = 'advertiser_management:ad_view'

    def get_redirect_url(self, *args, **kwargs):
        return super().get_redirect_url(*args, **kwargs)


class OpenAdView(DetailView, APIView):
    model = Ad
    template_name = 'advertiser_management/ad.html'
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [AllowAny]

    def get_context_data(self, **kwargs):
        context = {
            'ad': get_object_or_404(Ad, pk=self.kwargs.get('pk'))
        }
        return context


class CreateNewAdView(CreateView, APIView):
    model = Ad
    form_class = CreateNewAdForm
    template_name = 'advertiser_management/new_ad.html'
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAdminUser]


def get_action_properties(context):
    ads = Ad.objects.filter(approve=True)
    for ad in ads:
        context['actions'][ad] = {}
        action = {}
        clicks_count = 0
        views_count = 0
        clicks = Click.objects.filter(ad=ad).annotate(hour=TruncHour('time')).values('hour').annotate(
            clicks=Count('id'))
        views = View.objects.filter(ad=ad).annotate(hour=TruncHour('time')).values('hour').annotate(views=Count('id'))
        for v in views:
            action[v['hour']] = [v['hour'] + timedelta(hours=1), 0, v['views'], 0]
            views_count += v['views']
        for c in clicks:
            action[c['hour']][1] = c['clicks']
            action[c['hour']][3] = c['clicks'] / action[c['hour']][2]
            clicks_count += c['clicks']
        context['actions'][ad]['action'] = sorted(action.items(), reverse=True, key=lambda t: t[1])
        context['actions'][ad]['cpv'] = clicks_count / views_count


def get_avg_click_view(context):
    ads = Ad.objects.filter(approve=True)
    for ad in ads:
        clicks = Click.objects.filter(ad=ad)
        sum_diff = 0
        for click in clicks:
            v = None
            views = View.objects.filter(ad=ad, ip=click.ip).order_by('time')
            for view in views:
                if (v is None) or (view.ip == click.ip and click.time > view.time > v.time):
                    v = view
            sum_diff += (click.time - v.time).seconds
        avg = -1
        if clicks.count() > 0:
            avg = sum_diff / clicks.count()
        context['avg'][ad] = avg


class ReportView(ListView, APIView):
    queryset = Ad.objects.filter(approve=True)
    template_name = 'advertiser_management/report.html'
    context_object_name = 'ads'
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAdminUser]

    def get_context_data(self, **kwargs):
        ads = Ad.objects.filter(approve=True)
        context = {
            'ads': ads,
            'actions': {},
            'avg': {},
        }
        get_action_properties(context)
        get_avg_click_view(context)
        return context
