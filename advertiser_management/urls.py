from django.urls import path

from . import views
from .views import ClickTaskView, CreateNewAdView, OpenAdView, ReportView, AdsView

app_name = 'advertiser_management'
urlpatterns = [
    path('', AdsView.as_view(), name='index'),
    path('click/<int:pk>/', ClickTaskView.as_view(), name='click_task_view'),
    path('ad/<int:pk>/', OpenAdView.as_view(), name='ad_view'),
    path('create_new_ad/', CreateNewAdView.as_view(), name='create_new_ad'),
    path('report/', ReportView.as_view(), name='report_view'),
]
