from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

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


'''Sekce pohledů pro přidávání do databáze'''


class OsobaCreateView(CreateView):
    model = Osoba
    fields = ['jmeno', 'prijmeni', 'datum_narozeni', 'rodne_cislo', 'cislo_op', 'mesto', 'ulice', 'psc',
              'tel_cislo', 'email']
    template_name = 'stranky/osoba_form.html'


class PojistovnaCreateView(CreateView):
    model = Pojistovna
    fields = ['pojistovna']
    template_name = 'stranky/pojistovna_form.html'


class OdberoveMistoCreateView(CreateView):
    model = Misto
    fields = ['zemepisna_sirka', 'zemepisna_delka', 'mesto']
    template_name = 'stranky/misto_form.html'


class LaboratorCreateView(CreateView):
    model = Laborator
    fields = '__all__'
    template_name = 'stranky/laborator_form.html'


class PojistenecCreateView(CreateView):
    model = Pojistenec
    fields = ['cislo_pojistence', 'osoba', 'zp']
    template_name = 'stranky/pojistenec_form.html'


class TestCreateView(CreateView):
    model = Test
    fields = '__all__'
    template_name = 'stranky/test_form.html'


''' Sekce pohledů pro odstraňování z databáze a úpravu dat v databázi '''


class OsobaDeleteView(DeleteView):
    #success_url = reverse_lazy('seznam_testu')
    model = Osoba
    template_name = 'stranky/osoba_confirm_delete.html'
    success_url = reverse_lazy('seznam_testu')

    '''
    def get_object(self):
        id_ = self.kwargs.get("pk")
        return get_object_or_404(Osoba, pk=id_)

    def get_success_url(self):
        return reverse('seznam_testu') '''


class OsobaUpdateView(UpdateView):
    model = Osoba
    fields = ['jmeno', 'prijmeni', 'datum_narozeni', 'rodne_cislo', 'cislo_op', 'mesto', 'ulice', 'psc',
              'tel_cislo', 'email']
    template_name = 'stranky/update/osoba_form_update.html'


class PojistenecUpdateView(UpdateView):
    model = Pojistenec
    fields = ['cislo_pojistence', 'osoba', 'zp']
    template_name = 'stranky/update/pojistenec_form_update.html'


class TestUpdateView(UpdateView):
    model = Test
    fields = '__all__'
    template_name = 'stranky/update/test_form_update.html'