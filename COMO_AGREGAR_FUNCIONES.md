# INSTRUCCIONES: Cómo Agregar Múltiples Funciones

## ¿Dónde está el botón "+"?

El botón "+" se encuentra **justo a la derecha del campo de entrada de la primera función**.

```
dy₁/dx = f₁(x, y₁, y₂, ...)
┌─────────────────────────────┐  ┌─────┐
│ [Campo de entrada aquí]      │  │  +  │
└─────────────────────────────┘  └─────┘
                                  botón
```

## Pasos para Agregar Funciones:

### Paso 1: Completar la primera función
```
En el campo: escribir  "y2"
```

### Paso 2: Hacer clic en el botón "+"
```
Aparecerá un nuevo campo con la etiqueta:
dy₂/dx = f₂(x, y₁, y₂, ...)
En el campo: escribir  "-y1"
```

### Paso 3: Hacer clic en "+" de nuevo (opcional)
```
Aparecerá un tercer campo:
dy₃/dx = f₃(x, y₁, y₂, ...)
```

## Condiciones Iniciales

Cuando agregues funciones, **automáticamente se agregarán campos de condición inicial**:

```
Condiciones Iniciales y₀
┌─────────┐
│ y₁(x₀): │ [1.0]  [−]
├─────────┤
│ y₂(x₀): │ [0.0]  [−]
├─────────┤
│ y₃(x₀): │ [0.0]  [−]
└─────────┘
```

## Para Eliminar Funciones

Haz clic en el botón **"−"** (rojo) a la derecha de la función que deseas eliminar.

```
dy₂/dx = f₂(...)
┌─────────────────────────────┐  ┌─────┐
│ [Campo de función]           │  │  −  │
└─────────────────────────────┘  └─────┘
                                  botón eliminar
```

**Nota:** Cuando elimines una función, su condición inicial y₀ también se elimina automáticamente.

## Verificación: ¿Está funcionando?

### ✓ Debería pasar esto:
1. Ver el botón "+" verde al lado de la primera función
2. Al hacer clic, aparecer un nuevo campo
3. Las condiciones iniciales agregarse automáticamente
4. El botón "−" rojo permitir eliminar

### ✗ Si NO funciona:
1. **Limpia la caché del navegador**: Presiona `Ctrl+Shift+Supr` (en Chrome/Edge)
2. **Recarga la página**: `F5` o `Ctrl+R`
3. **Abre la consola**: `F12` → pestaña "Console"
4. Si hay errores rojos, captura una imagen

## Resumen de Controles

```
┌────────────────────────────────────────────────────────────┐
│                    FUNCIONES                                │
├────────────────────────────────────────────────────────────┤
│ dy₁/dx = f₁(...)  [Escribir expresión]  [+]               │
│                                                            │
│ dy₂/dx = f₂(...)  [Escribir expresión]  [−]  ← Agregada  │
│                                                            │
│ dy₃/dx = f₃(...)  [Escribir expresión]  [−]  ← Agregada  │
└────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────┐
│              CONDICIONES INICIALES Y₀                       │
├────────────────────────────────────────────────────────────┤
│ y₁(x₀): [1.0]  [−]  ← Se agrega/elimina auto              │
│                                                            │
│ y₂(x₀): [0.0]  [−]  ← Se agrega/elimina auto              │
│                                                            │
│ y₃(x₀): [0.0]  [−]  ← Se agrega/elimina auto              │
└────────────────────────────────────────────────────────────┘
```

## Ejemplo Completo: Oscilador Armónico

```
PASO 1: Escribir funciones
  Función 1: y2
  Click en "+"
  Función 2: -y1

PASO 2: Establecer condiciones iniciales (automáticas)
  y₁(0) = 1
  y₂(0) = 0

PASO 3: Parámetros
  x₀ = 0
  xf = 2π = 6.28
  n = 50 pasos

PASO 4: Seleccionar método
  Runge-Kutta 4

PASO 5: Hacer clic en "Calcular"
  
RESULTADO:
  Tabla con:
  x     | y1   | y2
  ------+------+------
  0.0   | 1.0  | 0.0
  0.126 | 0.99 |-0.13
  0.253 | 0.96 |-0.25
  ...
```

---

**¿Necesitas ayuda? Abre la consola del navegador (F12) y busca errores rojo.**
