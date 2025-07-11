# API Rest para Gestión de Usuarios y Películas 🎬👥  

Bienvenido al repositorio de la API Rest desarrollada con **Python**, **FastAPI** y **MongoDB**, diseñada para gestionar usuarios y películas de manera eficiente.  

## 📌 Características  

- **Gestión de Usuarios**: Registro, autenticación (JWT), y administración de perfiles.  
- **Gestión de Películas**: CRUD completo para películas con detalles como título, género, año, etc.  
- **Autenticación Segura**: Basada en tokens JWT (JSON Web Tokens).  
- **Base de Datos NoSQL**: MongoDB para almacenamiento flexible y escalable.  
- **Documentación Interactiva**: Integrada con Swagger UI y Redoc.  

## 🛠 Tecnologías Utilizadas  

- **Python 3.9+**  
- **FastAPI** (Framework web moderno y rápido)  
- **MongoDB** (Base de datos NoSQL)  
- **PyMongo** (Driver de MongoDB para Python)  
- **JWT** (Autenticación con tokens)  
- **Pydantic** (Validación de datos)  
- **Uvicorn** (Servidor ASGI para producción)  

## 📄 Endpoints Principales  

### 🔐 Autenticación  
- `POST /login` → Iniciar sesión y obtener token JWT.  

### 👥 Usuarios  
- `GET /users/` → Obtener información de los usuarios.
- `GET /users/{id}` → Obtener información de un usuario.
- `PUT /users/{id}` → Actualizar información del usuario.  
- `DELETE /users/{id}` → Eliminar cuenta de usuario.
- `POST /users/` → Crear cuenta de usuario.

### 🎬 Películas  
- `GET /movies/` → Obtener todas las películas (con filtros opcionales).  
- `GET /movies/{movie_id}` → Obtener detalles de una película específica.  
- `POST /movies/` → Crear una nueva película (requiere autenticación).  
- `PUT /movies/{movie_id}` → Actualizar una película (requiere autenticación).  
- `DELETE /movies/{movie_id}` → Eliminar una película (requiere autenticación).  

## 🚀 Instalación y Ejecución  

### Requisitos Previos  
- Python 3.9+ instalado.  
- MongoDB instalado y en ejecución (local o remoto).  

### Pasos para Configuración  

1. **Clonar el repositorio**:  
   ```bash
   git clone https://github.com/tu-usuario/fastapi-mongodb-movies.git
   cd fastapi-mongodb-movies