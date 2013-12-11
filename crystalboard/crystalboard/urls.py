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
    url(r'^logout/$', 'principal.views.egreso_usuario'),
    url(r'^perfil/$', 'principal.views.perfil'),
    #url(r'^conectar/dropbox/$', 'principal.views.conectar_dropbox'),

    # URL para crear nuevo curso
    url(r'^nuevo_curso/$', 'principal.views.nuevo_curso'),

    url(r'^(?P<cur>[0-9]+)/(?P<avso>[0-9]+)/$', 'principal.views.comentarios'),
    url(r'^(?P<cur>[0-9]+)/$', 'principal.views.cursodash'),
    url(r'^(?P<cur>[0-9]+)/info/$', 'principal.views.informacion'),
    url(r'^(?P<cur>[0-9]+)/docente/$', 'principal.views.docente'),
    url(r'^(?P<cur>[0-9]+)/directorio/$', 'principal.views.directorio'),
    url(r'^dashboard/$', 'principal.views.dashboard'),
    url(r'^(?P<cur>[0-9]+)/clases/(?P<clse>[0-9]+)/lista/$', 'principal.views.lista'),
    url(r'^(?P<cur>[0-9]+)/clases/(?P<clse>[0-9]+)/eliminar/$', 'principal.views.clase_eliminar'),
    url(r'^(?P<cur>[0-9]+)/tareas/$', 'principal.views.tareas'),
    url(r'^(?P<cur>[0-9]+)/tareas/(?P<tar>[0-9]+)/$', 'principal.views.tarea'),
    url(r'^(?P<cur>[0-9]+)/clases/(?P<cls>[0-9]+)/$', 'principal.views.clase'),
    url(r'^(?P<cur>[0-9]+)/clases/(?P<cls>[0-9]+)/editar/$', 'principal.views.editar_clase'),
    url(r'^(?P<cur>[0-9]+)/foro/$', 'principal.views.foro'),
    url(r'^(?P<cur>[0-9]+)/foro/nuevo/$', 'principal.views.nuevo_foro'),
    url(r'^(?P<cur>[0-9]+)/foro/(?P<forr>[0-9]+)/$', 'principal.views.ver_foro'),
    url(r'^(?P<cur>[0-9]+)/foro/(?P<forr>[0-9]+)/respuesta/$', 'principal.views.nuevo_respuesta'),
    url(r'^(?P<cur>[0-9]+)/foro/(?P<forr>[0-9]+)/respuesta/(?P<res>[0-9]+)/comentarios/$', 'principal.views.ver_comentarios'),
    url(r'^(?P<cur>[0-9]+)/clases/(?P<clse>[0-9]+)/lista/nuevo/$', 'principal.views.nuevo_lista'),

    url(r'^panel-control/(?P<cur>[0-9]+)/asistencia/$', 'principal.views.panel_asistencia'),
    

    url(r'^(?P<cur>[0-9]+)/clases/(?P<clse>[0-9]+)/nuevo-envivo/$', 'principal.views.nuevo_envivo'),
    url(r'^(?P<cur>[0-9]+)/clases/(?P<clse>[0-9]+)/nuevo-presentacion/$', 'principal.views.nuevo_presentacion'),
    url(r'^(?P<cur>[0-9]+)/clases/(?P<clse>[0-9]+)/nuevo-recursos/$', 'principal.views.nuevo_recursos'),
    url(r'^(?P<cur>[0-9]+)/clases/(?P<clse>[0-9]+)/nuevo-codigo/$', 'principal.views.nuevo_codigo'),
    url(r'^(?P<cur>[0-9]+)/clases/$', 'principal.views.clases'),

    url(r'^(?P<cur>[0-9]+)/clases/nuevo/$', 'principal.views.nuevo_clase'),

    url(r'^media/(?P<path>.*)$','django.views.static.serve', 
        {'document_root':settings.MEDIA_ROOT,}),
)
