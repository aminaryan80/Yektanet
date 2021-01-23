from django.urls import path

from . import views
from .views import ClickTaskView

urlpatterns = [
    path('', views.index, name='index'),
    path('click/<int:ad_id>/', ClickTaskView.as_view(), name='click_task_view'),
    path('ad/<int:ad_id>/', views.ad, name='ad_view'),
]
