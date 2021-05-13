from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import *


def index(request):
    num_test = Test.objects.all().count()
    test = Test.objects.order_by('-navsteva')[:3]
    cp = Pojistenec.objects.order_by('osoba')
    pojistovny = Pojistovna.objects.order_by('pojistovna')

    context = {
        'num_test': num_test,
        'test': test,
        'cp': cp,
        'pojistovny': pojistovny,
    }

    return render(request, 'index.html', context=context)


class NakazeniView(ListView):
    model = Test
    num_pojistencu = Test.objects.all().count()
    '''
    pojistenci = Pojistenec.objects.all()
    context_object_name = {'testovani_detail'}'''
    template_name = 'test_list.html'

    ordering = ['zp']


def nakazeni_view(request):
    num_pojistencu = Pojistenec.objects.all().count()
    pojistenec = Pojistenec.objects.order_by('zp')
    num_test = Test.objects.all().count()
    test = Test.objects.order_by('navsteva')

    context = {
        'num_pojistencu': num_pojistencu,
        'pojistenec': pojistenec,
        'num_test': num_test,
        'test': test,
    }
    return render(request, 'stranky/test_list.html', context=context)


class NakazenyDetail(DetailView):
    model = Osoba
    context_object_name = 'osoba_detail'
    extra_context = {'pojistenci': Pojistenec.objects.all(), 'testy':Test.objects.all()}
    template_name = 'stranky/detail.html'


