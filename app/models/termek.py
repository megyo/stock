from django.db import models
from django.core.validators import URLValidator
from django.core.validators import MinValueValidator


class TermekGyarto(models.Model):
    termekgyarto = models.CharField(max_length=255, blank=False, null=False, unique=True)

    class Meta:
        verbose_name_plural = "Termék gyártók"
        ordering = ('termekgyarto',)

    def __str__(self):
        return self.termekgyarto


class TermekKategoria(models.Model):
    termekkategoria = models.CharField(max_length=255, blank=False, null=False, unique=True)

    class Meta:
        verbose_name_plural = "Termék kategóriák"
        ordering = ('termekkategoria',)

    def __str__(self):
        return self.termekkategoria


class Termek(models.Model):
    MENNYISEGI_EGYSEG = (
        ('', 'Kérem válasszon'),
        ('Csomag', 'Csomag'),
        ('db', 'db'),
        ('kg', 'Kilogramm'),
        ('Méter', 'Méter'),
    )
    termek_nev = models.CharField(max_length=255, blank=False, null=False)
    gyari_cikkszam = models.CharField(max_length=255, blank=False, null=False)
    sajat_cikkszam = models.CharField(max_length=255, blank=True, null=True)
    ar_web_netto = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    ar_bolt_brutto = models.IntegerField(validators=[MinValueValidator(0)], blank=False, null=False)
    elhelyezes = models.CharField(max_length=255, blank=True, null=True)
    min_keszlet = models.IntegerField(validators=[MinValueValidator(0)], blank=False, null=False)
    mennyisegi_egyseg = models.CharField(max_length=255, choices=MENNYISEGI_EGYSEG, blank=False, null=False)
    web_link = models.TextField(validators=[URLValidator()], blank=True, null=True)
    termekkategoria = models.ForeignKey(TermekKategoria, blank=False, null=False)
    termekgyarto = models.ForeignKey(TermekGyarto, blank=True, null=True)
    megjegyzes = models.TextField(blank=True, null=True)
    aktiv = models.BooleanField()

    class Meta:
        verbose_name_plural = "Termékek"
        unique_together = ('gyari_cikkszam', 'termek_nev')

    def __str__(self):
        return str(self.termek_nev)

