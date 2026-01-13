# Sistema de Ecuaciones Diferenciales - Múltiples Funciones

## Resumen de Cambios

El módulo de ecuaciones diferenciales ha sido **extendido para soportar sistemas de ecuaciones** (múltiples funciones simultáneamente), manteniendo la compatibilidad hacia atrás con ecuaciones únicas.

## Características Nuevas

### 1. Métodos Nuevos en `metodos.py`

Se agregaron dos métodos para resolver sistemas de ecuaciones:

#### `euler_sistema(x0, y0, xf, n, f_exprs)`
- Método de Euler para sistemas
- **Parámetros:**
  - `x0`: valor inicial de x
  - `y0`: lista de valores iniciales [y1_0, y2_0, ...]
  - `xf`: valor final de x
  - `n`: número de pasos
  - `f_exprs`: lista de funciones como strings [f1, f2, ...]
  
- **Retorna:** (x_valores, [[y1_valores], [y2_valores], ...], detalles)

#### `runge_kutta_4_sistema(x0, y0, xf, n, f_exprs)`
- Método de Runge-Kutta orden 4 para sistemas (recomendado por precisión)
- Mismos parámetros y retorno que `euler_sistema`

### 2. Función Auxiliar Mejorada

```python
def _eval_function(f_expr: str, x: float, y_values: List[float]) -> float:
```
- Evalúa expresiones con soporte para `x`, `y1`, `y2`, `y3`, etc.
- Mantiene compatibilidad con código que usa `y` para la primera variable

### 3. Interfaz Web Mejorada

#### Cambios en HTML (`ecuaciones_diferenciales.html`):
- **Sección de Funciones:**
  - Campo inicial para dy₁/dx
  - Botón "+" para agregar más funciones
  - Botón "-" para eliminar funciones
  - Uso de y1, y2, y3 en lugar de y

- **Sección de Condiciones Iniciales:**
  - Campos individuales para y₁(x₀), y₂(x₀), etc.
  - Botones + y - para agregar/eliminar condiciones iniciales

#### Cambios en JavaScript:
- `agregarFuncion()`: Crea nuevos campos de función
- `eliminarFuncion(index)`: Elimina función y su condición inicial
- `agregarY0()`: Agrega condición inicial
- `eliminarY0(index)`: Elimina condición inicial
- Validación que numero de funciones = numero de y0

#### Tabla de Resultados:
- Soporta múltiples columnas (y1, y2, y3, ...)
- Para ecuación única, muestra solo "y" (no "y1")

### 4. Endpoint API Mejorado

**POST `/api/ecuaciones-diferenciales`**

#### Para Ecuación Única (compatibilidad hacia atrás):
```json
{
  "metodo": "rk4",
  "x0": 0,
  "y0": 1,
  "xf": 1,
  "n": 10,
  "f_expr": "x + y"
}
```

**Retorna:**
```json
{
  "x_valores": [x0, x1, ..., xn],
  "y_valores": [[y0, y1, ..., yn]],
  "detalles": {...},
  "pares": [[x0, y0], [x1, y1], ...]
}
```

#### Para Sistema de Ecuaciones (nuevo):
```json
{
  "metodo": "rk4",
  "x0": 0,
  "y0": [1, 0],
  "xf": 1,
  "n": 10,
  "functions": ["y2", "-y1"]
}
```

**Retorna:**
```json
{
  "x_valores": [x0, x1, ..., xn],
  "y_valores": [
    [y1_0, y1_1, ..., y1_n],
    [y2_0, y2_1, ..., y2_n]
  ],
  "detalles": {...}
}
```

## Ejemplos de Uso

### Ejemplo 1: Oscilador Armónico (2x2)
```
dy₁/dx = y₂
dy₂/dx = -y₁

Condiciones iniciales: y₁(0) = 1, y₂(0) = 0

En la web:
- Función 1: y2
- Función 2: -y1
- y₁(0) = 1
- y₂(0) = 0
- Método: Runge-Kutta 4
- Pasos: 50
- x final: 2π ≈ 6.28
```

### Ejemplo 2: Sistema 3x3
```
dy₁/dx = y₂
dy₂/dx = y₃
dy₃/dx = -y₁

Condiciones iniciales: [1, 0, 0]

En la web:
- Función 1: y2
- Función 2: y3
- Función 3: -y1
- y₁(0) = 1, y₂(0) = 0, y₃(0) = 0
```

### Ejemplo 3: Predador-Presa (Lotka-Volterra)
```
dP/dt = αP - βPQ  (población de presas)
dQ/dt = δPQ - γQ  (población de depredadores)

Con: α=1, β=0.1, δ=0.075, γ=1.5

Función 1: y1 - 0.1*y1*y2
Función 2: 0.075*y1*y2 - 1.5*y2
```

## Compatibilidad

- ✅ Ecuaciones únicas siguen funcionando igual
- ✅ Todos los métodos existentes (Euler, Taylor 2/3/4, RK3, RK4, etc.)
- ✅ Sistemas soportan: Euler, Runge-Kutta 4
- ℹ️ Otros métodos pueden usarse pero se cae a RK4 para sistemas

## Pruebas

Se incluyen scripts de prueba:
- `test_sistema_odes.py`: Pruebas directas de métodos
- `test_api.py`: Pruebas de endpoint (requiere Flask ejecutándose)
- `test_api_final.py`: Suite completa de pruebas

## Limitaciones y Consideraciones

1. **Seguridad:** El sistema usa `eval()` para evaluar expresiones. No usar entrada no validada en producción.
2. **Variables:** Se soportan hasta donde sea necesario (y1, y2, y3, ..., y99)
3. **Métodos:** Para sistemas, usar Euler o RK4. Otros métodos (Taylor, Adams, etc.) se planean para futuras versiones.
4. **Precisión:** Runge-Kutta 4 recomendado para mejor precisión
5. **Estabilidad:** Para sistemas stiff, podría necesitarse reducir paso de integración

## Archivos Modificados

1. `metodos/metodos.py` - Nuevos métodos y función auxiliar
2. `app.py` - Endpoint mejorado para manejar ambos casos
3. `templates/ecuaciones_diferenciales.html` - UI mejorada
4. Se mantienen todos los archivos originales sin cambios de funcionalidad

## Próximas Mejoras Posibles

- Métodos adicionales para sistemas (Taylor orden 2+, Adams, etc.)
- Visualización gráfica de múltiples variables
- Métodos adaptativos de paso
- Soporte para ODEs rígidas (stiff)
- Exportación de resultados a CSV/Excel
