from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from app.models import Raktar
from app.models import Ertekesit
from app.models import Beszallito
from app.models import Dokumentum
from app.models import Termek
from app.models import TermekKategoria, TermekGyarto
from dal import autocomplete


class BootstrapAuthenticationForm(AuthenticationForm):
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Név'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder': 'Jelszó'}))


class TermekSearchForm(forms.Form):
    autocomplete = forms.CharField(label='Keres: ', max_length=100)
    autocomplete_id = forms.IntegerField(required=False)


class DokForm(forms.ModelForm):
    dok_nev = forms.CharField(required=True, label="Dokumentum neve")
    dokfile = forms.FileField(label='Feltöltés')

    class Meta(forms.ModelForm):
        model = Dokumentum
        fields = ('dok_nev', 'dokfile')


class TermekForm(forms.ModelForm):
    termek_nev = forms.CharField(label='Termék neve: ', max_length=255, required=True)
    gyari_cikkszam = forms.CharField(label='Gyári cikkszám: ', max_length=255, required=True)
    sajat_cikkszam = forms.CharField(label='Saját cikkszám: ', max_length=255, required=False)
    ar_web_netto = forms.DecimalField(label='Webes nettó ár: ', required=True)
    ar_bolt_brutto = forms.IntegerField(label='Bolti bruttó ár: ', required=True)
    elhelyezes = forms.CharField(label='Elhelyezés: ', max_length=255, required=True)
    min_keszlet = forms.DecimalField(label='Minimum készlet: ', required=True)
    mennyisegi_egyseg = forms.ChoiceField(
        required=True,
        label="Mennyiségi egység",
        widget=forms.Select,
        choices=Termek.MENNYISEGI_EGYSEG,
    )
    web_link = forms.URLField(label='Web link: ', max_length=255, required=False)
    termekkategoria = forms.ModelChoiceField(queryset=TermekKategoria.objects.all(), empty_label="Kérem válasszon", required=True, label="Termékkategória")
    termekgyarto = forms.ModelChoiceField(queryset=TermekGyarto.objects.all(), empty_label="Kérem válasszon", required=False, label="Termék gyártó")

    aktiv = forms.BooleanField(label='Aktív: ', initial=True, required=False)
    megjegyzes = forms.CharField(required=False, label="Megjegyzés", widget=forms.Textarea)

    class Meta(forms.ModelForm):
        model = Termek
        fields = ('__all__')


class TermekKategoriaForm(forms.ModelForm):
    termekkategoria = forms.CharField(label='Termékkategória neve: ', max_length=255, required=True)

    class Meta(forms.ModelForm):
        model = TermekKategoria
        fields = ('__all__')


class TermekGyartoForm(forms.ModelForm):
    termekgyarto = forms.CharField(label='Termék gyártó neve: ', max_length=255, required=False)

    class Meta(forms.ModelForm):
        model = TermekGyarto
        fields = ('__all__')


class ErtekesitForm(forms.ModelForm):
    def __init__(self, current_user, *args, **kwargs):
        super(ErtekesitForm, self).__init__(*args, **kwargs)
        self.fields['raktar'].queryset = Raktar.objects.filter(user=current_user)
        self.fields['raktar'].empty_label = None
        self.fields['raktar'].required = True

    eladas_mennyiseg = forms.DecimalField(label='Mennyiség: ', required=True)
    ar_eladas_brutto = forms.IntegerField(label='Eladási ár: ', required=True)
    # raktar = forms.ModelChoiceField(queryset= Raktar.objects.filter(user=current_user), required=True, label='Raktárból: ', empty_label=None)
    megjegyzes = forms.CharField(required=False, label="Megjegyzés", widget=forms.Textarea)

    class Meta(forms.ModelForm):
        model = Ertekesit
        fields = ('raktar', 'eladas_mennyiseg', 'ar_eladas_brutto', 'megjegyzes')


class BeszallitoForm(forms.ModelForm):
    beszallito_nev = forms.CharField(label='Beszállító neve: ', max_length=255, required=True)
    beszallito_cim = forms.CharField(label='Beszállító címe: ', max_length=255, required=False)
    beszallito_ugyintezo = forms.CharField(label='Ügyintéző: ', max_length=255, required=False)
    beszallito_email = forms.EmailField(label='Email cím: ', max_length=255, required=False)
    beszallito_telefon = forms.CharField(label='Telefon: ', max_length=255, required=False)
    megjegyzes = forms.CharField(required=False, label="Megjegyzés", widget=forms.Textarea)

    class Meta(forms.ModelForm):
        model = Beszallito
        fields = ('beszallito_nev', 'beszallito_cim', 'beszallito_ugyintezo', 'beszallito_email', 'beszallito_telefon', 'megjegyzes')


class BeveteltermekForm(forms.Form):
    # termek = forms.ModelChoiceField(queryset=Termek.objects.all(), widget=autocomplete.ModelSelect2(url='termek-autocomplete'))
    # termek = forms.ModelChoiceField(queryset=Termek.objects.all(), empty_label="Kérem válasszon", required=True, label="Termék")
    termek = forms.CharField(required=True, label="Termék")
    termek_id = forms.CharField(required=True, label="Termék_id", widget=forms.HiddenInput())
    raktar = forms.ModelChoiceField(queryset=Raktar.objects.all(), empty_label="Kérem válasszon", required=True, label="Raktár")
    bevetel_mennyiseg = forms.DecimalField(label='Mennyiség: ', required=True)
    ar_bevetel_netto = forms.DecimalField(label='Nettó ár: ', required=False)


class BevetelalapForm(forms.Form):
    # beszallito = forms.CharField(required=True, label="Beszállító")
    # beszallito = forms.ModelChoiceField(queryset=Beszallito.objects.all(), required=True, label="Beszállító")
    beszallito = forms.ModelChoiceField(queryset=Beszallito.objects.all(), widget=autocomplete.ModelSelect2(url='beszallito-autocomplete'))
    bevetel_datum = forms.DateField(required=True, label="Bevételezés dátuma", widget=forms.TextInput(attrs={'class':'datum'}))
    szallitolevel_szam = forms.CharField(label='Szállítólevél száma: ', max_length=255, required=False)
    megjegyzes = forms.CharField(required=False, label="Megjegyzés", widget=forms.Textarea(attrs={'rows': 4}))
    # termekek = TermekFormset()


# Termék átvezetés Formok
class TermekAtvazetAlapForm(forms.Form):
    raktarbol = forms.ModelChoiceField(queryset=Raktar.objects.all(), empty_label="Kérem válasszon", required=True, label="Raktárból")
    raktarba = forms.ModelChoiceField(queryset=Raktar.objects.all(), empty_label="Kérem válasszon", required=True, label="Raktárba")


class TermekAtvezetTermekForm(forms.Form):
    termek = forms.CharField(required=True, label="Termék")
    termek_id = forms.CharField(required=True, label="Termék_id", widget=forms.HiddenInput())
    mennyiseg = forms.DecimalField(label='Mennyiség: ', required=True)


class TermekImport(forms.Form):
    termekek = forms.FileField(label='Feltöltés', help_text='csv fájl, utf-8 BOM nélkül, az első sort törölni kell a mintából, <a href="/media/export/termek_import_minta.csv">Minta fájl</a>')
