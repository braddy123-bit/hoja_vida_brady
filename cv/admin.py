from django.contrib import admin
from .models import (
    DATOSPERSONALES, EXPERIENCIALABORAL, VENTAGARAGE, 
    PRODUCTOSACADEMICOS, PRODUCTOSLABORALES, 
    RECONOCIMIENTOS, CURSOSREALIZADOS
)

class ValidatedAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.full_clean()
        super().save_model(request, obj, form, change)

class ReconocimientosInline(admin.TabularInline):
    model = RECONOCIMIENTOS
    extra = 0

class CursosInline(admin.TabularInline):
    model = CURSOSREALIZADOS
    extra = 0

@admin.register(DATOSPERSONALES)
class DatosPersonalesAdmin(ValidatedAdmin):
    list_display = ("nombres", "apellidos", "numerocedula")
    inlines = [ReconocimientosInline, CursosInline]

admin.site.register(EXPERIENCIALABORAL, ValidatedAdmin)
admin.site.register(VENTAGARAGE, ValidatedAdmin)
admin.site.register(PRODUCTOSACADEMICOS, ValidatedAdmin)
admin.site.register(PRODUCTOSLABORALES, ValidatedAdmin)
admin.site.register(RECONOCIMIENTOS, ValidatedAdmin)
admin.site.register(CURSOSREALIZADOS, ValidatedAdmin)
