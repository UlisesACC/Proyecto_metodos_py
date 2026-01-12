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
├── app.py                           # Aplicación principal de Flask y rutas API
├── requirements.txt                 # Dependencias del proyecto
├── Dockerfile                       # Configuración de Docker
├── docker-compose.yml               # Configuración de Docker Compose
├── .dockerignore                    # Archivos a ignorar en Docker
├── .gitignore                       # Archivos a ignorar en Git
├── README.md                        # Este archivo
├── metodos/
│   ├── __init__.py                 # Inicializador del paquete
│   └── metodos.py                  # Implementación de métodos numéricos
├── templates/
│   ├── index.html                  # Página principal
│   ├── diferencias_divididas.html  # Interfaz interpolación
│   └── derivacion.html             # Interfaz derivación numérica
└── static/
    └── style.css                    # Estilos CSS (estilo novato)
```

## Métodos Numéricos Disponibles

### Interpolación - Diferencias Divididas
- **Hacia Adelante**: Utiliza los nodos posteriores para calcular la interpolación
- **Hacia Atrás**: Utiliza los nodos anteriores para calcular la interpolación  
- **Neville**: Método de interpolación polinomial sin calcular coeficientes

### Derivación Numérica

#### Hacia Adelante (Forward Differences)
- **2 Puntos**: $f'(x) \\approx \\frac{f(x+h) - f(x)}{h}$
- **3 Puntos**: $f'(x) \\approx \\frac{-3f(x) + 4f(x+h) - f(x+2h)}{2h}$
- **5 Puntos**: $f'(x) \\approx \\frac{-11f(x) + 18f(x+h) - 9f(x+2h) + 2f(x+3h)}{6h}$

#### Hacia Atrás (Backward Differences)
- **2 Puntos**: $f'(x) \\approx \\frac{f(x) - f(x-h)}{h}$
- **3 Puntos**: $f'(x) \\approx \\frac{3f(x) - 4f(x-h) + f(x-2h)}{2h}$
- **5 Puntos**: $f'(x) \\approx \\frac{-2f(x-3h) + 9f(x-2h) - 18f(x-h) + 11f(x)}{6h}$

#### Centrada (Centered Differences)
- **2 Puntos**: $f'(x) \\approx \\frac{f(x+h) - f(x-h)}{2h}$
- **3 Puntos**: $f'(x) \\approx \\frac{-f(x+h) + f(x-h)}{2h}$
- **5 Puntos**: $f'(x) \\approx \\frac{-f(x+2h) + 8f(x+h) - 8f(x-h) + f(x-2h)}{12h}$

#### Extrapolación de Richardson
- Mejora la precisión usando dos tamaños de paso diferentes

## Características

- ✨ Interfaz web intuitiva con acordeón para mejor organización
- 📐 Visualización de fórmulas matemáticas con LaTeX (MathJax)
- 📊 Tablas de cálculos detallados
- 🚀 API REST para integración con otras aplicaciones
- 🐳 Soporte para Docker y Docker Compose
- 📱 Diseño responsivo (CSS novato)
- 🔄 Soporte para múltiples métodos numéricos

## Desarrollo

El proyecto está configurado para ejecutarse en modo de desarrollo con hot-reload automático al modificar los archivos.
