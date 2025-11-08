from rest_framework import serializers
from django.contrib.auth.models import User
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

# =============================
# USER & PROFILE
# =============================
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ["id", "user", "role", "activo"]


# =============================
# INSTRUMENTO
# =============================
class InstrumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instrumento
        fields = "__all__"


# =============================
# FACTOR CONVERSION
# =============================
class FactorConversionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FactorConversion
        fields = "__all__"


# =============================
# ARCHIVO DE CARGA + ERRORES
# =============================
class CargaErrorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CargaError
        fields = ["id", "linea", "mensaje"]


class ArchivoCargaSerializer(serializers.ModelSerializer):
    usuario = UserSerializer(read_only=True)
    errores = CargaErrorSerializer(many=True, read_only=True)

    class Meta:
        model = ArchivoCarga
        fields = [
            "id",
            "archivo",
            "usuario",
            "fecha_carga",
            "estado",
            "tipo_archivo",
            "mensaje",
            "errores",
        ]


# =============================
# CALIFICACIONES TRIBUTARIAS
# =============================
class CalificacionTributariaSerializer(serializers.ModelSerializer):
    creado_por = UserSerializer(read_only=True)
    instrumento = InstrumentoSerializer(read_only=True)
    factor = FactorConversionSerializer(read_only=True)
    archivo_origen = ArchivoCargaSerializer(read_only=True)

    instrumento_id = serializers.PrimaryKeyRelatedField(
        queryset=Instrumento.objects.all(), source="instrumento", write_only=True
    )
    factor_id = serializers.PrimaryKeyRelatedField(
        queryset=FactorConversion.objects.all(), source="factor", allow_null=True, required=False, write_only=True
    )
    archivo_origen_id = serializers.PrimaryKeyRelatedField(
        queryset=ArchivoCarga.objects.all(), source="archivo_origen", allow_null=True, required=False, write_only=True
    )

    class Meta:
        model = CalificacionTributaria
        fields = [
            "id",
            "instrumento",
            "instrumento_id",
            "rut",
            "tipo",
            "monto",
            "factor",
            "factor_id",
            "fecha",
            "estado",
            "comentario",
            "archivo_origen",
            "archivo_origen_id",
            "creado_por",
            "creado_en",
            "actualizado_en",
        ]


# =============================
# HISTORIAL CALIFICACIONES
# =============================
class HistorialCalificacionSerializer(serializers.ModelSerializer):
    usuario = UserSerializer(read_only=True)

    class Meta:
        model = HistorialCalificacion
        fields = ["id", "calificacion", "usuario", "accion", "descripcion", "fecha"]


# =============================
# AUDITORIA GENERAL
# =============================
class AuditoriaSerializer(serializers.ModelSerializer):
    usuario = UserSerializer(read_only=True)

    class Meta:
        model = Auditoria
        fields = ["id", "usuario", "accion", "fecha", "ip", "detalle"]


# =============================
# REGISTROS DE CARGA
# =============================
class CargaRegistroSerializer(serializers.ModelSerializer):
    usuario = UserSerializer(read_only=True)

    class Meta:
        model = CargaRegistro
        fields = ["id", "archivo", "usuario", "fecha_registro", "descripcion"]
