import os
import csv
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.utils import timezone
from app.forms import ErtekesitForm
from app.forms import TermekForm
from app.forms import TermekImport
from app.forms import TermekAtvazetAlapForm
from app.forms import TermekAtvezetTermekForm
from app.models import TermekKategoria
from app.models import Termek
from app.models import Raktarkeszlet
from django.core.urlresolvers import reverse
from django.forms import formset_factory
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.files.storage import FileSystemStorage
from django.conf import settings


@login_required(login_url='/login/')
def termek_list(request):
    # termek_list = termek_riport.objects.all().values()
    # termekek = json.dumps(list(termek_list), ensure_ascii=False, cls=DjangoJSONEncoder)

    return render(
        request,
        'app/termek_list.html',
        {
            'title': 'Termékek listája',
            # 'termekek': termekek,
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
def termek_atvezetes(request):
    TermekFormset = formset_factory(TermekAtvezetTermekForm)
    hibas_felvitel = []

    if request.method == "POST":
        form = TermekAtvazetAlapForm(request.POST)
        termekform = TermekFormset(request.POST)

        if form.is_valid() and termekform.is_valid():
            raktarbol = form.cleaned_data['raktarbol']
            raktarba = form.cleaned_data['raktarba']

            if raktarbol == raktarba:
                hibas_felvitel.append("Egyező raktárak!")

            if termekform is not None and raktarbol != raktarba:
                for item in termekform.cleaned_data:
                     try:
                        termek_nev = item['termek']
                        termek_id = item['termek_id']
                        mennyiseg = item['mennyiseg']
                        termek = get_object_or_404(Termek, pk=termek_id)

                        raktarkeszletbol = Raktarkeszlet.objects.get(termek=termek, raktar=raktarbol)
                        raktarkeszletbe = Raktarkeszlet.objects.get(termek=termek, raktar=raktarba)

                        jelenlegi_mennyiseg_bol = raktarkeszletbol.keszlet
                        jelenlegi_mennyiseg_be = raktarkeszletbe.keszlet

                        if mennyiseg > jelenlegi_mennyiseg_bol:
                            hibas_felvitel.append(termek_nev + " -- " + str(jelenlegi_mennyiseg_bol) + "-bol " + str(mennyiseg) + " -t szeretett volna átvezetni.")
                        else:
                            aktualis_mennyiseg_bol = jelenlegi_mennyiseg_bol - mennyiseg
                            raktarkeszletbol.keszlet = aktualis_mennyiseg_bol
                            raktarkeszletbol.save()

                            aktualis_mennyiseg_be = mennyiseg + jelenlegi_mennyiseg_be
                            raktarkeszletbe.keszlet = aktualis_mennyiseg_be
                            raktarkeszletbe.save()

                     except:
                        try:
                            hibas_felvitel.append(termek_nev + " -  Nem átvezethető")
                        except:
                            pass
            else:
                pass #return HttpResponse('Nincs termék!', content_type="text/plain")
            # return redirect('termek_atvezetes')
    # else:
    form = TermekAtvazetAlapForm()
    termekform = TermekFormset()

    return render(
        request,
        'app/termek_atvezetes.html',
        {
            'title': 'Termék átvezetés',
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
                termekkat = int(row[8].strip())
                aktiv = row[9].strip()
                megjegyzes = row[10].strip()
                web_link = row[11].strip()
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
