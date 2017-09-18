from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
import json
import csv
from django.db.models import Q
from django.utils import timezone
from app.forms import TermekSearchForm, BevetelalapForm, BeveteltermekForm
from app.forms import ErtekesitForm
from app.forms import BeszallitoForm
from app.forms import TermekForm
from app.forms import Beszallito
from app.forms import DokForm
from app.forms import TermekImport
from app.forms import TermekKategoriaForm
from app.models import TermekKategoria
from app.models import Termek, Termek_Osszdb
from app.models import Raktarkeszlet
from app.models import Bevetel
from app.models import Dokumentum
# from app.models import Ertekesit
from app.models import termek_riport
# from app.models import Raktar
from django.core.urlresolvers import reverse
from django.forms import formset_factory
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
import os
from django.core.mail import send_mail
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder


@login_required(login_url='/login/')
def dok_list(request, pk):
    dok_list = Dokumentum.objects.filter(termek_id=pk).order_by('felt_datum').reverse()
    termek = Termek.objects.get(id=pk)
    termek_nev = termek.termek_nev

    return render(request, 'app/dok_list.html',
                  {'title': 'Dokumentumok', 'doklist': dok_list, 'termeknev': termek_nev, 'termek_id': pk})


@staff_member_required(login_url='/login/')
def dok_new(request, pk):
    if request.method == "POST":
        form = DokForm(request.POST, request.FILES)
        if form.is_valid():
            dok = form.save(commit=False)
            today = timezone.now()
            dok.felt_datum = today
            dok.termek_id = pk
            dok.save()
            return redirect('dok_list', pk=pk)
    else:
        form = DokForm()
    return render(request, 'app/dok_new.html', {'form': form})


@staff_member_required(login_url='/login/')
def dok_del(request, pk, termek_id):
    dok = Dokumentum.objects.get(id=pk)
    docnev = str(dok.dokfile)
    dok.delete()

    try:
        os.remove(os.path.join(settings.MEDIA_ROOT, docnev))

    except ValueError:
        print("Valami gáz van...")

    return redirect('dok_list', pk=termek_id)


@login_required(login_url='/login/')
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


@login_required(login_url='/login/')
def termek_list(request):
    termek_list = termek_riport.objects.all().values()
    termekek = json.dumps(list(termek_list), ensure_ascii=False, cls=DjangoJSONEncoder)

    return render(
        request,
        'app/termek_list.html',
        {
            'title': 'Termékek listája',
            'termekek': termekek,
        }
    )


@staff_member_required(login_url='/login/')
def termek_new(request):
    if request.method == "POST":
        form = TermekForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('termek_list')
    else:
        form = TermekForm()

    return render(
        request,
        'app/termek_new.html',
        {
            'title': 'Új termék létrehozása',
            'form': form
        }
    )


@staff_member_required(login_url='/login/')
def termek_edit(request, pk):
    termek = get_object_or_404(Termek, pk=pk)
    if request.method == "POST":
        form = TermekForm(request.POST, instance=termek)
        if form.is_valid():
            form.save()
            return redirect('termek_list')
    else:
        form = TermekForm(instance=termek)

    return render(
        request,
        'app/termek_edit.html',
        {
            'title': 'Termék módosítása',
            'form': form
        }
    )


@staff_member_required(login_url='/login/')
def termekkategoria_list(request):
    termekkategoria_list = TermekKategoria.objects.all().values()
    termekkategoria = json.dumps(list(termekkategoria_list), ensure_ascii=False, cls=DjangoJSONEncoder)

    return render(
        request,
        'app/termekkategoria_list.html',
        {
            'title': 'Termékkategóriák listája',
            'termekkategoria': termekkategoria,
        }
    )



@staff_member_required(login_url='/login/')
def termekkategoria_new(request):
    if request.method == "POST":
        form = TermekKategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('termekkategoria_list')
    else:
        form = TermekKategoriaForm()

    return render(
        request,
        'app/termekkategoria_new.html',
        {
            'title': 'Új termékkategoria létrehozása',
            'form': form
        }
    )


@staff_member_required(login_url='/login/')
def termekkategoria_edit(request, pk):
    termekkategoria = get_object_or_404(TermekKategoria, pk=pk)
    if request.method == "POST":
        form = TermekKategoriaForm(request.POST, instance=termekkategoria)
        if form.is_valid():
            form.save()
            return redirect('termekkategoria_list')
    else:
        form = TermekKategoriaForm(instance=termekkategoria)

    return render(
        request,
        'app/termekkategoria_edit.html',
        {
            'title': 'Termékkategória módosítása',
            'form': form
        }
    )

@login_required(login_url='/login/')
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


@login_required(login_url='/login/')
def beszallito_list(request):
    beszallitok_list = Beszallito.objects.all().values()
    beszallitok = json.dumps(list(beszallitok_list), ensure_ascii=False, cls=DjangoJSONEncoder)

    return render(
        request,
        'app/beszallito_list.html',
        {
            'title': 'Beszállítók listája',
            'beszallitok': beszallitok,
        }
    )


@staff_member_required(login_url='/login/')
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


@staff_member_required(login_url='/login/')
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


@staff_member_required(login_url='/login/')
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
                        try:
                            hibas_felvitel.append(termek_nev)
                        except:
                            pass
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


@staff_member_required(login_url='/login/')
def termek_import(request):
    hiba_import = []
    with open(os.path.join(settings.MEDIA_ROOT, 'export/termek_import.csv'), 'r', encoding='utf-8') as termek_import:
        reader = csv.reader(termek_import, delimiter=';')
        for index, row in enumerate(reader):
            try:
                termek_nev = row[0].strip()
                gyari_cikkszam = row[1].strip()
                sajat_cikkszam = row[2].strip()
                ar_web_netto = float(row[3].strip())
                ar_bolt_brutto = int(row[4].strip())
                elhelyezes = row[5].strip()
                min_keszlet = int(row[6].strip())
                mennyisegi_egyseg = row[7].strip()
                web_link = row[8].strip()
                termekkat = int(row[9].strip())
                megjegyzes = row[10].strip()
                aktiv = row[11].strip()
                termekkategoria = TermekKategoria.objects.get(pk=termekkat)

                termek = Termek(termek_nev=termek_nev, gyari_cikkszam=gyari_cikkszam, sajat_cikkszam=sajat_cikkszam, ar_web_netto=ar_web_netto,
                                ar_bolt_brutto=ar_bolt_brutto, elhelyezes=elhelyezes, min_keszlet=min_keszlet, mennyisegi_egyseg=mennyisegi_egyseg,
                                web_link=web_link, termekkategoria=termekkategoria, megjegyzes=megjegyzes, aktiv=aktiv)
                termek.save()
            except:
                h = str(index+1) + " - " + termek_nev
                hiba_import.append(h)

    # Hibára futott import termékek file-ba írása
    with open(os.path.join(settings.MEDIA_ROOT, 'export/termek_import_error.csv'), 'w', encoding='utf-8') as termek_import_error:
        termek_import_error.write('\n'.join(hiba_import))

    # ha van hiba akkor paraméterrel átirányít
    if not hiba_import:
        return redirect('termek_import_feltolt')
    else:
        return redirect(reverse('termek_import_feltolt') + '?hiba=1')

@staff_member_required(login_url='/login/')
def termek_import_feltolt(request):
    form = TermekImport()
    termek_lista = []
    hiba_import = ""
    termek_import_hiba = False

    # Importálandó termékek file törlése
    if os.path.isfile(os.path.join(settings.MEDIA_ROOT, 'export/termek_import.csv')):
        os.remove(os.path.join(settings.MEDIA_ROOT, 'export/termek_import.csv'))

    # Ha létezik a termék imoprt hiba paraméter akkor a nézetben megjelenítjük a hibafile linket
    if request.method == 'GET' and 'hiba' in request.GET:
        hiba = request.GET['hiba']

        if hiba == '1':
            termek_import_hiba = True

    if request.method == "POST" and request.FILES['termekek']:
        # Nem importált termékek file törlése
        if os.path.isfile(os.path.join(settings.MEDIA_ROOT, 'export/termek_import_error.csv')):
            os.remove(os.path.join(settings.MEDIA_ROOT, 'export/termek_import_error.csv'))
            termek_import_hiba = False

        # Termék import file létrehozása
        myfile = request.FILES['termekek']
        fs = FileSystemStorage()
        filename = fs.save(os.path.join(settings.MEDIA_ROOT,'export/termek_import.csv'), myfile)
        # uploaded_file_url = fs.url(filename)

        # Ha sikerült megnyitni a termék import file-t akkor beolvasom, ha nem törlöm az import file-t és error log létrehozás
        try:
            with open(os.path.join(settings.MEDIA_ROOT, 'export/termek_import.csv'), 'r', encoding='utf-8') as termek_import:
                sorok = csv.reader(termek_import, delimiter=';',)
                termek_lista = list(sorok)
        except:
            today = timezone.now()
            with open(os.path.join(settings.MEDIA_ROOT, 'export/error_log.csv'), 'a+', encoding='utf-8') as error_log:
                error_log.write(str(today) + " -  File betöltés valami nem volt jó! \n")
                hiba_import = "Hibás a betöltött fájl!"
                termek_lista = []

                if os.path.isfile(os.path.join(settings.MEDIA_ROOT, 'export/termek_import.csv')):
                    os.remove(os.path.join(settings.MEDIA_ROOT, 'export/termek_import.csv'))

    return render(request, 'app/termek_import.html', {'form': form, 'title': 'Termék import', 'termek_lista': termek_lista, 'hiba_import': hiba_import, 'termek_hiba': termek_import_hiba})


def email_termek_osszdb(request):
    raktar_keszlet = Termek_Osszdb.objects.all()
    email_kuld = False
    email_szoveg = "Kedves Péter!\n\nA következő termékeknek csökkent a készlete a megadott minimum alá: \n\n"

    for k in raktar_keszlet:
        min_keszlet = k.min_keszlet
        akt_keszlet = k.keszlet
        if akt_keszlet < min_keszlet:
            email_kuld = True
            email_szoveg += "Termék neve: " + k.termek_nev + " -- Gyári cikkszáma: " + k.gyari_cikkszam + " -- Jelenlegi készlet: " + str(k.keszlet) + "\n"

    if email_kuld:
        pass
        # send_mail(
        #     'Raktárkészlet figyelés',
        #     email_szoveg,
        #     'info@hegesztescentrum.hu',
        #     ['medgyesi.peter@gmail.com'],
        #     fail_silently=False,
        # )

    return HttpResponse(email_szoveg, content_type="text/plain")
