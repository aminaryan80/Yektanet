from django.shortcuts import render, get_object_or_404
from django.views.generic import RedirectView, CreateView

from .forms import CreateNewAdForm
from .models import Advertiser, Ad


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


def ad(request, ad_id):
    context = {
        'ad': get_object_or_404(Ad, pk=ad_id)
    }
    return render(request, 'advertiser_management/ad.html', context)


class CreateNewAd(CreateView):
    model = Ad
    form_class = CreateNewAdForm
    template_name = 'advertiser_management/new_ad.html'
