from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    #url(r'^$', 'principal.views.ingreso_usuario'),
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^login/$', 'principal.views.ingreso_usuario'),
    #url(r'^logout/$', 'principal.views.egreso_usuario'),
    #url(r'^perfil/$', 'principal.views.perfil'),
	url(r'^$', 'Main.views.home'),
	url(r'^cursos/$', 'Main.views.cursos'),
	url(r'^cursos/nuevo/$', 'Main.views.nuevoCurso'),
	
	url(r'^(?P<curso>[a-z-0-9]+)/$', 'Main.views.curso'),
	url(r'^(?P<curso>[a-z-0-9]+)/(?P<clase>[a-z-0-9]+)/$', 'Main.views.clase'),

) + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
