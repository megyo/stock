from app.models import Termek_Osszdb
from django.core.mail import send_mail
from django.http import HttpResponse
from django.utils import timezone
from app.models import Termek
from django.contrib.auth.decorators import login_required
import urllib.request
from django.conf import settings
import os
import csv


@login_required(login_url='/login/')
def email(request):
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
        send_mail(
            'Raktárkészlet figyelés',
            email_szoveg,
            'info@hegesztescentrum.hu',
            ['medgyesi.peter@gmail.com'],
            fail_silently=False,
        )

    return HttpResponse(email_szoveg, content_type="text/plain")


# Webáruház ár szinkron
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