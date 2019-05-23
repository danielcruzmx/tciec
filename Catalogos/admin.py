import csv
from django.http import HttpResponse
from django.contrib import admin
from main.procesos import run_acum

# Register your models here.

from Catalogos.models import Banco, Condominio, PeriodoCorte, CuentaContable

@admin.register(CuentaContable)
class CuentaContableAdmin(admin.ModelAdmin):
    list_display = ('num_cuenta', 'descripcion')
    list_filter = ('num_cuenta',)

@admin.register(Banco)
class BancoAdmin(admin.ModelAdmin):
    list_display = ('clave','descripcion')

@admin.register(Condominio)
class CondominioAdmin(admin.ModelAdmin):
    list_display = ('nombre','calle','colonia','delegacion')

@admin.register(PeriodoCorte)
class PeriodoAdmin(admin.ModelAdmin):
    list_display = ('condominio', 'fecha_inicial', 'fecha_final')
    actions = ['acumulados']

    def acumulados(self, request, queryset):
        for obj in queryset:
            #field_value = getattr(obj, 'condominio')
            print(" genera acumulados %s " % obj.condominio)
            run_acum(obj.condominio)

        self.message_user(request, " Fin del proceso de generacion de acumulados ")

    acumulados.short_description = "Obtiene acumulados"    

    