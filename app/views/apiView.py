from django.http import HttpResponse
from django.db.models import Q
from django.utils import timezone
from app.forms import Beszallito
from app.models import Termek
from dal import autocomplete
from django.contrib.auth.decorators import login_required
import urllib.request
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
import os
import json
import csv


# API-k
# Értékesítés termék keresés
@login_required(login_url='/login/')
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


class TermekAutocomplete(LoginRequiredMixin, autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Termek.objects.none()

        qs = Termek.objects.all()

        if self.q:
            qs = qs.filter(termek_nev__icontains=self.q)

        return qs


class BeszallitoAutocomplete(LoginRequiredMixin, autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Beszallito.objects.none()

        qs = Beszallito.objects.all()

        if self.q:
            qs = qs.filter(beszallito_nev__icontains=self.q)

        return qs


@login_required(login_url='/login/')
def web_ar_mod(request):
    try:
        url = 'http://www.hegeszteskozpont.hu/export_price_api.phpa'
        # url = 'http://www.hegeszteskozpont.hu/media/export/export_csv.csv'
        web_file = urllib.request.urlopen(url).read()
        with open(os.path.join(settings.MEDIA_ROOT, 'export/ar_import.csv'), 'wb+') as csvfile:
            csvfile.write(web_file)

        with open(os.path.join(settings.MEDIA_ROOT, 'export/ar_import.csv'), 'r', newline='') as ar_import:
            reader = csv.reader(ar_import, delimiter=',',)
            for row in reader:
                try:
                    sku = row[0]
                    ar = float(row[1])
                    # print(sku+" "+ar)

                    termek = Termek.objects.get(gyari_cikkszam=sku)
                    # print(termek.ar_web_netto)
                    if termek.ar_web_netto != ar:
                        # print("Nem")
                        termek.ar_web_netto = ar
                        termek.save()
                except:
                    pass
    except:
        today = timezone.now()
        with open(os.path.join(settings.MEDIA_ROOT, 'export/error_log.csv'), 'a+', encoding='utf-8') as error_log:
            error_log.write(str(today) + " -  Ár módosítás valami nem volt jó! \n")

    return HttpResponse('Ok', content_type="text/plain")