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
	
	url(r'^cursos/(?P<curso>[a-z-0-9]+)/$', 'Main.views.curso'),
	url(r'^cursos/(?P<curso>[a-z-0-9]+)/clases/nuevo/$', 'Main.views.nuevaClase'),
	url(r'^cursos/(?P<curso>[a-z-0-9]+)/clases/$', 'Main.views.clases'),
	url(r'^cursos/(?P<curso>[a-z-0-9]+)/avisos/$', 'Main.views.avisos'),
	url(r'^cursos/(?P<curso>[a-z-0-9]+)/miembros/$', 'Main.views.miembros'),
	url(r'^cursos/(?P<curso>[a-z-0-9]+)/miembros/nuevo$', 'Main.views.nuevoMiembro'),

	url(r'^cursos/(?P<curso>[a-z-0-9]+)/foros/$', 'Main.views.foros'),
	url(r'^cursos/(?P<curso>[a-z-0-9]+)/foros/(?P<foro>[0-9]+)/$', 'Main.views.foro'),
	url(r'^cursos/(?P<curso>[a-z-0-9]+)/foros/(?P<foro>[0-9]+)/comentar/$', 'Main.views.comentarForo'),
	url(r'^cursos/(?P<curso>[a-z-0-9]+)/foros/nuevo$', 'Main.views.nuevoForo'),
	
	url(r'^cursos/(?P<curso>[a-z-0-9]+)/quizes/$', 'Main.views.quizes'),
	url(r'^cursos/(?P<curso>[a-z-0-9]+)/quizes/nuevo$', 'Main.views.nuevoQuiz'),
	url(r'^cursos/(?P<curso>[a-z-0-9]+)/quizes/(?P<quiz>[0-9]+)/$', 'Main.views.quiz'),
	url(r'^cursos/(?P<curso>[a-z-0-9]+)/quizes/(?P<quiz>[0-9]+)/preguntas/(?P<pregunta>[0-9]+)/$', 'Main.views.preguntas'),
	url(r'^cursos/(?P<curso>[a-z-0-9]+)/quizes/(?P<quiz>[0-9]+)/preguntas/nuevo/$', 'Main.views.nuevaPregunta'),
	url(r'^cursos/(?P<curso>[a-z-0-9]+)/quizes/(?P<quiz>[0-9]+)/preguntas/(?P<pregunta>[0-9]+)/respuesta/$', 'Main.views.nuevaRespuesta'),

	
	url(r'^cursos/(?P<curso>[a-z-0-9]+)/avisos/nuevo$', 'Main.views.nuevoAviso'),
	url(r'^cursos/(?P<curso>[a-z-0-9]+)/avisos/(?P<aviso>[0-9]+)/$', 'Main.views.aviso'),
	url(r'^cursos/(?P<curso>[a-z-0-9]+)/avisos/(?P<aviso>[0-9]+)/borrar/$', 'Main.views.borrarAviso'),
	url(r'^cursos/(?P<curso>[a-z-0-9]+)/capitulos/$', 'Main.views.capitulos'),
	url(r'^cursos/(?P<curso>[a-z-0-9]+)/capitulos/nuevo/$', 'Main.views.nuevoCapitulo'),
	url(r'^cursos/(?P<curso>[a-z-0-9]+)/capitulos/(?P<capitulo>[0-9]+)/del/$', 'Main.views.borrarCapitulo'),
	



	url(r'^cursos/(?P<curso>[a-z-0-9]+)/(?P<clase>[a-z-0-9]+)/$', 'Main.views.clase'),

) + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
