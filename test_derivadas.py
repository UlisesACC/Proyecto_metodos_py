#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test para la funcionalidad de cálculo de derivadas"""

import sys
import json
import urllib.request
import urllib.error

def test_endpoint_derivadas():
    """Test del endpoint /api/calcular-derivadas"""
    
    # Asegurarse de que el servidor está corriendo
    url = "http://localhost:5000/api/calcular-derivadas"
    
    test_cases = [
        {"f_expr": "x + y", "description": "Simple: x + y"},
        {"f_expr": "sin(x) + y", "description": "sin(x) + y"},
        {"f_expr": "x*y", "description": "x*y"},
        {"f_expr": "y", "description": "Solo y"},
        {"f_expr": "1 + y", "description": "1 + y (ecuación lineal simple)"},
    ]
    
    print("=" * 60)
    print("Test de Derivadas Automáticas")
    print("=" * 60)
    
    for test in test_cases:
        print(f"\nTest: {test['description']}")
        print(f"f(x,y) = {test['f_expr']}")
        
        payload = json.dumps({
            "f_expr": test['f_expr'],
            "orden": 3
        }).encode('utf-8')
        
        try:
            req = urllib.request.Request(url, data=payload)
            req.add_header('Content-Type', 'application/json')
            
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read())
                print(f"✓ df/dy = {data.get('df_expr', 'N/A')}")
                print(f"✓ d²f/dy² = {data.get('ddf_expr', 'N/A')}")
                print(f"✓ d³f/dy³ = {data.get('dddf_expr', 'N/A')}")
        
        except urllib.error.URLError as e:
            print(f"✗ Error: No se puede conectar al servidor. ¿Está corriendo en {url}?")
            print(f"  Detalle: {e}")
            return False
        except Exception as e:
            print(f"✗ Error: {e}")
            return False
    
    print("\n" + "=" * 60)
    print("Todos los tests completados")
    print("=" * 60)
    return True

if __name__ == "__main__":
    success = test_endpoint_derivadas()
    sys.exit(0 if success else 1)

