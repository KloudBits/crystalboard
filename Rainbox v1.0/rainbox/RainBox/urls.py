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

) + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
