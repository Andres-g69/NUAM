from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db.models import Q

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

from .serializers import (
    UserSerializer,
    UserProfileSerializer,
    InstrumentoSerializer,
    FactorConversionSerializer,
    ArchivoCargaSerializer,
    CargaErrorSerializer,
    CalificacionTributariaSerializer,
    HistorialCalificacionSerializer,
    AuditoriaSerializer,
    CargaRegistroSerializer,
)

# =============================
# USER PROFILE
# =============================
class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.select_related("user").all()
    serializer_class = UserProfileSerializer


# =============================
# INSTRUMENTOS
# =============================
class InstrumentoViewSet(viewsets.ModelViewSet):
    queryset = Instrumento.objects.all()
    serializer_class = InstrumentoSerializer


# =============================
# FACTORES DE CONVERSIÓN
# =============================
class FactorConversionViewSet(viewsets.ModelViewSet):
    queryset = FactorConversion.objects.all()
    serializer_class = FactorConversionSerializer


# =============================
# CALIFICACIONES TRIBUTARIAS
# =============================
class CalificacionTributariaViewSet(viewsets.ModelViewSet):
    queryset = CalificacionTributaria.objects.select_related(
        "instrumento", "factor", "creado_por", "archivo_origen"
    ).all().order_by("-creado_en")
    serializer_class = CalificacionTributariaSerializer

    def perform_create(self, serializer):
        obj = serializer.save(creado_por=self.request.user)
        HistorialCalificacion.objects.create(
            calificacion=obj,
            usuario=self.request.user,
            accion="Creó",
            descripcion="Calificación creada"
        )

    def perform_update(self, serializer):
        obj = serializer.save()
        HistorialCalificacion.objects.create(
            calificacion=obj,
            usuario=self.request.user,
            accion="Modificó",
            descripcion="Calificación actualizada"
        )

    def perform_destroy(self, instance):
        HistorialCalificacion.objects.create(
            calificacion=instance,
            usuario=self.request.user,
            accion="Eliminó",
            descripcion="Calificación eliminada"
        )
        instance.delete()

    # =============================
    # BUSQUEDA AVANZADA
    # =============================
    @action(detail=False, methods=["get"], url_path="buscar")
    def buscar(self, request):
        rut = request.GET.get("rut")
        instrumento = request.GET.get("instrumento")
        tipo = request.GET.get("tipo")
        estado = request.GET.get("estado")
        fecha_desde = request.GET.get("fecha_desde")
        fecha_hasta = request.GET.get("fecha_hasta")

        qs = CalificacionTributaria.objects.all()

        if rut:
            qs = qs.filter(rut__icontains=rut)
        if instrumento:
            qs = qs.filter(instrumento__nombre__icontains=instrumento)
        if tipo:
            qs = qs.filter(tipo=tipo)
        if estado:
            qs = qs.filter(estado=estado)
        if fecha_desde and fecha_hasta:
            qs = qs.filter(fecha__range=[fecha_desde, fecha_hasta])

        serializer = CalificacionTributariaSerializer(qs, many=True)
        return Response(serializer.data)


# =============================
# HISTORIAL CALIFICACIONES
# =============================
class HistorialCalificacionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = HistorialCalificacion.objects.select_related("usuario", "calificacion").all()
    serializer_class = HistorialCalificacionSerializer


# =============================
# ARCHIVO DE CARGA + PROCESAMIENTO
# =============================
class ArchivoCargaViewSet(viewsets.ModelViewSet):
    queryset = ArchivoCarga.objects.all().order_by("-fecha_carga")
    serializer_class = ArchivoCargaSerializer

    @action(detail=False, methods=["post"], url_path="procesar")
    def procesar_archivo(self, request):
        archivo = request.FILES.get("archivo")
        tipo = request.POST.get("tipo_archivo")

        if not archivo:
            return Response({"error": "Debe subir un archivo"}, status=400)

        carga = ArchivoCarga.objects.create(
            archivo=archivo,
            usuario=request.user,
            tipo_archivo=tipo,
            estado="Procesando"
        )

        # Procesamiento real se implementará luego
        try:
            carga.estado = "Completado"
            carga.mensaje = "Archivo procesado correctamente"
            carga.save()
        except Exception as e:
            carga.estado = "Error"
            carga.mensaje = str(e)
            carga.save()
            return Response({"error": str(e)}, status=500)

        return Response(ArchivoCargaSerializer(carga).data)


# =============================
# ERRORES DE CARGA
# =============================
class CargaErrorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CargaError.objects.select_related("archivo").all()
    serializer_class = CargaErrorSerializer


# =============================
# REGISTROS DE CARGA
# =============================
class CargaRegistroViewSet(viewsets.ModelViewSet):
    queryset = CargaRegistro.objects.all().order_by("-fecha_registro")
    serializer_class = CargaRegistroSerializer


# =============================
# AUDITORIA GENERAL
# =============================
class AuditoriaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Auditoria.objects.select_related("usuario").all().order_by("-fecha")
    serializer_class = AuditoriaSerializer
