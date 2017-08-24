
from datetime import datetime
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include
from django.contrib import admin
import django.contrib.auth.views
import app.forms
import app.views
import debug_toolbar
from app.views import TermekAutocomplete
from app.views import BeszallitoAutocomplete

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


    # Alap URL
    url(r'^$', app.views.index, name='index'),
    url(r'^ertekesites_termek/(?P<pk>[0-9]+)/show/$', app.views.ertekesites_termek, name='ertekesites_termek'),
    url(r'^beszallito/$', app.views.beszallito_list, name='beszallito_list'),
    url(r'^beszallito/new$', app.views.beszallito_new, name='beszallito_new'),
    url(r'^beszallito/(?P<pk>[0-9]+)/edit$', app.views.beszallito_edit, name='beszallito_edit'),
    url(r'^bevetel/new$', app.views.bevetel_new, name='bevetel_new'),

    # Export URL
    url(r'^export_termek/$', app.views.export_termek, name='export_termek'),
    url(r'^export_ertekesit/$', app.views.export_ertekesit, name='export_ertekesit'),
    url(r'^export_bevetel/$', app.views.export_bevetel, name='export_bevetel'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [url(r'^__debug__/', include(debug_toolbar.urls)),]