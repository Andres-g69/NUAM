from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'api'
# =============================
# ROUTER API REST PRINCIPAL
# =============================
router = DefaultRouter()
router.register(r'usuarios', views.UserProfileViewSet, basename='usuarios')
router.register(r'instrumentos', views.InstrumentoViewSet, basename='instrumentos')
router.register(r'factores', views.FactorConversionViewSet, basename='factores')
router.register(r'calificaciones', views.CalificacionTributariaViewSet, basename='calificaciones')
router.register(r'historial', views.HistorialCalificacionViewSet, basename='historial')
router.register(r'archivos', views.ArchivoCargaViewSet, basename='archivos')
router.register(r'errores', views.CargaErrorViewSet, basename='errores')
router.register(r'registros', views.CargaRegistroViewSet, basename='registros')
router.register(r'auditoria', views.AuditoriaViewSet, basename='auditoria')

router = DefaultRouter()


from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'api'

router = DefaultRouter()
router.register(r'usuarios', views.UserProfileViewSet, basename='usuarios')
router.register(r'instrumentos', views.InstrumentoViewSet, basename='instrumentos')
router.register(r'factores', views.FactorConversionViewSet, basename='factores')
router.register(r'calificaciones', views.CalificacionTributariaViewSet, basename='calificaciones')
router.register(r'historial', views.HistorialCalificacionViewSet, basename='historial')
router.register(r'archivos', views.ArchivoCargaViewSet, basename='archivos')
router.register(r'errores', views.CargaErrorViewSet, basename='errores')
router.register(r'registros', views.CargaRegistroViewSet, basename='registros')
router.register(r'auditoria', views.AuditoriaViewSet, basename='auditoria')

urlpatterns = [
    # Calificaciones
    path('calificaciones/', views.calificacion_list_view, name='calificacion_list_view'),
    path('calificaciones/nueva/', views.calificacion_create_view, name='calificacion_create_view'),
    path('calificaciones/<int:id>/editar/', views.calificacion_update_view, name='calificacion_update_view'),
    path('calificaciones/<int:id>/eliminar/', views.calificacion_delete_view, name='calificacion_delete_view'),
    path('busqueda/', views.calificacion_read_view, name='calificacion_read_view'),
    path('busqueda/<int:id>/ver/', views.calificacion_read_detail_view, name='calificacion_read_detail_view'), 

    # Admin
    path('admin-dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('admin-usuarios/', views.admin_usuarios_view, name='admin_usuarios'),
    path('admin-auditorias/', views.admin_auditorias_view, name='admin_auditorias'),
    path('admin-usuarios/crear/', views.admin_usuario_crear_view, name='admin_usuario_crear'),
    path('admin-usuarios/editar/<int:user_id>/', views.admin_usuario_editar_view, name='admin_usuario_editar'),
    path('admin-usuarios/eliminar/<int:user_id>/', views.admin_usuario_eliminar_view, name='admin_usuario_eliminar'),

    # Carga masiva
    path('carga/', views.carga_view, name='carga_dashboard'),
    path('carga/listado/', views.listado_carga_view, name='listado_carga'),
    path('carga/procesar/', views.procesar_archivo, name='archivo-carga-procesar'),
    path('cargas/descargar/<int:archivo_id>/', views.descarga_archivo, name='archivo_descargar'),
    path("cargas/eliminar/<int:archivo_id>/", views.eliminar_archivo, name="archivo_eliminar"),

    path('', include(router.urls)),
]
