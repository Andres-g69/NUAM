from django.contrib import admin, messages
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


# =============================
# VISTAS FRONTEND (HTML)
# =============================

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('usuario')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Credenciales incorrectas.')

    return render(request, 'api/Login.html')


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        pw1 = request.POST.get('password1', '')
        pw2 = request.POST.get('password2', '')

        if not username or not email or not pw1 or not pw2:
            messages.error(request, 'Completa todos los campos.')
            return render(request, 'api/Register.html')

        if pw1 != pw2:
            messages.error(request, 'Las contraseñas no coinciden.')
            return render(request, 'api/Register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'El usuario ya existe.')
            return render(request, 'api/Register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'El correo ya está en uso.')
            return render(request, 'api/Register.html')

        user = User.objects.create_user(username=username, email=email, password=pw1)
        user.save()

        messages.success(request, 'Cuenta creada correctamente. Ahora inicia sesión.')
        return redirect('login')

    return render(request, 'api/Register.html')


def logout_view(request):
    logout(request)
    messages.info(request, 'Has cerrado sesión.')
    return redirect('login')


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

    # JWT AUTH
    path('api/auth/login/', TokenObtainPairView.as_view(), name='jwt_login'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='jwt_refresh'),

    # FRONTEND
    path('', login_view, name='login'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('gestion/', gestion_view, name='gestion'),
    path('carga/', carga_view, name='carga'),
    path('busqueda/', busqueda_view, name='busqueda'),
    path('adminpanel/', admin_view, name='adminpanel'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
