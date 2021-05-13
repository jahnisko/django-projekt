# Router
# Základní směrovač celé aplikace
# Stará se o to, že když přijde požadavek, má ho poslat na určité místo

from django.contrib import admin
from django.urls import path
from covidtest import views

urlpatterns = [
    path('', views.index, name='index'),
    path('testy/', views.nakazeni_view, name='seznam_testu'),
    path('testy/<int:pk>', views.NakazenyDetail.as_view(), name='pacient-detail'),
]