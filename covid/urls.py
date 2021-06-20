"""covid URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from covidtest import views
from django.urls import path, include, re_path
from django.views.generic import RedirectView
import covidtest

urlpatterns = [
    path('admin/', admin.site.urls),
    path('covid/', include('covidtest.urls')),
    path('', RedirectView.as_view(url="covid/")),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'covidtest.views.error_404'
handler500 = 'covidtest.views.error_500'
handler403 = 'covidtest.views.error_403'
handler400 = 'covidtest.views.error_400'

if settings.DEBUG:
    urlpatterns += [re_path(r'^500/$', covidtest.views.error_500)]
    urlpatterns += [re_path(r'^400/$', covidtest.views.error_400)]
    urlpatterns += [re_path(r'^404/$', covidtest.views.error_404)]
    urlpatterns += [re_path(r'^403/$', covidtest.views.error_403)]

