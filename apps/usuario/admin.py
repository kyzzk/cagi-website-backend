from django.contrib import admin
from .models import Usuario
from import_export.admin import ImportExportModelAdmin


@admin.register(Usuario)
class UsuarioAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'nome',  'foto_de_perfil', 'email', 'telefone',  'codigo_recuperacao', 'created_at', 'last_login')
    search_fields = ('id', 'nome', 'email', 'telefone', 'codigo_recuperacao',)
    readonly_fields = ('foto_de_perfil',)
    list_display_links = ('nome',)
    list_filter = ('last_login', 'created_at', 'updated_at')

