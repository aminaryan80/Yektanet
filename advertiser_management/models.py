from django.db import models


class Advertiser(models.Model):
    name = models.CharField(max_length=200)
    clicks = models.IntegerField(default=0, null=False)
    views = models.IntegerField(default=0, null=False)


class Ad(models.Model):
    title = models.CharField(max_length=200)
    img_url = models.ImageField(upload_to="ads/")
    link = models.URLField(max_length=200)
    clicks = models.IntegerField(default=0, null=False)
    views = models.IntegerField(default=0, null=False)
    advertiser = models.ForeignKey(Advertiser, on_delete=models.CASCADE)
