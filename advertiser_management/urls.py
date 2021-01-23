from django.urls import path

from . import views
from .views import ClickTaskView, CreateNewAd

app_name = 'advertiser_management'
urlpatterns = [
    path('', views.index, name='index'),
    path('click/<int:ad_id>/', ClickTaskView.as_view(), name='click_task_view'),
    path('ad/<int:ad_id>/', views.ad, name='ad_view'),
    path('create_new_ad/', CreateNewAd.as_view(), name='create_new_ad'),
]
