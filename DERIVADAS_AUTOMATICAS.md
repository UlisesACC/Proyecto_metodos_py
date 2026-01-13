# Cálculo Automático de Derivadas - Documentación

## Resumen

Se implementó la funcionalidad de **cálculo automático de derivadas** para los métodos de Taylor y Runge-Kutta en el módulo de Ecuaciones Diferenciales. Ahora, cuando el usuario selecciona un método que requiera derivadas, el sistema calcula automáticamente las derivadas parciales respecto a `y` utilizando cálculo simbólico con SymPy.

## Componentes Implementados

### 1. Endpoint Flask: `/api/calcular-derivadas` (POST)

**Archivo:** `app.py` (línea 54-93)

**Función:** `api_calcular_derivadas()`

**Entrada (JSON):**
```json
{
  "f_expr": "expresión en términos de x e y",
  "orden": 3  // Cantidad de derivadas a calcular (1-3)
}
```

**Salida (JSON):**
```json
{
  "f_expr": "expresión original",
  "df_expr": "∂f/∂y",
  "ddf_expr": "∂²f/∂y²",
  "dddf_expr": "∂³f/∂y³",
  "orden": 3
}
```

**Características:**
- Utiliza SymPy para cálculo simbólico
- Maneja excepciones de expresiones inválidas
- Retorna derivadas como strings (formato legible)
- Calcula hasta 3 derivadas sucesivas respecto a y

### 2. Función JavaScript: `calcularDerivadas()`

**Archivo:** `templates/ecuaciones_diferenciales.html` (línea 607-643)

**Funcionalidad:**
- Obtiene la expresión de la función desde el input `.f_expr_input`
- Llama al endpoint `/api/calcular-derivadas`
- Llena automáticamente los campos:
  - `df_expr` (Primera derivada)
  - `ddf_expr` (Segunda derivada)
  - `dddf_expr` (Tercera derivada)
- Marca los campos como `readOnly` para evitar ediciones accidentales

### 3. Función JavaScript: `actualizarCampos()`

**Archivo:** `templates/ecuaciones_diferenciales.html` (línea 570-603)

**Cambios:**
- Detecta cuando el usuario selecciona un método Taylor o Runge-Kutta
- Muestra/oculta los campos de derivadas según el método:
  - **Taylor Orden 2:** Muestra `df_expr`
  - **Taylor Orden 3:** Muestra `df_expr` y `ddf_expr`
  - **Taylor Orden 4:** Muestra `df_expr`, `ddf_expr` y `dddf_expr`
  - **Runge-Kutta (RK3, RK4, RKF):** Muestra `df_expr` (opcional)
- Llama automáticamente a `calcularDerivadas()` para pre-llenar los valores

### 4. Event Listener

**Archivo:** `templates/ecuaciones_diferenciales.html` (línea 645-653)

- Se ejecuta cuando la página carga
- Escucha cambios en los inputs de funciones (`.f_expr_input`)
- Recalcula las derivadas automáticamente si el usuario cambia la expresión

## Ejemplo de Uso

### Caso 1: Taylor Orden 2 con f(x,y) = y²

1. Usuario ingresa: `y**2` en el campo de función
2. Selecciona "Taylor Orden 2"
3. El sistema ejecuta:
   ```
   GET /api/calcular-derivadas
   {f_expr: "y**2", orden: 1}
   ```
4. El campo `df_expr` se rellena automáticamente con: `2*y`

### Caso 2: Taylor Orden 4 con f(x,y) = sin(y)

1. Usuario ingresa: `sin(y)` en el campo de función
2. Selecciona "Taylor Orden 4"
3. El sistema calcula:
   - `df_expr = cos(y)`
   - `ddf_expr = -sin(y)`
   - `dddf_expr = -cos(y)`

## Limitaciones Conocidas y Soluciones

### Bug Corregido: `real=True` en SymPy

**Problema:** Cuando se creaban símbolos con `symbols('x y', real=True)`, SymPy no reconocía correctamente los símbolos en las expresiones parseadas con `parsing.parse_expr()`.

**Solución:** Se removió el argumento `real=True`. Los símbolos se crean como:
```python
x, y = symbols('x y')  # Sin real=True
```

**Resultado:** Las derivadas ahora se calculan correctamente.

## Expresiones Soportadas

El endpoint soporta cualquier expresión que SymPy puede parsear, incluyendo:

- Polinomios: `y**2`, `x*y + 1`
- Funciones trigonométricas: `sin(y)`, `cos(x + y)`
- Funciones exponenciales: `exp(y)`, `exp(x*y)`
- Funciones logarítmicas: `log(y)`, `log(1 + x*y)`
- Combinaciones: `sin(y)**2 + cos(x)*y`

## Pruebas Realizadas

Todas las pruebas con derivadas correctas han sido verificadas:

```
y²:        ∂f/∂y = 2*y      ✓
1+y:       ∂f/∂y = 1        ✓
xy:        ∂f/∂y = x        ✓
sin(y):    ∂f/∂y = cos(y)   ✓
x+y:       ∂f/∂y = 1        ✓
```

## Flujo de Ejecución

```
Usuario selecciona método Taylor
    ↓
JavaScript ejecuta actualizarCampos()
    ↓
Se muestra el campo de derivadas
    ↓
JavaScript ejecuta calcularDerivadas()
    ↓
Solicitud POST a /api/calcular-derivadas
    ↓
SymPy calcula derivadas simbólicamente
    ↓
Respuesta JSON con derivadas
    ↓
Campos se rellenan automáticamente
    ↓
Campos marcados como readOnly
```

## Notas Técnicas

- Las derivadas se calculan respecto a `y` (variable dependiente)
- Se calcula hasta 3 órdenes de derivadas
- Las respuestas se convierten a strings para mayor legibilidad
- Se incluye manejo robusto de errores en ambos lados (backend y frontend)
- Los campos de derivadas son read-only después del cálculo automático

## Archivos Modificados

1. `app.py` - Agregado endpoint `/api/calcular-derivadas`
2. `templates/ecuaciones_diferenciales.html` - Actualizado JavaScript
3. `templates/test_derivadas.html` - Página de prueba (DEBUG)

## Próximas Mejoras Posibles

- [ ] Agregar opción para editar derivadas manualmente
- [ ] Mostrar paso a paso cómo se calculan las derivadas
- [ ] Validación visual de errores en la expresión
- [ ] Soporte para derivadas parciales respecto a x
- [ ] Cache de derivadas calculadas para mejorar rendimiento
