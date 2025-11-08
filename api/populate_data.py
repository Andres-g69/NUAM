from api.models import (
    Usuario,
    Rol,
    Auditoria,
    ArchivoCarga,
    Instrumento,
    CalificacionTributaria,
    HistorialCalificacion,
    FactorConversion,
    CargaRegistro
)
from datetime import date, datetime
from decimal import Decimal

# Si es que los datos no estan en el admin pon en el cmd:
# python manage.py shell / from myapp.populate_data import run / run() / luego puedes revisarlo

def run():
    # USUARIOS
    u1, _ = Usuario.objects.get_or_create(nombre="Carlos", apellido="Pérez", correo="carlos@example.com")
    u2, _ = Usuario.objects.get_or_create(nombre="María", apellido="Gómez", correo="maria@example.com")

    # ROLES
    Rol.objects.get_or_create(nombre_rol="Administrador", usuario=u1)
    Rol.objects.get_or_create(nombre_rol="Analista", usuario=u2)

    # FACTORES DE CONVERSIÓN
    f1, _ = FactorConversion.objects.get_or_create(descripcion="Factor General", valor=1.25)
    f2, _ = FactorConversion.objects.get_or_create(descripcion="Factor Preferencial", valor=1.10)

    # INSTRUMENTOS
    i1, _ = Instrumento.objects.get_or_create(nombre="Bono Tesorería", tipo="Bono", inscrito=True)
    i2, _ = Instrumento.objects.get_or_create(nombre="Acción Empresa X", tipo="Acción", inscrito=False)

    # ARCHIVOS DE CARGA
    a1, _ = ArchivoCarga.objects.get_or_create(usuario=u1, estado="Procesado", tipo_archivo="CSV")
    a2, _ = ArchivoCarga.objects.get_or_create(usuario=u2, estado="Pendiente", tipo_archivo="XLSX")

    # CALIFICACIONES TRIBUTARIAS
    c1, _ = CalificacionTributaria.objects.get_or_create(
        usuario=u1,
        instrumento=i1,
        fecha=date.today(),
        tipo="Ordinaria",
        monto=Decimal("120000.00"),
        factor=f1,
        estado="Aprobada"
    )
    c2, _ = CalificacionTributaria.objects.get_or_create(
        usuario=u2,
        instrumento=i2,
        fecha=date.today(),
        tipo="Especial",
        monto=Decimal("80000.00"),
        factor=f2,
        estado="Pendiente"
    )

    # HISTORIAL DE CALIFICACIÓN
    HistorialCalificacion.objects.get_or_create(
        calificacion=c1,
        observacion="Revisión inicial completada."
    )
    HistorialCalificacion.objects.get_or_create(
        calificacion=c2,
        observacion="Pendiente de aprobación final."
    )

    # AUDITORÍA
    Auditoria.objects.get_or_create(usuario=u1, accion="Creación de usuario", ip="192.168.1.10")
    Auditoria.objects.get_or_create(usuario=u2, accion="Carga de archivo", ip="192.168.1.15")

    # REGISTROS DE CARGA
    CargaRegistro.objects.get_or_create(
        archivo=a1,
        usuario=u1,
        descripcion="Archivo CSV de prueba cargado correctamente."
    )
    CargaRegistro.objects.get_or_create(
        archivo=a2,
        usuario=u2,
        descripcion="Archivo XLSX pendiente de revisión."
    )

    print("✅ Datos cargados correctamente en la base de datos.")
