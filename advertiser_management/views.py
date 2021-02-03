import collections
from datetime import datetime, timedelta

from django.db.models import Min, Count
from django.db.models.functions import TruncHour
from django.shortcuts import render, get_object_or_404
from django.views.generic import RedirectView, CreateView, DetailView, ListView

from .forms import CreateNewAdForm
from .models import Advertiser, Ad, Click, View


def index(request):
    # for advertiser in Advertiser.objects.all():
    #     # for ad in advertiser.ad_set.all():
    #     #     ad.inc_views()
    context = {
        'advertisers': Advertiser.objects.all()
    }
    return render(request, 'advertiser_management/ads.html', context)


class ClickTaskView(RedirectView):
    pattern_name = 'advertiser_management:ad_view'

    def get_redirect_url(self, *args, **kwargs):
        # ad = get_object_or_404(Ad, pk=kwargs['ad_id'])
        # ad.inc_clicks()
        return super().get_redirect_url(*args, **kwargs)


class OpenAdView(DetailView):
    model = Ad
    template_name = 'advertiser_management/ad.html'

    def get_context_data(self, **kwargs):
        context = {
            'ad': get_object_or_404(Ad, pk=self.kwargs.get('pk'))
        }
        return context


class CreateNewAdView(CreateView):
    model = Ad
    form_class = CreateNewAdForm
    template_name = 'advertiser_management/new_ad.html'


def get_action_properties(context):
    ads = Ad.objects.filter(approve=True)
    for ad in ads:
        context['actions'][ad] = {}
        oldest_click_time = Click.objects.filter(ad=ad).aggregate(Min('time'))['time__min']
        start_date = datetime.now()
        action = {}
        clicks = Click.objects.annotate(
            hour=TruncHour('time')).values('hour').filter(ad=ad).annotate(
            clicks=Count('id'))
        views = View.objects.annotate(
            hour=TruncHour('time')).values('hour').filter(ad=ad).annotate(
            views=Count('id'))
        for v in views:
            # action[v['hour']] = [v['hour'] + timedelta(hours=1), 0, v['views']]
            action[v['hour']] = v['views']
        for c in clicks:
            action[c['hour']] = c['clicks']
        context['actions'][ad] = sorted(action.items(), key=lambda t: t[0])
        # while oldest_click_time.replace(tzinfo=pytz.UTC) < start_date.replace(tzinfo=pytz.UTC):
        #     end_date = start_date - timedelta(hours=1)
        #     # clicks = Click.objects.filter(time__range=[end_date, start_date], ad=ad)
        #     views = View.objects.filter(time__range=[end_date, start_date], ad=ad)
        #     clicks_count = clicks.count()
        #     views_count = views.count()
        #     if clicks_count > 0 or views_count > 0:
        #         # print("\n\nad: " + str(ad.title) + "\n" + str(start_date) + " - " + str(end_date) + "\n" +
        #         #       str(clicks_count) + "\n\n")
        #         # print("\n" + str(start_date))
        #         context['actions'][ad][str(start_date)] = [str(end_date), clicks_count, views_count ]
        #                                                    clicks_count / views_count]
        #     start_date -= timedelta(hours=1)
    # print("\n\n" + str(context['actions']) + "\n\n")


class ReportView(ListView):
    queryset = Ad.objects.filter(approve=True)
    template_name = 'advertiser_management/report.html'
    context_object_name = 'ads'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        ads = Ad.objects.filter(approve=True)
        context = {
            'ads': ads,
            'actions': {},
        }
        get_action_properties(context)
        return context
