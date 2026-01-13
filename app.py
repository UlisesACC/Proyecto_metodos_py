from flask import Flask, render_template, request, jsonify
import numpy as np
from sympy import symbols, diff, lambdify, parsing, sympify, expand
from metodos.metodos import DiferenciasFinitas, Derivacion, Integracion, SistemasLineales, EcuacionesDiferenciales, EcuacionesUnaVariable

app = Flask(__name__)

@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')

@app.route('/diferencias-divididas')
def diferencias_divididas():
    """Página de diferencias divididas"""
    return render_template('diferencias_divididas.html')

@app.route('/derivacion')
def derivacion():
    """Página de derivación numérica"""
    return render_template('derivacion.html')

@app.route('/integracion')
def integracion():
    """Página de integración numérica"""
    return render_template('integracion.html')

@app.route('/sistemas-lineales')
def sistemas_lineales():
    """Página de sistemas de ecuaciones lineales"""
    return render_template('sistemas_lineales.html')

@app.route('/ecuaciones-diferenciales')
def ecuaciones_diferenciales():
    """Página de ecuaciones diferenciales"""
    return render_template('ecuaciones_diferenciales.html')

@app.route('/ecuaciones-una-variable')
def ecuaciones_una_variable():
    """Página de solución de ecuaciones de una variable"""
    return render_template('ecuaciones_una_variable.html')

@app.route('/test-derivadas')
def test_derivadas():
    """Página de prueba para derivadas (DEBUG)"""
    return render_template('test_derivadas.html')

@app.route('/api/health', methods=['GET'])
def health():
    """Endpoint de verificación de salud"""
    return jsonify({'status': 'ok', 'message': 'App de Métodos Numéricos funcionando'})

@app.route('/api/calcular-derivadas', methods=['POST'])
def api_calcular_derivadas():
    """Calcular derivadas totales automáticamente usando sympy para métodos de Taylor"""
    try:
        datos = request.get_json()
        f_expr_str = datos.get('f_expr', '')
        orden = datos.get('orden', 3)
        
        if not f_expr_str:
            return jsonify({'error': 'Se requiere una expresión'}), 400
        
        try:
            # Crear símbolos
            x, y = symbols('x y')
            
            # Parsear la expresión (reemplazar y1 por y para compatibilidad)
            expr_str = f_expr_str.replace('y1', 'y')
            
            # Procesar la expresión para agregar multiplicación implícita
            # Por ejemplo: 2y -> 2*y, xy -> x*y, etc.
            processed_expr = _process_implicit_multiplication(expr_str)
            
            f = sympify(processed_expr)
            
            # Calcular derivadas totales usando el método correcto
            # f (función original)
            derivs = [f]
            
            # f' = ∂f/∂x + ∂f/∂y * f
            f_prime = diff(f, x) + diff(f, y) * f
            
            if orden >= 1:
                derivs.append(f_prime)
            
            if orden >= 2:
                # f'' = ∂f'/∂x + ∂f'/∂y * f'
                f_double_prime = diff(f_prime, x) + diff(f_prime, y) * f_prime
                derivs.append(f_double_prime)
            
            if orden >= 3:
                # f''' = ∂f''/∂x + ∂f''/∂y * f''
                f_triple_prime = diff(f_double_prime, x) + diff(f_double_prime, y) * f_double_prime
                derivs.append(f_triple_prime)
            
            # Construir respuesta simplificando las expresiones
            resultado = {
                'f_expr': f_expr_str,
                'orden': orden
            }
            
            if len(derivs) > 1:
                resultado['df_expr'] = str(expand(derivs[1]))
            if len(derivs) > 2:
                resultado['ddf_expr'] = str(expand(derivs[2]))
            if len(derivs) > 3:
                resultado['dddf_expr'] = str(expand(derivs[3]))
            
            return jsonify(resultado), 200
            
        except Exception as e:
            return jsonify({'error': f'Error al calcular derivadas: {str(e)}'}), 400
    
    except Exception as e:
        return jsonify({'error': f'Error en el servidor: {str(e)}'}), 500


def _process_implicit_multiplication(expr: str) -> str:
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

@app.route('/api/diferencias-divididas', methods=['POST'])
def api_diferencias_divididas():
    """API para calcular diferencias divididas"""
    try:
        datos = request.get_json()
        
        # Validar datos
        if not datos:
            return jsonify({'error': 'No se recibieron datos'}), 400
        
        metodo = datos.get('metodo')
        nodos_x = datos.get('nodos_x')
        nodos_y = datos.get('nodos_y')
        punto_eval = datos.get('punto_eval')
        
        # Validar campos requeridos
        if not all([metodo, nodos_x, nodos_y, punto_eval is not None]):
            return jsonify({'error': 'Faltan campos requeridos'}), 400
        
        # Ejecutar método seleccionado
        if metodo == 'adelante':
            resultado, detalles = DiferenciasFinitas.diferencias_divididas_adelante(
                nodos_x, nodos_y, punto_eval
            )
        elif metodo == 'atras':
            resultado, detalles = DiferenciasFinitas.diferencias_divididas_atras(
                nodos_x, nodos_y, punto_eval
            )
        elif metodo == 'neville':
            resultado, detalles = DiferenciasFinitas.neville(
                nodos_x, nodos_y, punto_eval
            )
        else:
            return jsonify({'error': 'Método no válido'}), 400
        
        return jsonify({
            'resultado': resultado,
            'detalles': detalles
        }), 200
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Error en el cálculo: {str(e)}'}), 500

@app.route('/api/derivacion', methods=['POST'])
def api_derivacion():
    """API para calcular derivación numérica"""
    try:
        datos = request.get_json()
        
        # Validar datos
        if not datos:
            return jsonify({'error': 'No se recibieron datos'}), 400
        
        metodo = datos.get('metodo')
        nodos_x = datos.get('nodos_x')
        nodos_y = datos.get('nodos_y')
        paso = datos.get('paso')
        
        # Validar campos requeridos
        if not all([metodo, nodos_x, nodos_y, paso]):
            return jsonify({'error': 'Faltan campos requeridos'}), 400
        
        # Ejecutar método seleccionado
        if metodo == '2_adelante':
            derivadas, detalles = Derivacion.dos_puntos_adelante(nodos_x, nodos_y, paso)
        elif metodo == '2_atras':
            derivadas, detalles = Derivacion.dos_puntos_atras(nodos_x, nodos_y, paso)
        elif metodo == '3_adelante':
            derivadas, detalles = Derivacion.tres_puntos_adelante(nodos_x, nodos_y, paso)
        elif metodo == '3_atras':
            derivadas, detalles = Derivacion.tres_puntos_atras(nodos_x, nodos_y, paso)
        elif metodo == '2_centrada':
            derivadas, detalles = Derivacion.dos_puntos_centrada(nodos_x, nodos_y, paso)
        elif metodo == '3_centrada':
            derivadas, detalles = Derivacion.tres_puntos_centrada(nodos_x, nodos_y, paso)
        elif metodo == '5_adelante':
            derivadas, detalles = Derivacion.cinco_puntos_adelante(nodos_x, nodos_y, paso)
        elif metodo == '5_atras':
            derivadas, detalles = Derivacion.cinco_puntos_atras(nodos_x, nodos_y, paso)
        elif metodo == '5_centrada':
            derivadas, detalles = Derivacion.cinco_puntos_centrada(nodos_x, nodos_y, paso)
        elif metodo == 'richardson':
            paso2 = datos.get('paso2')
            if not paso2:
                return jsonify({'error': 'Debe proporcionar paso2 para Richardson'}), 400
            derivadas, detalles = Derivacion.extrapolacion_richardson(
                nodos_x, nodos_y, paso, paso2, metodo='centrada'
            )
        else:
            return jsonify({'error': 'Método no válido'}), 400
        
        return jsonify({
            'derivadas': derivadas,
            'detalles': detalles
        }), 200
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Error en el cálculo: {str(e)}'}), 500

@app.route('/api/integracion', methods=['POST'])
def api_integracion():
    """API para calcular integración numérica"""
    try:
        datos = request.get_json()
        
        # Validar datos
        if not datos:
            return jsonify({'error': 'No se recibieron datos'}), 400
        
        metodo = datos.get('metodo')
        a = datos.get('a')
        b = datos.get('b')
        n = datos.get('n')
        valores_f = datos.get('valores_f')
        
        # Validar campos requeridos
        if not all([metodo, a is not None, b is not None, n, valores_f]):
            return jsonify({'error': 'Faltan campos requeridos'}), 400
        
        # Convertir a tipos correctos
        try:
            a = float(a)
            b = float(b)
            n = int(n)
            valores_f = [float(v) for v in valores_f]
        except (ValueError, TypeError):
            return jsonify({'error': 'Datos inválidos'}), 400
        
        # Ejecutar método seleccionado
        if metodo == 'trapecio':
            resultado, detalles = Integracion.trapecio(a, b, n, valores_f)
        elif metodo == 'simpson_1_3':
            resultado, detalles = Integracion.simpson_1_3(a, b, n, valores_f)
        elif metodo == 'simpson_3_8':
            resultado, detalles = Integracion.simpson_3_8(a, b, n, valores_f)
        elif metodo == 'cuadratura_gaussiana':
            n_points = datos.get('n_points', 2)
            try:
                n_points = int(n_points)
            except (ValueError, TypeError):
                n_points = 2
            resultado, detalles = Integracion.cuadratura_gaussiana(a, b, valores_f, n_points)
        elif metodo == 'trapecio_multiple':
            resultado, detalles = Integracion.trapecio_multiple(a, b, n, valores_f)
        elif metodo == 'simpson_1_3_multiple':
            resultado, detalles = Integracion.simpson_1_3_multiple(a, b, n, valores_f)
        elif metodo == 'extrapolacion':
            n2 = datos.get('n2')
            valores_f2 = datos.get('valores_f2')
            
            if not all([n2 is not None, valores_f2]):
                return jsonify({'error': 'Faltan campos para extrapolación'}), 400
            
            try:
                n2 = int(n2)
                valores_f2 = [float(v) for v in valores_f2]
            except (ValueError, TypeError):
                return jsonify({'error': 'Datos inválidos para extrapolación'}), 400
            
            resultado, detalles = Integracion.extrapolacion_richardson_integracion(
                a, b, n, n2, valores_f, valores_f2
            )
        else:
            return jsonify({'error': 'Método no válido'}), 400
        
        return jsonify({
            'resultado': resultado,
            'detalles': detalles
        }), 200
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Error en el cálculo: {str(e)}'}), 500

@app.route('/api/sistemas-lineales', methods=['POST'])
def api_sistemas_lineales():
    """API para resolver sistemas de ecuaciones lineales"""
    try:
        datos = request.get_json()
        
        if not datos:
            return jsonify({'error': 'No se recibieron datos'}), 400
        
        metodo = datos.get('metodo')
        matriz_A = datos.get('matriz_A')
        vector_b = datos.get('vector_b')
        
        if not all([metodo, matriz_A, vector_b]):
            return jsonify({'error': 'Faltan campos requeridos'}), 400
        
        try:
            matriz_A = [[float(x) for x in fila] for fila in matriz_A]
            vector_b = [float(x) for x in vector_b]
        except (ValueError, TypeError):
            return jsonify({'error': 'Datos inválidos'}), 400
        
        if metodo == 'gaussiana_simple':
            solucion, detalles = SistemasLineales.eliminacion_gaussiana_simple(matriz_A, vector_b)
        elif metodo == 'gaussiana_parcial':
            solucion, detalles = SistemasLineales.eliminacion_gaussiana_pivoteo_parcial(matriz_A, vector_b)
        elif metodo == 'gaussiana_total':
            solucion, detalles = SistemasLineales.eliminacion_gaussiana_pivoteo_total(matriz_A, vector_b)
        elif metodo == 'lu':
            L, U, detalles = SistemasLineales.factorizacion_lu(matriz_A)
            return jsonify({
                'L': L,
                'U': U,
                'detalles': detalles
            }), 200
        elif metodo == 'plu':
            P, L, U, detalles = SistemasLineales.factorizacion_plu(matriz_A)
            return jsonify({
                'P': P,
                'L': L,
                'U': U,
                'detalles': detalles
            }), 200
        elif metodo == 'llt':
            L, detalles = SistemasLineales.factorizacion_llt(matriz_A)
            return jsonify({
                'L': L,
                'detalles': detalles
            }), 200
        else:
            return jsonify({'error': 'Método no válido'}), 400
        
        return jsonify({
            'solucion': solucion,
            'detalles': detalles
        }), 200
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Error en el cálculo: {str(e)}'}), 500

@app.route('/api/ecuaciones-diferenciales', methods=['POST'])
def api_ecuaciones_diferenciales():
    """API para resolver ecuaciones diferenciales (single o sistemas)"""
    try:
        datos = request.get_json()
        
        if not datos:
            return jsonify({'error': 'No se recibieron datos'}), 400
        
        metodo = datos.get('metodo')
        x0 = datos.get('x0')
        y0 = datos.get('y0')  # Puede ser número (single) o lista (sistema)
        xf = datos.get('xf')
        n = datos.get('n')
        
        # Verificar si es un sistema (functions) o ecuación única (f_expr)
        functions = datos.get('functions')  # Lista de funciones para sistemas
        f_expr = datos.get('f_expr')  # String para ecuación única
        
        # Si viene functions con una sola función, convertir a f_expr para ecuación única
        if functions and len(functions) == 1 and not f_expr:
            f_expr = functions[0]
            functions = None
        
        if not all([metodo, x0 is not None, y0 is not None, xf is not None, n is not None]):
            return jsonify({'error': 'Faltan campos requeridos'}), 400
        
        # Determinar si es sistema (más de una función) o ecuación única
        is_sistema = (functions is not None and len(functions) > 1)
        
        try:
            x0 = float(x0)
            xf = float(xf)
            n = int(n)
            
            if is_sistema:
                if not isinstance(y0, list):
                    y0 = [y0]
                y0 = [float(v) for v in y0]
            else:
                # Para ecuación única, tomar el primer valor si es lista
                if isinstance(y0, list):
                    y0 = float(y0[0])
                else:
                    y0 = float(y0)
        except (ValueError, TypeError) as e:
            return jsonify({'error': f'Datos inválidos: {str(e)}'}), 400
        
        # RESOLVER SISTEMAS DE ECUACIONES
        if is_sistema:
            if not functions:
                return jsonify({'error': 'Se requiere lista de funciones para sistema'}), 400
            
            if metodo == 'euler':
                x_vals, y_vals, detalles = EcuacionesDiferenciales.euler_sistema(x0, y0, xf, n, functions)
            elif metodo == 'rk4':
                x_vals, y_vals, detalles = EcuacionesDiferenciales.runge_kutta_4_sistema(x0, y0, xf, n, functions)
            else:
                # Para otros métodos en sistema, usar RK4 por defecto
                x_vals, y_vals, detalles = EcuacionesDiferenciales.runge_kutta_4_sistema(x0, y0, xf, n, functions)
            
            return jsonify({
                'x_valores': x_vals,
                'y_valores': y_vals,
                'detalles': detalles
            }), 200
        
        # RESOLVER ECUACIÓN ÚNICA (comportamiento original)
        if not f_expr:
            return jsonify({'error': 'Se requiere f_expr para ecuación única'}), 400
        
        if metodo == 'euler':
            x_vals, y_vals, detalles = EcuacionesDiferenciales.euler(x0, y0, xf, n, f_expr)
        elif metodo == 'taylor_2':
            # Las derivadas se calculan automáticamente usando SymPy
            x_vals, y_vals, detalles = EcuacionesDiferenciales.taylor_orden_2(x0, y0, xf, n, f_expr)
        elif metodo == 'taylor_3':
            # Las derivadas se calculan automáticamente usando SymPy
            x_vals, y_vals, detalles = EcuacionesDiferenciales.taylor_orden_3(x0, y0, xf, n, f_expr)
        elif metodo == 'taylor_4':
            # Las derivadas se calculan automáticamente usando SymPy
            x_vals, y_vals, detalles = EcuacionesDiferenciales.taylor_orden_4(x0, y0, xf, n, f_expr)
        elif metodo == 'rk3':
            x_vals, y_vals, detalles = EcuacionesDiferenciales.runge_kutta_3(x0, y0, xf, n, f_expr)
        elif metodo == 'rk4':
            x_vals, y_vals, detalles = EcuacionesDiferenciales.runge_kutta_4(x0, y0, xf, n, f_expr)
        elif metodo == 'rkf':
            x_vals, y_vals, detalles = EcuacionesDiferenciales.runge_kutta_fehlberg(x0, y0, xf, n, f_expr)
        elif metodo == 'adams_b':
            x_vals, y_vals, detalles = EcuacionesDiferenciales.adams_bashforth(x0, y0, xf, n, f_expr)
        elif metodo == 'adams_m':
            x_vals, y_vals, detalles = EcuacionesDiferenciales.adams_moulton(x0, y0, xf, n, f_expr)
        else:
            return jsonify({'error': 'Método no válido'}), 400
        
        return jsonify({
            'x_valores': x_vals,
            'y_valores': [y_vals],  # Envolver en lista para mantener formato consistente
            'detalles': detalles,
            'pares': list(zip(x_vals, y_vals))
        }), 200
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Error en el cálculo: {str(e)}'}), 500

@app.route('/api/ecuaciones-una-variable', methods=['POST'])
def api_ecuaciones_una_variable():
    """API para resolver ecuaciones de una variable"""
    try:
        datos = request.get_json()
        
        if not datos:
            return jsonify({'error': 'No se recibieron datos'}), 400
        
        metodo = datos.get('metodo')
        funcion = datos.get('funcion')
        tolerancia = datos.get('tolerancia', 1e-5)
        max_iteraciones = datos.get('max_iteraciones', 100)
        
        if not all([metodo, funcion]):
            return jsonify({'error': 'Faltan campos requeridos'}), 400
        
        try:
            tolerancia = float(tolerancia)
            max_iteraciones = int(max_iteraciones)
        except (ValueError, TypeError):
            return jsonify({'error': 'Datos inválidos'}), 400
        
        # Ejecutar método seleccionado
        if metodo == 'biseccion':
            a = datos.get('a')
            b = datos.get('b')
            if not all([a is not None, b is not None]):
                return jsonify({'error': 'Se requieren a y b para bisección'}), 400
            try:
                a = float(a)
                b = float(b)
            except (ValueError, TypeError):
                return jsonify({'error': 'a y b deben ser números'}), 400
            
            raiz, detalles = EcuacionesUnaVariable.biseccion(funcion, a, b, tolerancia, max_iteraciones)
            
        elif metodo == 'falsa_posicion':
            a = datos.get('a')
            b = datos.get('b')
            if not all([a is not None, b is not None]):
                return jsonify({'error': 'Se requieren a y b para falsa posición'}), 400
            try:
                a = float(a)
                b = float(b)
            except (ValueError, TypeError):
                return jsonify({'error': 'a y b deben ser números'}), 400
            
            raiz, detalles = EcuacionesUnaVariable.falsa_posicion(funcion, a, b, tolerancia, max_iteraciones)
            
        elif metodo == 'secante':
            x0 = datos.get('x0')
            x1 = datos.get('x1')
            if not all([x0 is not None, x1 is not None]):
                return jsonify({'error': 'Se requieren x0 y x1 para secante'}), 400
            try:
                x0 = float(x0)
                x1 = float(x1)
            except (ValueError, TypeError):
                return jsonify({'error': 'x0 y x1 deben ser números'}), 400
            
            raiz, detalles = EcuacionesUnaVariable.secante(funcion, x0, x1, tolerancia, max_iteraciones)
            
        elif metodo == 'newton_raphson':
            x0 = datos.get('x0')
            derivada = datos.get('derivada')
            if not all([x0 is not None, derivada]):
                return jsonify({'error': 'Se requieren x0 y derivada para Newton-Raphson'}), 400
            try:
                x0 = float(x0)
            except (ValueError, TypeError):
                return jsonify({'error': 'x0 debe ser un número'}), 400
            
            raiz, detalles = EcuacionesUnaVariable.newton_raphson(funcion, derivada, x0, tolerancia, max_iteraciones)
            
        elif metodo == 'punto_fijo':
            x0 = datos.get('x0')
            g = datos.get('g')
            if not all([x0 is not None, g]):
                return jsonify({'error': 'Se requieren x0 y g para punto fijo'}), 400
            try:
                x0 = float(x0)
            except (ValueError, TypeError):
                return jsonify({'error': 'x0 debe ser un número'}), 400
            
            raiz, detalles = EcuacionesUnaVariable.punto_fijo(g, x0, tolerancia, max_iteraciones)
            
        elif metodo == 'muller':
            x0 = datos.get('x0')
            x1 = datos.get('x1')
            x2 = datos.get('x2')
            if not all([x0 is not None, x1 is not None, x2 is not None]):
                return jsonify({'error': 'Se requieren x0, x1 y x2 para Müller'}), 400
            try:
                x0 = float(x0)
                x1 = float(x1)
                x2 = float(x2)
            except (ValueError, TypeError):
                return jsonify({'error': 'x0, x1 y x2 deben ser números'}), 400
            
            raiz, detalles = EcuacionesUnaVariable.muller(funcion, x0, x1, x2, tolerancia, max_iteraciones)
            
        else:
            return jsonify({'error': 'Método no válido'}), 400
        
        return jsonify({
            'raiz': raiz,
            'fx': detalles['fx'],
            'iteraciones': detalles['iteraciones'],
            'error_estimado': detalles['error_estimado'],
            'historial': detalles['historial'],
            'metodo': detalles['metodo']
        }), 200
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Error en el cálculo: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
