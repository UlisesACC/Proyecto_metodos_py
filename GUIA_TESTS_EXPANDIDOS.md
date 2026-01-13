# 📋 GUIA DE PRUEBAS UNITARIAS EXPANDIDAS

## ✅ Estado Actual: 20/20 Tests Pasando

Archivo principal: `test_funcionalidad_expandido.py`

---

## 🚀 Ejecución Rápida

### Ver todos los tests con salida visible:
```bash
python -m pytest test_funcionalidad_expandido.py -v -s
```

### Generar reporte HTML interactivo:
```bash
python -m pytest test_funcionalidad_expandido.py -v --html=test_report_expandido.html --self-contained-html
```

---

## 📚 Categorías de Tests

### 1️⃣ INTEGRACION NUMERICA (4 tests)

**Archivo**: `TestIntegracion`

```bash
python -m pytest test_funcionalidad_expandido.py::TestIntegracion -v -s
```

**Métodos probados:**
- ✅ Trapecio Simple
- ✅ Simpson 1/3
- ✅ Simpson 3/8
- ✅ Cuadratura Adaptiva

**Ejemplo de salida:**
```
METODO: Trapecio Simple
FUNCION: f(x) = x**2
INTERVALO: [0, 1], n=10 subintervalos
SALIDA: 0.3350000000
ESPERADA (1/3): 0.3333333333
ERROR: 0.0016666667
ESTADO: CORRECTO ✅
```

---

### 2️⃣ ECUACIONES DIFERENCIALES (7 tests)

**Archivo**: `TestEcuacionesDiferenciales`

```bash
python -m pytest test_funcionalidad_expandido.py::TestEcuacionesDiferenciales -v -s
```

#### 📊 Métodos probados:

**Euler (1 test)**
- ✅ Método de Euler

**Taylor - TODOS LOS ORDENES (3 tests)**
- ✅ Taylor Orden 2
- ✅ Taylor Orden 3
- ✅ Taylor Orden 4

**Runge-Kutta - TODOS LOS ORDENES (3 tests)**
- ✅ Runge-Kutta Orden 3
- ✅ Runge-Kutta Orden 4
- ✅ Runge-Kutta-Fehlberg (Adaptativo)

**Ejemplo de salida:**
```
METODO: Taylor Orden 2
FUNCION: dy/dx = x + y
CONDICIONES: x0=0, y0=1, xf=0.5, n=5
Salida en x=0.5: 1.7948935319
ESTADO: EJECUTADO CORRECTAMENTE ✅

METODO: Runge-Kutta Orden 4
FUNCION: dy/dx = -y
CONDICIONES: x0=0, y0=1, xf=1, n=20
Solucion analitica en x=1: y = exp(-1) = 0.3678794412
Salida numerica en x=1: 0.3678794611
ERROR: 0.0000000200
ESTADO: CORRECTO ✅
```

---

### 3️⃣ DERIVADAS NUMERICAS (6 tests)

**Archivo**: `TestDerivadas`

```bash
python -m pytest test_funcionalidad_expandido.py::TestDerivadas -v -s
```

#### 📊 Métodos probados:

**2 Puntos (2 tests)**
- ✅ 2 Puntos Adelante
- ✅ 2 Puntos Atras

**3 Puntos (3 tests)**
- ✅ 3 Puntos Adelante
- ✅ 3 Puntos Atras
- ✅ 3 Puntos Centrada

**5 Puntos (1 test)**
- ✅ 5 Puntos Centrada (Máxima Precisión)

**Ejemplo de salida:**
```
METODO: Derivada 5 Puntos Centrada
FUNCION: f(x) = sin(x)
PUNTO CENTRAL: x = 0
Paso: h = 0.01
Derivada en x=0: 0.9999999999
Esperada (cos(0)): 1.0000000000
ERROR: 0.0000000001
ESTADO: CORRECTO ✅
```

---

### 4️⃣ SISTEMAS LINEALES (3 tests)

**Archivo**: `TestSistemasLineales`

```bash
python -m pytest test_funcionalidad_expandido.py::TestSistemasLineales -v -s
```

#### 📊 Métodos probados:

- ✅ Eliminación Gaussiana Simple
- ✅ Eliminación Gaussiana Pivoteo Parcial
- ✅ Eliminación Gaussiana Pivoteo Total

**Sistema de prueba:**
```
Ecuación 1: 2x + y = 5
Ecuación 2: x - y = 1
Solución: x = [2, 1]
```

**Ejemplo de salida:**
```
METODO: Eliminacion Gaussiana con Pivoteo Total
SISTEMA: 2x + y = 5, x - y = 1
ENTRADA: A = [[2, 1], [1, -1]], b = [5, 1]
SALIDA: x = [2.000000, 1.000000]
ESPERADO: x = [2, 1]
ERROR: 0.0000000000
ESTADO: CORRECTO ✅
```

---

## 🎯 Ejecución Selectiva

### Ejecutar un test específico:
```bash
# Solo un test
python -m pytest test_funcionalidad_expandido.py::TestIntegracion::test_trapecio_simple -v -s

# Todos los tests que contienen "taylor"
python -m pytest test_funcionalidad_expandido.py -k taylor -v -s

# Todos los tests que contienen "runge"
python -m pytest test_funcionalidad_expandido.py -k runge -v -s
```

### Ver solo los resultados (sin salida detallada):
```bash
python -m pytest test_funcionalidad_expandido.py -v
```

---

## 📊 Estadísticas de Ejecución

```
✅ Total de Tests: 20
✅ Tests Pasando: 20 (100%)
❌ Tests Fallando: 0
⏱️ Tiempo: ~2 segundos
```

---

## 📋 Estructura de Salida de Cada Test

Cada test imprime información visible:

```
==================================================================
METODO: [Nombre del método numérico]
FUNCION: [Expresión matemática]
ENTRADA/CONDICIONES: [Parámetros iniciales]
SALIDA: [Resultado calculado]
ESPERADA: [Valor analítico/esperado]
ERROR: [Diferencia absoluta]
ESTADO: [CORRECTO ✅ o INCORRECTO ❌]
==================================================================
```

---

## 🔧 Agregar Nuevos Tests

### Plantilla para crear un nuevo test:

```python
def test_nuevo_metodo(self):
    """TEST: Descripción del método"""
    
    # 1. Preparar datos
    entrada = ...
    
    # 2. Ejecutar método
    resultado = Metodo.funcion(entrada)
    
    # 3. Imprimir información visible
    print("\n" + "="*70)
    print("METODO: Nombre del Método")
    print("FUNCION: f(x) = ...")
    print(f"ENTRADA: {entrada}")
    print(f"SALIDA: {resultado}")
    print(f"ESPERADA: {esperado}")
    error = abs(resultado - esperado)
    print(f"ERROR: {error}")
    print(f"ESTADO: {'CORRECTO' if error < tolerancia else 'INCORRECTO'}")
    print("="*70)
    
    # 4. Validar
    assert error < tolerancia
```

### Pasos para agregar:
1. Copiar la plantilla arriba
2. Cambiar el nombre, entrada, salida esperada
3. Ejecutar: `python -m pytest test_funcionalidad_expandido.py::NuevaClase::test_nuevo_metodo -v -s`
4. Si pasa, está listo

---

## 🐛 Solucionar Problemas

### Test falla con error "AttributeError: no attribute..."
→ Verificar que el nombre del método en `metodos.py` es correcto

### Test falla con error de tolerancia
→ Aumentar la tolerancia en el assert: `assert error < tolerancia_mayor`

### No se ve la salida visible
→ Ejecutar con flag `-s`: `pytest ... -s`

### Generar reporte HTML
```bash
python -m pytest test_funcionalidad_expandido.py --html=report.html --self-contained-html
```

---

## 📁 Archivos Relacionados

- `test_funcionalidad_expandido.py` - Suite principal de tests (20 tests)
- `test_report_expandido.html` - Reporte HTML de ejecución
- `RESUMEN_TESTS_EXPANDIDOS.md` - Tabla de resultados detallada
- `README_TESTS.md` - Documentación anterior

---

## ✨ Resumen

| Aspecto | Estado |
|---------|--------|
| **Tests Creados** | 20 ✅ |
| **Tests Pasando** | 20/20 (100%) ✅ |
| **Integracion** | 4/4 ✅ |
| **EDO (Euler)** | 1/1 ✅ |
| **EDO (Taylor)** | 3/3 (Orden 2,3,4) ✅ |
| **EDO (Runge-Kutta)** | 3/3 (Orden 3,4,Fehlberg) ✅ |
| **Derivadas** | 6/6 (2,3,5 puntos) ✅ |
| **Sistemas Lineales** | 3/3 (3 variantes) ✅ |
| **Salida Visible** | Sí ✅ |
| **Reporte HTML** | Sí ✅ |

---

**¡Los tests están listos para usar!** 🎉
