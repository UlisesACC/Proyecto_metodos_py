from flask import Flask, render_template, request, jsonify
import numpy as np
from metodos.metodos import DiferenciasFinitas, Derivacion

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
        if metodo == '2_atras':
            derivadas, detalles = Derivacion.dos_puntos_atras(nodos_x, nodos_y, paso)
        elif metodo == '2_centrada':
            derivadas, detalles = Derivacion.dos_puntos_centrada(nodos_x, nodos_y, paso)
        elif metodo == '3_atras':
            derivadas, detalles = Derivacion.tres_puntos_atras(nodos_x, nodos_y, paso)
        elif metodo == '3_centrada':
            derivadas, detalles = Derivacion.tres_puntos_centrada(nodos_x, nodos_y, paso)
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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
