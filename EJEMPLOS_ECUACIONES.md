# Ejemplos de Uso - Ecuaciones de Una Variable

Esta guía proporciona ejemplos de cómo usar cada método para encontrar raíces de ecuaciones.

## Sintaxis de Funciones

- **Operadores**: `+`, `-`, `*`, `/`, `**` (potencia)
- **Funciones**: `sqrt()`, `sin()`, `cos()`, `tan()`, `exp()`, `log()`, `log10()`, `abs()`
- **Constantes**: `pi`, `e`
- **Variable**: `x`

---

## 1. Método de Bisección

**Requisitos**: Función f(x), intervalo [a, b] donde f(a) y f(b) tienen signos opuestos

### Ejemplo 1: Raíz de x² - 4
- **f(x)**: `x**2 - 4`
- **a**: `-5`
- **b**: `5`
- **Raíz esperada**: `2` (o `-2`)

### Ejemplo 2: Raíz de cos(x) - x
- **f(x)**: `cos(x) - x`
- **a**: `0`
- **b**: `1`
- **Raíz esperada**: `~0.739` (punto fijo de cos(x))

---

## 2. Método de Falsa Posición

Funciona similar a bisección pero usa interpolación lineal. Generalmente converge más rápido.

### Ejemplo 1: f(x) = x³ - 2
- **f(x)**: `x**3 - 2`
- **a**: `1`
- **b**: `2`
- **Raíz esperada**: `~1.260` (raíz cúbica de 2)

### Ejemplo 2: f(x) = e^x - 3x
- **f(x)**: `exp(x) - 3*x`
- **a**: `0`
- **b**: `1`
- **Raíz esperada**: `~0.619`

---

## 3. Método de la Secante

**Requisitos**: Función f(x), dos puntos iniciales x₀ y x₁

### Ejemplo 1: f(x) = x² - 4
- **f(x)**: `x**2 - 4`
- **x₀**: `1`
- **x₁**: `3`
- **Raíz esperada**: `2`

### Ejemplo 2: f(x) = ln(x) - 1
- **f(x)**: `log(x) - 1`
- **x₀**: `2`
- **x₁**: `3`
- **Raíz esperada**: `~2.718` (e)

---

## 4. Método de Newton-Raphson

**Requisitos**: Función f(x), su derivada f'(x), punto inicial x₀

### Ejemplo 1: f(x) = x² - 4, f'(x) = 2x
- **f(x)**: `x**2 - 4`
- **f'(x)**: `2*x`
- **x₀**: `3`
- **Raíz esperada**: `2`

### Ejemplo 2: f(x) = cos(x) - x, f'(x) = -sin(x) - 1
- **f(x)**: `cos(x) - x`
- **f'(x)**: `-sin(x) - 1`
- **x₀**: `0.5`
- **Raíz esperada**: `~0.739`

### Ejemplo 3: f(x) = e^x - 3x, f'(x) = e^x - 3
- **f(x)**: `exp(x) - 3*x`
- **f'(x)**: `exp(x) - 3`
- **x₀**: `1`
- **Raíz esperada**: `~0.619`

---

## 5. Método de Punto Fijo

**Requisitos**: Función de iteración g(x) tal que x = g(x), punto inicial x₀

Para resolver f(x) = 0, despeja x: x = g(x) = x - f(x) o cualquier otra forma

### Ejemplo 1: Resolver x² - 4 = 0
Despejar como: x = √4 = 2 (o x = 4/x)
- **g(x)**: `4/x`
- **x₀**: `3`
- **Raíz esperada**: `2`

### Ejemplo 2: Resolver x - cos(x) = 0
Despejar como: x = cos(x)
- **g(x)**: `cos(x)`
- **x₀**: `0.5`
- **Raíz esperada**: `~0.739`

### Ejemplo 3: Resolver x³ - 2 = 0
Despejar como: x = (2/x²)^(1/3) o x = ∛(2)
- **g(x)**: `(2/x**2)**(1/3)`
- **x₀**: `1.5`
- **Raíz esperada**: `~1.260`

---

## 6. Método de Müller

**Requisitos**: Función f(x), tres puntos iniciales x₀, x₁, x₂

### Ejemplo 1: f(x) = x² - 4
- **f(x)**: `x**2 - 4`
- **x₀**: `0`
- **x₁**: `1`
- **x₂**: `4`
- **Raíz esperada**: `2` (o `±2`)

### Ejemplo 2: f(x) = x³ - x - 1
- **f(x)**: `x**3 - x - 1`
- **x₀**: `1`
- **x₁**: `1.5`
- **x₂**: `2`
- **Raíz esperada**: `~1.325`

---

## Comparación de Métodos

| Método | Ventajas | Desventajas | Convergencia |
|--------|----------|-------------|--------------|
| **Bisección** | Siempre converge, simple | Lento | Lineal |
| **Falsa Posición** | Más rápido que bisección | Puede ser lento | Lineal/Superlineal |
| **Secante** | No necesita derivada | Puede no converger | Superlineal |
| **Newton-Raphson** | Muy rápido | Necesita derivada | Cuadrática |
| **Punto Fijo** | Simple y flexible | Convergencia lenta | Lineal |
| **Müller** | Puede encontrar complejas | Más cálculos | Superlineal |

---

## Consejos

1. **Tolerancia**: Usa `1e-5` para precisión estándar, `1e-8` para mayor precisión
2. **Iteraciones máximas**: `100` es usualmente suficiente, aumenta si no converge
3. **Punto inicial (Newton-Raphson)**: Debe estar cerca de la raíz para converger
4. **Intervalo (Bisección)**: Verifica que f(a) y f(b) tengan signos opuestos
5. **Función de iteración (Punto Fijo)**: |g'(x)| < 1 cerca de la raíz para convergencia

---

## Errores Comunes

- ❌ "No hay cambio de signo": Asegúrate de que f(a) × f(b) < 0 para bisección/falsa posición
- ❌ "La derivada es cero": El punto está en un extremo local, cambia x₀ en Newton-Raphson
- ❌ "Denominador muy pequeño": Los puntos son demasiado cercanos, aumenta la distancia inicial
- ❌ "No converge": Incrementa max_iteraciones o revisa la función/parámetros iniciales
