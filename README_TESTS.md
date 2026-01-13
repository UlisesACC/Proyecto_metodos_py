# PRUEBAS UNITARIAS DE FUNCIONALIDAD

## Descripción

Este archivo contiene las pruebas unitarias que verifican que todos los métodos numéricos implementados estén funcionando correctamente.

## Estructura de las Pruebas

Las pruebas están organizadas en las siguientes categorías:

### 1. **TestIntegracion** - Métodos de Integración Numérica
- ✅ `test_trapecio_simple` - Regla del Trapecio para ∫x² dx [0,1]
- ✅ `test_simpson_1_3` - Simpson 1/3 para ∫sin(x) dx [0,π]
- ✅ `test_simpson_3_8` - Simpson 3/8 para ∫x³ dx [0,1]
- ✅ `test_cuadratura_adaptiva` - Simpson Adaptativo para ∫x² dx [0,1]

### 2. **TestEcuacionesDiferenciales** - Métodos para Ecuaciones Diferenciales
- ✅ `test_euler` - Método de Euler para dy/dx = -2y
- ✅ `test_taylor_orden_2` - Taylor Orden 2 para dy/dx = x + y
- ✅ `test_rk4` - Runge-Kutta Orden 4 para dy/dx = -y

### 3. **TestSistemasLineales** - Métodos para Sistemas de Ecuaciones
- ✅ `test_gauss_simple` - Eliminación Gaussiana Simple

---

## ¿Cómo Ejecutar los Tests?

### Opción 1: Ejecutar todos los tests (Con salida en terminal)
```bash
python -m pytest test_funcionalidad_v2.py -v -s
```

**Salida esperada:**
- Mostrará cada test que se ejecuta
- Mostrará los valores calculados vs esperados
- Mostrará si paso (PASSED) o falló (FAILED)

### Opción 2: Ejecutar un test específico
```bash
python -m pytest test_funcionalidad_v2.py::TestIntegracion::test_trapecio_simple -v -s
```

### Opción 3: Generar Reporte HTML (RECOMENDADO)
```bash
python -m pytest test_funcionalidad_v2.py -v --html=test_report.html --self-contained-html
```

Esto genera un archivo `test_report.html` que puedes abrir en tu navegador para ver:
- Resumen visual de pass/fail
- Gráficos estadísticos
- Tiempos de ejecución
- Detalles de cada test

### Opción 4: Ver Cobertura de Código
```bash
python -m pytest test_funcionalidad_v2.py --cov=metodos --cov-report=html
```

Genera un reporte en `htmlcov/index.html` mostrando qué % del código está testeado.

---

## Estructura de Cada Test

Cada test sigue este formato **VISIBLE Y LEGIBLE**:

```
METODO: [Nombre del método]
FUNCION: [Expresión matemática]
INTERVALO/CONDICIONES: [Parámetros de entrada]
ENTRADA: [Valores específicos]
SALIDA: [Resultado calculado]
ESPERADA: [Valor correcto/analítico]
ERROR: [Diferencia entre ambos]
ESTADO: CORRECTO / INCORRECTO
```

### Ejemplo de salida real:
```
==============================================================================
METODO: Trapecio Simple
FUNCION: f(x) = x**2
INTERVALO: [0, 1], n=10 subintervalos
Entrada y: ['0.0000', '0.0100', '0.0400', '0.0900', '0.1600', '0.2500'] ...
SALIDA: 0.3350000000
ESPERADA (1/3): 0.3333333333
ERROR: 0.0016666667
ESTADO: CORRECTO
==============================================================================
```

---

## ¿Qué Significan los Resultados?

### ✅ CORRECTO
El método calculó un resultado dentro del rango de tolerancia aceptable.

### ❌ INCORRECTO
El error supera la tolerancia definida. Algo está mal en la implementación.

### Tolerancias por defecto:
- **Integración**: Error < 0.01 (Trapecio), < 0.001 (Simpson)
- **Ecuaciones Diferenciales**: Error < 0.05 (Euler), < 0.001 (RK4)
- **Sistemas Lineales**: Error < 0.0001 (Gauss)

---

## Modificar o Agregar Tests

Para agregar un nuevo test, usa este template:

```python
def test_mi_nuevo_metodo(self):
    """TEST: Descripción breve"""
    # Setup
    entrada = ...
    esperado = ...
    
    # Ejecutar
    resultado, detalles = ClaseDelMetodo.miMetodo(...)
    
    # Mostrar (importante para visibilidad)
    print("\n" + "="*70)
    print("METODO: Mi Nuevo Método")
    print("FUNCION: f(x) = ...")
    print(f"SALIDA: {resultado:.10f}")
    print(f"ESPERADA: {esperado:.10f}")
    print(f"ERROR: {abs(resultado - esperado):.10f}")
    print(f"ESTADO: {'CORRECTO' if abs(resultado - esperado) < 0.001 else 'INCORRECTO'}")
    print("="*70)
    
    # Assert
    assert abs(resultado - esperado) < 0.001
```

---

## Dependencias Necesarias

Instalar con:
```bash
pip install pytest pytest-html pytest-cov
```

Ya están incluidas en `requirements.txt`

---

## Última Ejecución

- **Fecha**: 13 de Enero de 2026
- **Total Tests**: 8
- **Pasados**: 8 ✅
- **Fallidos**: 0
- **Tiempo**: ~1.8 segundos
