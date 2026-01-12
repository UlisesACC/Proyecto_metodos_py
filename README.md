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

### 1. Interpolación - Diferencias Divididas
- **Hacia Adelante**: Utiliza los nodos posteriores para calcular la interpolación
- **Hacia Atrás**: Utiliza los nodos anteriores para calcular la interpolación  
- **Neville**: Método de interpolación polinomial sin calcular coeficientes

### 2. Derivación Numérica

#### Hacia Adelante (Forward Differences)
- **2 Puntos**: $f'(x) \approx \frac{f(x+h) - f(x)}{h}$
- **3 Puntos**: $f'(x) \approx \frac{-3f(x) + 4f(x+h) - f(x+2h)}{2h}$
- **5 Puntos**: $f'(x) \approx \frac{-11f(x) + 18f(x+h) - 9f(x+2h) + 2f(x+3h)}{6h}$

#### Hacia Atrás (Backward Differences)
- **2 Puntos**: $f'(x) \approx \frac{f(x) - f(x-h)}{h}$
- **3 Puntos**: $f'(x) \approx \frac{3f(x) - 4f(x-h) + f(x-2h)}{2h}$
- **5 Puntos**: $f'(x) \approx \frac{-2f(x-3h) + 9f(x-2h) - 18f(x-h) + 11f(x)}{6h}$

#### Centrada (Centered Differences)
- **2 Puntos**: $f'(x) \approx \frac{f(x+h) - f(x-h)}{2h}$
- **3 Puntos**: $f'(x) \approx \frac{-f(x+h) + f(x-h)}{2h}$
- **5 Puntos**: $f'(x) \approx \frac{-f(x+2h) + 8f(x+h) - 8f(x-h) + f(x-2h)}{12h}$

#### Extrapolación de Richardson
- Mejora la precisión usando dos tamaños de paso diferentes

### 3. Integración Numérica
- **Trapecio**: $\int_a^b f(x)dx \approx \frac{h}{2}[f_0 + 2f_1 + ... + 2f_{n-1} + f_n]$
- **Simpson 1/3**: $\int_a^b f(x)dx \approx \frac{h}{3}[f_0 + 4f_1 + 2f_2 + ... + f_n]$
- **Simpson 3/8**: $\int_a^b f(x)dx \approx \frac{3h}{8}[f_0 + 3f_1 + 3f_2 + ... + f_n]$
- **Cuadratura Gaussiana**: Integración usando puntos óptimos y pesos
- **Integración Múltiple**: Extensión 2D de Trapecio y Simpson 1/3
- **Extrapolación Richardson**: Mejora de precisión combinando intervalos

### 4. Sistemas de Ecuaciones Lineales

#### Eliminación Gaussiana
- **Simple**: Método básico sin pivoteo
- **Pivoteo Parcial**: Selecciona el máximo en la columna
- **Pivoteo Total**: Selecciona el máximo en toda la submatriz

#### Factorización de Matrices
- **LU**: Descomposición $A = LU$
- **PLU**: Descomposición con pivoteo $PA = LU$
- **LLT (Cholesky)**: Para matrices simétricas positivas definidas $A = LL^T$

### 5. Ecuaciones Diferenciales Ordinarias

#### Métodos de Paso Fijo
- **Euler**: Orden 1, $y_{n+1} = y_n + hf(x_n, y_n)$
- **Taylor Orden 2**: Incorpora primera derivada
- **Taylor Orden 3**: Incorpora segunda derivada
- **Taylor Orden 4**: Incorpora tercera derivada

#### Runge-Kutta
- **Orden 3**: 3 evaluaciones de función
- **Orden 4**: 4 evaluaciones de función (más popular)
- **Runge-Kutta-Fehlberg (4-5)**: Método adaptativo con control de error

#### Métodos Multi-paso
- **Adams-Bashforth**: Método explícito de 4 pasos
- **Adams-Moulton**: Método implícito de 4 pasos (predictor-corrector)

## Características

- ✨ Interfaz web intuitiva con acordeón para mejor organización
- 📐 Visualización de fórmulas matemáticas con LaTeX (MathJax)
- 📊 Tablas de cálculos detallados
- 🚀 API REST para integración con otras aplicaciones
- 🐳 Soporte para Docker y Docker Compose
- 📱 Diseño responsivo (CSS novato)
- 🔄 Soporte para múltiples métodos numéricos
- 📖 Botones "Ver fórmula" en cada método para consultar la ecuación matemática

## Documentación Completa de Fórmulas

Para una documentación detallada con **todas las fórmulas matemáticas**, consulta:

📄 **[README_FORMULAS.md](README_FORMULAS.md)**

Este archivo contiene:
- Todas las fórmulas en notación LaTeX
- Explicación de parámetros
- Órdenes de error y convergencia
- Tabla comparativa de métodos
- Notas sobre estabilidad y precisión

## Desarrollo

El proyecto está configurado para ejecutarse en modo de desarrollo con hot-reload automático al modificar los archivos.
