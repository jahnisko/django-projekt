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
    path('osoba/create/', views.OsobaCreateView.as_view(), name='osoba-create'),
    path('pojistovna/create/', views.PojistovnaCreateView.as_view(), name='pojistovna-create'),
    path('misto/create/', views.OdberoveMistoCreateView.as_view(), name='misto-create'),
    path('laborator/create/', views.LaboratorCreateView.as_view(), name='laborator-create'),
    path('pojistenec/create/', views.PojistenecCreateView.as_view(), name='pojistenec-create'),
    path('test/create/', views.TestCreateView.as_view(), name='test-create'),
    path('osoba/<int:pk>/delete/', views.OsobaDeleteView.as_view(), name='delete-osoba'),
    path('osoba/<int:pk>/update/', views.OsobaUpdateView.as_view(), name='update-osoba'),
    path('pojistenec/<int:pk>/update/', views.PojistenecUpdateView.as_view(), name='update-pojistenec'),
    path('test/<int:pk>/update/', views.TestUpdateView.as_view(), name="update-test"),
]