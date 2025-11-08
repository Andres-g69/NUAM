from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# =============================
# VISTAS DEL FRONTEND (HTML)
# =============================
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('usuario')
        password = request.POST.get('password')
        from django.contrib.auth import authenticate, login

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # ✅ no dashboard.html
        else:
            return render(request, 'api/Login.html', {'error': 'Credenciales incorrectas'})

    return render(request, 'api/Login.html')

def dashboard_view(request):
    return render(request, 'api/Dashboard.html')

def gestion_view(request):
    return render(request, 'api/Gestion.html')

def carga_view(request):
    return render(request, 'api/Carga.html')

def busqueda_view(request):
    return render(request, 'api/Busqueda.html')

def admin_view(request):
    return render(request, 'api/Admin.html')

# =============================
# URLS PRINCIPALES
# =============================
urlpatterns = [
    path('admin/', admin.site.urls),

    # API REST
    path('api/', include('api.urls')),

    # JWT AUTH (CORRECTO)
    path('api/auth/login/', TokenObtainPairView.as_view(), name='jwt_login'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='jwt_refresh'),

    # FRONTEND
    path('', login_view, name='login'),          # 👈 también puede tener name='login'
    path('login/', login_view, name='login'),    # ✅ esto permite usar {% url 'login' %}
    path('dashboard/', dashboard_view, name='dashboard'),
    path('gestion/', gestion_view, name='gestion'),
    path('carga/', carga_view, name='carga'),
    path('busqueda/', busqueda_view, name='busqueda'),
    path('adminpanel/', admin_view, name='adminpanel'),     # evitar conflicto con /admin/
]

# =============================
# STATIC y MEDIA
# =============================
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
