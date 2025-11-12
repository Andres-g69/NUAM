import re, os
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import JsonResponse, FileResponse, Http404
from .utils import registrar_auditoria

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
from django.http import HttpResponse, Http404


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

# ======================
# ADMIN Y AUDITORIAS
# ======================

# Decorador personalizado para admin
def admin_required(view_func):
    return user_passes_test(lambda u: u.is_superuser or u.is_staff)(view_func)

@login_required
@admin_required
def admin_dashboard_view(request):
    return render(request, 'admin/admin_dashboard.html')


@login_required
@admin_required
def admin_usuarios_view(request):
    usuarios = User.objects.all().order_by('id')

    if not usuarios.exists():
        messages.warning(request, "Actualmente no hay usuarios registrados en el sistema.")

    return render(request, 'admin/admin_usuarios.html', {'usuarios': usuarios})


@login_required
@admin_required
def admin_auditorias_view(request):
    auditorias = Auditoria.objects.select_related('usuario').order_by('-fecha')
    return render(request, 'admin/admin_auditorias.html', {'auditorias': auditorias})

@login_required
@admin_required
def admin_usuario_crear_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        rol = request.POST.get('rol')

        # Validaciones básicas
        if not username or not email or not password:
            messages.error(request, "Todos los campos son obligatorios.")
            return redirect('api:admin_usuario_crear')

        if User.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya existe.")
            return redirect('api:admin_usuario_crear')

        if User.objects.filter(email=email).exists():
            messages.error(request, "El correo electrónico ya está en uso.")
            return redirect('api:admin_usuario_crear')

        # Crear usuario
        usuario = User.objects.create_user(username=username, email=email, password=password)
        if rol == 'admin':
            usuario.is_superuser = True
            usuario.is_staff = True
        usuario.save()

        registrar_auditoria(request.user, f"Creó un nuevo usuario {usuario.username}", request, detalle= "Gestion Usuarios")
        messages.success(request, f"Usuario '{usuario.username}' creado correctamente.")
        return redirect('api:admin_usuarios')

    return render(request, 'admin/admin_usuario_crear.html')

@login_required
@admin_required
def admin_usuario_editar_view(request, user_id):
    usuario = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        is_active = bool(request.POST.get('is_active'))
        rol = request.POST.get('rol')

        usuario.username = username
        usuario.email = email
        usuario.is_active = is_active
        usuario.is_superuser = True if rol == 'admin' else False
        usuario.is_staff = usuario.is_superuser
        usuario.save()

        registrar_auditoria(request.user, f"Editó usuario {usuario.username}", request, detalle= "Gestion Usuarios")

        messages.success(request, "Usuario actualizado correctamente.")
        return redirect('api:admin_usuarios')

    return render(request, 'admin/admin_usuario_editar.html', {'usuario': usuario})


@login_required
@admin_required
def admin_usuario_eliminar_view(request, user_id):
    usuario = get_object_or_404(User, id=user_id)

    # Evitar eliminar todos los usuarios normales
    if not usuario.is_superuser:
        usuarios_normales = User.objects.filter(is_superuser=False)
        if usuarios_normales.count() <= 1:
            messages.error(request, "No puedes eliminar el último usuario del sistema.")
            return redirect('api:admin_usuarios')

    registrar_auditoria(request.user, f"Eliminó usuario {usuario.username}", request, detalle= "Gestion Usuarios")
    usuario.delete()
    messages.success(request, f"Usuario '{usuario.username}' eliminado correctamente.")
    return redirect('api:admin_usuarios')


# ======================
# CALIFICACIONES
# ======================
@login_required
def calificacion_list_view(request):
    calificaciones = CalificacionTributaria.objects.all()
    return render(request, 'calificaciones/listado.html', {'calificaciones': calificaciones})

@login_required
def calificacion_create_view(request):
    if request.method == 'POST':
        form = CalificacionTributariaForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.creado_por = request.user
            obj.save()
            registrar_auditoria(request.user, f"Creó calificación ID {obj.id}", request, detalle= "CRUD Calificaciones")
            messages.success(request, "✅ Calificación creada correctamente.")
            return redirect('api:calificacion_list_view')
        else:
            messages.error(request, "❌ Error al crear la calificación.")
    else:
        form = CalificacionTributariaForm()
    return render(request, 'calificaciones/formulario.html', {'form': form})

@login_required
def calificacion_update_view(request, id):
    calificacion = get_object_or_404(CalificacionTributaria, id=id)
    if request.method == 'POST':
        form = CalificacionTributariaForm(request.POST, instance=calificacion)
        if form.is_valid():
            form.save()
            registrar_auditoria(request.user, f"Modificó calificación ID {calificacion.id}", request, detalle= "CRUD Califiaciones")
            messages.success(request, "✏️ Calificación actualizada correctamente.")
            return redirect('api:calificacion_list_view')
        else:
            messages.error(request, "❌ Error al actualizar la calificación.")
    else:
        form = CalificacionTributariaForm(instance=calificacion)
    return render(request, 'calificaciones/formulario.html', {'form': form, 'calificacion': calificacion})

@login_required
def calificacion_delete_view(request, id):
    calificacion = get_object_or_404(CalificacionTributaria, id=id)
    if request.method == 'POST':
        registrar_auditoria(request.user, f"Eliminó calificación ID {calificacion.id}", request, detalle= "CRUD Calificaciones")
        calificacion.delete()
        messages.success(request, "🗑️ Calificación eliminada correctamente.")
        return redirect('api:calificacion_list_view')
    return render(request, 'calificaciones/confirmar_eliminacion.html', {'calificacion': calificacion})

# ======================
# BUSQUEDA
# ======================
@login_required
def calificacion_read_view(request):
    rut = request.GET.get('rut', '').strip()
    calificaciones = CalificacionTributaria.objects.all()
    if rut:
        rut_limpio = re.sub(r'[\.\-]', '', rut)
        calificaciones = calificaciones.filter(rut__iregex=r'{}|{}'.format(rut, rut_limpio))
    return render(request, 'api/Busqueda.html', {'calificaciones': calificaciones})

# SOLO LECTURA
@login_required
def calificacion_read_detail_view(request, id):
    """
    Muestra la información completa de una calificación tributaria
    desde la búsqueda, en modo solo lectura (sin edición).
    """
    calificacion = get_object_or_404(CalificacionTributaria, id=id)
    form = CalificacionTributariaForm(instance=calificacion)

    # Deshabilitar los campos del formulario para modo lectura
    for field in form.fields.values():
        field.widget.attrs['readonly'] = True
        field.widget.attrs['disabled'] = True

    return render(request, 'calificaciones/formulario.html', {
        'form': form,
        'modo': 'ver',
        'calificacion': calificacion,
    })

# ======================
# CARGA MASIVA
# ======================
@login_required
def carga_view(request):
    cargas = ArchivoCarga.objects.all().order_by('-fecha_carga')
    return render(request, 'api/Carga.html', {'cargas': cargas})

@login_required
def listado_carga_view(request):
    cargas = ArchivoCarga.objects.all().order_by('-fecha_carga')
    return render(request, 'api/listado_carga.html', {'cargas': cargas})

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
    registrar_auditoria(request.user, f"Subió archivo {archivo.name}", request, detalle= "Carga Archivos")
    serializer = ArchivoCargaSerializer(carga)
    return Response({'success': True, 'carga': serializer.data})

@login_required
def descarga_archivo(request, archivo_id):
    from .models import ArchivoCarga
    import os

    try:
        archivo = ArchivoCarga.objects.get(id=archivo_id)
    except ArchivoCarga.DoesNotExist:
        messages.error(request, "El archivo solicitado no existe en la base de datos.")
        return redirect('api:listado_carga')

    if not archivo.archivo:
        messages.error(request, "El archivo no tiene contenido disponible para descargar.")
        return redirect('api:listado_carga')

    # 🔹 Verificar si el archivo existe físicamente
    file_path = archivo.archivo.path
    if not os.path.exists(file_path):
        messages.error(request, "El archivo ya no existe en el servidor.")
        return redirect('api:listado_carga')

    # 🔹 Si existe, devolver descarga
    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
        return response
