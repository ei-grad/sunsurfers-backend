from django.urls import path
from django.views.generic import TemplateView

from surfers import views


app_name = 'surfers'
urlpatterns = [
    path('map', views.sunmap, name='sunmap'),
    path('policy', TemplateView.as_view(template_name='policy.html'), name='policy'),
    path('latest', views.latest, name='latest_geojson'),
]
