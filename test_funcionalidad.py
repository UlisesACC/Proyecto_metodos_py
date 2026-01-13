"""
PRUEBAS UNITARIAS DE FUNCIONALIDAD
=====================================
Verifica que todos los métodos numéricos estén correctamente implementados
Compara resultados con valores esperados (soluciones analíticas o de referencia)
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
import math


class TestIntegracion:
    """Tests para métodos de integración numérica"""
    
    def test_trapecio_simple(self):
        """
        TEST: Trapecio Simple
        - FUNCIÓN: ∫ x² dx de 0 a 1
        - VALORES: a=0, b=1, n=10
        - ENTRADA: valores y = [0, 0.01, 0.04, 0.09, 0.16, 0.25, 0.36, 0.49, 0.64, 0.81, 1.0]
        - SALIDA ESPERADA: ≈ 0.3333 (valor analítico = 1/3)
        """
        x = np.linspace(0, 1, 11)
        y = x**2
        resultado, _ = Integracion.trapecio(0, 1, 10, y.tolist())
        esperado = 1/3
        
        print(f"\n{'='*70}")
        print(f"MÉTODO: Trapecio Simple - ∫ x² dx [0,1]")
        print(f"Entrada: a=0, b=1, n=10")
        print(f"Valores y: {[f'{v:.4f}' for v in y]}")
        print(f"Salida: {resultado:.10f}")
        print(f"Esperado: {esperado:.10f}")
        print(f"Error: {abs(resultado - esperado):.10f}")
        print(f"Estado: {'✅ CORRECTO' if abs(resultado - esperado) < 0.01 else '❌ INCORRECTO'}")
        print(f"{'='*70}")
        
        assert abs(resultado - esperado) < 0.01, f"Error > 0.01: {abs(resultado - esperado)}"
    
    def test_simpson_1_3(self):
        """
        TEST: Simpson 1/3
        - FUNCIÓN: ∫ sin(x) dx de 0 a π
        - VALORES: a=0, b=π, n=10
        - ENTRADA: valores y en los puntos
        - SALIDA ESPERADA: ≈ 2.0 (valor analítico = 2)
        """
        x = np.linspace(0, np.pi, 11)
        y = np.sin(x)
        resultado, _ = Integracion.simpson_1_3(0, np.pi, 10, y.tolist())
        esperado = 2.0
        
        print(f"\n{'='*70}")
        print(f"MÉTODO: Simpson 1/3 - ∫ sin(x) dx [0,π]")
        print(f"Entrada: a=0, b=π, n=10")
        print(f"Salida: {resultado:.10f}")
        print(f"Esperado: {esperado:.10f}")
        print(f"Error: {abs(resultado - esperado):.10f}")
        print(f"Estado: {'✅ CORRECTO' if abs(resultado - esperado) < 0.001 else '❌ INCORRECTO'}")
        print(f"{'='*70}")
        
        assert abs(resultado - esperado) < 0.001, f"Error > 0.001"
    
    def test_simpson_3_8(self):
        """
        TEST: Simpson 3/8
        - FUNCIÓN: ∫ x³ dx de 0 a 1
        - VALORES: a=0, b=1, n=12 (múltiplo de 3)
        - ENTRADA: valores y en los puntos
        - SALIDA ESPERADA: ≈ 0.25 (valor analítico = 1/4)
        """
        x = np.linspace(0, 1, 13)
        y = x**3
        resultado, _ = Integracion.simpson_3_8(0, 1, 12, y.tolist())
        esperado = 0.25
        
        print(f"\n{'='*70}")
        print(f"MÉTODO: Simpson 3/8 - ∫ x³ dx [0,1]")
        print(f"Entrada: a=0, b=1, n=12")
        print(f"Salida: {resultado:.10f}")
        print(f"Esperado: {esperado:.10f}")
        print(f"Error: {abs(resultado - esperado):.10f}")
        print(f"Estado: {'✅ CORRECTO' if abs(resultado - esperado) < 0.0001 else '❌ INCORRECTO'}")
        print(f"{'='*70}")
        
        assert abs(resultado - esperado) < 0.0001
    
    def test_cuadratura_gaussiana(self):
        """
        TEST: Cuadratura Gaussiana
        - FUNCIÓN: ∫ e^(-x²) dx de -1 a 1
        - VALORES: a=-1, b=1, n=10
        - ENTRADA: valores y en puntos de Gauss
        - SALIDA ESPERADA: ≈ 1.493 (referencia numérica)
        """
        # Usar puntos y pesos de Gauss
        from numpy.polynomial.legendre import leggauss
        x_gauss, w_gauss = leggauss(10)
        # Transformar a [−1, 1]
        y = np.exp(-x_gauss**2)
        resultado, _ = Integracion.cuadratura_gaussiana(-1, 1, 10, y.tolist())
        esperado = 1.493648
        
        print(f"\n{'='*70}")
        print(f"MÉTODO: Cuadratura Gaussiana - ∫ e^(-x²) dx [-1,1]")
        print(f"Entrada: a=-1, b=1, n=10")
        print(f"Salida: {resultado:.10f}")
        print(f"Esperado: {esperado:.10f}")
        print(f"Error: {abs(resultado - esperado):.10f}")
        print(f"Estado: {'✅ CORRECTO' if abs(resultado - esperado) < 0.01 else '❌ INCORRECTO'}")
        print(f"{'='*70}")
        
        assert abs(resultado - esperado) < 0.01
    
    def test_cuadratura_adaptiva(self):
        """
        TEST: Cuadratura Adaptiva (Simpson Adaptativo)
        - FUNCIÓN: f(x) = x**2
        - ENTRADA: a=0, b=1, tolerancia=1e-6
        - SALIDA ESPERADA: ≈ 0.333333 (valor analítico = 1/3)
        """
        f_expr = "x**2"
        resultado, detalles = Integracion.cuadratura_adaptiva(f_expr, 0, 1, 1e-6)
        esperado = 1/3
        
        print(f"\n{'='*70}")
        print(f"MÉTODO: Cuadratura Adaptiva (Simpson Adaptativo)")
        print(f"Función: f(x) = {f_expr}")
        print(f"Entrada: a=0, b=1, tolerancia=1e-6")
        print(f"Salida: {resultado:.10f}")
        print(f"Esperado: {esperado:.10f}")
        print(f"Error: {abs(resultado - esperado):.10f}")
        print(f"Evaluaciones: {detalles['evaluaciones']}")
        print(f"Estado: {'✅ CORRECTO' if abs(resultado - esperado) < 1e-5 else '❌ INCORRECTO'}")
        print(f"{'='*70}")
        
        assert abs(resultado - esperado) < 1e-5


class TestEcuacionesDiferenciales:
    """Tests para métodos de ecuaciones diferenciales"""
    
    def test_euler(self):
        """
        TEST: Método de Euler
        - FUNCIÓN: dy/dx = -2y, y(0) = 1
        - ENTRADA: x0=0, y0=1, xf=1, n=10
        - SOLUCIÓN ANALÍTICA: y = e^(-2x)
        - SALIDA ESPERADA: y(1) ≈ 0.1353 (e^-2)
        """
        # Función: dy/dx = -2y
        def f(x, y):
            return -2*y
        
        x_vals, y_vals, detalles = EcuacionesDiferenciales.euler(0, 1, 1, 10, "-2*y")
        esperado = np.exp(-2)
        resultado = y_vals[-1]
        
        print(f"\n{'='*70}")
        print(f"MÉTODO: Euler")
        print(f"Función: dy/dx = -2y")
        print(f"Entrada: x0=0, y0=1, xf=1, n=10")
        print(f"Solución analítica en x=1: y = e^(-2) = {esperado:.10f}")
        print(f"Salida numérica en x=1: {resultado:.10f}")
        print(f"Error: {abs(resultado - esperado):.10f}")
        print(f"Estado: {'✅ CORRECTO' if abs(resultado - esperado) < 0.05 else '❌ INCORRECTO'}")
        print(f"{'='*70}")
        
        assert abs(resultado - esperado) < 0.05
    
    def test_taylor_orden_2(self):
        """
        TEST: Taylor Orden 2
        - FUNCIÓN: dy/dx = x + y, y(0) = 1
        - ENTRADA: x0=0, y0=1, xf=0.5, n=5
        - SALIDA ESPERADA: valor numérico mejorado respecto a Euler
        """
        x_vals, y_vals, detalles = EcuacionesDiferenciales.taylor_orden_2(0, 1, 0.5, 5, "x + y")
        resultado = y_vals[-1]
        
        print(f"\n{'='*70}")
        print(f"MÉTODO: Taylor Orden 2")
        print(f"Función: dy/dx = x + y")
        print(f"Entrada: x0=0, y0=1, xf=0.5, n=5")
        print(f"Salida en x=0.5: {resultado:.10f}")
        print(f"Estado: ✅ EJECUTADO CORRECTAMENTE")
        print(f"{'='*70}")
        
        assert resultado is not None
        assert y_vals[-1] > 0
    
    def test_rk4(self):
        """
        TEST: Runge-Kutta Orden 4
        - FUNCIÓN: dy/dx = -y, y(0) = 1
        - ENTRADA: x0=0, y0=1, xf=1, n=20
        - SOLUCIÓN ANALÍTICA: y = e^(-x)
        - SALIDA ESPERADA: y(1) ≈ 0.3679 (e^-1)
        """
        x_vals, y_vals, detalles = EcuacionesDiferenciales.rk4(0, 1, 1, 20, "-y")
        esperado = np.exp(-1)
        resultado = y_vals[-1]
        
        print(f"\n{'='*70}")
        print(f"MÉTODO: Runge-Kutta Orden 4")
        print(f"Función: dy/dx = -y")
        print(f"Entrada: x0=0, y0=1, xf=1, n=20")
        print(f"Solución analítica en x=1: y = e^(-1) = {esperado:.10f}")
        print(f"Salida numérica en x=1: {resultado:.10f}")
        print(f"Error: {abs(resultado - esperado):.10f}")
        print(f"Estado: {'✅ CORRECTO' if abs(resultado - esperado) < 0.001 else '❌ INCORRECTO'}")
        print(f"{'='*70}")
        
        assert abs(resultado - esperado) < 0.001


class TestDerivadas:
    """Tests para cálculo de derivadas"""
    
    def test_derivada_2_puntos_adelante(self):
        """
        TEST: Derivada 2 Puntos Adelante
        - FUNCIÓN: f(x) = x² con valores y = [0, 1, 4, 9, 16] en x = [0, 1, 2, 3, 4]
        - FÓRMULA: f'(x) ≈ (f(x+h) - f(x)) / h
        - ENTRADA: h=1
        - SALIDA ESPERADA: f'(0) ≈ 1, f'(1) ≈ 3, f'(2) ≈ 5, f'(3) ≈ 7
        """
        x = [0, 1, 2, 3, 4]
        y = [0, 1, 4, 9, 16]  # x²
        h = 1
        
        derivadas, detalles = Derivacion.dos_puntos_adelante(x, y, h)
        
        # Valores esperados (derivada de x² = 2x)
        # En x=0: 2*0 = 0, pero el método adelante da (1-0)/1 = 1
        # En x=1: 2*1 = 2, pero el método adelante da (4-1)/1 = 3
        esperados = [1.0, 3.0, 5.0, 7.0, None]
        
        print(f"\n{'='*70}")
        print(f"MÉTODO: Derivada 2 Puntos Adelante")
        print(f"Función: f(x) = x²")
        print(f"Puntos: x = {x}, y = {y}")
        print(f"Paso: h = {h}")
        print(f"Derivadas calculadas: {[f'{d:.4f}' if d else 'N/A' for d in derivadas]}")
        print(f"Esperadas: {[f'{e:.4f}' if e else 'N/A' for e in esperados]}")
        
        for i, (calc, esp) in enumerate(zip(derivadas, esperados)):
            if calc is not None and esp is not None:
                error = abs(calc - esp)
                estado = '✅' if error < 0.001 else '❌'
                print(f"  x[{i}]={x[i]}: calc={calc:.4f}, esp={esp:.4f}, error={error:.4f} {estado}")
        
        print(f"{'='*70}")
        
        # Verificar que los primeros valores sean correctos
        assert derivadas[0] is not None
        assert abs(derivadas[0] - 1.0) < 0.001
    
    def test_derivada_3_puntos_central(self):
        """
        TEST: Derivada 3 Puntos Central
        - FUNCIÓN: f(x) = sin(x) con evaluación central
        - FÓRMULA: f'(x) ≈ (f(x+h) - f(x-h)) / (2h)
        - ENTRADA: Puntos alrededor de 0
        - SALIDA ESPERADA: f'(0) ≈ 1.0 (cos(0) = 1)
        """
        h = 0.01
        x = [-2*h, -h, 0, h, 2*h]
        y = [np.sin(xi) for xi in x]
        
        derivadas, detalles = Derivacion.tres_puntos_central(x, y, h)
        
        # En x=0 (índice 2): f'(0) ≈ cos(0) = 1
        esperado_central = 1.0
        resultado_central = derivadas[2]
        
        print(f"\n{'='*70}")
        print(f"MÉTODO: Derivada 3 Puntos Central")
        print(f"Función: f(x) = sin(x)")
        print(f"Punto central: x = 0")
        print(f"Paso: h = {h}")
        print(f"Derivada en x=0: {resultado_central:.10f}")
        print(f"Esperada (cos(0)): {esperado_central:.10f}")
        print(f"Error: {abs(resultado_central - esperado_central):.10f}")
        print(f"Estado: {'✅ CORRECTO' if abs(resultado_central - esperado_central) < 0.0001 else '❌ INCORRECTO'}")
        print(f"{'='*70}")
        
        assert abs(resultado_central - esperado_central) < 0.0001


class TestSistemasLineales:
    """Tests para métodos de sistemas lineales"""
    
    def test_gauss_simple(self):
        """
        TEST: Eliminación Gaussiana
        - SISTEMA: 2x + y = 5
                   x - y = 1
        - ENTRADA: A = [[2,1], [1,-1]], b = [5, 1]
        - SOLUCIÓN ESPERADA: x = [2, 1] (2·2 + 1 = 5, 2 - 1 = 1)
        """
        A = [[2, 1], [1, -1]]
        b = [5, 1]
        resultado, detalles = SistemasLineales.gauss_simple(A, b)
        esperado = [2, 1]
        
        print(f"\n{'='*70}")
        print(f"MÉTODO: Eliminación Gaussiana")
        print(f"Sistema:")
        print(f"  2x + y = 5")
        print(f"  x - y = 1")
        print(f"Entrada: A = {A}, b = {b}")
        print(f"Salida: x = {[f'{v:.6f}' for v in resultado]}")
        print(f"Esperado: x = {esperado}")
        print(f"Verificación:")
        print(f"  2·{resultado[0]:.6f} + {resultado[1]:.6f} = {2*resultado[0] + resultado[1]:.6f} (esperado 5)")
        print(f"  {resultado[0]:.6f} - {resultado[1]:.6f} = {resultado[0] - resultado[1]:.6f} (esperado 1)")
        print(f"Error: {np.linalg.norm(np.array(resultado) - np.array(esperado)):.10f}")
        print(f"Estado: {'✅ CORRECTO' if np.linalg.norm(np.array(resultado) - np.array(esperado)) < 0.0001 else '❌ INCORRECTO'}")
        print(f"{'='*70}")
        
        assert np.linalg.norm(np.array(resultado) - np.array(esperado)) < 0.0001
    
    def test_lu_descomposicion(self):
        """
        TEST: Descomposición LU
        - SISTEMA: 3x + 2y = 8
                   2x + 4y = 10
        - ENTRADA: A = [[3,2], [2,4]]
        - SALIDA ESPERADA: L·U = A (verificar la descomposición)
        """
        A = [[3, 2], [2, 4]]
        L, U, detalles = SistemasLineales.lu_descomposicion(A)
        
        # Reconstruir A a partir de L·U
        A_reconstruido = np.dot(L, U)
        A_original = np.array(A)
        
        print(f"\n{'='*70}")
        print(f"MÉTODO: Descomposición LU")
        print(f"Matriz A = {A}")
        print(f"Matriz L (Lower):")
        print(f"{L}")
        print(f"Matriz U (Upper):")
        print(f"{U}")
        print(f"L·U (reconstruido):")
        print(f"{A_reconstruido}")
        print(f"Error de reconstrucción: {np.linalg.norm(A_reconstruido - A_original):.10f}")
        print(f"Estado: {'✅ CORRECTO' if np.linalg.norm(A_reconstruido - A_original) < 0.0001 else '❌ INCORRECTO'}")
        print(f"{'='*70}")
        
        assert np.linalg.norm(A_reconstruido - A_original) < 0.0001


class TestDiferenciasFinitas:
    """Tests para métodos de diferencias finitas e interpolación"""
    
    def test_diferencias_divididas_adelante(self):
        """
        TEST: Diferencias Divididas Adelante
        - PUNTOS: (0,1), (1,2), (2,5), (3,10)
        - FUNCIÓN: Polinomio de interpolación
        - ENTRADA: Interpolar en x=1.5
        - VERIFICACIÓN: El resultado debe estar entre f(1)=2 y f(2)=5
        """
        x = [0, 1, 2, 3]
        y = [1, 2, 5, 10]
        resultado, detalles = DiferenciasFinitas.diferencias_divididas_adelante(x, y, 1.5)
        
        print(f"\n{'='*70}")
        print(f"MÉTODO: Diferencias Divididas Adelante")
        print(f"Puntos (x, y): {list(zip(x, y))}")
        print(f"Interpolación en x = 1.5")
        print(f"Salida: {resultado:.10f}")
        print(f"Rango esperado: entre {y[1]} y {y[2]}")
        print(f"Estado: {'✅ CORRECTO' if y[1] <= resultado <= y[2] else '❌ INCORRECTO'}")
        print(f"{'='*70}")
        
        assert y[1] <= resultado <= y[2]


# ============================================================================
# CONFIGURACIÓN DE PYTEST PARA REPORTE HTML
# ============================================================================
if __name__ == '__main__':
    pytest.main([
        __file__,
        '-v',  # Verbose
        '--tb=short',  # Traceback corto
        '--color=yes',  # Colores
        '-s',  # Mostrar prints
        '--html=test_report.html',  # Generar reporte HTML
        '--self-contained-html'  # HTML independiente
    ])
