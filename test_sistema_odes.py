#!/usr/bin/env python
"""
Script de prueba para sistemas de ecuaciones diferenciales
"""

import sys
import time
sys.path.insert(0, '.')

from metodos.metodos import EcuacionesDiferenciales

# Prueba 1: Sistema simple (oscilador armónico)
print("="*50)
print("PRUEBA 1: Oscilador Armónico")
print("="*50)
print("Sistema: dy1/dx = y2, dy2/dx = -y1")
print("Condiciones iniciales: y1(0) = 1, y2(0) = 0")
print()

x, y_vals, detalles = EcuacionesDiferenciales.euler_sistema(
    x0=0,
    y0=[1, 0],
    xf=2*3.14159,  # 2π
    n=50,
    f_exprs=['y2', '-y1']
)

print(f"Método: {detalles['metodo']}")
print(f"Pasos: {detalles['n']}")
print(f"x inicial: {x[0]}, x final: {x[-1]}")
print()

# Mostrar primeros 5 puntos
print("Primeros 5 puntos:")
print("   x        y1        y2")
for i in range(min(5, len(x))):
    print(f"{x[i]:6.4f}  {y_vals[0][i]:8.6f}  {y_vals[1][i]:8.6f}")

print()

# Prueba 2: Sistema más complejo
print("="*50)
print("PRUEBA 2: Sistema 3x3")
print("="*50)
print("Sistema: dy1/dx = y2, dy2/dx = y3, dy3/dx = -y1")
print("Condiciones iniciales: y1(0)=1, y2(0)=0, y3(0)=0")
print()

x, y_vals, detalles = EcuacionesDiferenciales.runge_kutta_4_sistema(
    x0=0,
    y0=[1, 0, 0],
    xf=3,
    n=30,
    f_exprs=['y2', 'y3', '-y1']
)

print(f"Método: {detalles['metodo']}")
print(f"Número de variables: {len(y_vals)}")
print(f"Pasos calculados: {len(x)}")
print()

# Mostrar primeros 3 puntos
print("Primeros 3 puntos:")
print("   x        y1        y2        y3")
for i in range(min(3, len(x))):
    print(f"{x[i]:6.4f}  {y_vals[0][i]:8.6f}  {y_vals[1][i]:8.6f}  {y_vals[2][i]:8.6f}")

print()
print("✅ PRUEBAS COMPLETADAS EXITOSAMENTE")
