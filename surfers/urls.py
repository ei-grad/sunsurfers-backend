from django.urls import path

from surfers import views


app_name = 'surfers'
urlpatterns = [
    path('', views.sunmap, name='sunmap'),
    path('latest', views.latest, name='latest_geojson'),
]
