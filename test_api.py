#!/usr/bin/env python
"""
Script para probar el endpoint de API
"""

import requests
import json
import time

# Esperar a que Flask esté listo
time.sleep(2)

url = 'http://127.0.0.1:5000/api/ecuaciones-diferenciales'

# Prueba 1: Ecuación única (compatibilidad hacia atrás)
print("="*60)
print("PRUEBA 1: Ecuación Única (Compatibilidad hacia atrás)")
print("="*60)

data = {
    'metodo': 'rk4',
    'x0': 0,
    'y0': 1,
    'xf': 1,
    'n': 10,
    'f_expr': 'x + y'
}

try:
    response = requests.post(url, json=data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        resultado = response.json()
        print(f"x_valores (primeros 3): {resultado['x_valores'][:3]}")
        print(f"y_valores estructura: {type(resultado['y_valores'])}, elementos: {len(resultado['y_valores'])}")
        print(f"y_valores[0] (primeros 3): {resultado['y_valores'][0][:3]}")
        print(f"✅ ÉXITO")
    else:
        print(f"❌ ERROR: {response.json()}")
except Exception as e:
    print(f"❌ EXCEPCIÓN: {e}")

print()

# Prueba 2: Sistema de ecuaciones (nuevo)
print("="*60)
print("PRUEBA 2: Sistema de Ecuaciones (Oscilador Armónico)")
print("="*60)

data = {
    'metodo': 'rk4',
    'x0': 0,
    'y0': [1, 0],
    'xf': 2,
    'n': 20,
    'functions': ['y2', '-y1']
}

try:
    response = requests.post(url, json=data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        resultado = response.json()
        print(f"x_valores (primeros 3): {resultado['x_valores'][:3]}")
        print(f"y_valores estructura: {type(resultado['y_valores'])}, num variables: {len(resultado['y_valores'])}")
        print(f"y1 (primeros 3): {resultado['y_valores'][0][:3]}")
        print(f"y2 (primeros 3): {resultado['y_valores'][1][:3]}")
        print(f"Detalles metodo: {resultado['detalles']['metodo']}")
        print(f"✅ ÉXITO")
    else:
        print(f"❌ ERROR: {response.json()}")
except Exception as e:
    print(f"❌ EXCEPCIÓN: {e}")

print()

# Prueba 3: Sistema 3x3
print("="*60)
print("PRUEBA 3: Sistema 3x3")
print("="*60)

data = {
    'metodo': 'euler',
    'x0': 0,
    'y0': [1, 0, 0],
    'xf': 1,
    'n': 15,
    'functions': ['y2', 'y3', '-y1']
}

try:
    response = requests.post(url, json=data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        resultado = response.json()
        print(f"Variables: {len(resultado['y_valores'])}")
        print(f"Pasos: {len(resultado['x_valores'])}")
        print(f"y1[0]: {resultado['y_valores'][0][0]:.6f}")
        print(f"y2[0]: {resultado['y_valores'][1][0]:.6f}")
        print(f"y3[0]: {resultado['y_valores'][2][0]:.6f}")
        print(f"✅ ÉXITO")
    else:
        print(f"❌ ERROR: {response.json()}")
except Exception as e:
    print(f"❌ EXCEPCIÓN: {e}")

print()
print("="*60)
print("TODAS LAS PRUEBAS COMPLETADAS")
print("="*60)
