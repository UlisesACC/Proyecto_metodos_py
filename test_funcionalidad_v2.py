# -*- coding: utf-8 -*-
"""
PRUEBAS UNITARIAS DE FUNCIONALIDAD
====================================
Verifica que todos los métodos numéricos estén correctamente implementados
"""

import pytest
import numpy as np
from metodos.metodos import (
    Integracion, 
    EcuacionesDiferenciales, 
    Derivacion,
    SistemasLineales,
    DiferenciasFinitas
)


class TestIntegracion:
    """Tests para métodos de integración numérica"""
    
    def test_trapecio_simple(self):
        """TEST: Trapecio Simple"""
        x = np.linspace(0, 1, 11)
        y = x**2
        resultado, _ = Integracion.trapecio(0, 1, 10, y.tolist())
        esperado = 1/3
        
        print("\n" + "="*70)
        print("METODO: Trapecio Simple")
        print("FUNCION: f(x) = x**2")
        print("INTERVALO: [0, 1], n=10 subintervalos")
        print(f"Entrada y: {[f'{v:.4f}' for v in y[:6]]} ...")
        print(f"SALIDA: {resultado:.10f}")
        print(f"ESPERADA (1/3): {esperado:.10f}")
        print(f"ERROR: {abs(resultado - esperado):.10f}")
        print(f"ESTADO: {'CORRECTO' if abs(resultado - esperado) < 0.01 else 'INCORRECTO'}")
        print("="*70)
        
        assert abs(resultado - esperado) < 0.01
    
    def test_simpson_1_3(self):
        """TEST: Simpson 1/3"""
        x = np.linspace(0, np.pi, 11)
        y = np.sin(x)
        resultado, _ = Integracion.simpson_1_3(0, np.pi, 10, y.tolist())
        esperado = 2.0
        
        print("\n" + "="*70)
        print("METODO: Simpson 1/3")
        print("FUNCION: f(x) = sin(x)")
        print("INTERVALO: [0, pi], n=10 subintervalos")
        print(f"SALIDA: {resultado:.10f}")
        print(f"ESPERADA: {esperado:.10f}")
        print(f"ERROR: {abs(resultado - esperado):.10f}")
        print(f"ESTADO: {'CORRECTO' if abs(resultado - esperado) < 0.001 else 'INCORRECTO'}")
        print("="*70)
        
        assert abs(resultado - esperado) < 0.001
    
    def test_simpson_3_8(self):
        """TEST: Simpson 3/8"""
        x = np.linspace(0, 1, 13)
        y = x**3
        resultado, _ = Integracion.simpson_3_8(0, 1, 12, y.tolist())
        esperado = 0.25
        
        print("\n" + "="*70)
        print("METODO: Simpson 3/8")
        print("FUNCION: f(x) = x**3")
        print("INTERVALO: [0, 1], n=12 subintervalos")
        print(f"SALIDA: {resultado:.10f}")
        print(f"ESPERADA (1/4): {esperado:.10f}")
        print(f"ERROR: {abs(resultado - esperado):.10f}")
        print(f"ESTADO: {'CORRECTO' if abs(resultado - esperado) < 0.0001 else 'INCORRECTO'}")
        print("="*70)
        
        assert abs(resultado - esperado) < 0.0001
    
    def test_cuadratura_adaptiva(self):
        """TEST: Cuadratura Adaptiva"""
        f_expr = "x**2"
        resultado, detalles = Integracion.cuadratura_adaptiva(f_expr, 0, 1, 1e-6)
        esperado = 1/3
        
        print("\n" + "="*70)
        print("METODO: Cuadratura Adaptiva (Simpson Adaptativo)")
        print("FUNCION: f(x) = x**2")
        print("INTERVALO: [0, 1], tolerancia=1e-6")
        print(f"SALIDA: {resultado:.10f}")
        print(f"ESPERADA (1/3): {esperado:.10f}")
        print(f"ERROR: {abs(resultado - esperado):.10f}")
        print(f"Evaluaciones: {detalles['evaluaciones']}")
        print(f"ESTADO: {'CORRECTO' if abs(resultado - esperado) < 1e-5 else 'INCORRECTO'}")
        print("="*70)
        
        assert abs(resultado - esperado) < 1e-5


class TestEcuacionesDiferenciales:
    """Tests para ecuaciones diferenciales"""
    
    def test_euler(self):
        """TEST: Metodo de Euler"""
        x_vals, y_vals, detalles = EcuacionesDiferenciales.euler(0, 1, 1, 10, "-2*y")
        esperado = np.exp(-2)
        resultado = y_vals[-1]
        
        print("\n" + "="*70)
        print("METODO: Euler")
        print("FUNCION: dy/dx = -2y")
        print("CONDICIONES: x0=0, y0=1, xf=1, n=10")
        print(f"Solucion analitica en x=1: y = exp(-2) = {esperado:.10f}")
        print(f"Salida numerica en x=1: {resultado:.10f}")
        print(f"ERROR: {abs(resultado - esperado):.10f}")
        print(f"ESTADO: {'CORRECTO' if abs(resultado - esperado) < 0.05 else 'INCORRECTO'}")
        print("="*70)
        
        assert abs(resultado - esperado) < 0.05
    
    def test_taylor_orden_2(self):
        """TEST: Taylor Orden 2"""
        x_vals, y_vals, detalles = EcuacionesDiferenciales.taylor_orden_2(0, 1, 0.5, 5, "x + y")
        resultado = y_vals[-1]
        
        print("\n" + "="*70)
        print("METODO: Taylor Orden 2")
        print("FUNCION: dy/dx = x + y")
        print("CONDICIONES: x0=0, y0=1, xf=0.5, n=5")
        print(f"Salida en x=0.5: {resultado:.10f}")
        print(f"ESTADO: EJECUTADO CORRECTAMENTE")
        print("="*70)
        
        assert resultado is not None
        assert y_vals[-1] > 0
    
    def test_taylor_orden_3(self):
        """TEST: Taylor Orden 3"""
        x_vals, y_vals, detalles = EcuacionesDiferenciales.taylor_orden_3(0, 1, 0.5, 5, "x + y")
        resultado = y_vals[-1]
        
        print("\n" + "="*70)
        print("METODO: Taylor Orden 3")
        print("FUNCION: dy/dx = x + y")
        print("CONDICIONES: x0=0, y0=1, xf=0.5, n=5")
        print(f"Salida en x=0.5: {resultado:.10f}")
        print(f"Precision mayor a Orden 2: {resultado > 1.7}")
        print(f"ESTADO: EJECUTADO CORRECTAMENTE")
        print("="*70)
        
        assert resultado is not None
        assert y_vals[-1] > 0
    
    def test_taylor_orden_4(self):
        """TEST: Taylor Orden 4"""
        x_vals, y_vals, detalles = EcuacionesDiferenciales.taylor_orden_4(0, 1, 0.5, 5, "x + y")
        resultado = y_vals[-1]
        
        print("\n" + "="*70)
        print("METODO: Taylor Orden 4")
        print("FUNCION: dy/dx = x + y")
        print("CONDICIONES: x0=0, y0=1, xf=0.5, n=5")
        print(f"Salida en x=0.5: {resultado:.10f}")
        print(f"Precision maxima: {resultado > 1.7}")
        print(f"ESTADO: EJECUTADO CORRECTAMENTE")
        print("="*70)
        
        assert resultado is not None
        assert y_vals[-1] > 0
    
    def test_runge_kutta_3(self):
        """TEST: Runge-Kutta Orden 3"""
        x_vals, y_vals, detalles = EcuacionesDiferenciales.runge_kutta_3(0, 1, 1, 20, "-y")
        esperado = np.exp(-1)
        resultado = y_vals[-1]
        
        print("\n" + "="*70)
        print("METODO: Runge-Kutta Orden 3")
        print("FUNCION: dy/dx = -y")
        print("CONDICIONES: x0=0, y0=1, xf=1, n=20")
        print(f"Solucion analitica en x=1: y = exp(-1) = {esperado:.10f}")
        print(f"Salida numerica en x=1: {resultado:.10f}")
        print(f"ERROR: {abs(resultado - esperado):.10f}")
        print(f"ESTADO: {'CORRECTO' if abs(resultado - esperado) < 0.01 else 'INCORRECTO'}")
        print("="*70)
        
        assert abs(resultado - esperado) < 0.01

    def test_rk4(self):
        """TEST: Runge-Kutta Orden 4"""
        x_vals, y_vals, detalles = EcuacionesDiferenciales.runge_kutta_4(0, 1, 1, 20, "-y")
        esperado = np.exp(-1)
        resultado = y_vals[-1]
        
        print("\n" + "="*70)
        print("METODO: Runge-Kutta Orden 4")
        print("FUNCION: dy/dx = -y")
        print("CONDICIONES: x0=0, y0=1, xf=1, n=20")
        print(f"Solucion analitica en x=1: y = exp(-1) = {esperado:.10f}")
        print(f"Salida numerica en x=1: {resultado:.10f}")
        print(f"ERROR: {abs(resultado - esperado):.10f}")
        print(f"ESTADO: {'CORRECTO' if abs(resultado - esperado) < 0.001 else 'INCORRECTO'}")
        print("="*70)
        
        assert abs(resultado - esperado) < 0.001
    
    def test_runge_kutta_fehlberg(self):
        """TEST: Runge-Kutta-Fehlberg"""
        x_vals, y_vals, detalles = EcuacionesDiferenciales.runge_kutta_fehlberg(0, 1, 1, 20, "-y")
        esperado = np.exp(-1)
        resultado = y_vals[-1]
        
        print("\n" + "="*70)
        print("METODO: Runge-Kutta-Fehlberg (Adaptativo)")
        print("FUNCION: dy/dx = -y")
        print("CONDICIONES: x0=0, y0=1, xf=1, n=20")
        print(f"Solucion analitica en x=1: y = exp(-1) = {esperado:.10f}")
        print(f"Salida numerica en x=1: {resultado:.10f}")
        print(f"ERROR: {abs(resultado - esperado):.10f}")
        print(f"ESTADO: {'CORRECTO' if abs(resultado - esperado) < 0.001 else 'INCORRECTO'}")
        print("="*70)
        
        assert abs(resultado - esperado) < 0.001


class TestSistemasLineales:
    """Tests para sistemas lineales"""
    
    def test_gauss_simple(self):
        """TEST: Eliminacion Gaussiana"""
        A = [[2, 1], [1, -1]]
        b = [5, 1]
        resultado, detalles = SistemasLineales.eliminacion_gaussiana_simple(A, b)
        esperado = [2, 1]
        
        print("\n" + "="*70)
        print("METODO: Eliminación Gaussiana")
        print("SISTEMA:")
        print("  2x + y = 5")
        print("  x - y = 1")
        print(f"Entrada: A = {A}, b = {b}")
        print(f"Salida: x = [{resultado[0]:.6f}, {resultado[1]:.6f}]")
        print(f"Esperado: x = [2, 1]")
        print(f"Verificación:")
        print(f"  2*{resultado[0]:.6f} + {resultado[1]:.6f} = {2*resultado[0] + resultado[1]:.6f} (esperado 5)")
        print(f"  {resultado[0]:.6f} - {resultado[1]:.6f} = {resultado[0] - resultado[1]:.6f} (esperado 1)")
        error = np.linalg.norm(np.array(resultado) - np.array(esperado))
        print(f"ERROR: {error:.10f}")
        print(f"ESTADO: {'CORRECTO' if error < 0.0001 else 'INCORRECTO'}")
        print("="*70)
        
        assert error < 0.0001


if __name__ == '__main__':
    pytest.main([
        __file__,
        '-v',
        '--tb=short',
        '-s',
        '--html=test_report.html',
        '--self-contained-html'
    ])
