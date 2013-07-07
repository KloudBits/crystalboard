from django.conf.urls import patterns, include, url
from django.conf import settings

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
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT,}),

    url(r'^$', 'principal.views.ingreso_usuario'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'principal.views.ingreso_usuario'),
    url(r'^perfil/$', 'principal.views.perfil'),
    #url(r'^conectar/dropbox/$', 'principal.views.conectar_dropbox'),

    url(r'^(?P<cur>[0-9]+)/(?P<avso>[0-9]+)/$', 'principal.views.comentarios'),
    url(r'^(?P<cur>[0-9]+)/$', 'principal.views.cursodash'),
    url(r'^(?P<cur>[0-9]+)/info/$', 'principal.views.informacion'),
    url(r'^(?P<cur>[0-9]+)/docente/$', 'principal.views.docente'),
    url(r'^(?P<cur>[0-9]+)/directorio/$', 'principal.views.directorio'),
    url(r'^dashboard/$', 'principal.views.dashboard'),
    url(r'^(?P<cur>[0-9]+)/listas/$', 'principal.views.listas'),
    url(r'^(?P<cur>[0-9]+)/tareas/$', 'principal.views.tareas'),
    url(r'^(?P<cur>[0-9]+)/tareas/(?P<tar>[0-9]+)/$', 'principal.views.tarea'),
    url(r'^(?P<cur>[0-9]+)/clases/(?P<cls>[0-9]+)/$', 'principal.views.clase'),
    url(r'^(?P<cur>[0-9]+)/clases/(?P<cls>[0-9]+)/editar/$', 'principal.views.editar_clase'),

    url(r'^media/(?P<path>.*)$','django.views.static.serve', 
        {'document_root':settings.MEDIA_ROOT,}),
)
