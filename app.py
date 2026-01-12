from flask import Flask, render_template, request, jsonify
import numpy as np
from metodos.metodos import DiferenciasFinitas, Derivacion, Integracion, SistemasLineales, EcuacionesDiferenciales

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

@app.route('/api/health', methods=['GET'])
def health():
    """Endpoint de verificación de salud"""
    return jsonify({'status': 'ok', 'message': 'App de Métodos Numéricos funcionando'})

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
    """API para resolver ecuaciones diferenciales"""
    try:
        datos = request.get_json()
        
        if not datos:
            return jsonify({'error': 'No se recibieron datos'}), 400
        
        metodo = datos.get('metodo')
        x0 = datos.get('x0')
        y0 = datos.get('y0')
        xf = datos.get('xf')
        n = datos.get('n')
        f_expr = datos.get('f_expr')
        
        if not all([metodo, x0 is not None, y0 is not None, xf is not None, n, f_expr]):
            return jsonify({'error': 'Faltan campos requeridos'}), 400
        
        try:
            x0 = float(x0)
            y0 = float(y0)
            xf = float(xf)
            n = int(n)
        except (ValueError, TypeError):
            return jsonify({'error': 'Datos inválidos'}), 400
        
        if metodo == 'euler':
            x_vals, y_vals, detalles = EcuacionesDiferenciales.euler(x0, y0, xf, n, f_expr)
        elif metodo == 'taylor_2':
            df_expr = datos.get('df_expr')
            if not df_expr:
                return jsonify({'error': 'Se requiere df_expr para Taylor orden 2'}), 400
            x_vals, y_vals, detalles = EcuacionesDiferenciales.taylor_orden_2(x0, y0, xf, n, f_expr, df_expr)
        elif metodo == 'taylor_3':
            df_expr = datos.get('df_expr')
            ddf_expr = datos.get('ddf_expr')
            if not all([df_expr, ddf_expr]):
                return jsonify({'error': 'Se requieren derivadas para Taylor orden 3'}), 400
            x_vals, y_vals, detalles = EcuacionesDiferenciales.taylor_orden_3(x0, y0, xf, n, f_expr, df_expr, ddf_expr)
        elif metodo == 'taylor_4':
            df_expr = datos.get('df_expr')
            ddf_expr = datos.get('ddf_expr')
            dddf_expr = datos.get('dddf_expr')
            if not all([df_expr, ddf_expr, dddf_expr]):
                return jsonify({'error': 'Se requieren derivadas para Taylor orden 4'}), 400
            x_vals, y_vals, detalles = EcuacionesDiferenciales.taylor_orden_4(x0, y0, xf, n, f_expr, df_expr, ddf_expr, dddf_expr)
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
            'y_valores': y_vals,
            'detalles': detalles,
            'pares': list(zip(x_vals, y_vals))
        }), 200
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Error en el cálculo: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
