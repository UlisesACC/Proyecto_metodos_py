# Mapa de Cambios - Sistema de Ecuaciones Diferenciales

## 📍 Ubicación de Cambios en el Código

### Archivo: `metodos/metodos.py`

#### 1. Clase `EcuacionesDiferenciales` - Método auxiliar nuevo
**Línea:** ~1375 (justo después del inicio de la clase)
```python
@staticmethod
def _eval_function(f_expr: str, x: float, y_values: List[float]) -> float:
    """Evalúa expresiones con soporte para y1, y2, y3, ..."""
```
**Cambio:** Agregado método auxiliar para evaluar funciones con múltiples variables

#### 2. Métodos nuevos para sistemas
**Línea:** ~1728 (después de `adams_moulton`)
```python
# ================== MÉTODOS PARA SISTEMAS DE ECUACIONES ==================

@staticmethod
def euler_sistema(x0, y0, xf, n, f_exprs):
    """Método de Euler para sistemas"""
    ...

@staticmethod
def runge_kutta_4_sistema(x0, y0, xf, n, f_exprs):
    """Método de Runge-Kutta orden 4 para sistemas"""
    ...
```
**Cambio:** Agregados dos métodos completos (~120 líneas) para resolver sistemas

---

### Archivo: `app.py`

#### Endpoint modificado
**Línea:** 288-383
```python
@app.route('/api/ecuaciones-diferenciales', methods=['POST'])
def api_ecuaciones_diferenciales():
    """API para resolver ecuaciones diferenciales (single o sistemas)"""
```

**Cambios principales:**
- Detección automática de tipo (sistema vs ecuación única)
- Routing a métodos apropiados según tipo
- Manejo de `y0` como lista o escalar
- Manejo de `functions` vs `f_expr`
- Retorno consistente con estructura matricial

**Líneas clave:**
- 307: `is_sistema = isinstance(y0, list) or functions is not None`
- 318-329: Bloque RESOLVER SISTEMAS DE ECUACIONES
- 331-383: Bloque RESOLVER ECUACIÓN ÚNICA (original)

---

### Archivo: `templates/ecuaciones_diferenciales.html`

#### 1. Sección de Funciones (Nueva)
**Línea:** ~362-405
```html
<div class="form-group">
    <label>Funciones del Sistema</label>
    <div id="functionsContainer" style="margin-bottom: 15px;">
        <div class="function-input-group" style="...">
            <div style="flex: 1;">
                <label for="f_expr_1">dy₁/dx = f₁(...)</label>
                <input type="text" id="f_expr_1" class="f_expr_input" required>
            </div>
            <button type="button" class="btn-add-function" onclick="agregarFuncion()">+</button>
        </div>
        <div id="additionalFunctions"></div>
    </div>
</div>
```

#### 2. Sección de Condiciones Iniciales (Modificada)
**Línea:** ~430-448
```html
<div class="form-group">
    <label>Condiciones Iniciales y₀</label>
    <div id="y0Container">
        <div class="y0-input-group">
            <label for="y0_1">y₁(x₀):</label>
            <input type="number" id="y0_1" class="y0_input" required>
        </div>
        <div id="additionalY0s"></div>
    </div>
</div>
```

#### 3. Event Listener del Formulario (Reescrito)
**Línea:** ~616-687
```javascript
formulario.addEventListener('submit', async (e) => {
    // Recopilar todas las funciones
    const functionsElements = document.querySelectorAll('.f_expr_input');
    const functions = [];
    
    // Recopilar todas las y0
    const y0Elements = document.querySelectorAll('.y0_input');
    const y0 = [];
    
    // Crear requestBody con arrays
    const requestBody = {
        metodo: metodo,
        x0: x0,
        y0: y0,  // Ahora es array
        functions: functions  // Array de funciones
    };
    ...
});
```

#### 4. Función mostrarResultados (Reescrita)
**Línea:** ~763-809
```javascript
function mostrarResultados(datos) {
    // Detectar si es sistema o ecuación única
    let numVars = datos.y_valores.length;
    
    // Encabezado dinámico
    for (let j = 0; j < numVars; j++) {
        if (numVars === 1) {
            html += '<th>y</th>';
        } else {
            html += '<th>y' + (j + 1) + '</th>';
        }
    }
    
    // Llenar tabla con múltiples variables
    for (let j = 0; j < numVars; j++) {
        let val = datos.y_valores[j][i];
    }
}
```

#### 5. Funciones JavaScript Nuevas
**Línea:** ~739-810
```javascript
// Funciones para agregar/quitar funciones y condiciones iniciales
let functionCount = 1;
let y0Count = 1;

function agregarFuncion() {
    functionCount++;
    const newDiv = document.createElement('div');
    newDiv.innerHTML = `
        <input type="text" id="f_expr_${functionCount}" class="f_expr_input">
        <button onclick="eliminarFuncion(${functionCount})">-</button>
    `;
    document.getElementById('additionalFunctions').appendChild(newDiv);
}

function eliminarFuncion(index) { ... }
function agregarY0() { ... }
function eliminarY0(index) { ... }
```

---

## 📊 Resumen de Cambios

| Archivo | Tipo de Cambio | Líneas | Descripción |
|---------|---|---|---|
| `metodos.py` | Adición | +150 | 2 métodos nuevos + 1 auxiliar |
| `app.py` | Modificación | ~100 | Endpoint reescrito |
| `ecuaciones_diferenciales.html` | Modificación | +200 | 5 secciones modificadas/nuevas |
| **Total** | **Extensión** | **~450** | Sin ruptura de compatibilidad |

---

## 🔄 Flujo de Datos

### Entrada: Sistema 2x2
```
HTML Form
├─ Función 1: "y2"
├─ Función 2: "-y1"
├─ y1(x0): 1
└─ y2(x0): 0

↓ JavaScript: agregarFuncion(), agregarY0(), event listener

JSON POST
{
  "metodo": "rk4",
  "x0": 0, "y0": [1, 0], "xf": 1, "n": 10,
  "functions": ["y2", "-y1"]
}

↓ Flask: app.py línea 307 detecta is_sistema=true

Python
EcuacionesDiferenciales.runge_kutta_4_sistema(
    0, [1, 0], 1, 10, ["y2", "-y1"]
)

↓ metodos.py línea ~1780 ejecuta loop

Salida
{
  "x_valores": [0, 0.1, 0.2, ...],
  "y_valores": [
    [1, 0.995, 0.98, ...],
    [0, -0.1, -0.198, ...]
  ]
}

↓ HTML: mostrarResultados() línea 763

Tabla de resultados
x     y1      y2
0     1       0
0.1   0.995   -0.1
0.2   0.98    -0.198
```

---

## ✅ Checklist de Cambios

- [x] Método auxiliar `_eval_function` agregado
- [x] Método `euler_sistema` implementado
- [x] Método `runge_kutta_4_sistema` implementado
- [x] Endpoint API detecta tipo automáticamente
- [x] HTML campos dinámicos para funciones
- [x] HTML campos dinámicos para y0
- [x] JavaScript maneja agregar/eliminar
- [x] JavaScript valida cantidad de funciones = y0
- [x] Tabla de resultados muestra múltiples variables
- [x] Compatibilidad hacia atrás verificada
- [x] Tests unitarios pasando
- [x] Documentación completa

---

## 🧪 Archivo de Pruebas Incluidos

1. `test_sistema_odes.py` - Pruebas de métodos Python directos
2. `test_api.py` - Pruebas del endpoint (con Flask)
3. `test_api_final.py` - Suite completa
4. `run_production.py` - Para ejecutar Flask sin reloading

---

## 📝 Documentación Incluida

1. `CAMBIOS_SISTEMAS_ODE.md` - Detalles técnicos completos
2. `RESUMEN_IMPLEMENTACION.md` - Resumen ejecutivo
3. `GUIA_PRUEBA.md` - Instrucciones paso a paso para probar
4. Este archivo (`MAPA_CAMBIOS.md`) - Ubicación exacta de cambios

---

**Última actualización:** 12 de Enero, 2026
**Estado:** ✅ Completado y verificado
