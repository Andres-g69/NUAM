from django.contrib import admin
from .models import (
    UserProfile,
    Instrumento,
    FactorConversion,
    ArchivoCarga,
    CargaError,
    CalificacionTributaria,
    HistorialCalificacion,
    Auditoria,
    CargaRegistro,
)

admin.site.register(UserProfile)
admin.site.register(Instrumento)
admin.site.register(FactorConversion)
admin.site.register(ArchivoCarga)
admin.site.register(CargaError)
admin.site.register(CalificacionTributaria)
admin.site.register(HistorialCalificacion)
admin.site.register(Auditoria)
admin.site.register(CargaRegistro)
