from app.models import Termek_Osszdb
from django.core.mail import send_mail
from django.http import HttpResponse

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