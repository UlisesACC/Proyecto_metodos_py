# Cambios Realizados - Actualización Derivación Numérica

## Resumen
Se han agregado métodos de derivación **hacia adelante** y **hacia atrás** a la aplicación, junto con una mejora de la interfaz usando un **acordeón** para mejor organización.

## Métodos Agregados

### Derivación Hacia Adelante (Forward Differences)
✅ **2 Puntos Hacia Adelante** - `dos_puntos_adelante()`
✅ **3 Puntos Hacia Adelante** - `tres_puntos_adelante()` 
✅ **5 Puntos Hacia Adelante** - `cinco_puntos_adelante()`

### Derivación Hacia Atrás (Backward Differences)
✅ **5 Puntos Hacia Atrás** - `cinco_puntos_atras()`
(Los métodos 2 y 3 puntos hacia atrás ya existían)

## Cambios en Archivos

### 1. `metodos/metodos.py`
- Agregadas 4 nuevas funciones de derivación
- Cada método incluye:
  - Validación de parámetros
  - Cálculos detallados por punto
  - Diccionario de detalles con fórmulas utilizadas
  - Manejo de excepciones

### 2. `app.py`
- Actualizado endpoint `/api/derivacion` para manejar los 4 nuevos métodos
- Rutas agregadas:
  - `metodo == '2_adelante'` → `Derivacion.dos_puntos_adelante()`
  - `metodo == '3_adelante'` → `Derivacion.tres_puntos_adelante()`
  - `metodo == '5_adelante'` → `Derivacion.cinco_puntos_adelante()`
  - `metodo == '5_atras'` → `Derivacion.cinco_puntos_atras()`

### 3. `templates/derivacion.html`
- **Rediseño completo de la interfaz con Acordeón**:
  - Sección "Hacia Adelante" (expandible)
  - Sección "Hacia Atrás" (expandible)
  - Sección "Centrada" (expandible)
  - Sección "Extrapolación" (expandible)
- Agregadas 4 nuevas fórmulas LaTeX en el diccionario JavaScript
- Funcionalidad `toggleAccordion()` para expandir/contraer secciones
- Ahora soporta todos los 11 métodos de derivación
- Primera opción seleccionada: "2 Puntos Hacia Adelante"

## Fórmulas Matemáticas Implementadas

### Hacia Adelante
```
2 Puntos:   f'(x) ≈ (f(x+h) - f(x)) / h
3 Puntos:   f'(x) ≈ (-3f(x) + 4f(x+h) - f(x+2h)) / (2h)
5 Puntos:   f'(x) ≈ (-11f(x) + 18f(x+h) - 9f(x+2h) + 2f(x+3h)) / (6h)
```

### Hacia Atrás
```
2 Puntos:   f'(x) ≈ (f(x) - f(x-h)) / h
3 Puntos:   f'(x) ≈ (3f(x) - 4f(x-h) + f(x-2h)) / (2h)
5 Puntos:   f'(x) ≈ (-2f(x-3h) + 9f(x-2h) - 18f(x-h) + 11f(x)) / (6h)
```

### Centrada
```
2 Puntos:   f'(x) ≈ (f(x+h) - f(x-h)) / (2h)
3 Puntos:   f'(x) ≈ (-f(x+h) + f(x-h)) / (2h)
5 Puntos:   f'(x) ≈ (-f(x+2h) + 8f(x+h) - 8f(x-h) + f(x-2h)) / (12h)
```

### Extrapolación
```
Richardson: f'(x) ≈ (4f'(h₂) - f'(h₁)) / 3
```

## Mejoras de UX

### Acordeón
- Interfaz más limpia y organizada
- Agrupa métodos similares
- Expandible/contraíble con click
- Flecha indicadora del estado
- Fondo gris para headers (estilo novato)

### Fórmulas
- Botón "Ver fórmula" en cada método
- Modal con fórmula LaTeX renderizada
- Títulos descriptivos en español

## Validación

✅ Todos los métodos se pueden llamar via API
✅ Retornan formato JSON correcto
✅ Manejo de errores implementado
✅ Validación de parámetros en backend
✅ HTML bien formado
✅ JavaScript funcional sin errores

## Próximas Mejoras Sugeridas

- [ ] Agregar gráficas de resultados
- [ ] Exportar resultados a CSV/PDF
- [ ] Agregar más métodos numéricos
- [ ] Mejorar estilos CSS (si el usuario desea)
- [ ] Tests unitarios para los métodos

## Cómo Usar

### Desde la Web
1. Ir a http://localhost:5000/derivacion
2. Seleccionar método expandiendo la sección deseada
3. Ver fórmula con el botón "Ver fórmula"
4. Ingresar datos (nodos X, Y y tamaño paso)
5. Hacer clic en "Calcular"

### Desde API
```bash
curl -X POST http://localhost:5000/api/derivacion \
  -H "Content-Type: application/json" \
  -d '{
    "metodo": "2_adelante",
    "nodos_x": [0, 0.5, 1, 1.5, 2],
    "nodos_y": [1, 2, 3, 4, 5],
    "paso": 0.5
  }'
```
