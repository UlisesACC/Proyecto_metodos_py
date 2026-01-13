#!/usr/bin/env python
"""
Guía Rápida de Prueba - Sistema de Ecuaciones Diferenciales
"""

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║       GUÍA DE PRUEBA - SISTEMA DE ECUACIONES DIFERENCIALES (MÚLTIPLES)      ║
╚══════════════════════════════════════════════════════════════════════════════╝

PASO 1: Iniciar Flask
────────────────────────────────────────────────────────────────────────────────
  cd Proyecto_metodos_py
  python app.py
  
  (Debe mostrar: Running on http://127.0.0.1:5000)

PASO 2: Abrir navegador
────────────────────────────────────────────────────────────────────────────────
  http://127.0.0.1:5000
  
  Navegue a: "Ecuaciones Diferenciales"

PASO 3: Probar Sistema 2x2 (Oscilador Armónico)
────────────────────────────────────────────────────────────────────────────────
  1. En "Funciones del Sistema":
     - Función 1: y2
     - Función 2: -y1
  
  2. En "Condiciones Iniciales y0":
     - y1(x0) = 1
     - y2(x0) = 0
  
  3. Parámetros:
     - x0 = 0
     - xf = 6.28 (aproximadamente 2π)
     - n = 50 (pasos)
     - Método = Runge-Kutta 4
  
  4. Hacer clic en "Calcular"
  
  5. Resultado esperado:
     - Tabla mostrando x, y1, y2
     - y1 oscilando entre -1 y 1
     - y2 desfasado 90°

PASO 4: Probar Sistema 3x3
────────────────────────────────────────────────────────────────────────────────
  1. Agregar tercera función con botón "+"
  
  2. Funciones:
     - Función 1: y2
     - Función 2: y3
     - Función 3: -y1
  
  3. Condiciones iniciales (agregar tercera con "+"):
     - y1 = 1
     - y2 = 0
     - y3 = 0
  
  4. Calcular

PASO 5: Probar Regresión (Ecuación Única)
────────────────────────────────────────────────────────────────────────────────
  1. Limpiar todas las funciones excepto la primera con botones "-"
  
  2. Función 1: x + y
  
  3. Limpiar condiciones y0 excepto la primera
  
  4. y1 = 1
  
  5. Calcular
  
  6. Debe funcionar igual que antes

═════════════════════════════════════════════════════════════════════════════════

EJEMPLOS ADICIONALES PARA PROBAR:
───────────────────────────────────────────────────────────────────────────────

Ejemplo A: Système Lineal 2x2
  Función 1: y2
  Función 2: -2*y1
  y1(0) = 1, y2(0) = 0
  xf = 5, n = 50

Ejemplo B: Sistema No-Lineal (Predador-Presa - Lotka-Volterra)
  Función 1: y1 - 0.1*y1*y2
  Función 2: 0.075*y1*y2 - 1.5*y2
  y1(0) = 50, y2(0) = 5
  xf = 50, n = 100
  (50 = población presas, 5 = población depredadores)

Ejemplo C: Sistema 4x4
  Función 1: y2
  Función 2: y3
  Función 3: y4
  Función 4: -y1
  y1(0)=1, y2(0)=0, y3(0)=0, y4(0)=0
  xf = 4, n = 40

═════════════════════════════════════════════════════════════════════════════════

FUNCIONALIDADES NUEVAS IMPLEMENTADAS:
───────────────────────────────────────────────────────────────────────────────

✓ Botón "+" para agregar funciones dinámicamente
✓ Botón "-" para eliminar funciones
✓ Campos de y0 que se agregan/quitan automáticamente
✓ Validación que funciones = condiciones iniciales
✓ Tabla de resultados con múltiples columnas (y1, y2, y3, ...)
✓ Soporte en backend para hasta N variables
✓ Métodos nuevos: euler_sistema, runge_kutta_4_sistema
✓ API soporta ambos: ecuación única Y sistemas

═════════════════════════════════════════════════════════════════════════════════

VERIFICAR FUNCIONAMIENTO CORRECTO:
───────────────────────────────────────────────────────────────────────────────

1. Oscilador Armónico:
   ✓ y1 debe oscilar
   ✓ y2 debe oscilar con desfase
   ✓ Energía debe conservarse (y1² + y2² ≈ cte)

2. Predador-Presa:
   ✓ Ciclos de población predecibles
   ✓ Desfase entre depredadores y presas

3. Ecuación Única:
   ✓ Resultados idénticos a versión anterior
   ✓ Tabla muestra solo "y" (no "y1")

═════════════════════════════════════════════════════════════════════════════════

EN CASO DE PROBLEMAS:
───────────────────────────────────────────────────────────────────────────────

Error: "Número de funciones debe coincidir con condiciones iniciales"
  → Agregar/eliminar funciones o y0 hasta que coincidan

Error: "Se requiere lista de funciones para sistema"
  → Cuando y0 es una lista, debe haber campo "functions"

Error: "Se requiere f_expr para ecuación única"
  → Cuando y0 es escalar, debe haber campo "f_expr"

Las funciones no se agregan:
  → Asegurar que JavaScript esté habilitado en el navegador
  → Abrir consola (F12) para ver errores

═════════════════════════════════════════════════════════════════════════════════
""")
