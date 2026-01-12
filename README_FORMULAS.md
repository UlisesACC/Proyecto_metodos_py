# Fórmulas de Métodos Numéricos

Documento completo con todas las fórmulas implementadas en la aplicación.

## 📚 Tabla de Contenidos

1. [Interpolación - Diferencias Divididas](#interpolación---diferencias-divididas)
2. [Derivación Numérica](#derivación-numérica)
3. [Integración Numérica](#integración-numérica)
4. [Sistemas de Ecuaciones Lineales](#sistemas-de-ecuaciones-lineales)
5. [Ecuaciones Diferenciales Ordinarias](#ecuaciones-diferenciales-ordinarias)

---

## Interpolación - Diferencias Divididas

### 1. Diferencias Divididas Hacia Adelante

**Fórmula:**
$$f[x_0, x_1, \ldots, x_n] = \frac{f[x_1, \ldots, x_n] - f[x_0, \ldots, x_{n-1}]}{x_n - x_0}$$

**Polinomio de Newton:**
$$P_n(x) = f[x_0] + f[x_0, x_1](x - x_0) + f[x_0, x_1, x_2](x - x_0)(x - x_1) + \cdots$$

### 2. Diferencias Divididas Hacia Atrás

**Fórmula Recursiva:**
$$f[x_i, x_{i-1}, \ldots, x_{i-j}] = \frac{f[x_{i-1}, \ldots, x_{i-j}] - f[x_i, x_{i-1}, \ldots, x_{i-j+1}]}{x_{i-j} - x_i}$$

### 3. Método de Neville

**Fórmula:**
$$P(x) = \frac{(x - x_j)P_{i,j-1}(x) - (x - x_i)P_{i+1,j}(x)}{x_i - x_j}$$

---

## Derivación Numérica

### Hacia Adelante (Forward Differences)

#### 2 Puntos
$$f'(x) \approx \frac{f(x+h) - f(x)}{h}$$
**Error: $O(h)$**

#### 3 Puntos
$$f'(x) \approx \frac{-3f(x) + 4f(x+h) - f(x+2h)}{2h}$$
**Error: $O(h^2)$**

#### 5 Puntos
$$f'(x) \approx \frac{-11f(x) + 18f(x+h) - 9f(x+2h) + 2f(x+3h)}{6h}$$
**Error: $O(h^4)$**

---

### Hacia Atrás (Backward Differences)

#### 2 Puntos
$$f'(x) \approx \frac{f(x) - f(x-h)}{h}$$
**Error: $O(h)$**

#### 3 Puntos
$$f'(x) \approx \frac{3f(x) - 4f(x-h) + f(x-2h)}{2h}$$
**Error: $O(h^2)$**

#### 5 Puntos
$$f'(x) \approx \frac{-2f(x-3h) + 9f(x-2h) - 18f(x-h) + 11f(x)}{6h}$$
**Error: $O(h^4)$**

---

### Centrada (Centered Differences)

#### 2 Puntos
$$f'(x) \approx \frac{f(x+h) - f(x-h)}{2h}$$
**Error: $O(h^2)$**

#### 3 Puntos
$$f'(x) \approx \frac{-f(x+h) + f(x-h)}{2h}$$
**Error: $O(h^2)$**

#### 5 Puntos
$$f'(x) \approx \frac{-f(x+2h) + 8f(x+h) - 8f(x-h) + f(x-2h)}{12h}$$
**Error: $O(h^4)$**

---

### Extrapolación de Richardson

**Fórmula:**
$$f'(x) \approx \frac{4f'(h/2) - f'(h)}{3}$$

Mejora la precisión combinando dos estimaciones con diferentes tamaños de paso.

---

## Integración Numérica

### 1. Regla del Trapecio
$$\int_a^b f(x)dx \approx \frac{h}{2}[f(x_0) + 2f(x_1) + 2f(x_2) + \cdots + 2f(x_{n-1}) + f(x_n)]$$

donde $h = \frac{b-a}{n}$

**Error: $O(h^2)$**

---

### 2. Simpson 1/3
$$\int_a^b f(x)dx \approx \frac{h}{3}[f(x_0) + 4f(x_1) + 2f(x_2) + 4f(x_3) + \cdots + f(x_n)]$$

**Requisito:** $n$ debe ser par
**Error: $O(h^4)$**

---

### 3. Simpson 3/8
$$\int_a^b f(x)dx \approx \frac{3h}{8}[f(x_0) + 3f(x_1) + 3f(x_2) + 2f(x_3) + \cdots + f(x_n)]$$

**Requisito:** $n$ debe ser divisible por 3
**Error: $O(h^4)$**

---

### 4. Cuadratura Gaussiana (Gauss-Legendre)

**2 puntos:**
$$\int_{-1}^{1} f(x)dx \approx f\left(-\frac{1}{\sqrt{3}}\right) + f\left(\frac{1}{\sqrt{3}}\right)$$

**3 puntos:**
$$\int_{-1}^{1} f(x)dx \approx \frac{5}{9}f\left(-\sqrt{\frac{3}{5}}\right) + \frac{8}{9}f(0) + \frac{5}{9}f\left(\sqrt{\frac{3}{5}}\right)$$

**Para $[a,b]$:**
$$\int_a^b f(x)dx = \frac{b-a}{2}\int_{-1}^{1} f\left(\frac{(b-a)x + a + b}{2}\right)dx$$

---

### 5. Integración Múltiple (2D)

#### Trapecio Múltiple
$$I \approx \frac{h_x h_y}{4} \sum_{i,j} w_{ij}f(x_i, y_j)$$

#### Simpson 1/3 Múltiple
$$I \approx \frac{h_x h_y}{9} \sum_{i,j} w_{ij}f(x_i, y_j)$$

---

### 6. Extrapolación de Richardson (Integración)
$$I \approx \frac{4I_{h/2} - I_h}{3}$$

Combina dos aproximaciones con diferentes números de intervalos.

---

## Sistemas de Ecuaciones Lineales

### 1. Eliminación Gaussiana Simple

**Fase de Eliminación (hacia adelante):**
$$m_{ik} = \frac{a_{ik}^{(k)}}{a_{kk}^{(k)}}$$
$$a_{ij}^{(k+1)} = a_{ij}^{(k)} - m_{ik} \cdot a_{kj}^{(k)}$$
$$b_i^{(k+1)} = b_i^{(k)} - m_{ik} \cdot b_k^{(k)}$$

**Sustitución hacia atrás:**
$$x_n = \frac{b_n^{(n)}}{a_{nn}^{(n)}}$$
$$x_i = \frac{b_i^{(n)} - \sum_{j=i+1}^{n} a_{ij}^{(n)}x_j}{a_{ii}^{(n)}} \quad \text{para } i = n-1, \ldots, 1$$

---

### 2. Eliminación Gaussiana con Pivoteo Parcial

**Selección de Pivote:**
$$|a_{kk}^{(k)}| = \max_{i=k}^{n} |a_{ik}^{(k)}|$$

Intercambiar filas $k$ y la fila con el máximo, luego proceder como en el método simple.

**Ventaja:** Mayor estabilidad numérica

---

### 3. Eliminación Gaussiana con Pivoteo Total

**Selección de Pivote:**
$$|a_{pq}^{(k)}| = \max_{i,j=k}^{n} |a_{ij}^{(k)}|$$

Intercambiar filas y columnas según sea necesario.

**Ventaja:** Máxima estabilidad numérica (a costo computacional)

---

### 4. Factorización LU

**Descomposición:**
$$A = LU$$

donde $L$ es triangular inferior y $U$ es triangular superior.

**Cálculo:**
$$u_{ij} = a_{ij} - \sum_{k=1}^{i-1} l_{ik}u_{kj}$$
$$l_{ij} = \frac{1}{u_{jj}}\left(a_{ij} - \sum_{k=1}^{j-1} l_{ik}u_{kj}\right)$$

**Ventaja:** Reutilizable para múltiples vectores $b$

---

### 5. Factorización PLU (con Pivoteo Parcial)

**Descomposición:**
$$PA = LU$$

donde $P$ es una matriz de permutación.

**Beneficio:** Estabilidad mejorada del método LU

---

### 6. Factorización LLT (Cholesky)

**Para matrices simétricas positivas definidas:**
$$A = LL^T$$

**Cálculo:**
$$l_{ii} = \sqrt{a_{ii} - \sum_{k=1}^{i-1} l_{ik}^2}$$
$$l_{ji} = \frac{1}{l_{ii}}\left(a_{ji} - \sum_{k=1}^{i-1} l_{jk}l_{ik}\right) \quad \text{para } j > i$$

**Ventaja:** $\approx 50\%$ más rápido que LU

---

## Ecuaciones Diferenciales Ordinarias

### PVI (Problema de Valor Inicial)
$$\frac{dy}{dx} = f(x, y), \quad y(x_0) = y_0$$

---

### 1. Método de Euler

**Fórmula:**
$$y_{n+1} = y_n + h \cdot f(x_n, y_n)$$

**Error local:** $O(h^2)$
**Error global:** $O(h)$

---

### 2. Método de Taylor (Orden 2)

**Fórmula:**
$$y_{n+1} = y_n + h \cdot f(x_n, y_n) + \frac{h^2}{2} \cdot f'(x_n, y_n)$$

**Error global:** $O(h^2)$

donde $f' = \frac{\partial f}{\partial x} + \frac{\partial f}{\partial y} \cdot f$

---

### 3. Método de Taylor (Orden 3)

**Fórmula:**
$$y_{n+1} = y_n + h \cdot f + \frac{h^2}{2} \cdot f' + \frac{h^3}{6} \cdot f''$$

**Error global:** $O(h^3)$

---

### 4. Método de Taylor (Orden 4)

**Fórmula:**
$$y_{n+1} = y_n + h \cdot f + \frac{h^2}{2} \cdot f' + \frac{h^3}{6} \cdot f'' + \frac{h^4}{24} \cdot f'''$$

**Error global:** $O(h^4)$

---

### 5. Runge-Kutta Orden 3

**Fórmula:**
$$k_1 = f(x_n, y_n)$$
$$k_2 = f(x_n + \frac{h}{2}, y_n + \frac{h}{2}k_1)$$
$$k_3 = f(x_n + h, y_n - hk_1 + 2hk_2)$$
$$y_{n+1} = y_n + \frac{h}{6}(k_1 + 4k_2 + k_3)$$

**Error global:** $O(h^3)$

---

### 6. Runge-Kutta Orden 4 (Clásico)

**Fórmula:**
$$k_1 = f(x_n, y_n)$$
$$k_2 = f(x_n + \frac{h}{2}, y_n + \frac{h}{2}k_1)$$
$$k_3 = f(x_n + \frac{h}{2}, y_n + \frac{h}{2}k_2)$$
$$k_4 = f(x_n + h, y_n + hk_3)$$
$$y_{n+1} = y_n + \frac{h}{6}(k_1 + 2k_2 + 2k_3 + k_4)$$

**Error global:** $O(h^4)$

---

### 7. Runge-Kutta-Fehlberg (4-5)

**Fórmula combinada:** Utiliza un método RK de orden 4 y otro de orden 5 para estimar el error local.

**Características:**
- Adaptativo: ajusta automáticamente el tamaño del paso
- Más eficiente que RK4 con paso fijo
- Ideal para problemas con soluciones de variabilidad alta

---

### 8. Adams-Bashforth (Método de 4 pasos)

**Fórmula explícita:**
$$y_{n+1} = y_n + \frac{h}{24}(55f_n - 59f_{n-1} + 37f_{n-2} - 9f_{n-3})$$

**Requisito:** 3 valores iniciales (típicamente de RK4)
**Error global:** $O(h^4)$

---

### 9. Adams-Moulton (Método implícito de 4 pasos)

**Fórmula:**
$$y_{n+1} = y_n + \frac{h}{24}(9f_{n+1} + 19f_n - 5f_{n-1} + f_{n-2})$$

**Predictor-Corrector:**
1. Predictor (Adams-Bashforth): $y_{n+1}^{(0)}$
2. Corrector (Adams-Moulton): iterar hasta convergencia

**Error global:** $O(h^4)$

---

## 📊 Comparativa de Métodos

### Derivación
| Método | Precisión | Complejidad |
|--------|-----------|-------------|
| 2 puntos (adelante) | $O(h)$ | Muy baja |
| 3 puntos | $O(h^2)$ | Baja |
| 5 puntos | $O(h^4)$ | Media |
| Richardson | $O(h^4)$ | Media-Alta |

### Integración
| Método | Precisión | Convergencia |
|--------|-----------|--------------|
| Trapecio | $O(h^2)$ | Lineal |
| Simpson 1/3 | $O(h^4)$ | Cuadrática |
| Simpson 3/8 | $O(h^4)$ | Cuadrática |
| Gaussiana | Variable | Rápida |

### EDO
| Método | Orden | Multi-paso |
|--------|-------|-----------|
| Euler | 1 | No |
| Taylor-2 | 2 | No |
| RK-3 | 3 | No |
| RK-4 | 4 | No |
| Adams-B | 4 | **Sí** |
| Adams-M | 4 | **Sí** |

---

## 🔍 Notas Importantes

1. **Estabilidad:** Los métodos con pivoteo son más estables numéricamente
2. **Precisión vs Costo:** Mayor orden = más precisión pero más evaluaciones de función
3. **Paso adaptativo:** RK-Fehlberg es ideal para funciones con comportamiento variable
4. **Métodos multi-paso:** Requieren valores iniciales adicionales
5. **Matrices especiales:** Usar Cholesky solo para simétricas positivas definidas

---

**Última actualización:** 12 de enero de 2026
**Aplicación:** Métodos Numéricos - ESCOM
