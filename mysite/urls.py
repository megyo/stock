
from datetime import datetime
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include
from django.contrib import admin
import django.contrib.auth.views
from app.views import TermekAutocomplete
from app.views import BeszallitoAutocomplete
import app.views
import debug_toolbar

# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
# from django.contrib import admin
# admin.autodiscover()
urlpatterns = [
    url(r'^login/$',
        django.contrib.auth.views.login,
        {
            'template_name': 'app/login.html',
            'authentication_form': app.forms.BootstrapAuthenticationForm,
            'extra_context':
            {
                'title': 'Log in',
                'year': datetime.now().year,
            }
        },
        name='login'),
    url(r'^logout$',
        django.contrib.auth.views.logout,
        {
            'next_page': '/',
        },
        name='logout'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^password/$', app.views.change_password, name='change_password'),

    # API URL
    url(r'^api/get_termek/$', app.views.get_termek, name='get_termek'),
    url(r'^termek-autocomplete/$', TermekAutocomplete.as_view(), name='termek-autocomplete', ),
    url(r'^beszallito-autocomplete/$', BeszallitoAutocomplete.as_view(), name='beszallito-autocomplete', ),
    # url(r'^api/get_beszallito/$', app.views.get_beszallito, name='get_beszallito'),
    url(r'^api/get_termekapi/$', app.views.get_termek_api, name='get_termekapi'),


    # Alap URL
    url(r'^$', app.views.index, name='index'),
    url(r'^ertekesites_termek/(?P<pk>[0-9]+)/show/$', app.views.ertekesites_termek, name='ertekesites_termek'),
    url(r'^beszallito/$', app.views.beszallito_list, name='beszallito_list'),
    url(r'^beszallito/new$', app.views.beszallito_new, name='beszallito_new'),
    url(r'^beszallito/(?P<pk>[0-9]+)/edit$', app.views.beszallito_edit, name='beszallito_edit'),
    url(r'^bevetel/new$', app.views.bevetel_new, name='bevetel_new'),
    url(r'^termekatvezetes$', app.views.termek_atvezetes, name='termek_atvezetes'),

    url(r'^termek/$', app.views.termek_list, name='termek_list'),
    url(r'^termek/new$', app.views.termek_new, name='termek_new'),
    url(r'^termek/(?P<pk>[0-9]+)/edit$', app.views.termek_edit, name='termk_edit'),

    url(r'^termekkategoria/$', app.views.termekkategoria_list, name='termekkategoria_list'),
    url(r'^termekkategoria/new$', app.views.termekkategoria_new, name='termekkategoria_new'),
    url(r'^termekkategoria/(?P<pk>[0-9]+)/edit$', app.views.termekkategoria_edit, name='termekkategoria_edit'),

    url(r'^dokumentum/(?P<pk>[0-9]+)/list$', app.views.dok_list, name='dok_list'),
    url(r'^dokumentum/(?P<pk>[0-9]+)/new$', app.views.dok_new, name='dok_new'),
    url(r'^dokumentum/(?P<pk>[0-9]+)/(?P<termek_id>[0-9]+)/del$', app.views.dok_del, name='dok_del'),

    url(r'^termekimportfel/$', app.views.termek_import_feltolt, name='termek_import_feltolt'),
    url(r'^termekimport/$', app.views.termek_import, name='termek_import'),

    url(r'^webarmod/$', app.views.web_ar_mod, name='web_ar_mod'),
    url(r'^termekosszdb/$', app.views.email_termek_osszdb, name='email_termek_osszdb'),


    # Export URL
    url(r'^export_termek/$', app.views.export_termek, name='export_termek'),
    url(r'^export_ertekesit/$', app.views.export_ertekesit, name='export_ertekesit'),
    url(r'^export_bevetel/$', app.views.export_bevetel, name='export_bevetel'),
    url(r'^export_raktarkeszlet/$', app.views.export_raktarkeszlet, name='export_raktarkeszlet'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [url(r'^__debug__/', include(debug_toolbar.urls)),]