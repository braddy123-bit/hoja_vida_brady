from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

def validar_no_futuro(value):
    if value and value > timezone.now().date():
        raise ValidationError("la fecha no puede ser futura.")

class DATOSPERSONALES(models.Model):
    nombres = models.CharField(max_length=60)
    apellidos = models.CharField(max_length=60)
    descripcionperfil = models.CharField(max_length=50)
    nacionalidad = models.CharField(max_length=20)
    lugarnacimiento = models.CharField(max_length=60)
    fechanacimiento = models.DateField(validators=[validar_no_futuro])
    numerocedula = models.CharField(max_length=10, unique=True)
    sexo = models.CharField(max_length=1, choices=[("H", "hombre"), ("M", "mujer")])
    estadocivil = models.CharField(max_length=50)
    licenciaconducir = models.CharField(max_length=6, blank=True, null=True)
    telefonoconvencional = models.CharField(max_length=15)
    telefonofijo = models.CharField(max_length=15, blank=True, null=True)
    direcciontrabajo = models.CharField(max_length=50, blank=True, null=True)
    direcciondomiciliaria = models.CharField(max_length=50)
    sitioweb = models.URLField(max_length=60, blank=True, null=True)
    descripcion = models.TextField()
    foto = models.ImageField(upload_to="perfil/", blank=True, null=True)

    class Meta:
        db_table = 'DATOSPERSONALES'
        verbose_name = "datos personales"

    def clean(self):
        super().clean()
        if self.numerocedula and (not self.numerocedula.isdigit() or len(self.numerocedula) != 10):
            raise ValidationError({"numerocedula": "la cédula debe tener 10 dígitos numéricos."})

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

class EXPERIENCIALABORAL(models.Model):
    idperfilconqueestaactivo = models.ForeignKey(DATOSPERSONALES, on_delete=models.CASCADE, related_name="experiencias")
    nombrempresa = models.CharField(max_length=50)
    cargodesempenado = models.CharField(max_length=100)
    fecha_inicio = models.DateField(validators=[validar_no_futuro])
    fecha_fin = models.DateField(blank=True, null=True, validators=[validar_no_futuro])
    descripcion = models.TextField()

    class Meta:
        db_table = 'EXPERIENCIALABORAL'

    def clean(self):
        if self.fecha_inicio and self.fecha_fin and self.fecha_inicio > self.fecha_fin:
            raise ValidationError("la fecha de inicio no puede ser mayor a la de fin.")

class PRODUCTOSACADEMICOS(models.Model):
    idperfilconqueestaactivo = models.ForeignKey(DATOSPERSONALES, on_delete=models.CASCADE, related_name="productos_academicos")
    nombrerecurso = models.CharField(max_length=100)
    clasificador = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=100)
    activarparaqueseveaenfront = models.BooleanField(default=True)

    class Meta:
        db_table = 'PRODUCTOSACADEMICOS'

class PRODUCTOSLABORALES(models.Model):
    idperfilconqueestaactivo = models.ForeignKey(DATOSPERSONALES, on_delete=models.CASCADE, related_name="productos_laborales")
    nombreproducto = models.CharField(max_length=100)
    fechaproducto = models.DateField(validators=[validar_no_futuro])
    descripcion = models.CharField(max_length=100)
    activarparaqueseveaenfront = models.BooleanField(default=True)

    class Meta:
        db_table = 'PRODUCTOSLABORALES'

class RECONOCIMIENTOS(models.Model):
    idperfilconqueestaactivo = models.ForeignKey(DATOSPERSONALES, on_delete=models.CASCADE, related_name="reconocimientos")
    nombrereconocimiento = models.CharField(max_length=150)
    institucion = models.CharField(max_length=150)
    fechareconocimiento = models.DateField(validators=[validar_no_futuro])
    descripcion = models.TextField(blank=True)

    class Meta:
        db_table = 'RECONOCIMIENTOS'

class CURSOSREALIZADOS(models.Model):
    idperfilconqueestaactivo = models.ForeignKey(DATOSPERSONALES, on_delete=models.CASCADE, related_name="cursos")
    nombrecurso = models.CharField(max_length=150)
    centroestudios = models.CharField(max_length=150)
    fechafinalizacion = models.DateField(validators=[validar_no_futuro])
    duracionhoras = models.PositiveIntegerField()

    class Meta:
        db_table = 'CURSOSREALIZADOS'

class VENTAGARAGE(models.Model):
    idperfilconqueestaactivo = models.ForeignKey(DATOSPERSONALES, on_delete=models.CASCADE, related_name="ventas_garage")
    nombreproducto = models.CharField(max_length=100)
    estadoproducto = models.CharField(max_length=40)
    descripcion = models.CharField(max_length=100)
    valordelbien = models.DecimalField(max_digits=10, decimal_places=2)
    disponible = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to="venta_garage/", blank=True, null=True)

    class Meta:
        db_table = 'VENTAGARAGE'

    def clean(self):
        if self.valordelbien is not None and self.valordelbien < 0:
            raise ValidationError("el valor del bien no puede ser negativo.")
