Bastian Cabello y Andres Gonzalez

⚡ Instrucciones Comunes

Antes de comenzar:

- Asegúrate de tener Python 3.11 o superior instalado.

- Descarga e instala MySQL Server (recomendado versión 8.0) y MySQL Workbench.

- Recuerda la contraseña del usuario root de MySQL durante la instalación.


🛠️ Instalación del Sistema NUAM en Linux

Sigue los pasos a continuación para instalar y ejecutar el proyecto NUAM en un entorno Linux.


1️⃣ Clonar el repositorio

Abre una terminal y clona el proyecto desde GitHub:

- git clone https://github.com/Andres-g69/NUAM.git

Luego entra al directorio del proyecto:

- cd NUAM


2️⃣ Crear un entorno virtual (recomendado)

Crea un entorno virtual de Python para aislar las dependencias del proyecto:

- python3 -m venv environment


Activa el entorno virtual:

- source environment/bin/activate

💡 Si al intentar usar python3 no funciona, puedes probar con python.

3️⃣ Instalar las dependencias

Antes de instalar las librerias se aplican los siguientes comandos requeridos:

- sudo apt update (colocar su contraseña de dispositivo si la requiere)
- sudo apt install mysql-server
- sudo apt install pkg-config libmysqlclient-dev build-essential (instala paquetees esenciales para mysqlclient)

Instala todas las librerías necesarias desde el archivo requirements.txt:

- pip install -r requirements.txt

- sudo mysql
- source db_setup.sql;
- exit

4️⃣ Aplicar las migraciones de la base de datos

Ejecuta los siguientes comandos para crear las tablas necesarias en la base de datos:

- python manage.py makemigrations
- python manage.py migrate


5️⃣ Crear un superusuario (opcional, para administración)

Si deseas acceder al panel de administración de Django y Sistema, crea un superusuario:

- python manage.py createsuperuser


Sigue las instrucciones en pantalla (nombre, correo y contraseña).


6️⃣ Ejecutar el servidor

Inicia el servidor de desarrollo de Django:

- python manage.py runserver


Por defecto, el servidor estará disponible en:

👉 http://127.0.0.1:8000/


7️⃣Acceder a Panel de Administración

Para poder acceder a este panel debe iniciar sesion con las credenciales registradas al crear el superusuario.


8️⃣ Detener el servidor

Para detener el servidor presiona Ctrl + C en la terminal donde se esté ejecutando.


🪟 Instalación en Windows

1️⃣ Clonar el repositorio

Abre PowerShell o CMD y ejecuta:

- git clone https://github.com/Andres-g69/NUAM.git
- cd NUAM

2️⃣ Crear y activar entorno virtual

- python -m venv environment
- environment\Scripts\activate

3️⃣ Instalar dependencias

- pip install -r requirements.txt

4️⃣ Crear la base de datos

- Abre MySQL Workbench o la terminal de MySQL y ejecuta:
- mysql -u root -p < db_setup.sql

Esto creará la base de datos nuam, el usuario nuamuser y asignará los permisos necesarios.

5️⃣ Aplicar migraciones de Django

- python manage.py makemigrations
- python manage.py migrate

6️⃣ Crear superusuario (opcional)

- python manage.py createsuperuser
- Sigue las instrucciones en pantalla (nombre, correo y contraseña).

Con este superusuario puedes acceder al panel de administración para gestionar usuarios y auditorías usando el username y contraseña.

7️⃣ Ejecutar el servidor

-python manage.py runserver

Accede al sistema en: http://127.0.0.1:8000/

8️⃣ Detener el servidor

Para detener el servidor presiona Ctrl + C en la terminal donde se esté ejecutando.
