from django.db import models
from app.models import Termek
from django.core.validators import MinValueValidator


class Raktar(models.Model):
    raktar_nev = models.CharField(max_length=255, blank=False, null=False, unique=True)
    megjegyzes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Raktárak"

    def __str__(self):
        return self.raktar_nev


class Raktarkeszlet(models.Model):
    termek = models.ForeignKey(Termek, blank=False, null=False)
    raktar = models.ForeignKey(Raktar, blank=False, null=False)
    keszlet = models.DecimalField(max_digits=9, decimal_places=2, blank=False, null=False)

    class Meta:
        verbose_name_plural = "Raktárkészlet"
        unique_together = ('termek', 'raktar')

    def __str__(self):
        return str(self.termek) + "   " + str(self.keszlet)