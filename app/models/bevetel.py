from django.db import models
from app.models import Beszallito
from app.models import Termek
from app.models import Raktar
from django.core.validators import MinValueValidator

class Bevetel(models.Model):
    beszallito = models.ForeignKey(Beszallito, blank=False, null=False)
    termek = models.ForeignKey(Termek, blank=False, null=False)
    raktar = models.ForeignKey(Raktar, blank=False, null=False)
    bevetel_mennyiseg = models.DecimalField(max_digits=9, decimal_places=2, blank=False, null=False)
    ar_bevetel_netto = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    bevetel_datum = models.DateField(blank=False, null=False)
    szallitolevel_szam = models.CharField(max_length=255, blank=True, null=True)
    megjegyzes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Bételezés"

    def __str__(self):
        return str(self.beszallito)