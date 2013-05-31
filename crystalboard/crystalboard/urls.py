from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'crystalboard.views.home', name='home'),
    # url(r'^crystalboard/', include('crystalboard.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^$', 'principal.views.ingreso_usuario'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'principal.views.ingreso_usuario'),
    url(r'^perfil/$', 'principal.views.perfil'),
    url(r'^conectar/dropbox/$', 'principal.views.conectar_dropbox'),

    url(r'^(?P<cur>[0-9]+)/(?P<avso>[0-9]+)/$', 'principal.views.comentarios'),
    url(r'^(?P<cur>[0-9]+)/$', 'principal.views.cursodash'),
    url(r'^dashboard/$', 'principal.views.dashboard'),
    url(r'^(?P<cur>[0-9]+)/listas/$', 'principal.views.listas'),
    url(r'^(?P<cur>[0-9]+)/tareas/$', 'principal.views.tareas'),
    url(r'^(?P<cur>[0-9]+)/tareas/(?P<tar>[0-9]+)/$', 'principal.views.tarea'),
)
