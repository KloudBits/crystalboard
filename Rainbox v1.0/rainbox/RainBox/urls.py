from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    #url(r'^$', 'principal.views.ingreso_usuario'),
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^login/$', 'principal.views.ingreso_usuario'),
    url(r'^logout/$', 'Main.views.egreso_usuario'),
    #url(r'^perfil/$', 'principal.views.perfil'),
	url(r'^$', 'Main.views.home'),
	


	url(r'^cursos/$', 'Main.views.cursos'),
	url(r'^info/$', 'Main.views.perfil'),
	
	url(r'^login/$', 'Main.views.ingreso_usuario'),
	
	#url(r'^cursos/nuevo/$', 'Main.views.nuevoCurso'),
	url(r'^cursos/(?P<curso>[a-z-0-9]+)/tareas/$', 'Main.views.tareas'),
	url(r'^cursos/(?P<curso>[a-z-0-9]+)/tareas/(?P<tarea>[0-9]+)/$', 'Main.views.tarea'),
	url(r'^cursos/(?P<curso>[a-z-0-9]+)/tareas/nuevo/$', 'Main.views.nuevoTarea'),
	
	url(r'^cursos/(?P<curso>[a-z-0-9]+)/grade-center/$', 'Main.views.gradecenter'),
	
	url(r'^cursos/(?P<curso>[a-z-0-9]+)/grade-center/quizzes/(?P<quiz>[0-9]+)/$', 'Main.views.gradequiz'),
	url(r'^cursos/(?P<curso>[a-z-0-9]+)/grade-center/quizzes/(?P<quiz>[0-9]+)/(?P<aplicacion>[0-9]+)/$', 'Main.views.gradequiz_aplicacion'),
	
	url(r'^cursos/(?P<curso>[a-z-0-9]+)/grade-center/tareas/(?P<tarea>[0-9]+)/$', 'Main.views.gradetarea'),
	url(r'^cursos/(?P<curso>[a-z-0-9]+)/grade-center/tareas/(?P<tarea>[0-9]+)/(?P<entrega>[0-9]+)/$', 'Main.views.gradetarea_entrega'),

	url(r'^cursos/(?P<curso>[a-z-0-9]+)/$', 'Main.views.curso'),
	url(r'^cursos/(?P<curso>[a-z-0-9]+)/clases/nuevo/$', 'Main.views.nuevaClase'),
	url(r'^cursos/(?P<curso>[a-z-0-9]+)/clases/$', 'Main.views.clases'),
	url(r'^cursos/(?P<curso>[a-z-0-9]+)/avisos/$', 'Main.views.avisos'),
	url(r'^cursos/(?P<curso>[a-z-0-9]+)/miembros/$', 'Main.views.miembros'),
	#url(r'^cursos/(?P<curso>[a-z-0-9]+)/miembros/nuevo/$', 'Main.views.nuevoMiembro'),

	url(r'^cursos/(?P<curso>[a-z-0-9]+)/foros/$', 'Main.views.foros'),
	url(r'^cursos/(?P<curso>[a-z-0-9]+)/foros/(?P<foro>[0-9]+)/$', 'Main.views.foro'),
	url(r'^cursos/(?P<curso>[a-z-0-9]+)/foros/(?P<foro>[0-9]+)/comentar/$', 'Main.views.comentarForo'),
	url(r'^cursos/(?P<curso>[a-z-0-9]+)/foros/nuevo/$', 'Main.views.nuevoForo'),
	
	url(r'^cursos/(?P<curso>[a-z-0-9]+)/quizzes/$', 'Main.views.quizes'),
	url(r'^cursos/(?P<curso>[a-z-0-9]+)/quizzes/nuevo/$', 'Main.views.nuevoQuiz'),
	url(r'^cursos/(?P<curso>[a-z-0-9]+)/quizzes/(?P<quiz>[0-9]+)/$', 'Main.views.quiz'),
	url(r'^cursos/(?P<curso>[a-z-0-9]+)/quizzes/(?P<quiz>[0-9]+)/preguntas/(?P<pregunta>[0-9]+)/$', 'Main.views.preguntas'),
	url(r'^cursos/(?P<curso>[a-z-0-9]+)/quizzes/(?P<quiz>[0-9]+)/preguntas/nuevo/$', 'Main.views.nuevaPregunta'),
	url(r'^cursos/(?P<curso>[a-z-0-9]+)/quizzes/(?P<quiz>[0-9]+)/preguntas/(?P<pregunta>[0-9]+)/respuesta/$', 'Main.views.nuevaRespuesta'),

	
	url(r'^cursos/(?P<curso>[a-z-0-9]+)/avisos/nuevo/$', 'Main.views.nuevoAviso'),
	url(r'^cursos/(?P<curso>[a-z-0-9]+)/avisos/(?P<aviso>[0-9]+)/$', 'Main.views.aviso'),
	url(r'^cursos/(?P<curso>[a-z-0-9]+)/avisos/(?P<aviso>[0-9]+)/borrar/$', 'Main.views.borrarAviso'),
	url(r'^cursos/(?P<curso>[a-z-0-9]+)/capitulos/$', 'Main.views.capitulos'),
	url(r'^cursos/(?P<curso>[a-z-0-9]+)/capitulos/nuevo/$', 'Main.views.nuevoCapitulo'),
	url(r'^cursos/(?P<curso>[a-z-0-9]+)/capitulos/(?P<capitulo>[0-9]+)/del/$', 'Main.views.borrarCapitulo'),
	

	url(r'^cursos/(?P<curso>[a-z-0-9]+)/vivo/$', 'Main.views.envivo'),
	url(r'^cursos/(?P<curso>[a-z-0-9]+)/(?P<clase>[a-z-0-9]+)/$', 'Main.views.clase'),
	


	url(r'^cursos/(?P<curso>[a-z-0-9]+)/(?P<clase>[a-z-0-9]+)/recurso/slideshare/$', 'Main.views.add_slideshare'),
	url(r'^cursos/(?P<curso>[a-z-0-9]+)/(?P<clase>[a-z-0-9]+)/recurso/dropbox/$', 'Main.views.add_dropbox'),
	url(r'^cursos/(?P<curso>[a-z-0-9]+)/(?P<clase>[a-z-0-9]+)/recurso/youtube/$', 'Main.views.add_youtube'),
	url(r'^cursos/(?P<curso>[a-z-0-9]+)/(?P<clase>[a-z-0-9]+)/recurso/weblink/$', 'Main.views.add_weblink'),
	
	url(r'^cursos/(?P<curso>[a-z-0-9]+)/(?P<clase>[a-z-0-9]+)/recursos/(?P<recurso>[a-z-0-9]+)/del/$', 'Main.views.del_recurso'),
	




) + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)

urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
