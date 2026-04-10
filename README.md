# Blacklist Microservice - Proyecto 1

Microservicio robusto para la gestión de listas negras de emails, diseñado para ser escalable, seguro y fácil de desplegar.

## 🏗️ Estructura del Proyecto

```Plaintext
.
├── app/                    # Lógica principal del microservicio
│   ├── __init__.py         # Configuración de Flask y extensiones (Factory Pattern)
│   ├── config.py           # Gestión de variables de entorno y constantes
│   ├── models.py           # Definición de tablas con SQLAlchemy
│   ├── schemas.py          # Validación y serialización con Marshmallow
│   └── resources.py        # Definición de Endpoints (Flask-RESTful)
├── migrations/             # Historial de versiones de la base de datos (Alembic)
│   └── versions/           # Scripts de migración generados automáticamente
├── postman/                # Colecciones y entornos para pruebas de integración
│   ├── Blacklist_Collection.postman_collection.json
│   └── Dev.postman_environment.json
├── tests/                  # Pruebas unitarias y de integración (Pytest)
│   ├── conftest.py         # Fixtures y configuración de los tests
│   └── test_blacklist.py   # Casos de prueba del microservicio
├── .env.example            # Plantilla de variables de entorno para nuevos devs
├── .gitignore              # Archivos y carpetas excluidos del repositorio
├── application.py          # Punto de entrada para el servidor (WSGI)
├── docker-compose.yml      # Orquestación de la base de datos PostgreSQL
├── gen_token.py            # Script para generar tokens JWT de prueba
└── requirements.txt        # Dependencias del proyecto (incluye pytest-flask)
```

## 🚀 Requisitos Previos

- **Python 3.12+**

- **Docker & Docker Compose**

- **Postman** o **cURL**

- **Node.js & Newman**

## 🛠️ Configuración Inicial

1. **Clonar el repositorio y entrar a la carpeta:**

```bash

git clone https://github.com/DevOps-Misw4304-202610/Proyecto1.git

cd Proyecto1

```

1. **Configurar el entorno virtual:**

```bash

python -m venv .venv

source .venv/bin/activate # En Linux/macOS

# .venv\Scripts\activate # En Windows

pip install -r requirements.txt

```

1. **Variables de entorno:**

```bash

cp .env.example .env

```

## 📦 Base de Datos y Migraciones

1. **Levantar el contenedor de PostgreSQL:**

```bash

docker compose up -d

```

1. **Preparar las tablas (Alembic):**

Si es la primera vez o si se limpió la base de datos:

```bash

flask db upgrade

```

*Nota: Si necesitas resetear las migraciones desde cero, usa `flask db stamp head` después de un upgrade si la base de datos ya está sincronizada.*

## 🏃 Ejecución del Servicio

Para iniciar el servidor de desarrollo:

```bash

python application.py

```

El servicio estará disponible en `http://localhost:5000`.

## 🧪 Pruebas y Validación

### 1. Pruebas Unitarias (Pytest)

Ejecuta los tests automáticos para verificar la lógica interna y la conexión a la base de datos (usa SQLite en memoria para aislamiento):

```bash
python -m pytest -v -s
```

### 2. Pruebas de Integración (Newman/Postman)

Asegúrate de que el servidor (`application.py`) esté corriendo en otra terminal y ejecuta la suite completa de pruebas:

```bash
newman run postman/Blacklist_Collection.postman_collection.json -e postman/Dev.postman_environment.json
```

### 3. Verificación Manual con cURL

#### A. Health Check (Público)

```bash
curl -X GET http://localhost:5000/health
```

#### B. Agregar a Blacklist (Protegido)

Sustituye `<TOKEN>` por el string generado con `python gen_token.py`.

```bash
curl -X POST http://localhost:5000/blacklists \
     -H "Authorization: Bearer <TOKEN>" \
     -H "Content-Type: application/json" \
     -d '{
           "email": "estudiante@uniandes.edu.co",
           "app_uuid": "550e8400-e29b-41d4-a716-446655440000",
           "blocked_reason": "Prueba de integración"
         }'
```

#### C. Consultar Email (Protegido)

Verifica si el email anterior fue registrado correctamente:

```bash
curl -X GET http://localhost:5000/blacklists/estudiante@uniandes.edu.co \
     -H "Authorization: Bearer <TOKEN>"
```

### 4. Verificar en Base de Datos (Docker Exec)

Para confirmar la persistencia real en el contenedor de PostgreSQL:

```bash
docker exec -it proyecto1-db-1 psql -U user_blacklist -d blacklist_db -x -c "SELECT * FROM blacklist ORDER BY \"createdAt\" DESC LIMIT 1;"
```

## 🛠️ Guía de Desarrollo para el Equipo

Si necesitas agregar una nueva funcionalidad o endpoint, sigue este flujo para mantener la consistencia:

1. **Modelos:** Si necesitas una nueva tabla, defínela en `app/models.py`.

2. **Migraciones:** Después de cambiar un modelo, genera la migración:

```bash

flask db migrate -m "Descripción del cambio"

flask db upgrade

```

*¡No olvides hacer commit de la carpeta `migrations/`!*

1. **Schemas:** Define la validación en `app/schemas.py` usando Marshmallow.

2. **Recursos:** Crea la lógica del endpoint en `app/resources.py`.

3. **Rutas:** Registra el nuevo recurso en `app/__init__.py` usando `api.add_resource()`.

---

### Notas de Seguridad

- El archivo `.env` está en el `.gitignore`. Nunca subas credenciales reales al repositorio.

- Para producción (AWS Beanstalk), las variables de entorno se configuran desde la consola de AWS, no desde el archivo `.env`.

## 🛠️ Comandos de Utilidad

- **Limpiar base de datos y volúmenes:**

```bash

docker compose down -v

```

- **Generar un nuevo token JWT para pruebas manuales:**

```bash

python gen_token.py

```
