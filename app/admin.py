from django.contrib import admin
from .models import *


admin.site.register(Raktar)
# admin.site.register(Ertekesit)
# admin.site.register(Termek)
# admin.site.register(TermekKategoria)
# admin.site.register(Beszallito)
# admin.site.register(Raktarkeszlet)


class BevetelAdmin(admin.ModelAdmin):
    list_display = ('bevetel_datum', 'szallitolevel_szam', 'beszallito', 'raktar', 'termek', 'bevetel_mennyiseg')
    list_filter = ('bevetel_datum','raktar','beszallito')
    def has_add_permission(self, request):
        return False
    # search_fields = ('tartozektipus',)

admin.site.register(Bevetel, BevetelAdmin)

