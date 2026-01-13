#!/usr/bin/env python
"""Script para probar API en otra instancia de Python"""

import time
time.sleep(3)

import requests
import json

BASE_URL = 'http://127.0.0.1:5000/api'

print("\n" + "="*70)
print("PRUEBA 1: Sistema 2x2 (Oscilador Armónico)")
print("="*70)

data = {
    'metodo': 'rk4',
    'x0': 0,
    'y0': [1, 0],
    'xf': 1,
    'n': 10,
    'functions': ['y2', '-y1']
}

print(f"Datos: {json.dumps(data)}")
resp = requests.post(f'{BASE_URL}/ecuaciones-diferenciales', json=data)
print(f"Status: {resp.status_code}")

if resp.status_code == 200:
    r = resp.json()
    print(f"✅ Variables: {len(r['y_valores'])}")
    print(f"✅ Pasos: {len(r['x_valores'])}")
    print(f"✅ x_valores (primeros 3): {r['x_valores'][:3]}")
    print(f"✅ y1 (primeros 3): {r['y_valores'][0][:3]}")
    print(f"✅ y2 (primeros 3): {r['y_valores'][1][:3]}")
    print(f"✅ ÉXITO - Sistema funcionando")
else:
    print(f"❌ Error: {resp.json()}")

print("\n" + "="*70)
print("PRUEBA 2: Ecuación única (Regresión)")
print("="*70)

data = {
    'metodo': 'rk4',
    'x0': 0,
    'y0': 1,
    'xf': 1,
    'n': 10,
    'f_expr': 'x + y'
}

print(f"Datos: {json.dumps(data)}")
resp = requests.post(f'{BASE_URL}/ecuaciones-diferenciales', json=data)
print(f"Status: {resp.status_code}")

if resp.status_code == 200:
    r = resp.json()
    print(f"✅ Estructura y_valores: {len(r['y_valores'])} arrays")
    print(f"✅ Pasos: {len(r['x_valores'])}")
    print(f"✅ y_valores[0] (primeros 3): {r['y_valores'][0][:3]}")
    print(f"✅ ÉXITO - Ecuación única aún funciona")
else:
    print(f"❌ Error: {resp.json()}")

print("\n" + "="*70)
print("PRUEBA 3: Sistema 3x3")
print("="*70)

data = {
    'metodo': 'euler',
    'x0': 0,
    'y0': [1, 0, 0],
    'xf': 1,
    'n': 10,
    'functions': ['y2', 'y3', '-y1']
}

print(f"Datos: {json.dumps(data)}")
resp = requests.post(f'{BASE_URL}/ecuaciones-diferenciales', json=data)
print(f"Status: {resp.status_code}")

if resp.status_code == 200:
    r = resp.json()
    print(f"✅ Variables: {len(r['y_valores'])}")
    print(f"✅ Pasos: {len(r['x_valores'])}")
    print(f"✅ y1[0]: {r['y_valores'][0][0]:.6f}")
    print(f"✅ y2[0]: {r['y_valores'][1][0]:.6f}")
    print(f"✅ y3[0]: {r['y_valores'][2][0]:.6f}")
    print(f"✅ ÉXITO - Sistema 3x3 funcionando")
else:
    print(f"❌ Error: {resp.json()}")

print("\n" + "="*70)
print("TODAS LAS PRUEBAS COMPLETADAS")
print("="*70)
