# Aplicación de Métodos Numéricos

Aplicación web desarrollada con Flask y Python para realizar cálculos y análisis utilizando diferentes métodos numéricos.

## Requisitos

- Python 3.11+
- Docker (opcional, para ejecutar con contenedores)

## Instalación Local

### 1. Crear entorno virtual

```bash
python -m venv venv
```

### 2. Activar entorno virtual

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Ejecutar la aplicación

```bash
python app.py
```

La aplicación estará disponible en `http://localhost:5000`

## Ejecución con Docker

### 1. Construir la imagen

```bash
docker build -t metodos-numericos .
```

### 2. Ejecutar el contenedor

```bash
docker run -p 5000:5000 metodos-numericos
```

### Con Docker Compose

```bash
docker-compose up
```

## Estructura del Proyecto

```
Proyecto_metodos_py/
├── app.py                 # Aplicación principal de Flask
├── requirements.txt       # Dependencias del proyecto
├── Dockerfile            # Configuración de Docker
├── docker-compose.yml    # Configuración de Docker Compose
├── .dockerignore         # Archivos a ignorar en Docker
├── .gitignore           # Archivos a ignorar en Git
├── templates/           # Plantillas HTML
│   └── index.html       # Página principal
└── static/              # Archivos estáticos
    └── style.css        # Estilos CSS
```

## Métodos Numéricos Disponibles

- Bisección
- Newton-Raphson
- Interpolación
- Integración Numérica

## Desarrollo

El proyecto está configurado para ejecutarse en modo de desarrollo con hot-reload automático al modificar los archivos.
