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
- source /home/frontend1/NUAM/db_setup.sql; (colocar direccion de archivo db_setup.ql)
- exit

4️⃣ Aplicar las migraciones de la base de datos

Ejecuta los siguientes comandos para crear las tablas necesarias en la base de datos:

- python manage.py makemigrations
- python manage.py migrate


5️⃣ Crear un superusuario (opcional, para administración)

Si deseas acceder al panel de administración de Django, crea un superusuario:

- python manage.py createsuperuser


Sigue las instrucciones en pantalla (nombre, correo y contraseña).


6️⃣ Ejecutar el servidor

Inicia el servidor de desarrollo de Django:

- python manage.py runserver


Por defecto, el servidor estará disponible en:

👉 http://127.0.0.1:8000/


7️⃣ Acceder al sistema

Una vez iniciado el servidor, puedes acceder a las siguientes rutas principales:

- Login: /login/

- Registro: /register/

- Dashboard principal: /dashboard/

Ejemplo:
http://127.0.0.1:8000/login/


8️⃣Acceder a Panel de Administración

De la misma manera de las rutas principales seguiremos con el panel de administración:

- http://127.0.0.1:8000/admin/

- con los valores del superuser creados anteriormente iniciar sesion

- full acceso al panel de administración del sistema


9️⃣Detener el servidor

Para detener el servidor presiona Ctrl + C en la terminal donde se esté ejecutando.
