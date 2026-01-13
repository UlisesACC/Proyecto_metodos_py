import numpy as np
from typing import List, Tuple, Union
from sympy import symbols, sympify, diff, expand


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


class Derivacion:
    """Métodos de derivación numérica"""
    
    @staticmethod
    def dos_puntos_adelante(x: List[float], y: List[float], h: float) -> Tuple[List[float], dict]:
        """
        Derivación con 2 puntos hacia adelante
        f'(x) ≈ (f(x+h) - f(x)) / h
        
        Args:
            x: Lista de valores x
            y: Lista de valores y (función en los puntos)
            h: Tamaño del paso
        
        Returns:
            Tupla (derivadas, detalles_cálculo)
        """
        x = np.array(x, dtype=float)
        y = np.array(y, dtype=float)
        n = len(x)
        
        if n < 2:
            raise ValueError("Se necesitan al menos 2 puntos")
        
        derivadas = []
        calculos = []
        
        for i in range(n):
            if i == n - 1:
                # No se puede calcular en el último punto
                derivada = None
                calculo = "No calculable (último punto)"
            else:
                # Fórmula: f'(x) = (f(x+h) - f(x)) / h
                derivada = (y[i+1] - y[i]) / h
                calculo = f"({y[i+1]:.6f} - {y[i]:.6f}) / {h}"
            
            derivadas.append(derivada)
            calculos.append(calculo)
        
        detalles = {
            'metodo': 'Derivación 2 Puntos Hacia Adelante',
            'nodos_x': x.tolist(),
            'nodos_y': y.tolist(),
            'paso': h,
            'derivadas': [d.tolist() if isinstance(d, (np.ndarray, float)) and d is not None else d for d in derivadas],
            'calculos': calculos
        }
        
        return derivadas, detalles
    
    @staticmethod
    def dos_puntos_atras(x: List[float], y: List[float], h: float) -> Tuple[List[float], dict]:
        """
        Derivación con 2 puntos hacia atrás
        f'(x) ≈ (f(x) - f(x-h)) / h
        
        Args:
            x: Lista de valores x
            y: Lista de valores y (función en los puntos)
            h: Tamaño del paso
        
        Returns:
            Tupla (derivadas, detalles_cálculo)
        """
        x = np.array(x, dtype=float)
        y = np.array(y, dtype=float)
        n = len(x)
        
        if n < 2:
            raise ValueError("Se necesitan al menos 2 puntos")
        
        derivadas = []
        calculos = []
        
        for i in range(n):
            if i == 0:
                # No se puede calcular en el primer punto
                derivada = None
                calculo = "No calculable (primer punto)"
            else:
                # Fórmula: f'(x) = (f(x) - f(x-h)) / h
                derivada = (y[i] - y[i-1]) / h
                calculo = f"({y[i]:.6f} - {y[i-1]:.6f}) / {h}"
            
            derivadas.append(derivada)
            calculos.append(calculo)
        
        detalles = {
            'metodo': 'Derivación 2 Puntos Hacia Atrás',
            'nodos_x': x.tolist(),
            'nodos_y': y.tolist(),
            'paso': h,
            'derivadas': [d.tolist() if isinstance(d, (np.ndarray, float)) and d is not None else d for d in derivadas],
            'calculos': calculos
        }
        
        return derivadas, detalles
    
    @staticmethod
    def tres_puntos_adelante(x: List[float], y: List[float], h: float) -> Tuple[List[float], dict]:
        """
        Derivación con 3 puntos hacia adelante
        f'(x) ≈ (-3f(x) + 4f(x+h) - f(x+2h)) / (2h)
        
        Args:
            x: Lista de valores x
            y: Lista de valores y (función en los puntos)
            h: Tamaño del paso
        
        Returns:
            Tupla (derivadas, detalles_cálculo)
        """
        x = np.array(x, dtype=float)
        y = np.array(y, dtype=float)
        n = len(x)
        
        if n < 3:
            raise ValueError("Se necesitan al menos 3 puntos")
        
        derivadas = []
        calculos = []
        
        for i in range(n):
            if i >= n - 2:
                # No se puede calcular en los dos últimos puntos
                derivada = None
                calculo = "No calculable"
            else:
                # Fórmula: f'(x) = (-3f(x) + 4f(x+h) - f(x+2h)) / (2h)
                derivada = (-3 * y[i] + 4 * y[i+1] - y[i+2]) / (2 * h)
                calculo = f"(-3*{y[i]:.6f} + 4*{y[i+1]:.6f} - {y[i+2]:.6f}) / {2*h}"
            
            derivadas.append(derivada)
            calculos.append(calculo)
        
        detalles = {
            'metodo': 'Derivación 3 Puntos Hacia Adelante',
            'nodos_x': x.tolist(),
            'nodos_y': y.tolist(),
            'paso': h,
            'derivadas': [d.tolist() if isinstance(d, (np.ndarray, float)) and d is not None else d for d in derivadas],
            'calculos': calculos
        }
        
        return derivadas, detalles
    
    @staticmethod
    def tres_puntos_atras(x: List[float], y: List[float], h: float) -> Tuple[List[float], dict]:
        """
        Derivación con 3 puntos hacia atrás
        f'(x) ≈ (3f(x) - 4f(x-h) + f(x-2h)) / (2h)
        
        Args:
            x: Lista de valores x
            y: Lista de valores y (función en los puntos)
            h: Tamaño del paso
        
        Returns:
            Tupla (derivadas, detalles_cálculo)
        """
        x = np.array(x, dtype=float)
        y = np.array(y, dtype=float)
        n = len(x)
        
        if n < 3:
            raise ValueError("Se necesitan al menos 3 puntos")
        
        derivadas = []
        calculos = []
        
        for i in range(n):
            if i < 2:
                # No se puede calcular en los dos primeros puntos
                derivada = None
                calculo = "No calculable"
            else:
                # Fórmula: f'(x) = (3f(x) - 4f(x-h) + f(x-2h)) / (2h)
                derivada = (3 * y[i] - 4 * y[i-1] + y[i-2]) / (2 * h)
                calculo = f"(3*{y[i]:.6f} - 4*{y[i-1]:.6f} + {y[i-2]:.6f}) / {2*h}"
            
            derivadas.append(derivada)
            calculos.append(calculo)
        
        detalles = {
            'metodo': 'Derivación 3 Puntos Hacia Atrás',
            'nodos_x': x.tolist(),
            'nodos_y': y.tolist(),
            'paso': h,
            'derivadas': [d.tolist() if isinstance(d, (np.ndarray, float)) and d is not None else d for d in derivadas],
            'calculos': calculos
        }
        
        return derivadas, detalles
    
    @staticmethod
    def dos_puntos_centrada(x: List[float], y: List[float], h: float) -> Tuple[List[float], dict]:
        """
        Derivación con 2 puntos centrada
        f'(x) ≈ (f(x+h) - f(x-h)) / (2h)
        
        Args:
            x: Lista de valores x
            y: Lista de valores y (función en los puntos)
            h: Tamaño del paso
        
        Returns:
            Tupla (derivadas, detalles_cálculo)
        """
        x = np.array(x, dtype=float)
        y = np.array(y, dtype=float)
        n = len(x)
        
        if n < 3:
            raise ValueError("Se necesitan al menos 3 puntos para derivación centrada")
        
        derivadas = []
        calculos = []
        
        for i in range(n):
            if i == 0 or i == n - 1:
                # No se puede calcular en los extremos
                derivada = None
                calculo = "No calculable (punto extremo)"
            else:
                # Fórmula: f'(x) = (f(x+h) - f(x-h)) / (2h)
                derivada = (y[i+1] - y[i-1]) / (2 * h)
                calculo = f"({y[i+1]:.6f} - {y[i-1]:.6f}) / {2*h}"
            
            derivadas.append(derivada)
            calculos.append(calculo)
        
        detalles = {
            'metodo': 'Derivación 2 Puntos Centrada',
            'nodos_x': x.tolist(),
            'nodos_y': y.tolist(),
            'paso': h,
            'derivadas': [d.tolist() if isinstance(d, (np.ndarray, float)) and d is not None else d for d in derivadas],
            'calculos': calculos
        }
        
        return derivadas, detalles
    
    @staticmethod
    def tres_puntos_centrada(x: List[float], y: List[float], h: float) -> Tuple[List[float], dict]:
        """
        Derivación con 3 puntos centrada
        f'(x) ≈ (-f(x+h) + f(x-h)) / (2h)
        
        Args:
            x: Lista de valores x
            y: Lista de valores y (función en los puntos)
            h: Tamaño del paso
        
        Returns:
            Tupla (derivadas, detalles_cálculo)
        """
        x = np.array(x, dtype=float)
        y = np.array(y, dtype=float)
        n = len(x)
        
        if n < 3:
            raise ValueError("Se necesitan al menos 3 puntos")
        
        derivadas = []
        calculos = []
        
        for i in range(n):
            if i == 0 or i == n - 1:
                # No se puede calcular en los extremos
                derivada = None
                calculo = "No calculable (punto extremo)"
            else:
                # Fórmula: f'(x) = (-f(x+h) + f(x-h)) / (2h)
                derivada = (-y[i+1] + y[i-1]) / (2 * h)
                calculo = f"(-{y[i+1]:.6f} + {y[i-1]:.6f}) / {2*h}"
            
            derivadas.append(derivada)
            calculos.append(calculo)
        
        detalles = {
            'metodo': 'Derivación 3 Puntos Centrada',
            'nodos_x': x.tolist(),
            'nodos_y': y.tolist(),
            'paso': h,
            'derivadas': [d.tolist() if isinstance(d, (np.ndarray, float)) and d is not None else d for d in derivadas],
            'calculos': calculos
        }
        
        return derivadas, detalles
    
    @staticmethod
    def cinco_puntos_adelante(x: List[float], y: List[float], h: float) -> Tuple[List[float], dict]:
        """
        Derivación con 5 puntos hacia adelante
        f'(x) ≈ (-11f(x) + 18f(x+h) - 9f(x+2h) + 2f(x+3h)) / (6h)
        
        Args:
            x: Lista de valores x
            y: Lista de valores y (función en los puntos)
            h: Tamaño del paso
        
        Returns:
            Tupla (derivadas, detalles_cálculo)
        """
        x = np.array(x, dtype=float)
        y = np.array(y, dtype=float)
        n = len(x)
        
        if n < 4:
            raise ValueError("Se necesitan al menos 4 puntos")
        
        derivadas = []
        calculos = []
        
        for i in range(n):
            if i >= n - 3:
                # No se puede calcular en los últimos 3 puntos
                derivada = None
                calculo = "No calculable"
            else:
                # Fórmula: f'(x) = (-11f(x) + 18f(x+h) - 9f(x+2h) + 2f(x+3h)) / (6h)
                derivada = (-11 * y[i] + 18 * y[i+1] - 9 * y[i+2] + 2 * y[i+3]) / (6 * h)
                calculo = f"(-11*{y[i]:.6f} + 18*{y[i+1]:.6f} - 9*{y[i+2]:.6f} + 2*{y[i+3]:.6f}) / {6*h}"
            
            derivadas.append(derivada)
            calculos.append(calculo)
        
        detalles = {
            'metodo': 'Derivación 5 Puntos Hacia Adelante',
            'nodos_x': x.tolist(),
            'nodos_y': y.tolist(),
            'paso': h,
            'derivadas': [d.tolist() if isinstance(d, (np.ndarray, float)) and d is not None else d for d in derivadas],
            'calculos': calculos
        }
        
        return derivadas, detalles
    
    @staticmethod
    def cinco_puntos_atras(x: List[float], y: List[float], h: float) -> Tuple[List[float], dict]:
        """
        Derivación con 5 puntos hacia atrás
        f'(x) ≈ (-2f(x-3h) + 9f(x-2h) - 18f(x-h) + 11f(x)) / (6h)
        
        Args:
            x: Lista de valores x
            y: Lista de valores y (función en los puntos)
            h: Tamaño del paso
        
        Returns:
            Tupla (derivadas, detalles_cálculo)
        """
        x = np.array(x, dtype=float)
        y = np.array(y, dtype=float)
        n = len(x)
        
        if n < 4:
            raise ValueError("Se necesitan al menos 4 puntos")
        
        derivadas = []
        calculos = []
        
        for i in range(n):
            if i < 3:
                # No se puede calcular en los primeros 3 puntos
                derivada = None
                calculo = "No calculable"
            else:
                # Fórmula: f'(x) = (-2f(x-3h) + 9f(x-2h) - 18f(x-h) + 11f(x)) / (6h)
                derivada = (-2 * y[i-3] + 9 * y[i-2] - 18 * y[i-1] + 11 * y[i]) / (6 * h)
                calculo = f"(-2*{y[i-3]:.6f} + 9*{y[i-2]:.6f} - 18*{y[i-1]:.6f} + 11*{y[i]:.6f}) / {6*h}"
            
            derivadas.append(derivada)
            calculos.append(calculo)
        
        detalles = {
            'metodo': 'Derivación 5 Puntos Hacia Atrás',
            'nodos_x': x.tolist(),
            'nodos_y': y.tolist(),
            'paso': h,
            'derivadas': [d.tolist() if isinstance(d, (np.ndarray, float)) and d is not None else d for d in derivadas],
            'calculos': calculos
        }
        
        return derivadas, detalles
    
    @staticmethod
    def cinco_puntos_centrada(x: List[float], y: List[float], h: float) -> Tuple[List[float], dict]:
        """
        Derivación con 2 puntos hacia atrás
        f'(x) ≈ (f(x) - f(x-h)) / h
        
        Args:
            x: Lista de valores x
            y: Lista de valores y (función en los puntos)
            h: Tamaño del paso
        
        Returns:
            Tupla (derivadas, detalles_cálculo)
        """
        x = np.array(x, dtype=float)
        y = np.array(y, dtype=float)
        n = len(x)
        
        if n < 2:
            raise ValueError("Se necesitan al menos 2 puntos")
        
        derivadas = []
        calculos = []
        
        for i in range(n):
            if i == 0:
                # No se puede calcular en el primer punto
                derivada = None
                calculo = "No calculable (primer punto)"
            else:
                # Fórmula: f'(x) = (f(x) - f(x-h)) / h
                derivada = (y[i] - y[i-1]) / h
                calculo = f"({y[i]:.6f} - {y[i-1]:.6f}) / {h}"
            
            derivadas.append(derivada)
            calculos.append(calculo)
        
        detalles = {
            'metodo': 'Derivación 2 Puntos Hacia Atrás',
            'nodos_x': x.tolist(),
            'nodos_y': y.tolist(),
            'paso': h,
            'derivadas': [d.tolist() if isinstance(d, (np.ndarray, float)) and d is not None else d for d in derivadas],
            'calculos': calculos
        }
        
        return derivadas, detalles
    
    @staticmethod
    def dos_puntos_centrada(x: List[float], y: List[float], h: float) -> Tuple[List[float], dict]:
        """
        Derivación con 2 puntos centrada
        f'(x) ≈ (f(x+h) - f(x-h)) / (2h)
        
        Args:
            x: Lista de valores x
            y: Lista de valores y (función en los puntos)
            h: Tamaño del paso
        
        Returns:
            Tupla (derivadas, detalles_cálculo)
        """
        x = np.array(x, dtype=float)
        y = np.array(y, dtype=float)
        n = len(x)
        
        if n < 3:
            raise ValueError("Se necesitan al menos 3 puntos para derivación centrada")
        
        derivadas = []
        calculos = []
        
        for i in range(n):
            if i == 0 or i == n - 1:
                # No se puede calcular en los extremos
                derivada = None
                calculo = "No calculable (punto extremo)"
            else:
                # Fórmula: f'(x) = (f(x+h) - f(x-h)) / (2h)
                derivada = (y[i+1] - y[i-1]) / (2 * h)
                calculo = f"({y[i+1]:.6f} - {y[i-1]:.6f}) / {2*h}"
            
            derivadas.append(derivada)
            calculos.append(calculo)
        
        detalles = {
            'metodo': 'Derivación 2 Puntos Centrada',
            'nodos_x': x.tolist(),
            'nodos_y': y.tolist(),
            'paso': h,
            'derivadas': [d.tolist() if isinstance(d, (np.ndarray, float)) and d is not None else d for d in derivadas],
            'calculos': calculos
        }
        
        return derivadas, detalles
    
    @staticmethod
    def tres_puntos_atras(x: List[float], y: List[float], h: float) -> Tuple[List[float], dict]:
        """
        Derivación con 3 puntos hacia atrás
        f'(x) ≈ (3f(x) - 4f(x-h) + f(x-2h)) / (2h)
        
        Args:
            x: Lista de valores x
            y: Lista de valores y (función en los puntos)
            h: Tamaño del paso
        
        Returns:
            Tupla (derivadas, detalles_cálculo)
        """
        x = np.array(x, dtype=float)
        y = np.array(y, dtype=float)
        n = len(x)
        
        if n < 3:
            raise ValueError("Se necesitan al menos 3 puntos")
        
        derivadas = []
        calculos = []
        
        for i in range(n):
            if i < 2:
                # No se puede calcular en los dos primeros puntos
                derivada = None
                calculo = "No calculable"
            else:
                # Fórmula: f'(x) = (3f(x) - 4f(x-h) + f(x-2h)) / (2h)
                derivada = (3 * y[i] - 4 * y[i-1] + y[i-2]) / (2 * h)
                calculo = f"(3*{y[i]:.6f} - 4*{y[i-1]:.6f} + {y[i-2]:.6f}) / {2*h}"
            
            derivadas.append(derivada)
            calculos.append(calculo)
        
        detalles = {
            'metodo': 'Derivación 3 Puntos Hacia Atrás',
            'nodos_x': x.tolist(),
            'nodos_y': y.tolist(),
            'paso': h,
            'derivadas': [d.tolist() if isinstance(d, (np.ndarray, float)) and d is not None else d for d in derivadas],
            'calculos': calculos
        }
        
        return derivadas, detalles
    
    @staticmethod
    def tres_puntos_centrada(x: List[float], y: List[float], h: float) -> Tuple[List[float], dict]:
        """
        Derivación con 3 puntos centrada
        f'(x) ≈ (-f(x+h) + f(x-h)) / (2h)
        
        Args:
            x: Lista de valores x
            y: Lista de valores y (función en los puntos)
            h: Tamaño del paso
        
        Returns:
            Tupla (derivadas, detalles_cálculo)
        """
        x = np.array(x, dtype=float)
        y = np.array(y, dtype=float)
        n = len(x)
        
        if n < 3:
            raise ValueError("Se necesitan al menos 3 puntos")
        
        derivadas = []
        calculos = []
        
        for i in range(n):
            if i == 0 or i == n - 1:
                # No se puede calcular en los extremos
                derivada = None
                calculo = "No calculable (punto extremo)"
            else:
                # Fórmula: f'(x) = (-f(x+h) + f(x-h)) / (2h)
                derivada = (-y[i+1] + y[i-1]) / (2 * h)
                calculo = f"(-{y[i+1]:.6f} + {y[i-1]:.6f}) / {2*h}"
            
            derivadas.append(derivada)
            calculos.append(calculo)
        
        detalles = {
            'metodo': 'Derivación 3 Puntos Centrada',
            'nodos_x': x.tolist(),
            'nodos_y': y.tolist(),
            'paso': h,
            'derivadas': [d.tolist() if isinstance(d, (np.ndarray, float)) and d is not None else d for d in derivadas],
            'calculos': calculos
        }
        
        return derivadas, detalles
    
    @staticmethod
    def cinco_puntos_centrada(x: List[float], y: List[float], h: float) -> Tuple[List[float], dict]:
        """
        Derivación con 5 puntos centrada
        f'(x) ≈ (-f(x+2h) + 8f(x+h) - 8f(x-h) + f(x-2h)) / (12h)
        
        Args:
            x: Lista de valores x
            y: Lista de valores y (función en los puntos)
            h: Tamaño del paso
        
        Returns:
            Tupla (derivadas, detalles_cálculo)
        """
        x = np.array(x, dtype=float)
        y = np.array(y, dtype=float)
        n = len(x)
        
        if n < 5:
            raise ValueError("Se necesitan al menos 5 puntos")
        
        derivadas = []
        calculos = []
        
        for i in range(n):
            if i < 2 or i >= n - 2:
                # No se puede calcular en los extremos
                derivada = None
                calculo = "No calculable"
            else:
                # Fórmula: f'(x) = (-f(x+2h) + 8f(x+h) - 8f(x-h) + f(x-2h)) / (12h)
                derivada = (-y[i+2] + 8*y[i+1] - 8*y[i-1] + y[i-2]) / (12 * h)
                calculo = f"(-{y[i+2]:.6f} + 8*{y[i+1]:.6f} - 8*{y[i-1]:.6f} + {y[i-2]:.6f}) / {12*h}"
            
            derivadas.append(derivada)
            calculos.append(calculo)
        
        detalles = {
            'metodo': 'Derivación 5 Puntos Centrada',
            'nodos_x': x.tolist(),
            'nodos_y': y.tolist(),
            'paso': h,
            'derivadas': [d.tolist() if isinstance(d, (np.ndarray, float)) and d is not None else d for d in derivadas],
            'calculos': calculos
        }
        
        return derivadas, detalles
    
    @staticmethod
    def extrapolacion_richardson(x: List[float], y: List[float], h1: float, h2: float, 
                                 metodo: str = 'centrada') -> Tuple[List[float], dict]:
        """
        Extrapolación de Richardson para mejorar estimaciones de derivadas
        
        Args:
            x: Lista de valores x
            y: Lista de valores y
            h1: Primer tamaño de paso
            h2: Segundo tamaño de paso
            metodo: 'centrada' o 'atras'
        
        Returns:
            Tupla (derivadas mejoradas, detalles_cálculo)
        """
        x = np.array(x, dtype=float)
        y = np.array(y, dtype=float)
        n = len(x)
        
        if metodo == 'centrada':
            if n < 3:
                raise ValueError("Se necesitan al menos 3 puntos")
            
            der1 = []
            der2 = []
            der_richardson = []
            calculos = []
            
            for i in range(n):
                if i == 0 or i == n - 1:
                    der1.append(None)
                    der2.append(None)
                    der_richardson.append(None)
                    calculos.append("No calculable (punto extremo)")
                else:
                    d1 = (y[i+1] - y[i-1]) / (2 * h1)
                    d2 = (y[i+1] - y[i-1]) / (2 * h2)
                    
                    # Richardson: D_R = (4*D_h2 - D_h1) / 3
                    d_r = (4*d2 - d1) / 3
                    
                    der1.append(d1)
                    der2.append(d2)
                    der_richardson.append(d_r)
                    calculos.append(f"h1={h1}: {d1:.6f}, h2={h2}: {d2:.6f}, Richardson: {d_r:.6f}")
            
        else:  # atras
            if n < 2:
                raise ValueError("Se necesitan al menos 2 puntos")
            
            der1 = []
            der2 = []
            der_richardson = []
            calculos = []
            
            for i in range(n):
                if i == 0:
                    der1.append(None)
                    der2.append(None)
                    der_richardson.append(None)
                    calculos.append("No calculable (primer punto)")
                else:
                    d1 = (y[i] - y[i-1]) / h1
                    d2 = (y[i] - y[i-1]) / h2
                    
                    # Richardson
                    d_r = (4*d2 - d1) / 3
                    
                    der1.append(d1)
                    der2.append(d2)
                    der_richardson.append(d_r)
                    calculos.append(f"h1={h1}: {d1:.6f}, h2={h2}: {d2:.6f}, Richardson: {d_r:.6f}")
        
        detalles = {
            'metodo': f'Extrapolación Richardson ({metodo})',
            'nodos_x': x.tolist(),
            'nodos_y': y.tolist(),
            'paso_1': h1,
            'paso_2': h2,
            'derivadas_h1': [d.tolist() if isinstance(d, (np.ndarray, float)) and d is not None else d for d in der1],
            'derivadas_h2': [d.tolist() if isinstance(d, (np.ndarray, float)) and d is not None else d for d in der2],
            'derivadas_richardson': [d.tolist() if isinstance(d, (np.ndarray, float)) and d is not None else d for d in der_richardson],
            'calculos': calculos
        }
        
        return der_richardson, detalles

class Integracion:
    """Métodos de integración numérica"""
    
    @staticmethod
    def trapecio(a: float, b: float, n: int, f_values: List[float]) -> Tuple[float, dict]:
        """
        Regla del Trapecio
        
        Args:
            a: Límite inferior
            b: Límite superior
            n: Número de subintervalos
            f_values: Valores de la función en los puntos
        
        Returns:
            Tupla (valor_integral, detalles_cálculo)
        """
        h = (b - a) / n
        suma = f_values[0] + f_values[-1]
        
        for i in range(1, n):
            suma += 2 * f_values[i]
        
        integral = (h / 2) * suma
        
        detalles = {
            'metodo': 'Trapecio',
            'a': a,
            'b': b,
            'n': n,
            'h': h,
            'suma': suma,
            'integral': integral
        }
        
        return integral, detalles
    
    @staticmethod
    def simpson_1_3(a: float, b: float, n: int, f_values: List[float]) -> Tuple[float, dict]:
        """
        Regla de Simpson 1/3
        
        Args:
            a: Límite inferior
            b: Límite superior
            n: Número de subintervalos (debe ser par)
            f_values: Valores de la función en los puntos
        
        Returns:
            Tupla (valor_integral, detalles_cálculo)
        """
        if n % 2 != 0:
            raise ValueError("Para Simpson 1/3, n debe ser par")
        
        h = (b - a) / n
        suma_impar = sum(f_values[i] for i in range(1, n, 2))
        suma_par = sum(f_values[i] for i in range(2, n-1, 2))
        
        integral = (h / 3) * (f_values[0] + 4*suma_impar + 2*suma_par + f_values[-1])
        
        detalles = {
            'metodo': 'Simpson 1/3',
            'a': a,
            'b': b,
            'n': n,
            'h': h,
            'suma_impar': suma_impar,
            'suma_par': suma_par,
            'integral': integral
        }
        
        return integral, detalles
    
    @staticmethod
    def simpson_3_8(a: float, b: float, n: int, f_values: List[float]) -> Tuple[float, dict]:
        """
        Regla de Simpson 3/8
        
        Args:
            a: Límite inferior
            b: Límite superior
            n: Número de subintervalos (debe ser múltiplo de 3)
            f_values: Valores de la función en los puntos
        
        Returns:
            Tupla (valor_integral, detalles_cálculo)
        """
        if n % 3 != 0:
            raise ValueError("Para Simpson 3/8, n debe ser múltiplo de 3")
        
        h = (b - a) / n
        suma1 = sum(f_values[i] for i in range(1, n, 3))
        suma2 = sum(f_values[i] for i in range(2, n, 3))
        suma3 = sum(f_values[i] for i in range(3, n, 3))
        
        integral = (3*h / 8) * (f_values[0] + 3*suma1 + 3*suma2 + 2*suma3 + f_values[-1])
        
        detalles = {
            'metodo': 'Simpson 3/8',
            'a': a,
            'b': b,
            'n': n,
            'h': h,
            'integral': integral
        }
        
        return integral, detalles
    
    @staticmethod
    def cuadratura_gaussiana(a: float, b: float, f_values: List[float], n_points: int = 2) -> Tuple[float, dict]:
        """
        Cuadratura Gaussiana (Gauss-Legendre)
        
        Args:
            a: Límite inferior
            b: Límite superior
            f_values: Valores de la función en los puntos
            n_points: Número de puntos de Gauss
        
        Returns:
            Tupla (valor_integral, detalles_cálculo)
        """
        # Puntos y pesos de Gauss-Legendre para 2 y 3 puntos
        if n_points == 2:
            x = [-1/np.sqrt(3), 1/np.sqrt(3)]
            w = [1, 1]
        elif n_points == 3:
            x = [-np.sqrt(3/5), 0, np.sqrt(3/5)]
            w = [5/9, 8/9, 5/9]
        else:
            raise ValueError("Solo soporta 2 o 3 puntos de Gauss")
        
        # Transformar al intervalo [a, b]
        integral = 0
        for i in range(n_points):
            t = ((b - a) * x[i] + (a + b)) / 2
            integral += w[i] * f_values[i]
        
        integral *= (b - a) / 2
        
        detalles = {
            'metodo': f'Cuadratura Gaussiana ({n_points} puntos)',
            'a': a,
            'b': b,
            'n_points': n_points,
            'integral': integral
        }
        
        return integral, detalles
    
    @staticmethod
    def trapecio_multiple(a: float, b: float, n: int, f_values: List[float]) -> Tuple[float, dict]:
        """
        Integración múltiple con Trapecio (2D)
        
        Args:
            a: Límite inferior
            b: Límite superior
            n: Número de subintervalos
            f_values: Matriz de valores de la función
        
        Returns:
            Tupla (valor_integral, detalles_cálculo)
        """
        h = (b - a) / n
        integral = Integracion.trapecio(a, b, n, f_values)[0]
        
        detalles = {
            'metodo': 'Trapecio Múltiple',
            'a': a,
            'b': b,
            'n': n,
            'h': h,
            'integral': integral
        }
        
        return integral, detalles
    
    @staticmethod
    def simpson_1_3_multiple(a: float, b: float, n: int, f_values: List[float]) -> Tuple[float, dict]:
        """
        Integración múltiple con Simpson 1/3 (2D)
        
        Args:
            a: Límite inferior
            b: Límite superior
            n: Número de subintervalos (debe ser par)
            f_values: Matriz de valores de la función
        
        Returns:
            Tupla (valor_integral, detalles_cálculo)
        """
        if n % 2 != 0:
            raise ValueError("Para Simpson 1/3 múltiple, n debe ser par")
        
        integral = Integracion.simpson_1_3(a, b, n, f_values)[0]
        
        detalles = {
            'metodo': 'Simpson 1/3 Múltiple',
            'a': a,
            'b': b,
            'n': n,
            'integral': integral
        }
        
        return integral, detalles
    
    @staticmethod
    def extrapolacion_richardson_integracion(a: float, b: float, n1: int, n2: int, f_values_n1: List[float], f_values_n2: List[float]) -> Tuple[float, dict]:
        """
        Extrapolación de Richardson para integración
        
        Args:
            a: Límite inferior
            b: Límite superior
            n1: Primer número de subintervalos
            n2: Segundo número de subintervalos
            f_values_n1: Valores con n1 intervalos
            f_values_n2: Valores con n2 intervalos
        
        Returns:
            Tupla (valor_integral, detalles_cálculo)
        """
        I_n1, _ = Integracion.trapecio(a, b, n1, f_values_n1)
        I_n2, _ = Integracion.trapecio(a, b, n2, f_values_n2)
        
        # Extrapolación de Richardson para trapecio: p = 2
        integral = (4 * I_n2 - I_n1) / 3
        
        detalles = {
            'metodo': 'Extrapolación Richardson (Integración)',
            'a': a,
            'b': b,
            'n1': n1,
            'n2': n2,
            'I_n1': I_n1,
            'I_n2': I_n2,
            'integral': integral
        }
        
        return integral, detalles


class SistemasLineales:
    """Métodos para resolver sistemas de ecuaciones lineales"""
    
    @staticmethod
    def eliminacion_gaussiana_simple(A: List[List[float]], b: List[float]) -> Tuple[List[float], dict]:
        """
        Eliminación Gaussiana simple sin pivoteo
        
        Args:
            A: Matriz de coeficientes (n x n)
            b: Vector de términos independientes
        
        Returns:
            Tupla (solución, detalles)
        """
        A = np.array(A, dtype=float)
        b = np.array(b, dtype=float)
        n = len(b)
        
        # Crear matriz aumentada
        M = np.column_stack([A, b])
        
        # Eliminación hacia adelante
        for k in range(n - 1):
            for i in range(k + 1, n):
                if M[k, k] == 0:
                    raise ValueError(f"Elemento pivote cero en posición ({k}, {k})")
                factor = M[i, k] / M[k, k]
                M[i, k:] = M[i, k:] - factor * M[k, k:]
        
        # Sustitución hacia atrás
        x = np.zeros(n)
        for i in range(n - 1, -1, -1):
            x[i] = (M[i, -1] - np.dot(M[i, i+1:n], x[i+1:n])) / M[i, i]
        
        detalles = {
            'metodo': 'Eliminación Gaussiana Simple',
            'matriz_original': A.tolist(),
            'vector_b': b.tolist(),
            'matriz_escalonada': M[:, :-1].tolist(),
            'determinante': np.linalg.det(A),
            'numero_condicion': np.linalg.cond(A)
        }
        
        return x.tolist(), detalles
    
    @staticmethod
    def eliminacion_gaussiana_pivoteo_parcial(A: List[List[float]], b: List[float]) -> Tuple[List[float], dict]:
        """
        Eliminación Gaussiana con pivoteo parcial
        
        Args:
            A: Matriz de coeficientes
            b: Vector de términos independientes
        
        Returns:
            Tupla (solución, detalles)
        """
        A = np.array(A, dtype=float)
        b = np.array(b, dtype=float)
        n = len(b)
        
        # Crear matriz aumentada
        M = np.column_stack([A, b])
        permutaciones = list(range(n))
        
        # Eliminación hacia adelante con pivoteo parcial
        for k in range(n - 1):
            # Encontrar pivote máximo
            max_idx = k + np.argmax(np.abs(M[k:n, k]))
            
            # Intercambiar filas
            M[[k, max_idx]] = M[[max_idx, k]]
            permutaciones[k], permutaciones[max_idx] = permutaciones[max_idx], permutaciones[k]
            
            if abs(M[k, k]) < 1e-10:
                raise ValueError("Matriz singular o mal condicionada")
            
            # Eliminación
            for i in range(k + 1, n):
                factor = M[i, k] / M[k, k]
                M[i, k:] = M[i, k:] - factor * M[k, k:]
        
        # Sustitución hacia atrás
        x = np.zeros(n)
        for i in range(n - 1, -1, -1):
            x[i] = (M[i, -1] - np.dot(M[i, i+1:n], x[i+1:n])) / M[i, i]
        
        detalles = {
            'metodo': 'Eliminación Gaussiana con Pivoteo Parcial',
            'permutaciones': permutaciones,
            'matriz_escalonada': M[:, :-1].tolist()
        }
        
        return x.tolist(), detalles
    
    @staticmethod
    def eliminacion_gaussiana_pivoteo_total(A: List[List[float]], b: List[float]) -> Tuple[List[float], dict]:
        """
        Eliminación Gaussiana con pivoteo total
        """
        A = np.array(A, dtype=float)
        b = np.array(b, dtype=float)
        n = len(b)
        
        M = np.column_stack([A, b])
        perm_filas = list(range(n))
        perm_cols = list(range(n))
        
        for k in range(n - 1):
            # Encontrar pivote máximo en toda la submatriz
            max_val = 0
            max_i, max_j = k, k
            for i in range(k, n):
                for j in range(k, n):
                    if abs(M[i, j]) > abs(M[max_i, max_j]):
                        max_i, max_j = i, j
            
            # Intercambiar filas
            M[[k, max_i]] = M[[max_i, k]]
            perm_filas[k], perm_filas[max_i] = perm_filas[max_i], perm_filas[k]
            
            # Intercambiar columnas
            M[:, [k, max_j]] = M[:, [max_j, k]]
            perm_cols[k], perm_cols[max_j] = perm_cols[max_j], perm_cols[k]
            
            if abs(M[k, k]) < 1e-10:
                raise ValueError("Matriz singular")
            
            for i in range(k + 1, n):
                factor = M[i, k] / M[k, k]
                M[i, k:] = M[i, k:] - factor * M[k, k:]
        
        # Sustitución hacia atrás
        x = np.zeros(n)
        for i in range(n - 1, -1, -1):
            x[i] = (M[i, -1] - np.dot(M[i, i+1:n], x[i+1:n])) / M[i, i]
        
        # Reordenar solución según permutación de columnas
        x_reordenada = np.zeros(n)
        for i in range(n):
            x_reordenada[perm_cols[i]] = x[i]
        
        detalles = {
            'metodo': 'Eliminación Gaussiana con Pivoteo Total',
            'permutaciones_filas': perm_filas,
            'permutaciones_columnas': perm_cols
        }
        
        return x_reordenada.tolist(), detalles
    
    @staticmethod
    def factorizacion_lu(A: List[List[float]]) -> Tuple[List[List[float]], List[List[float]], dict]:
        """
        Factorización LU
        """
        A = np.array(A, dtype=float)
        n = len(A)
        
        L = np.eye(n)
        U = np.copy(A)
        
        for k in range(n - 1):
            if abs(U[k, k]) < 1e-10:
                raise ValueError("Factorización LU no es posible sin pivoteo")
            
            for i in range(k + 1, n):
                L[i, k] = U[i, k] / U[k, k]
                U[i, k:] = U[i, k:] - L[i, k] * U[k, k:]
                U[i, k] = 0
        
        detalles = {
            'metodo': 'Factorización LU',
            'matriz_L': L.tolist(),
            'matriz_U': U.tolist(),
            'verificacion': np.allclose(np.dot(L, U), A)
        }
        
        return L.tolist(), U.tolist(), detalles
    
    @staticmethod
    def factorizacion_plu(A: List[List[float]]) -> Tuple[List[List[float]], List[List[float]], List[List[float]], dict]:
        """
        Factorización PLU con pivoteo parcial
        """
        A = np.array(A, dtype=float)
        n = len(A)
        
        P = np.eye(n)
        L = np.eye(n)
        U = np.copy(A)
        
        for k in range(n - 1):
            # Encontrar pivote
            max_idx = k + np.argmax(np.abs(U[k:n, k]))
            
            # Intercambiar filas en U
            U[[k, max_idx]] = U[[max_idx, k]]
            
            # Intercambiar filas en L (excluyendo diagonal)
            L[[k, max_idx], :k] = L[[max_idx, k], :k]
            
            # Actualizar P
            P[[k, max_idx]] = P[[max_idx, k]]
            
            if abs(U[k, k]) < 1e-10:
                raise ValueError("Matriz singular")
            
            for i in range(k + 1, n):
                L[i, k] = U[i, k] / U[k, k]
                U[i, k:] = U[i, k:] - L[i, k] * U[k, k:]
                U[i, k] = 0
        
        detalles = {
            'metodo': 'Factorización PLU',
            'verificacion': np.allclose(np.dot(P, np.dot(L, U)), A)
        }
        
        return P.tolist(), L.tolist(), U.tolist(), detalles
    
    @staticmethod
    def factorizacion_llt(A: List[List[float]]) -> Tuple[List[List[float]], dict]:
        """
        Factorización LLT (Cholesky) - para matrices simétricas positivas definidas
        """
        A = np.array(A, dtype=float)
        n = len(A)
        
        # Verificar que sea simétrica
        if not np.allclose(A, A.T):
            raise ValueError("La matriz debe ser simétrica")
        
        L = np.zeros((n, n))
        
        for i in range(n):
            for j in range(i + 1):
                suma = np.sum(L[i, :j] * L[j, :j])
                if i == j:
                    val = A[i, i] - suma
                    if val <= 0:
                        raise ValueError("La matriz no es positiva definida")
                    L[i, j] = np.sqrt(val)
                else:
                    L[i, j] = (A[i, j] - suma) / L[j, j]
        
        detalles = {
            'metodo': 'Factorización LLT (Cholesky)',
            'matriz_L': L.tolist(),
            'verificacion': np.allclose(np.dot(L, L.T), A)
        }
        
        return L.tolist(), detalles


class EcuacionesDiferenciales:
    """Métodos para resolver ecuaciones diferenciales ordinarias"""
    
    @staticmethod
    def _eval_function(f_expr: str, x: float, y_values: List[float]) -> float:
        """
        Evalúa una función con las variables x, y1, y2, y3, ... (para sistemas)
        """
        # Reemplazar x
        expr = f_expr.replace('x', str(x))
        # Reemplazar y1, y2, y3, etc.
        for i, y_val in enumerate(y_values, 1):
            expr = expr.replace(f'y{i}', str(y_val))
        # Para compatibilidad con código antiguo, si no hay y1, reemplazar y con el primer valor
        if 'y' in expr and len(y_values) > 0:
            expr = expr.replace('y', str(y_values[0]))
        return eval(expr)
    
    @staticmethod
    def euler(x0: float, y0: float, xf: float, n: int, f_expr: str) -> Tuple[List, List, dict]:
        """
        Método de Euler
        
        Args:
            x0: Condición inicial x
            y0: Condición inicial y
            xf: Valor final de x
            n: Número de pasos
            f_expr: Función como string (ej: 'x + y')
        
        Returns:
            Tupla (x_valores, y_valores, detalles)
        """
        h = (xf - x0) / n
        x = [x0]
        y = [y0]
        
        for i in range(n):
            xi = x[-1]
            yi = y[-1]
            
            # Evaluar f(x, y)
            f_val = eval(f_expr.replace('x', str(xi)).replace('y', str(yi)))
            
            yi_new = yi + h * f_val
            xi_new = xi + h
            
            x.append(xi_new)
            y.append(yi_new)
        
        detalles = {
            'metodo': 'Euler',
            'x0': x0,
            'y0': y0,
            'xf': xf,
            'n': n,
            'h': h,
            'funcion': f_expr
        }
        
        return x, y, detalles
    
    @staticmethod
    def _taylor_derivatives(f_expr: str, order: int) -> List[str]:
        """
        Calcula simbólicamente f, f', f'', f''' como strings usando derivada total.
        
        Para una EDO dy/dx = f(x,y):
        - f(x,y)
        - f'(x,y) = ∂f/∂x + ∂f/∂y * f
        - f''(x,y) = ∂f'/∂x + ∂f'/∂y * f'
        - f'''(x,y) = ∂f''/∂x + ∂f''/∂y * f''
        
        Args:
            f_expr: Expresión de la función f(x,y)
            order: Número de derivadas a calcular (1, 2 o 3)
        
        Returns:
            Lista de strings [f, f', f'', f'''] hasta el orden especificado
        """
        import re
        
        x, y = symbols('x y')
        # Reemplazar y1 por y para compatibilidad
        expr_str = f_expr.replace('y1', 'y')
        
        # Procesar la expresión para agregar multiplicación implícita
        expr_str = _process_implicit_multiplication_metodos(expr_str)
        
        f = sympify(expr_str)
        
        # f (la función original)
        derivs = [f]
        
        # f' (primera derivada total)
        f_prime = diff(f, x) + diff(f, y) * f
        
        if order >= 1:
            derivs.append(f_prime)
        
        if order >= 2:
            # f'' (segunda derivada total de f')
            # f''(x,y) = ∂f'/∂x + ∂f'/∂y * f'
            f_double_prime = diff(f_prime, x) + diff(f_prime, y) * f_prime
            derivs.append(f_double_prime)
        
        if order >= 3:
            # f''' (tercera derivada total de f'')
            # f'''(x,y) = ∂f''/∂x + ∂f''/∂y * f''
            f_triple_prime = diff(f_double_prime, x) + diff(f_double_prime, y) * f_double_prime
            derivs.append(f_triple_prime)
        
        # Simplificar y convertir a strings
        simplified = []
        for d in derivs:
            # Expandir para obtener forma más clara
            d_expanded = expand(d)
            simplified.append(str(d_expanded))
        
        return simplified
    
    @staticmethod
    def taylor_orden_2(x0: float, y0: float, xf: float, n: int, f_expr: str) -> Tuple[List, List, dict]:
        """
        Método de Taylor orden 2.
        Calcula automáticamente la derivada f' usando derivada total.
        """
        from sympy import lambdify
        
        h = (xf - x0) / n
        x = [x0]
        y = [y0]
        
        # Calcular derivadas simbólicamente
        derivs = EcuacionesDiferenciales._taylor_derivatives(f_expr, 1)
        f_str, df_str = str(derivs[0]), str(derivs[1])
        
        # Crear funciones numéricas compiladas
        x_sym, y_sym = symbols('x y')
        f_expr_sym = sympify(f_expr.replace('y1', 'y'))
        df_expr_sym = sympify(df_str)
        
        f_func = lambdify((x_sym, y_sym), f_expr_sym, 'numpy')
        df_func = lambdify((x_sym, y_sym), df_expr_sym, 'numpy')
        
        for i in range(n):
            xi = x[-1]
            yi = y[-1]
            
            f_val = float(f_func(xi, yi))
            df_val = float(df_func(xi, yi))
            
            yi_new = yi + h * f_val + (h**2 / 2) * df_val
            
            x.append(xi + h)
            y.append(yi_new)
        
        detalles = {
            'metodo': 'Taylor Orden 2',
            'x0': x0,
            'y0': y0,
            'h': h,
            'n': n,
            'f_expr': f_str,
            'df_expr': df_str
        }
        
        return x, y, detalles
    
    @staticmethod
    def taylor_orden_3(x0: float, y0: float, xf: float, n: int, f_expr: str) -> Tuple[List, List, dict]:
        """
        Método de Taylor orden 3.
        Calcula automáticamente las derivadas f' y f'' usando derivada total.
        """
        from sympy import lambdify
        
        h = (xf - x0) / n
        x = [x0]
        y = [y0]
        
        # Calcular derivadas simbólicamente
        derivs = EcuacionesDiferenciales._taylor_derivatives(f_expr, 2)
        f_str, df_str, ddf_str = str(derivs[0]), str(derivs[1]), str(derivs[2])
        
        # Crear funciones numéricas compiladas
        x_sym, y_sym = symbols('x y')
        f_expr_sym = sympify(f_expr.replace('y1', 'y'))
        df_expr_sym = sympify(df_str)
        ddf_expr_sym = sympify(ddf_str)
        
        f_func = lambdify((x_sym, y_sym), f_expr_sym, 'numpy')
        df_func = lambdify((x_sym, y_sym), df_expr_sym, 'numpy')
        ddf_func = lambdify((x_sym, y_sym), ddf_expr_sym, 'numpy')
        
        for i in range(n):
            xi = x[-1]
            yi = y[-1]
            
            f_val = float(f_func(xi, yi))
            df_val = float(df_func(xi, yi))
            ddf_val = float(ddf_func(xi, yi))
            
            yi_new = yi + h * f_val + (h**2 / 2) * df_val + (h**3 / 6) * ddf_val
            
            x.append(xi + h)
            y.append(yi_new)
        
        detalles = {
            'metodo': 'Taylor Orden 3',
            'x0': x0,
            'y0': y0,
            'h': h,
            'n': n,
            'f_expr': f_str,
            'df_expr': df_str,
            'ddf_expr': ddf_str
        }
        
        return x, y, detalles
    
    @staticmethod
    def taylor_orden_4(x0: float, y0: float, xf: float, n: int, f_expr: str) -> Tuple[List, List, dict]:
        """
        Método de Taylor orden 4.
        Calcula automáticamente las derivadas f', f'' y f''' usando derivada total.
        """
        from sympy import lambdify
        
        h = (xf - x0) / n
        x = [x0]
        y = [y0]
        
        # Calcular derivadas simbólicamente
        derivs = EcuacionesDiferenciales._taylor_derivatives(f_expr, 3)
        f_str, df_str, ddf_str, dddf_str = str(derivs[0]), str(derivs[1]), str(derivs[2]), str(derivs[3])
        
        # Crear funciones numéricas compiladas
        x_sym, y_sym = symbols('x y')
        f_expr_sym = sympify(f_expr.replace('y1', 'y'))
        df_expr_sym = sympify(df_str)
        ddf_expr_sym = sympify(ddf_str)
        dddf_expr_sym = sympify(dddf_str)
        
        f_func = lambdify((x_sym, y_sym), f_expr_sym, 'numpy')
        df_func = lambdify((x_sym, y_sym), df_expr_sym, 'numpy')
        ddf_func = lambdify((x_sym, y_sym), ddf_expr_sym, 'numpy')
        dddf_func = lambdify((x_sym, y_sym), dddf_expr_sym, 'numpy')
        
        for i in range(n):
            xi = x[-1]
            yi = y[-1]
            
            f_val = float(f_func(xi, yi))
            df_val = float(df_func(xi, yi))
            ddf_val = float(ddf_func(xi, yi))
            dddf_val = float(dddf_func(xi, yi))
            
            yi_new = yi + h * f_val + (h**2 / 2) * df_val + (h**3 / 6) * ddf_val + (h**4 / 24) * dddf_val
            
            x.append(xi + h)
            y.append(yi_new)
        
        detalles = {
            'metodo': 'Taylor Orden 4',
            'x0': x0,
            'y0': y0,
            'h': h,
            'n': n,
            'f_expr': f_str,
            'df_expr': df_str,
            'ddf_expr': ddf_str,
            'dddf_expr': dddf_str
        }
        
        return x, y, detalles
    
    @staticmethod
    def runge_kutta_3(x0: float, y0: float, xf: float, n: int, f_expr: str) -> Tuple[List, List, dict]:
        """
        Método de Runge-Kutta orden 3
        """
        h = (xf - x0) / n
        x = [x0]
        y = [y0]
        
        for i in range(n):
            xi = x[-1]
            yi = y[-1]
            
            k1 = eval(f_expr.replace('x', str(xi)).replace('y', str(yi)))
            k2 = eval(f_expr.replace('x', str(xi + h/2)).replace('y', str(yi + h/2 * k1)))
            k3 = eval(f_expr.replace('x', str(xi + h)).replace('y', str(yi - h * k1 + 2 * h * k2)))
            
            yi_new = yi + (h / 6) * (k1 + 4 * k2 + k3)
            
            x.append(xi + h)
            y.append(yi_new)
        
        detalles = {
            'metodo': 'Runge-Kutta Orden 3',
            'h': h,
            'n': n
        }
        
        return x, y, detalles
    
    @staticmethod
    def runge_kutta_4(x0: float, y0: float, xf: float, n: int, f_expr: str) -> Tuple[List, List, dict]:
        """
        Método de Runge-Kutta orden 4
        """
        h = (xf - x0) / n
        x = [x0]
        y = [y0]
        
        for i in range(n):
            xi = x[-1]
            yi = y[-1]
            
            k1 = eval(f_expr.replace('x', str(xi)).replace('y', str(yi)))
            k2 = eval(f_expr.replace('x', str(xi + h/2)).replace('y', str(yi + h/2 * k1)))
            k3 = eval(f_expr.replace('x', str(xi + h/2)).replace('y', str(yi + h/2 * k2)))
            k4 = eval(f_expr.replace('x', str(xi + h)).replace('y', str(yi + h * k3)))
            
            yi_new = yi + (h / 6) * (k1 + 2*k2 + 2*k3 + k4)
            
            x.append(xi + h)
            y.append(yi_new)
        
        detalles = {
            'metodo': 'Runge-Kutta Orden 4',
            'h': h,
            'n': n,
            'funcion': f_expr
        }
        
        return x, y, detalles
    
    @staticmethod
    def runge_kutta_fehlberg(x0: float, y0: float, xf: float, n: int, f_expr: str) -> Tuple[List, List, dict]:
        """
        Método de Runge-Kutta-Fehlberg (4-5)
        """
        h = (xf - x0) / n
        x = [x0]
        y = [y0]
        
        c = [0, 1/4, 3/8, 12/13, 1, 1/2]
        a = [[0], [1/4], [3/32, 9/32], [1932/2197, -7200/2197, 7296/2197],
             [439/216, -8, 3680/513, -845/4104], [-8/27, 2, -3544/2565, 1859/4104, -11/40]]
        b = [16/135, 0, 6656/12825, 28561/56430, -9/50, 2/55]
        
        for i in range(n):
            xi = x[-1]
            yi = y[-1]
            
            K = [0] * 6
            for j in range(6):
                suma = sum(a[j][k] * K[k] for k in range(j))
                y_temp = yi + h * suma
                x_temp = xi + c[j] * h
                K[j] = eval(f_expr.replace('x', str(x_temp)).replace('y', str(y_temp)))
            
            yi_new = yi + h * sum(b[j] * K[j] for j in range(6))
            
            x.append(xi + h)
            y.append(yi_new)
        
        detalles = {
            'metodo': 'Runge-Kutta-Fehlberg (4-5)',
            'h': h,
            'n': n
        }
        
        return x, y, detalles
    
    @staticmethod
    def adams_bashforth(x0: float, y0: float, xf: float, n: int, f_expr: str) -> Tuple[List, List, dict]:
        """
        Método de Adams-Bashforth (multi-paso) de 4 pasos.
        Requiere al menos n >= 4 para usar el método de Adams.
        Si n < 4, se usa solo RK4.
        """
        if n < 4:
            raise ValueError("Adams-Bashforth requiere al menos 4 pasos (n >= 4)")
        
        h = (xf - x0) / n
        x = [x0]
        y = [y0]
        
        # Usar RK4 para los primeros 3 pasos (genera 4 puntos incluyendo el inicial)
        for i in range(3):
            xi = x[-1]
            yi = y[-1]
            
            k1 = eval(f_expr.replace('x', str(xi)).replace('y', str(yi)))
            k2 = eval(f_expr.replace('x', str(xi + h/2)).replace('y', str(yi + h/2 * k1)))
            k3 = eval(f_expr.replace('x', str(xi + h/2)).replace('y', str(yi + h/2 * k2)))
            k4 = eval(f_expr.replace('x', str(xi + h)).replace('y', str(yi + h * k3)))
            
            yi_new = yi + (h / 6) * (k1 + 2*k2 + 2*k3 + k4)
            x.append(xi + h)
            y.append(yi_new)
        
        # Calcular valores de f para los 4 puntos iniciales
        f_vals = []
        for xi, yi in zip(x, y):
            f_vals.append(eval(f_expr.replace('x', str(xi)).replace('y', str(yi))))
        
        # Adams-Bashforth de 4 pasos para los pasos restantes (n - 3 pasos más)
        for i in range(n - 3):
            yi_new = y[-1] + (h/24) * (55*f_vals[-1] - 59*f_vals[-2] + 37*f_vals[-3] - 9*f_vals[-4])
            xi_new = x[-1] + h
            
            x.append(xi_new)
            y.append(yi_new)
            
            f_new = eval(f_expr.replace('x', str(xi_new)).replace('y', str(yi_new)))
            f_vals.append(f_new)
            f_vals.pop(0)
        
        detalles = {
            'metodo': 'Adams-Bashforth',
            'h': h,
            'n': n
        }
        
        return x, y, detalles
    
    @staticmethod
    def adams_moulton(x0: float, y0: float, xf: float, n: int, f_expr: str) -> Tuple[List, List, dict]:
        """
        Método de Adams-Moulton (predictor-corrector) de 4 pasos.
        Requiere al menos n >= 4 para usar el método de Adams.
        Si n < 4, se usa solo RK4.
        """
        if n < 4:
            raise ValueError("Adams-Moulton requiere al menos 4 pasos (n >= 4)")
        
        h = (xf - x0) / n
        x = [x0]
        y = [y0]
        
        # Usar RK4 para los primeros 3 pasos (genera 4 puntos incluyendo el inicial)
        for i in range(3):
            xi = x[-1]
            yi = y[-1]
            
            k1 = eval(f_expr.replace('x', str(xi)).replace('y', str(yi)))
            k2 = eval(f_expr.replace('x', str(xi + h/2)).replace('y', str(yi + h/2 * k1)))
            k3 = eval(f_expr.replace('x', str(xi + h/2)).replace('y', str(yi + h/2 * k2)))
            k4 = eval(f_expr.replace('x', str(xi + h)).replace('y', str(yi + h * k3)))
            
            yi_new = yi + (h / 6) * (k1 + 2*k2 + 2*k3 + k4)
            x.append(xi + h)
            y.append(yi_new)
        
        # Calcular valores de f para los 4 puntos iniciales
        f_vals = []
        for xi, yi in zip(x, y):
            f_vals.append(eval(f_expr.replace('x', str(xi)).replace('y', str(yi))))
        
        # Adams-Moulton (predictor-corrector) para los pasos restantes (n - 3 pasos más)
        for i in range(n - 3):
            # Predictor: Adams-Bashforth
            y_pred = y[-1] + (h/24) * (55*f_vals[-1] - 59*f_vals[-2] + 37*f_vals[-3] - 9*f_vals[-4])
            x_new = x[-1] + h
            
            # Corrector: iteración de punto fijo
            y_corr = y_pred
            for _ in range(3):  # Iteraciones de corrección
                f_pred = eval(f_expr.replace('x', str(x_new)).replace('y', str(y_corr)))
                y_corr = y[-1] + (h/24) * (9*f_pred + 19*f_vals[-1] - 5*f_vals[-2] + f_vals[-3])
            
            x.append(x_new)
            y.append(y_corr)
            
            f_new = eval(f_expr.replace('x', str(x_new)).replace('y', str(y_corr)))
            f_vals.append(f_new)
            f_vals.pop(0)
        
        detalles = {
            'metodo': 'Adams-Moulton',
            'h': h,
            'n': n
        }
        
        return x, y, detalles
    
    # ================== MÉTODOS PARA SISTEMAS DE ECUACIONES ==================
    
    @staticmethod
    def euler_sistema(x0: float, y0: List[float], xf: float, n: int, f_exprs: List[str]) -> Tuple[List, List[List], dict]:
        """
        Método de Euler para sistemas de ecuaciones diferenciales
        
        Args:
            x0: Condición inicial x
            y0: Condiciones iniciales [y1_0, y2_0, ...]
            xf: Valor final de x
            n: Número de pasos
            f_exprs: Lista de funciones como strings (ej: ['y2', '-y1'])
        
        Returns:
            Tupla (x_valores, [[y1_vals], [y2_vals], ...], detalles)
        """
        h = (xf - x0) / n
        x = [x0]
        num_vars = len(y0)
        y_vals = [[y0[i]] for i in range(num_vars)]  # Inicializar para cada variable
        
        for step in range(n):
            xi = x[-1]
            yi = [y_vals[i][-1] for i in range(num_vars)]  # Obtener últimos valores
            
            # Calcular pendientes para cada ecuación
            slopes = []
            for f_expr in f_exprs:
                slope = EcuacionesDiferenciales._eval_function(f_expr, xi, yi)
                slopes.append(slope)
            
            # Actualizar valores
            for i in range(num_vars):
                y_new = yi[i] + h * slopes[i]
                y_vals[i].append(y_new)
            
            x.append(xi + h)
        
        detalles = {
            'metodo': 'Euler (Sistema)',
            'x0': x0,
            'y0': y0,
            'xf': xf,
            'n': n,
            'h': h,
            'funciones': f_exprs
        }
        
        return x, y_vals, detalles
    
    @staticmethod
    def runge_kutta_4_sistema(x0: float, y0: List[float], xf: float, n: int, f_exprs: List[str]) -> Tuple[List, List[List], dict]:
        """
        Método de Runge-Kutta orden 4 para sistemas de ecuaciones diferenciales
        """
        h = (xf - x0) / n
        x = [x0]
        num_vars = len(y0)
        y_vals = [[y0[i]] for i in range(num_vars)]
        
        for step in range(n):
            xi = x[-1]
            yi = [y_vals[i][-1] for i in range(num_vars)]
            
            # Calcular k1
            k1 = []
            for f_expr in f_exprs:
                k1.append(EcuacionesDiferenciales._eval_function(f_expr, xi, yi))
            
            # Calcular k2
            yi_k2 = [yi[i] + h/2 * k1[i] for i in range(num_vars)]
            k2 = []
            for f_expr in f_exprs:
                k2.append(EcuacionesDiferenciales._eval_function(f_expr, xi + h/2, yi_k2))
            
            # Calcular k3
            yi_k3 = [yi[i] + h/2 * k2[i] for i in range(num_vars)]
            k3 = []
            for f_expr in f_exprs:
                k3.append(EcuacionesDiferenciales._eval_function(f_expr, xi + h/2, yi_k3))
            
            # Calcular k4
            yi_k4 = [yi[i] + h * k3[i] for i in range(num_vars)]
            k4 = []
            for f_expr in f_exprs:
                k4.append(EcuacionesDiferenciales._eval_function(f_expr, xi + h, yi_k4))
            
            # Actualizar valores
            for i in range(num_vars):
                y_new = yi[i] + (h / 6) * (k1[i] + 2*k2[i] + 2*k3[i] + k4[i])
                y_vals[i].append(y_new)
            
            x.append(xi + h)
        
        detalles = {
            'metodo': 'Runge-Kutta Orden 4 (Sistema)',
            'x0': x0,
            'y0': y0,
            'xf': xf,
            'n': n,
            'h': h,
            'funciones': f_exprs
        }
        
        return x, y_vals, detalles


def _process_implicit_multiplication_metodos(expr: str) -> str:
    """
    Procesa una expresión para agregar multiplicación explícita donde sea necesario.
    Por ejemplo: '2y' -> '2*y', 'xy' -> 'x*y', '2(x+1)' -> '2*(x+1)', etc.
    """
    import re
    
    result = expr
    
    # Agregar * entre número y variable: 2y -> 2*y, 3x -> 3*x
    result = re.sub(r'(\d)([xy])', r'\1*\2', result)
    
    # Agregar * entre variable y variable: xy -> x*y, yx -> y*x (pero no en exponentes)
    result = re.sub(r'([xy])([xy])', r'\1*\2', result)
    
    # Agregar * entre número y paréntesis: 2(...) -> 2*(...)
    result = re.sub(r'(\d)\(', r'\1*(', result)
    
    # Agregar * entre variable y paréntesis: x(...) -> x*(...)
    result = re.sub(r'([xy])\(', r'\1*(', result)
    
    # Agregar * entre paréntesis y número: (...)2 -> (...)*2
    result = re.sub(r'\)(\d)', r')*\1', result)
    
    # Agregar * entre paréntesis y variable: (...)x -> (...)*x
    result = re.sub(r'\)([xy])', r')*\1', result)
    
    return result


class EcuacionesUnaVariable:
    """Métodos para resolver ecuaciones de una variable: f(x) = 0"""
    
    # Funciones matemáticas disponibles para eval
    _math_functions = {
        'sqrt': np.sqrt,
        'sin': np.sin,
        'cos': np.cos,
        'tan': np.tan,
        'exp': np.exp,
        'log': np.log,
        'log10': np.log10,
        'abs': abs,
        'pi': np.pi,
        'e': np.e
    }
    
    @staticmethod
    def _eval_function(expr: str, x: float) -> float:
        """Evalúa una expresión con soporte para funciones matemáticas"""
        try:
            # Reemplazar x con el valor
            expr_repl = expr.replace('x', f'({x})')
            # Evaluar con las funciones matemáticas disponibles
            return eval(expr_repl, {"__builtins__": {}}, EcuacionesUnaVariable._math_functions)
        except Exception as e:
            raise ValueError(f"Error al evaluar la función: {str(e)}")
    
    @staticmethod
    def biseccion(f_expr: str, a: float, b: float, tolerancia: float = 1e-5, max_iteraciones: int = 100) -> Tuple[float, dict]:
        """
        Método de Bisección
        
        Encuentra la raíz de f(x) = 0 en el intervalo [a, b]
        
        Args:
            f_expr: Función como string (ej: 'x**2 - 4')
            a: Límite inferior del intervalo
            b: Límite superior del intervalo
            tolerancia: Criterio de convergencia
            max_iteraciones: Número máximo de iteraciones
        
        Returns:
            Tupla (raíz, detalles con historial de iteraciones)
        """
        # Verificar que haya cambio de signo
        fa = EcuacionesUnaVariable._eval_function(f_expr, a)
        fb = EcuacionesUnaVariable._eval_function(f_expr, b)
        
        if fa * fb > 0:
            raise ValueError("No hay cambio de signo en el intervalo [a, b]. f(a) y f(b) deben tener signos opuestos")
        
        historial = []
        
        for i in range(max_iteraciones):
            c = (a + b) / 2
            fc = EcuacionesUnaVariable._eval_function(f_expr, c)
            
            error = abs(b - a)
            
            historial.append({
                'x': c,
                'fx': fc,
                'error': error
            })
            
            if abs(fc) < tolerancia or error < tolerancia:
                return c, {
                    'metodo': 'Bisección',
                    'raiz': c,
                    'fx': fc,
                    'iteraciones': i + 1,
                    'error_estimado': error,
                    'historial': historial
                }
            
            if fa * fc < 0:
                b = c
                fb = fc
            else:
                a = c
                fa = fc
        
        c = (a + b) / 2
        fc = EcuacionesUnaVariable._eval_function(f_expr, c)
        
        return c, {
            'metodo': 'Bisección',
            'raiz': c,
            'fx': fc,
            'iteraciones': max_iteraciones,
            'error_estimado': abs(b - a),
            'historial': historial
        }
    
    @staticmethod
    def falsa_posicion(f_expr: str, a: float, b: float, tolerancia: float = 1e-5, max_iteraciones: int = 100) -> Tuple[float, dict]:
        """
        Método de Falsa Posición (Regula Falsi)
        
        Args:
            f_expr: Función como string
            a: Límite inferior
            b: Límite superior
            tolerancia: Criterio de convergencia
            max_iteraciones: Número máximo de iteraciones
        
        Returns:
            Tupla (raíz, detalles)
        """
        fa = EcuacionesUnaVariable._eval_function(f_expr, a)
        fb = EcuacionesUnaVariable._eval_function(f_expr, b)
        
        if fa * fb > 0:
            raise ValueError("No hay cambio de signo en el intervalo [a, b]")
        
        historial = []
        x_anterior = a
        
        for i in range(max_iteraciones):
            # Fórmula de falsa posición
            c = (a * fb - b * fa) / (fb - fa)
            fc = EcuacionesUnaVariable._eval_function(f_expr, c)
            
            error = abs(c - x_anterior)
            
            historial.append({
                'x': c,
                'fx': fc,
                'error': error
            })
            
            if abs(fc) < tolerancia or error < tolerancia:
                return c, {
                    'metodo': 'Falsa Posición',
                    'raiz': c,
                    'fx': fc,
                    'iteraciones': i + 1,
                    'error_estimado': error,
                    'historial': historial
                }
            
            if fa * fc < 0:
                b = c
                fb = fc
            else:
                a = c
                fa = fc
            
            x_anterior = c
        
        return c, {
            'metodo': 'Falsa Posición',
            'raiz': c,
            'fx': fc,
            'iteraciones': max_iteraciones,
            'error_estimado': error,
            'historial': historial
        }
    
    @staticmethod
    def secante(f_expr: str, x0: float, x1: float, tolerancia: float = 1e-5, max_iteraciones: int = 100) -> Tuple[float, dict]:
        """
        Método de la Secante
        
        Args:
            f_expr: Función como string
            x0: Primer punto inicial
            x1: Segundo punto inicial
            tolerancia: Criterio de convergencia
            max_iteraciones: Número máximo de iteraciones
        
        Returns:
            Tupla (raíz, detalles)
        """
        f0 = EcuacionesUnaVariable._eval_function(f_expr, x0)
        f1 = EcuacionesUnaVariable._eval_function(f_expr, x1)
        
        historial = []
        
        for i in range(max_iteraciones):
            if abs(f1 - f0) < 1e-15:
                raise ValueError("Denominador muy pequeño - la función es casi horizontal")
            
            # Fórmula de la secante: x2 = x1 - f1 * (x1 - x0) / (f1 - f0)
            x2 = x1 - f1 * (x1 - x0) / (f1 - f0)
            f2 = EcuacionesUnaVariable._eval_function(f_expr, x2)
            
            error = abs(x2 - x1)
            
            historial.append({
                'x': x2,
                'fx': f2,
                'error': error
            })
            
            if abs(f2) < tolerancia or error < tolerancia:
                return x2, {
                    'metodo': 'Secante',
                    'raiz': x2,
                    'fx': f2,
                    'iteraciones': i + 1,
                    'error_estimado': error,
                    'historial': historial
                }
            
            x0, x1 = x1, x2
            f0, f1 = f1, f2
        
        return x2, {
            'metodo': 'Secante',
            'raiz': x2,
            'fx': f2,
            'iteraciones': max_iteraciones,
            'error_estimado': error,
            'historial': historial
        }
    
    @staticmethod
    def newton_raphson(f_expr: str, df_expr: str, x0: float, tolerancia: float = 1e-5, max_iteraciones: int = 100) -> Tuple[float, dict]:
        """
        Método de Newton-Raphson
        
        Args:
            f_expr: Función como string
            df_expr: Derivada como string
            x0: Punto inicial
            tolerancia: Criterio de convergencia
            max_iteraciones: Número máximo de iteraciones
        
        Returns:
            Tupla (raíz, detalles)
        """
        historial = []
        x = x0
        
        for i in range(max_iteraciones):
            f_val = EcuacionesUnaVariable._eval_function(f_expr, x)
            df_val = EcuacionesUnaVariable._eval_function(df_expr, x)
            
            if abs(df_val) < 1e-15:
                raise ValueError("La derivada es cero o muy cercana a cero")
            
            x_new = x - f_val / df_val
            error = abs(x_new - x)
            
            historial.append({
                'x': x_new,
                'fx': EcuacionesUnaVariable._eval_function(f_expr, x_new),
                'error': error
            })
            
            if abs(f_val) < tolerancia or error < tolerancia:
                return x_new, {
                    'metodo': 'Newton-Raphson',
                    'raiz': x_new,
                    'fx': EcuacionesUnaVariable._eval_function(f_expr, x_new),
                    'iteraciones': i + 1,
                    'error_estimado': error,
                    'historial': historial
                }
            
            x = x_new
        
        f_final = EcuacionesUnaVariable._eval_function(f_expr, x)
        
        return x, {
            'metodo': 'Newton-Raphson',
            'raiz': x,
            'fx': f_final,
            'iteraciones': max_iteraciones,
            'error_estimado': error,
            'historial': historial
        }
    
    @staticmethod
    def punto_fijo(g_expr: str, x0: float, tolerancia: float = 1e-5, max_iteraciones: int = 100) -> Tuple[float, dict]:
        """
        Método de Punto Fijo
        
        Resuelve x = g(x), encontrando raíces de f(x) = x - g(x) = 0
        
        Args:
            g_expr: Función de iteración como string (ej: 'x/2 + 1')
            x0: Punto inicial
            tolerancia: Criterio de convergencia
            max_iteraciones: Número máximo de iteraciones
        
        Returns:
            Tupla (raíz, detalles)
        """
        historial = []
        x = x0
        
        for i in range(max_iteraciones):
            x_new = EcuacionesUnaVariable._eval_function(g_expr, x)
            error = abs(x_new - x)
            
            # f(x) = x - g(x) en el nuevo punto
            fx = x_new - EcuacionesUnaVariable._eval_function(g_expr, x_new)
            
            historial.append({
                'x': x_new,
                'fx': fx,
                'error': error
            })
            
            if error < tolerancia:
                return x_new, {
                    'metodo': 'Punto Fijo',
                    'raiz': x_new,
                    'fx': fx,
                    'iteraciones': i + 1,
                    'error_estimado': error,
                    'historial': historial
                }
            
            x = x_new
        
        fx = x - EcuacionesUnaVariable._eval_function(g_expr, x)
        
        return x, {
            'metodo': 'Punto Fijo',
            'raiz': x,
            'fx': fx,
            'iteraciones': max_iteraciones,
            'error_estimado': error,
            'historial': historial
        }
    
    @staticmethod
    def muller(f_expr: str, x0: float, x1: float, x2: float, tolerancia: float = 1e-5, max_iteraciones: int = 100) -> Tuple[float, dict]:
        """
        Método de Müller
        
        Utiliza tres puntos iniciales y ajusta parábolas para encontrar raíces.
        Puede encontrar raíces complejas, aunque aquí trabajamos con reales.
        
        Args:
            f_expr: Función como string
            x0: Primer punto inicial
            x1: Segundo punto inicial
            x2: Tercer punto inicial
            tolerancia: Criterio de convergencia
            max_iteraciones: Número máximo de iteraciones
        
        Returns:
            Tupla (raíz, detalles)
        """
        f0 = EcuacionesUnaVariable._eval_function(f_expr, x0)
        f1 = EcuacionesUnaVariable._eval_function(f_expr, x1)
        f2 = EcuacionesUnaVariable._eval_function(f_expr, x2)
        
        historial = []
        
        for i in range(max_iteraciones):
            # Calcular diferencias divididas
            h0 = x1 - x0
            h1 = x2 - x1
            
            if abs(h0) < 1e-15 or abs(h1) < 1e-15:
                raise ValueError("Los puntos iniciales están demasiado cercanos")
            
            d0 = (f1 - f0) / h0
            d1 = (f2 - f1) / h1
            
            d2 = (d1 - d0) / (h1 + h0)
            
            # Coeficientes de la parábola: a*t^2 + b*t + c = 0
            # donde t = x - x2
            a = d2
            b = d1 + h1 * d2
            c = f2
            
            # Resolver la ecuación cuadrática
            discriminante = b**2 - 4*a*c
            
            if abs(a) < 1e-15:
                # Si a es muy pequeño, usar aproximación lineal
                if abs(b) > 1e-15:
                    x_new = x2 - c / b
                else:
                    raise ValueError("No se puede calcular la próxima aproximación")
            else:
                sqrt_disc = np.sqrt(abs(discriminante))
                
                # Usar la fórmula que da el denominador más grande para evitar cancelación
                if b > 0:
                    denominador = b + sqrt_disc
                else:
                    denominador = b - sqrt_disc
                
                if abs(denominador) > 1e-15:
                    x_new = x2 - 2*c / denominador
                else:
                    raise ValueError("Denominador demasiado pequeño")
            
            f_new = EcuacionesUnaVariable._eval_function(f_expr, x_new)
            error = abs(x_new - x2)
            
            historial.append({
                'x': x_new,
                'fx': f_new,
                'error': error
            })
            
            if abs(f_new) < tolerancia or error < tolerancia:
                return x_new, {
                    'metodo': 'Müller',
                    'raiz': x_new,
                    'fx': f_new,
                    'iteraciones': i + 1,
                    'error_estimado': error,
                    'historial': historial
                }
            
            # Actualizar puntos para la próxima iteración
            x0, x1, x2 = x1, x2, x_new
            f0, f1, f2 = f1, f2, f_new
        
        return x2, {
            'metodo': 'Müller',
            'raiz': x2,
            'fx': f2,
            'iteraciones': max_iteraciones,
            'error_estimado': error,
            'historial': historial
        }