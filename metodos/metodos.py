import numpy as np
from typing import List, Tuple, Union


class DiferenciasFinitas:
    """Métodos de interpolación usando diferencias finitas"""
    
    @staticmethod
    def diferencias_divididas_adelante(x: List[float], y: List[float], x_eval: float) -> Tuple[float, dict]:
        """
        Interpolación de Newton con diferencias divididas hacia adelante
        
        Args:
            x: Lista de valores x (nodos)
            y: Lista de valores y (función en los nodos)
            x_eval: Punto donde se desea evaluar la interpolación
        
        Returns:
            Tupla (valor_interpolado, detalles_cálculo)
        """
        n = len(x)
        x = np.array(x, dtype=float)
        y = np.array(y, dtype=float)
        
        # Verificar que los datos sean válidos
        if n != len(y):
            raise ValueError("x e y deben tener la misma longitud")
        if n < 2:
            raise ValueError("Se necesitan al menos 2 puntos para interpolar")
        
        # Calcular tabla de diferencias divididas
        tabla_diferencias = np.zeros((n, n))
        tabla_diferencias[:, 0] = y
        
        for j in range(1, n):
            for i in range(n - j):
                tabla_diferencias[i, j] = (tabla_diferencias[i + 1, j - 1] - tabla_diferencias[i, j - 1]) / (x[i + j] - x[i])
        
        # Evaluar el polinomio de Newton
        resultado = tabla_diferencias[0, 0]
        termino = 1.0
        
        for j in range(1, n):
            termino *= (x_eval - x[j - 1])
            resultado += tabla_diferencias[0, j] * termino
        
        detalles = {
            'metodo': 'Diferencias Divididas Hacia Adelante',
            'nodos_x': x.tolist(),
            'nodos_y': y.tolist(),
            'tabla_diferencias': tabla_diferencias.tolist(),
            'punto_evaluacion': x_eval,
            'resultado': resultado
        }
        
        return resultado, detalles
    
    @staticmethod
    def diferencias_divididas_atras(x: List[float], y: List[float], x_eval: float) -> Tuple[float, dict]:
        """
        Interpolación de Newton con diferencias divididas hacia atrás
        
        Args:
            x: Lista de valores x (nodos)
            y: Lista de valores y (función en los nodos)
            x_eval: Punto donde se desea evaluar la interpolación
        
        Returns:
            Tupla (valor_interpolado, detalles_cálculo)
        """
        n = len(x)
        x = np.array(x, dtype=float)
        y = np.array(y, dtype=float)
        
        # Verificar que los datos sean válidos
        if n != len(y):
            raise ValueError("x e y deben tener la misma longitud")
        if n < 2:
            raise ValueError("Se necesitan al menos 2 puntos para interpolar")
        
        # Invertir los nodos para usar diferencias hacia atrás
        x_inv = x[::-1]
        y_inv = y[::-1]
        
        # Calcular tabla de diferencias divididas
        tabla_diferencias = np.zeros((n, n))
        tabla_diferencias[:, 0] = y_inv
        
        for j in range(1, n):
            for i in range(n - j):
                tabla_diferencias[i, j] = (tabla_diferencias[i + 1, j - 1] - tabla_diferencias[i, j - 1]) / (x_inv[i + j] - x_inv[i])
        
        # Evaluar el polinomio de Newton con diferencias hacia atrás
        resultado = tabla_diferencias[0, 0]
        termino = 1.0
        
        for j in range(1, n):
            termino *= (x_eval - x_inv[j - 1])
            resultado += tabla_diferencias[0, j] * termino
        
        detalles = {
            'metodo': 'Diferencias Divididas Hacia Atrás',
            'nodos_x': x.tolist(),
            'nodos_y': y.tolist(),
            'nodos_x_invertidos': x_inv.tolist(),
            'nodos_y_invertidos': y_inv.tolist(),
            'tabla_diferencias': tabla_diferencias.tolist(),
            'punto_evaluacion': x_eval,
            'resultado': resultado
        }
        
        return resultado, detalles
    
    @staticmethod
    def neville(x: List[float], y: List[float], x_eval: float) -> Tuple[float, dict]:
        """
        Interpolación de Neville
        
        Args:
            x: Lista de valores x (nodos)
            y: Lista de valores y (función en los nodos)
            x_eval: Punto donde se desea evaluar la interpolación
        
        Returns:
            Tupla (valor_interpolado, detalles_cálculo)
        """
        n = len(x)
        x = np.array(x, dtype=float)
        y = np.array(y, dtype=float)
        
        # Verificar que los datos sean válidos
        if n != len(y):
            raise ValueError("x e y deben tener la misma longitud")
        if n < 2:
            raise ValueError("Se necesitan al menos 2 puntos para interpolar")
        
        # Tabla de Neville
        tabla_neville = np.zeros((n, n))
        tabla_neville[:, 0] = y
        
        # Llenar la tabla de Neville
        for j in range(1, n):
            for i in range(n - j):
                tabla_neville[i, j] = (
                    (x_eval - x[i + j]) * tabla_neville[i, j - 1] -
                    (x_eval - x[i]) * tabla_neville[i + 1, j - 1]
                ) / (x[i] - x[i + j])
        
        resultado = tabla_neville[0, n - 1]
        
        detalles = {
            'metodo': 'Neville',
            'nodos_x': x.tolist(),
            'nodos_y': y.tolist(),
            'tabla_neville': tabla_neville.tolist(),
            'punto_evaluacion': x_eval,
            'resultado': resultado
        }
        
        return resultado, detalles
