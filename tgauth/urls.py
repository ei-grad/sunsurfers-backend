from django.urls import path

from tgauth import views


app_name = 'tgauth'
urlpatterns = [
    path('webhook/<token>', views.botapi, name='webhook'),
    path('login/<token>', views.login, name='login'),
]
