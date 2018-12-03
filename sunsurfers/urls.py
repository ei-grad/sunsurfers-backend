"""sunsurfers URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.urls import path, include
from django.contrib.gis import admin
from django.shortcuts import render

from surfers.api import v1_api

from . import auth


def login_view(request):
    # XXX: "next" passthrough doesn't work when using JS-backed redirects and
    # auth widgets (they are unfortunately laying out of the PSA login flow)
    if 'next' in request.GET:
        request.session['next'] = request.GET['next']
    return render(request, 'login.html', {'tgauth_bot': settings.TGAUTH_BOT})


urlpatterns = [
    path('', include('surfers.urls')),
    path('admin/', admin.site.urls),
    path('api/', include(v1_api.urls)),
    path('checklist/', include('checklist.urls')),
    path('login/', login_view),
    path('register-by-token/<backend>/', auth.register_by_access_token, 'register_by_access_token'),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('tg/', include('tgauth.urls')),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
