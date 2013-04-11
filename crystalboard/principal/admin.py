from principal.models import Curso, Aviso, Comentario_Aviso, Tarea, Entrega_Tarea, Comentario_Tarea, Lista, UserProfile
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'perfiles'

# Definimos un  nuevo User admin
class UserAdmin(UserAdmin):
    inlines = (UserProfileInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Curso)
admin.site.register(Aviso)
admin.site.register(Comentario_Aviso)
admin.site.register(Tarea)
admin.site.register(Entrega_Tarea)
admin.site.register(Comentario_Tarea)
admin.site.register(Lista)
admin.site.register(UserProfile)
