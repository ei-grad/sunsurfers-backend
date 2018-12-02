from django.urls import path

from checklist import views

app_name = 'checklist'
urlpatterns = [
    path('', views.checklists, name='checklists'),
    path('<slug>', views.checklist, name='checklist'),
]
