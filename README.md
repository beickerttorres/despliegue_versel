# GestorPro — App CRUD con Django + PostgreSQL

Sistema de gestión de proyectos y tareas colaborativas.

## Tecnologías
- **Backend:** Django 4.2
- **Base de datos:** PostgreSQL (Supabase / Neon.tech)
- **Frontend:** Django Templates + Bootstrap 5
- **Despliegue:** Vercel (o Railway recomendado)

---

## Configuración local

### 1. Clonar e instalar dependencias

```bash
git clone <tu-repo>
cd proyecto_crud
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
sour
```

### 2. Configurar variables de entorno

```bash
cp .env.example .env
# Editar .env con tus datos de PostgreSQL
```

### Configurar PostgreSQL local (Linux)

Si quieres usar PostgreSQL en tu máquina (Ubuntu/Debian), estos son pasos rápidos para crear un usuario y una base de datos:

```bash
# Instalar PostgreSQL si no lo tienes
sudo apt update
sudo apt install postgresql postgresql-contrib

# Crear un usuario y una base de datos (reemplaza valores)
sudo -u postgres createuser --pwprompt tu_usuario
sudo -u postgres createdb --owner=tu_usuario nombre_de_tu_base_de_datos

# Alternativa: entrar al prompt de psql y ejecutar SQL
sudo -u postgres psql
CREATE USER tu_usuario WITH PASSWORD 'tu_contraseña';
CREATE DATABASE nombre_de_tu_base_de_datos OWNER tu_usuario;
ALTER ROLE tu_usuario SET client_encoding TO 'utf8';
ALTER ROLE tu_usuario SET default_transaction_isolation TO 'read committed';
ALTER ROLE tu_usuario SET timezone TO 'UTC';
\q
```

Luego copia el archivo de ejemplo y rellena las variables en `.env`:

```
cp .env.example .env
# Edita .env y pon las credenciales creadas arriba
```

Ejemplo mínimo de `.env` para conexión local:

```
SECRET_KEY=django-insecure-cambia-esta-clave-en-produccion-usa-una-larga-y-aleatoria
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=nombre_de_tu_base_de_datos
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
DB_HOST=localhost
DB_PORT=5432
```

Probar la conexión y aplicar migraciones:

```bash
source venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Abre http://127.0.0.1:8000 y verifica que la aplicación arranca sin errores de base de datos.

### Supabase / PostgreSQL remoto

Si usas Supabase u otra base Postgres remota, copia los valores de conexión que te da el servicio en tu `.env`. Por ejemplo Supabase te da `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME` y `DB_PORT` — pégalos tal cual en las variables del `.env`.

Notas importantes para entornos remotos:
- Asegúrate de que `psycopg2-binary` está instalado (ya aparece en `requirements.txt`).
- Si el proveedor requiere SSL (como Supabase), la conexión estándar con los parámetros anteriores suele funcionar; si necesitas opciones avanzadas (por ejemplo `sslmode=require`) podemos adaptar `config/settings.py` para usar `DATABASE_URL` o `dj-database-url`.
 
 Si despliegas en Vercel, Supabase o Railway normalmente te darán una única URL de conexión llamada `DATABASE_URL`. Esto es lo recomendado porque incluye usuario, contraseña, host, puerto y nombre de la base en una sola variable y además permite activar SSL fácilmente.

 Pasos rápidos para usar la `DATABASE_URL` de Vercel / Supabase:

 1. En la dashboard del proveedor copia la `DATABASE_URL` (empieza con `postgres://` o `postgresql://`).
 2. En tu proyecto local añade esa línea a tu `.env`:

 ```bash
 DATABASE_URL=postgres://usuario:password@db.xxxxxxxx.supabase.co:5432/postgres
 ```

 3. He añadido soporte en `config/settings.py` para leer `DATABASE_URL` usando `dj-database-url`. Asegúrate de instalar dependencias:

 ```bash
 source venv/bin/activate
 pip install -r requirements.txt
 ```

 4. Prueba la conexión rápida con el script `check_db.py` incluido en la raíz del proyecto:

 ```bash
 source venv/bin/activate
 python check_db.py
 ```

 El script imprimirá si la conexión fue exitosa o mostrará el error recibido por `psycopg2`.

 Notas para Vercel:
 - En Vercel añade `DATABASE_URL` en las Environment Variables del proyecto.
 - Vercel normalmente usa `NODE_ENV`/`VERCEL_ENV`, pero Django leerá `DATABASE_URL` con `python-decouple` sin cambios.
 - Si el proveedor requiere que la conexión use `sslmode=require` la `DATABASE_URL` suele incluirlo; `dj-database-url` está configurado aquí para requerir SSL cuando se usa la URL.


### 3. Crear la base de datos y aplicar migraciones

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 4. Correr el servidor

```bash
python manage.py runserver
```

Abre: http://127.0.0.1:8000

---

## Base de datos gratuita (Supabase)

1. Ve a https://supabase.com y crea una cuenta
2. Crea un nuevo proyecto
3. Ve a **Settings > Database** y copia los datos de conexión
4. Pégalos en tu `.env`:

```
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=tu_password_de_supabase
DB_HOST=db.xxxxxxxx.supabase.co
DB_PORT=5432
```

---

## Crear la base de datos remota y conectar desde Vercel (ejemplo con Supabase)

Si vas a alojar la base de datos en un servicio remoto y desplegar en Vercel, sigue estos pasos.

1) Crear la base de datos en Supabase (u otro proveedor)

```bash
# Ve a https://supabase.com y crea un proyecto nuevo (o usa otro proveedor como Railway)
# Durante la creación se generará la base de datos Postgres y un usuario por defecto.
```

2) Obtener la `DATABASE_URL`

```text
# En Supabase: Project > Settings > Database > Connection string
# Copia la URL que empieza por `postgres://` o `postgresql://` (contiene usuario, contraseña, host, puerto y DB).
```

3) Añadir `DATABASE_URL` en Vercel

```text
# En Vercel > Your Project > Settings > Environment Variables
# Añade una variable con nombre: DATABASE_URL
# Pega la URL que copiaste de Supabase como valor.
# Repite para los entornos que necesites (Preview / Production / Development).
```

4) Probar y preparar la base de datos desde tu máquina local

```bash
# En tu máquina local (con el virtualenv activado) crea un .env con la DATABASE_URL para probar:
cp .env.example .env
# Edita .env y añade la línea:
DATABASE_URL=postgres://usuario:password@db.xxxxxxxx.supabase.co:5432/postgres

# Instala dependencias y prueba la conexión con el script incluido:
source venv/bin/activate
pip install -r requirements.txt
python check_db.py
```

Si `check_db.py` imprime "Conexión exitosa ✅" puedes continuar con las migraciones.

5) Ejecutar migraciones y crear superusuario (aplican sobre la BD remota)

```bash
# Con la misma .env que contiene DATABASE_URL activa y el venv:
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

Estas migraciones se aplicarán en la base de datos remota indicada por `DATABASE_URL`.

6) Ajustes en Vercel antes de desplegar

- En Vercel, además de `DATABASE_URL`, añade variables importantes:
   - `SECRET_KEY` = una clave larga aleatoria
   - `DEBUG` = False
   - `ALLOWED_HOSTS` = dominio_de_tu_app.vercel.app

- Asegúrate que `requirements.txt` incluye `psycopg2-binary` y `dj-database-url` (ya están en este repo).
- `config/settings.py` está preparado para leer `DATABASE_URL` y requerir SSL cuando se usa la URL.

7) Despliegue

```bash
# Haz commit y push a la rama que tengas conectada a Vercel (por ejemplo main/master)
git add .
git commit -m "Config DB: use DATABASE_URL for remote Postgres"
git push origin main
```

Vercel desplegará automáticamente. Si las migraciones deben correrse en el servidor, la forma más sencilla es ejecutarlas localmente apuntando al `DATABASE_URL` (como se muestra arriba) antes de desplegar; otra opción es integrar un paso en CI (GitHub Actions) que ejecute `python manage.py migrate` usando las secrets del proyecto.

Importante — seguridad

- No subas `.env` ni compartas `DATABASE_URL` públicamente. Trátala como un secreto.
- Usa las Environment Variables de Vercel para producción.


## Despliegue en Railway (Recomendado sobre Vercel)

Vercel tiene soporte limitado para Django con archivos de sesión y migraciones.
**Railway** es más sencillo para Django:

1. Ve a https://railway.app y crea una cuenta con GitHub
2. Crea un nuevo proyecto → **Deploy from GitHub repo**
3. Agrega un plugin de **PostgreSQL** — Railway llena las variables automáticamente
4. En Variables de entorno agrega:
   - `SECRET_KEY` = una clave larga aleatoria
   - `DEBUG` = False
   - `ALLOWED_HOSTS` = tu-app.railway.app
5. Railway detecta Django y despliega automáticamente

---

## Estructura del proyecto

```
proyecto_crud/
├── config/              # Configuración Django
├── apps/
│   ├── usuarios/        # Autenticación y perfiles
│   ├── proyectos/       # CRUD de proyectos
│   └── tareas/          # CRUD de tareas
├── templates/           # Templates base y dashboard
└── static/              # CSS y JS
```

## Funcionalidades CRUD implementadas

| Módulo    | Crear | Leer | Editar | Eliminar |
|-----------|-------|------|--------|----------|
| Proyectos | ✅    | ✅   | ✅     | ✅       |
| Tareas    | ✅    | ✅   | ✅     | ✅       |
| Usuarios  | ✅    | ✅   | —      | —        |

Extras: Dashboard con estadísticas, filtros, vista Kanban, autenticación completa.
# despliegue_versel
