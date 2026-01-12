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
