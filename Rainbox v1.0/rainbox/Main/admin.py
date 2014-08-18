# encoding: utf-8
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from Main.models import UserProfile, Curso, Clase, Capitulo

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'perfiles'

class UserAdmin(UserAdmin):
    inlines = (UserProfileInline, )


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Curso)
admin.site.register(Capitulo)
admin.site.register(Clase)

