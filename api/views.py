import re, os
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import JsonResponse

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action, api_view

# =============================
# IMPORTS DE MODELOS Y SERIALIZERS
# =============================
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

from .forms import CalificacionTributariaForm


# =====================================================
#  🔹 API REST FRAMEWORK VIEWSETS
# =====================================================

# --- USUARIOS / PERFILES ---
class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.select_related("user").all()
    serializer_class = UserProfileSerializer


# --- INSTRUMENTOS ---
class InstrumentoViewSet(viewsets.ModelViewSet):
    queryset = Instrumento.objects.all()
    serializer_class = InstrumentoSerializer


# --- FACTORES DE CONVERSIÓN ---
class FactorConversionViewSet(viewsets.ModelViewSet):
    queryset = FactorConversion.objects.all()
    serializer_class = FactorConversionSerializer


# --- CALIFICACIONES TRIBUTARIAS ---
class CalificacionTributariaViewSet(viewsets.ModelViewSet):

    # ✅ eliminamos instrumento y factor porque ya NO son FK
    queryset = CalificacionTributaria.objects.select_related(
        "creado_por", "archivo_origen"
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

    # --- BUSQUEDA ---
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
            # ✅ ahora es texto, no FK
            qs = qs.filter(instrumento__icontains=instrumento)
        if tipo:
            qs = qs.filter(tipo=tipo)
        if estado:
            qs = qs.filter(estado=estado)
        if fecha_desde and fecha_hasta:
            qs = qs.filter(fecha__range=[fecha_desde, fecha_hasta])

        serializer = CalificacionTributariaSerializer(qs, many=True)
        return Response(serializer.data)


# --- HISTORIAL CALIFICACIONES ---
class HistorialCalificacionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = HistorialCalificacion.objects.select_related("usuario", "calificacion").all()
    serializer_class = HistorialCalificacionSerializer


# --- ARCHIVOS DE CARGA ---
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


# --- ERRORES DE CARGA ---
class CargaErrorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CargaError.objects.select_related("archivo").all()
    serializer_class = CargaErrorSerializer


# --- REGISTROS DE CARGA ---
class CargaRegistroViewSet(viewsets.ModelViewSet):
    queryset = CargaRegistro.objects.all().order_by("-fecha_registro")
    serializer_class = CargaRegistroSerializer


# --- AUDITORÍA ---
class AuditoriaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Auditoria.objects.select_related("usuario").all().order_by("-fecha")
    serializer_class = AuditoriaSerializer


# =====================================================
#  🔹 VISTAS HTML (CRUD y búsquedas)
# =====================================================

# 📄 LISTAR
@login_required
def calificacion_list_view(request):

    # ✅ corregido: no más select_related instrumento/factor
    calificaciones = CalificacionTributaria.objects.all()

    return render(request, 'calificaciones/listado.html', {
        'calificaciones': calificaciones
    })


# ➕ CREAR
@login_required
def calificacion_create_view(request):
    if request.method == 'POST':
        form = CalificacionTributariaForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.creado_por = request.user
            obj.save()

            HistorialCalificacion.objects.create(
                calificacion=obj,
                usuario=request.user,
                accion="Creó",
                descripcion="Creación manual desde el panel HTML"
            )

            messages.success(request, "✅ Calificación creada correctamente.")
            return redirect('api:calificacion_list_view')
        else:
            messages.error(request, "❌ Error al crear la calificación. Verifique los datos.")
    else:
        form = CalificacionTributariaForm()

    return render(request, 'calificaciones/formulario.html', {'form': form})


# ✏️ EDITAR
@login_required
def calificacion_update_view(request, id):
    calificacion = get_object_or_404(CalificacionTributaria, id=id)

    if request.method == 'POST':
        form = CalificacionTributariaForm(request.POST, instance=calificacion)
        if form.is_valid():
            form.save()

            HistorialCalificacion.objects.create(
                calificacion=calificacion,
                usuario=request.user,
                accion="Modificó",
                descripcion="Actualización manual desde el panel HTML"
            )

            messages.success(request, "✏️ Calificación actualizada correctamente.")
            return redirect('api:calificacion_list_view')
        else:
            messages.error(request, "❌ Error al actualizar la calificación.")
    else:
        form = CalificacionTributariaForm(instance=calificacion)

    return render(request, 'calificaciones/formulario.html', {
        'form': form,
        'calificacion': calificacion
    })


# 🗑️ ELIMINAR
@login_required
def calificacion_delete_view(request, id):
    calificacion = get_object_or_404(CalificacionTributaria, id=id)

    if request.method == 'POST':
        HistorialCalificacion.objects.create(
            calificacion=calificacion,
            usuario=request.user,
            accion="Eliminó",
            descripcion="Eliminación manual desde el panel HTML"
        )
        calificacion.delete()
        messages.success(request, "🗑️ Calificación eliminada correctamente.")
        return redirect('api:calificacion_list_view')

    return render(request, 'calificaciones/confirmar_eliminacion.html', {'calificacion': calificacion})


# 🔍 BUSCAR
@login_required
def calificacion_read_view(request):
    rut = request.GET.get('rut', '').strip()
    calificaciones = CalificacionTributaria.objects.all()

    if rut:
        rut_limpio = re.sub(r'[\.\-]', '', rut)
        calificaciones = calificaciones.filter(rut__iregex=r'{}|{}'.format(rut, rut_limpio))

    return render(request, 'api/Busqueda.html', {'calificaciones': calificaciones})


# 📤 CARGA MASIVA HTML
@login_required
def carga_view(request):
    cargas = ArchivoCarga.objects.all().order_by('-fecha_carga')
    return render(request, 'api/Carga.html', {'cargas': cargas})


@api_view(['POST'])
@login_required
def procesar_archivo(request):
    archivo = request.FILES.get('archivo')
    tipo = request.POST.get('tipo_archivo', 'OTRO')

    if not archivo:
        return Response({'error': 'Debe subir un archivo'}, status=400)

    carga = ArchivoCarga.objects.create(
        archivo=archivo,
        usuario=request.user,
        tipo_archivo=tipo,
        estado='Cargado'
    )

    serializer = ArchivoCargaSerializer(carga)
    return Response({'success': True, 'carga': serializer.data})
