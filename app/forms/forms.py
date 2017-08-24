from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from app.models import Raktar
from app.models import Ertekesit
from app.models import Beszallito
from app.models import Termek
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


def get_user(request):
    user = request.user.id
    return user

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


    # class Meta(forms.ModelForm):
    #     model = Bevetel
    #     fields = ('beszallito', 'termek', 'raktar', 'bevetel_mennyiseg', 'ar_bevetel_netto', 'bevetel_datum', 'szallitolevel_szam', 'megjegyzes')