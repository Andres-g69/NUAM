from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

# UserProfile (roles fijos)
class UserProfile(models.Model):
    ROLE_ADMIN = 'ADMIN'
    ROLE_ANALISTA = 'ANALISTA'
    ROLE_LECTOR = 'LECTOR'

    ROLE_CHOICES = [
        (ROLE_ADMIN, 'Administrador'),
        (ROLE_ANALISTA, 'Analista'),
        (ROLE_LECTOR, 'Lector'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_ANALISTA)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"


# Crear UserProfile automáticamente al crear User
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

# Instrumento
class Instrumento(models.Model):
    codigo = models.CharField(max_length=50, unique=True, blank=True, null=True)
    nombre = models.CharField(max_length=150)
    tipo = models.CharField(max_length=100)
    inscrito = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre


# Factor de conversión
class FactorConversion(models.Model):
    descripcion = models.CharField(max_length=150)
    valor = models.DecimalField(max_digits=20, decimal_places=8)

    def __str__(self):
        return f"{self.descripcion} = {self.valor}"


# Archivo de carga y CargasMasivas
class ArchivoCarga(models.Model):
    TIPO_DJ1948 = 'DJ1948'
    TIPO_FACTORES = 'FACTORES'
    TIPO_OTRO = 'OTRO'

    TIPO_CHOICES = [
        (TIPO_DJ1948, 'DJ1948'),
        (TIPO_FACTORES, 'Factores'),
        (TIPO_OTRO, 'Otro'),
    ]

    archivo = models.FileField(upload_to='uploads/%Y/%m/%d/')
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='archivos_carga')
    fecha_carga = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=30, default='Pendiente')
    tipo_archivo = models.CharField(max_length=20, choices=TIPO_CHOICES, default=TIPO_OTRO)
    mensaje = models.TextField(blank=True)

    def __str__(self):
        return f"ArchivoCarga {self.id} - {self.tipo_archivo} - {self.estado}"


class CargaError(models.Model):
    archivo = models.ForeignKey(ArchivoCarga, on_delete=models.CASCADE, related_name='errores')
    linea = models.PositiveIntegerField()
    mensaje = models.TextField()

    def __str__(self):
        return f"Error archivo {self.archivo.id} linea {self.linea}"


# Calificaciones Tributarias
class CalificacionTributaria(models.Model):
    TIPO_DJ1948 = 'DJ1948'
    TIPO_FACTOR = 'FACTOR'
    TIPO_MANUAL = 'MANUAL'

    TIPO_CHOICES = [
        (TIPO_DJ1948, 'DJ1948'),
        (TIPO_FACTOR, 'Factor'),
        (TIPO_MANUAL, 'Manual'),
    ]

    instrumento = models.CharField(max_length=255, blank=True, null=True)
    rut = models.CharField(max_length=15, blank=True, null=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    monto = models.DecimalField(max_digits=18, decimal_places=2)
    factor = models.CharField(max_length=255, blank=True, null=True)
    fecha = models.DateField()
    estado = models.CharField(max_length=30, default='Vigente')
    comentario = models.TextField(blank=True)

    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='calificaciones_creadas')
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    archivo_origen = models.ForeignKey(ArchivoCarga, on_delete=models.SET_NULL, null=True, blank=True, related_name='calificaciones_generadas')

    def __str__(self):
        return f"Calificacion {self.id} - {self.instrumento} - {self.tipo}"


# Historial de calificaciones (auditoría específica)
class HistorialCalificacion(models.Model):
    calificacion = models.ForeignKey(CalificacionTributaria, on_delete=models.CASCADE, related_name='historial')
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    accion = models.CharField(max_length=50)  # Creó / Modificó / Eliminó / Cargó
    descripcion = models.TextField(blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.accion} - {self.calificacion.id} - {self.fecha.isoformat()}"


# Auditoría general (más genérica que HistorialCalificacion)
class Auditoria(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    accion = models.CharField(max_length=255)
    fecha = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField(null=True, blank=True)

    detalle = models.TextField(blank=True)

    def __str__(self):
        return f"Auditoria {self.id} - {self.usuario} - {self.accion}"


# Registro de acciones / logs sobre la carga (opcional)
class CargaRegistro(models.Model):
    archivo = models.ForeignKey(ArchivoCarga, on_delete=models.CASCADE, related_name='registros')
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    descripcion = models.TextField()

    def __str__(self):
        return f"Registro {self.id} - archivo {self.archivo.id}"
