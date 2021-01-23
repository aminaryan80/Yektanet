from django.db import models
from django.urls import reverse


class Advertiser(models.Model):
    name = models.CharField(max_length=200)
    clicks = models.IntegerField(default=0, null=False)
    views = models.IntegerField(default=0, null=False)

    def inc_views(self):
        self.views += 1
        self.save()

    def inc_clicks(self):
        self.clicks += 1
        self.save()


class Ad(models.Model):
    advertiser = models.ForeignKey(Advertiser, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    img_url = models.ImageField(upload_to="ads/")
    clicks = models.IntegerField(default=0, null=False)
    views = models.IntegerField(default=0, null=False)

    def inc_views(self):
        self.views += 1
        self.save()
        self.advertiser.inc_views()

    def inc_clicks(self):
        self.clicks += 1
        self.save()
        self.advertiser.inc_clicks()

    def get_absolute_url(self):
        return reverse('advertiser_management:ad_view', args=(self.id,))
