# Blacklist Microservice

Microservicio para la gestión de listas negras de emails. Desarrollado con Flask, PostgreSQL y desplegable en AWS Beanstalk.

## 🚀 Requisitos Previos
- Python 3.12+
- Docker & Docker Compose
- Postman (para pruebas)

## 🛠️ Configuración Local

1. **Clonar y preparar entorno:**
   ```bash
   git clone <tu-repo>
   cd blacklist-service
   python -m venv venv
   source venv/bin/activate  # En Linux/CachyOS
   pip install -r requirements.txt
   ```

2. **Levantar Base de Datos (Docker):**
   ```bash
   docker compose up -d
   ```

3. **Configurar Variables:**
   Crea un archivo `.env` basado en el siguiente ejemplo:
   ```env
   DATABASE_URL=postgresql+psycopg://user_blacklist:password123@localhost:5417/blacklist_db
   JWT_SECRET_KEY=clave-secreta-proyecto
   ```

4. **Preparar la DB (Migraciones):**
   ```bash
   flask db upgrade
   ```

5. **Generar Token de Acceso:**
   Ejecuta el script para obtener el Bearer Token que usarás en Postman:
   ```bash
   python gen_token.py
   ```

## 🏃 Ejecución
```bash
python application.py
```
El servicio estará disponible en `http://localhost:5000`.

## 🧪 Endpoints Principales
- **GET /health**: Verifica el estado del servicio (Healthcheck).
- **POST /blacklists**: Agrega un email a la lista. 
  - Requiere: `Authorization: Bearer <TOKEN>`
  - Body: `{"email": "test@mail.com", "app_uuid": "UUID", "blocked_reason": "spam"}`
```
