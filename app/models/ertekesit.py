from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from app.models import Raktar
from app.models import Termek

class Ertekesit(models.Model):
    termek = models.ForeignKey(Termek, blank=False, null=False)
    raktar = models.ForeignKey(Raktar, blank=False, null=False)
    eladas_mennyiseg = models.DecimalField(max_digits=9, decimal_places=2, blank=False, null=False)
    ar_eladas_brutto = models.IntegerField(validators=[MinValueValidator(0)], blank=False, null=False)
    eladas_datum = models.DateField(blank=False, null=False)
    megjegyzes = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, related_name='user_ertekesit', related_query_name="ertekesito")

    class Meta:
        verbose_name_plural = "Értékesítések"

    def __str__(self):
        return str(self.termek)