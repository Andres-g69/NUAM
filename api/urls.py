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


urlpatterns = [
    path('calificaciones/', views.calificacion_list_view, name='calificacion_list_view'),
    path('calificaciones/nueva/', views.calificacion_create_view, name='calificacion_create_view'),
    path('calificaciones/<int:id>/editar/', views.calificacion_update_view, name='calificacion_update_view'),      
    path('calificaciones/<int:id>/eliminar/', views.calificacion_delete_view, name='calificacion_delete_view'),
    path('busqueda/', views.calificacion_read_view, name='calificacion_read_view'),
    path('', include(router.urls)),
    path('carga/', views.carga_view, name='carga'),
    path('api/carga/procesar/', views.procesar_archivo, name='archivo-carga-procesar'),
]

