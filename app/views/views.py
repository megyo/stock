from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
import json
import xlwt
from django.db.models import Q
from django.utils import timezone
from app.forms import TermekSearchForm, BevetelalapForm, BeveteltermekForm
from app.forms import ErtekesitForm
from app.forms import BeszallitoForm
from app.forms import Beszallito
from app.models import Termek
from app.models import Raktarkeszlet
from app.models import Bevetel
from app.models import Ertekesit
from app.models import Raktar
from django.forms import formset_factory
from dal import autocomplete


def index(request):
    if request.method == "POST":
        form = TermekSearchForm(request.POST)
        if form.is_valid():
            param = form.cleaned_data['autocomplete']
            param_id = form.cleaned_data['autocomplete_id']

            if param_id == None:
                termekek = Termek.objects.filter(Q(termek_nev__icontains=param) | Q(gyari_cikkszam__icontains=param) | Q(sajat_cikkszam__icontains=param))
                return render(request, 'app/index.html', {'title': 'Értékesítés termék lista', 'termekek': termekek, 'form': form, 'data': True})

            if param_id != None:
                return redirect('ertekesites_termek', pk=param_id)

    else:
        form = TermekSearchForm()

    return render(
        request,
        'app/index.html',
        {
            'title': 'Értékesítés termék kereső',
            'form': form,
            'data': False
        }
    )


def ertekesites_termek(request, pk):
    termek = get_object_or_404(Termek, pk=pk)
    raktarkeszlet = Raktarkeszlet.objects.filter(termek=pk)
    current_user = request.user

    if request.method == "POST":
        form = ErtekesitForm(current_user, request.POST)
        if form.is_valid():
            ertekesit = form.save(commit=False)
            ertekesit.termek = termek
            today = timezone.now()
            ertekesit.eladas_datum = today
            ertekesit.user = current_user
            ertekesit.save()

            #    Készlet módosítása
            try:
                keszlet_id = Raktarkeszlet.objects.get(termek=pk, raktar=ertekesit.raktar)
                raktárkeszlet = keszlet_id.keszlet
                uj_keszlet = raktárkeszlet - ertekesit.eladas_mennyiseg
                if uj_keszlet <= 0:
                    uj_keszlet = 0

                keszlet_id.keszlet = uj_keszlet
                keszlet_id.save()
            except:
                pass

            return redirect('index')
    else:
        form = ErtekesitForm(current_user)

    # return HttpResponse(raki, content_type="text/plain")
    return render(request, 'app/ertekesites_termek.html', {'title': 'Értékesítés termék', 'termek': termek, 'raktarkeszlet': raktarkeszlet, 'form': form})


def beszallito_list(request):
    beszallitok = Beszallito.objects.all()
    return render(
        request,
        'app/beszallito_list.html',
        {
            'title': 'Beszállítók listája',
            'beszallitok': beszallitok,
        }
    )


def beszallito_new(request):
    if request.method == "POST":
        form = BeszallitoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('beszallito_list')
    else:
        form = BeszallitoForm()

    return render(
        request,
        'app/beszallito_new.html',
        {
            'title': 'Új beszállító létrehozása',
            'form': form
        }
    )


def beszallito_edit(request, pk):
    beszallito = get_object_or_404(Beszallito, pk=pk)
    if request.method == "POST":
        form = BeszallitoForm(request.POST, instance=beszallito)
        if form.is_valid():
            form.save()
            return redirect('beszallito_list')
    else:
        form = BeszallitoForm(instance=beszallito)

    return render(
        request,
        'app/beszallito_edit.html',
        {
            'title': 'Beszállító módosítása',
            'form': form
        }
    )


def bevetel_new(request):
    TermekFormset = formset_factory(BeveteltermekForm)
    current_user = request.user
    hibas_felvitel = []
    if request.method == "POST":
        form = BevetelalapForm(request.POST)
        termekform = TermekFormset(request.POST)
        if form.is_valid() and termekform.is_valid():
            beszallito = form.cleaned_data['beszallito']
            bevetel_datum = form.cleaned_data['bevetel_datum']
            szallitolevel_szam = form.cleaned_data['szallitolevel_szam']
            megjegyzes = form.cleaned_data['megjegyzes']

            if termekform is not None:
                for item in termekform.cleaned_data:
                     try:
                        termek_nev = item['termek']
                        termek_id = item['termek_id']
                        raktar = item['raktar']
                        bevetel_mennyiseg = item['bevetel_mennyiseg']
                        ar_bevetel_netto = item['ar_bevetel_netto']
                        termek = get_object_or_404(Termek, pk=termek_id)

                        bevetelezes = Bevetel(beszallito=beszallito, bevetel_datum=bevetel_datum, szallitolevel_szam=szallitolevel_szam, megjegyzes=megjegyzes, termek=termek, raktar=raktar, bevetel_mennyiseg=bevetel_mennyiseg, ar_bevetel_netto=ar_bevetel_netto, user=current_user)
                        bevetelezes.save()

                        raktarkeszlet = Raktarkeszlet.objects.filter(termek=termek, raktar=raktar)

                        if not raktarkeszlet.count():
                            uj_raktarkeszlet = Raktarkeszlet(raktar=raktar, termek=termek, keszlet=bevetel_mennyiseg)
                            uj_raktarkeszlet.save()
                        else:
                            raktarkeszlet_id = Raktarkeszlet.objects.get(termek=termek, raktar=raktar)
                            raktarkeszlet_mennyiseg = raktarkeszlet_id.keszlet
                            uj_mennyiseg = raktarkeszlet_mennyiseg + bevetel_mennyiseg
                            raktarkeszlet_id.keszlet = uj_mennyiseg
                            raktarkeszlet_id.save()
                     except:
                         hibas_felvitel.append(termek_nev)
            else:
                return HttpResponse('Nincs termék!', content_type="text/plain")
            return redirect('bevetel_new')
    else:
        form = BevetelalapForm()
        termekform = TermekFormset()

    return render(
        request,
        'app/bevetelezes_new.html',
        {
            'title': 'Bevételezés',
            'form': form,
            'termekform': termekform,
            'hibas_felvitel': hibas_felvitel
        }
    )

# Exportok
def export_termek(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="termek_export.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Termékek')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Azonosító', 'Termék név', 'Gyári cikkszám', 'Saját cikkszám', 'Webes nettó ár', 'Bolti bruttó ár',
               'Elhelyezés', 'Minimum készlet', 'Mennyiségi egység', 'Web link', 'Termékkategória', 'Megjegyzés',
               'Aktív']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Termek.objects.all().values_list('id', 'termek_nev', 'gyari_cikkszam', 'sajat_cikkszam', 'ar_web_netto', 'ar_bolt_brutto', 'elhelyezes', 'min_keszlet', 'mennyisegi_egyseg', 'web_link', 'termekkategoria', 'megjegyzes', 'aktiv')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

def export_ertekesit(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="ertekesites_export.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Értékesítések')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Azonosító', 'Termék név', 'Raktár', 'Eladott mennyiség', 'Eladási ár', 'Eladás dátum',
               'Felhasználó', 'Megjegyzés']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Ertekesit.objects.all().values_list('id', 'termek', 'raktar', 'eladas_mennyiseg', 'ar_eladas_brutto', 'eladas_datum', 'user', 'megjegyzes')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

def export_bevetel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="bevetelek_export.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Bevételezések')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Azonosító', 'Beszállító', 'Termék', 'Raktár', 'Bevételezett mennyiség', 'Bevételezési nettó ár',
               'Bevételezés dátuma', 'Szállítólevél száma', 'Felhasználó', 'Megjegyzés']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Bevetel.objects.all().values_list('id', 'beszallito', 'termek', 'raktar', 'bevetel_mennyiseg', 'ar_bevetel_netto', 'bevetel_datum', 'szallitolevel_szam', 'user', 'megjegyzes')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


# API-k
# Értékesítés termék keresés
def get_termek(request):
    if request.is_ajax():
        param = request.GET.get('term', None)
        termek = Termek.objects.filter(Q(termek_nev__icontains=param) | Q(gyari_cikkszam__icontains=param) | Q(sajat_cikkszam__icontains=param))[:20]
        results = []
        for t in termek:
            termek_json = {}
            termek_json['id'] = t.id
            termek_json['value'] = t.termek_nev
            results.append(termek_json)
        data = json.dumps(results)
    else:
        data = 'fail'

    return HttpResponse(data, 'application/json')


# Beszállító autocomplete régi kód
# def get_beszallito(request):
#     if request.is_ajax():
#         param = request.GET.get('term', None)
#         beszallito = Beszallito.objects.filter(beszallito_nev__icontains=param)[:20]
#         results = []
#         for t in beszallito:
#             termek_json = {}
#             termek_json['id'] = t.id
#             termek_json['value'] = t.beszallito_nev
#             results.append(termek_json)
#         data = json.dumps(results)
#     else:
#         data = 'fail'
#
#     return HttpResponse(data, 'application/json')
#
#
def get_termek(request):
    if request.is_ajax():
        param = request.GET.get('term', None)
        termek = Termek.objects.filter(Q(termek_nev__icontains=param) | Q(gyari_cikkszam__icontains=param))[:20]
        results = []
        for t in termek:
            termek_json = {}
            termek_json['id'] = t.id
            termek_json['value'] = t.gyari_cikkszam + " - " + t.termek_nev
            results.append(termek_json)
        data = json.dumps(results)
    else:
        data = 'fail'

    return HttpResponse(data, 'application/json')


class TermekAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Termek.objects.none()

        qs = Termek.objects.all()

        if self.q:
            qs = qs.filter(termek_nev__icontains=self.q)

        return qs


class BeszallitoAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Beszallito.objects.none()

        qs = Beszallito.objects.all()

        if self.q:
            qs = qs.filter(beszallito_nev__icontains=self.q)

        return qs