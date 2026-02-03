from django.shortcuts import render
from .models import DATOSPERSONALES

def cv_view(request):
    perfil = DATOSPERSONALES.objects.first()

    if not perfil:
        return render(request, 'cv/cv.html', {'perfil': None})

    context = {
        'perfil': perfil,
        'experiencias': perfil.experiencias.all().order_by('-fecha_inicio'),
        'productos_academicos': perfil.productos_academicos.filter(activarparaqueseveaenfront=True),
        'productos_laborales': perfil.productos_laborales.filter(activarparaqueseveaenfront=True),
        'reconocimientos': perfil.reconocimientos.all().order_by('-fechareconocimiento'),
        'cursos': perfil.cursos.all().order_by('-fechafinalizacion'),
        'ventas': perfil.ventas_garage.filter(disponible=True)
    }

    return render(request, 'cv/cv.html', context)
