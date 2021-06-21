from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
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


# @permission_required('covidtest.add_laborator', login_url='/accounts/login/')
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

# Třída pro zobrazení detailu se nakonec ukázala jako nepoužitelná pro moji aplikaci, neboť nedocházelo k aktualizaci dat
'''
class NakazenyDetail(DetailView):
    model = Osoba
    context_object_name = 'osoba_detail'
    extra_context = {'pojistenci': Pojistenec.objects.all(), 'testy': Test.objects.all()}
    template_name = 'stranky/detail.html'
'''


# Vlastní pohledová metoda pro vytvoření detailu nakaženého
def detail_nakazeneho(request, pk):
    context = {
        'osoba_detail': Osoba.objects.get(id=pk),
        'pojistenci': Pojistenec.objects.all(),
        'testy': Test.objects.all()
    }

    return render(request, 'stranky/detail.html', context)


'''Sekce pohledů pro přidávání do databáze + využití tzv. Mixinů'''


class OsobaCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Osoba
    fields = ['jmeno', 'prijmeni', 'datum_narozeni', 'rodne_cislo', 'cislo_op', 'mesto', 'ulice', 'psc',
              'tel_cislo', 'email']
    template_name = 'stranky/osoba_form.html'
    success_url = reverse_lazy('pojistenec-create')
    login_url = '/accounts/login/'
    permission_required = 'covidtest.add_osoba'


class PojistovnaCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Pojistovna
    fields = ['pojistovna']
    template_name = 'stranky/pojistovna_form.html'
    success_url = reverse_lazy('pojistovna-create')
    login_url = '/accounts/login/'
    permission_required = 'covidtest.add_pojistovna'


class OdberoveMistoCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Misto
    fields = ['zemepisna_sirka', 'zemepisna_delka', 'mesto']
    template_name = 'stranky/misto_form.html'
    success_url = reverse_lazy('misto-create')
    login_url = '/accounts/login/'
    permission_required = 'covidtest.add_misto'


class LaboratorCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Laborator
    fields = '__all__'
    template_name = 'stranky/laborator_form.html'
    success_url = reverse_lazy('laborator-create')
    login_url = '/accounts/login/'
    permission_required = 'covidtest.add_laborator'


# Mixiny je potřeba dávat vždy před bázovou třídu pohledu
class PojistenecCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Pojistenec
    fields = ['cislo_pojistence', 'osoba', 'zp']
    template_name = 'stranky/pojistenec_form.html'
    success_url = reverse_lazy('test-create')
    login_url = '/accounts/login/'
    permission_required = 'covidtest.add_pojistenec'


class TestCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Test
    fields = '__all__'
    template_name = 'stranky/test_form.html'
    success_url = reverse_lazy('index')
    login_url = '/accounts/login/'
    permission_required = 'covidtest.add_test'


''' Sekce pohledů pro odstraňování z databáze a úpravu dat v databázi '''


class OsobaDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Osoba
    template_name = 'stranky/osoba_confirm_delete.html'
    success_url = reverse_lazy('seznam_testu')
    login_url = '/accounts/login/'
    permission_required = 'covidtest.delete_osoba'


class OsobaUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Osoba
    fields = ['jmeno', 'prijmeni', 'datum_narozeni', 'rodne_cislo', 'cislo_op', 'mesto', 'ulice', 'psc',
              'tel_cislo', 'email']
    template_name = 'stranky/update/osoba_form_update.html'
    success_url = reverse_lazy('seznam_testu')
    login_url = '/accounts/login/'
    permission_required = 'covidtest.change_osoba'


class PojistenecUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Pojistenec
    fields = ['cislo_pojistence', 'osoba', 'zp']
    template_name = 'stranky/update/pojistenec_form_update.html'
    success_url = reverse_lazy('seznam_testu')
    login_url = '/accounts/login/'
    permission_required = 'covidtest.change_pojistenec'


class TestUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Test
    fields = '__all__'
    template_name = 'stranky/update/test_form_update.html'
    success_url = reverse_lazy('seznam_testu')
    login_url = '/accounts/login/'
    permission_required = 'covidtest.change_test'


''' Pohled pro vyhledávání dat v databázi '''


def vyhledavani(request):
    if request.method == "POST":
        searched = request.POST['searched']
        osoby = Osoba.objects.filter(prijmeni__contains=searched)
        context = {
            'searched': searched,
            'osoby': osoby
        }
        return render(request, 'stranky/hledani.html', context)
    else:
        return render(request, 'stranky/hledani.html', {})

'''
Sekce pohledů k chybovým hláškám
'''


def error_404(request, exception=None):
    return render(request, 'errors/404.html')


def error_500(request):
    return render(request, 'errors/500.html')


def error_400(request, exception=None):
    return render(request, 'errors/400.html')


def error_403(request, exception=None):
    return render(request, 'errors/403.html')