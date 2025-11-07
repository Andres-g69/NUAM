Instrucciones para configurar el proyecto NUAM (con MySQL)
Primer paso:

Instalar MySQL Server (se recomienda la versión 8.0, aunque otras versiones también funcionan).
Instalar MySQL Workbench (recordar la contraseña del usuario root durante la instalación).

Segundo paso:

Clonar el repositorio del proyecto desde GitHub.
Crear y activar el entorno virtual.

Instalar las dependencias:
pip install -r requirements.txt

Tercer paso:

Ejecutar el siguiente comando en la terminal (dentro de la carpeta del proyecto) para crear la base de datos y el usuario configurado:
mysql -u root -p < db_setup.sql

Esto creará la base de datos nuam, el usuario nuamuser y asignará los permisos necesarios.

Cuarto paso:

Aplicar las migraciones de Django:
python manage.py migrate

No es necesario ejecutar makemigrations, ya que las migraciones están incluidas en el repositorio.

Quinto paso:

Ejecutar el servidor de desarrollo:
python manage.py runserver

Luego, acceder al proyecto desde el navegador en:
http://127.0.0.1:8000/

Sexto paso:

Abrir MySQL Workbench, conectarse a localhost:3306 con el usuario root,
y verificar que la base de datos nuam se haya creado correctamente.

▶️ 7. Ejecutar el servidor
python manage.py runserver
