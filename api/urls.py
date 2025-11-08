from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    UserProfileViewSet,
    InstrumentoViewSet,
    FactorConversionViewSet,
    CalificacionTributariaViewSet,
    HistorialCalificacionViewSet,
    ArchivoCargaViewSet,
    CargaErrorViewSet,
    CargaRegistroViewSet,
    AuditoriaViewSet,
)

router = DefaultRouter()

# =============================
# RUTAS API REST PRINCIPALES
# =============================
router.register(r'usuarios', UserProfileViewSet, basename='usuarios')
router.register(r'instrumentos', InstrumentoViewSet, basename='instrumentos')
router.register(r'factores', FactorConversionViewSet, basename='factores')
router.register(r'calificaciones', CalificacionTributariaViewSet, basename='calificaciones')
router.register(r'historial', HistorialCalificacionViewSet, basename='historial')
router.register(r'archivos', ArchivoCargaViewSet, basename='archivos')
router.register(r'errores', CargaErrorViewSet, basename='errores')
router.register(r'registros', CargaRegistroViewSet, basename='registros')
router.register(r'auditoria', AuditoriaViewSet, basename='auditoria')

urlpatterns = [
    path('', include(router.urls)),
]
