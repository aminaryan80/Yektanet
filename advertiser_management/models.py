from django.db import models
from django.urls import reverse


class Advertiser(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Ad(models.Model):
    advertiser = models.ForeignKey(Advertiser, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    img_url = models.ImageField(upload_to="ads/")
    approve = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('advertiser_management:ad_view', args=(self.id,))


class BaseAdActions(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    time = models.DateTimeField(null=False)
    ip = models.CharField(null=False, max_length=16)


class Click(BaseAdActions):
    pass


class View(BaseAdActions):
    pass
