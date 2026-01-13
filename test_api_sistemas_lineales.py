#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de prueba para verificar que la API de sistemas lineales funciona correctamente
"""

import json
from metodos.metodos import SistemasLineales

def test_api_sistemas_lineales():
    """Prueba las tres funciones de sistemas lineales"""
    
    # Datos de prueba: 2x + y = 5, x - y = 1 => x = [2, 1]
    matriz_A = [[2, 1], [1, -1]]
    vector_b = [5, 1]
    
    print("=" * 70)
    print("PRUEBA DE SISTEMAS LINEALES - Verificando Serialización JSON")
    print("=" * 70)
    
    # Test 1: Gaussiana Simple
    print("\n1. GAUSSIANA SIMPLE")
    try:
        solucion, detalles = SistemasLineales.eliminacion_gaussiana_simple(matriz_A, vector_b)
        resultado = {
            'solucion': solucion,
            'detalles': detalles
        }
        json_str = json.dumps(resultado)
        print("✅ Serialización OK")
        print(f"   Solución: {solucion}")
        print(f"   Tamaño JSON: {len(json_str)} caracteres")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 2: Pivoteo Parcial
    print("\n2. PIVOTEO PARCIAL")
    try:
        solucion, detalles = SistemasLineales.eliminacion_gaussiana_pivoteo_parcial(matriz_A, vector_b)
        resultado = {
            'solucion': solucion,
            'detalles': detalles
        }
        json_str = json.dumps(resultado)
        print("✅ Serialización OK")
        print(f"   Solución: {solucion}")
        print(f"   Tamaño JSON: {len(json_str)} caracteres")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 3: Pivoteo Total
    print("\n3. PIVOTEO TOTAL")
    try:
        solucion, detalles = SistemasLineales.eliminacion_gaussiana_pivoteo_total(matriz_A, vector_b)
        resultado = {
            'solucion': solucion,
            'detalles': detalles
        }
        json_str = json.dumps(resultado)
        print("✅ Serialización OK")
        print(f"   Solución: {solucion}")
        print(f"   Tamaño JSON: {len(json_str)} caracteres")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 4: Factorización LU
    print("\n4. FACTORIZACIÓN LU")
    try:
        L, U, detalles = SistemasLineales.factorizacion_lu(matriz_A)
        resultado = {
            'L': L,
            'U': U,
            'detalles': detalles
        }
        json_str = json.dumps(resultado)
        print("✅ Serialización OK")
        print(f"   Tamaño JSON: {len(json_str)} caracteres")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 5: Factorización PLU
    print("\n5. FACTORIZACIÓN PLU")
    try:
        P, L, U, detalles = SistemasLineales.factorizacion_plu(matriz_A)
        resultado = {
            'P': P,
            'L': L,
            'U': U,
            'detalles': detalles
        }
        json_str = json.dumps(resultado)
        print("✅ Serialización OK")
        print(f"   Tamaño JSON: {len(json_str)} caracteres")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 6: Factorización LLT (con matriz simétrica)
    print("\n6. FACTORIZACIÓN LLT")
    matriz_simetrica = [[4, 2], [2, 3]]
    try:
        L, detalles = SistemasLineales.factorizacion_llt(matriz_simetrica)
        resultado = {
            'L': L,
            'detalles': detalles
        }
        json_str = json.dumps(resultado)
        print("✅ Serialización OK")
        print(f"   Tamaño JSON: {len(json_str)} caracteres")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 70)
    print("✅ TODAS LAS PRUEBAS COMPLETADAS")
    print("=" * 70)

if __name__ == '__main__':
    test_api_sistemas_lineales()
