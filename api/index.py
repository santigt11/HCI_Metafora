"""
🚌 EL BUS DEL APRENDIZAJE EN PYTHON
Backend Flask - Toda la lógica en Python + Gemini AI para pistas
Para desplegar en Vercel
"""

import os
import sys
import json

from flask import Flask, jsonify, request, session
from flask_cors import CORS

# Importar google-generativeai solo cuando sea necesario (lazy loading)
def get_genai():
    import google.generativeai as genai
    return genai

app = Flask(__name__, static_folder='../public', static_url_path='')
app.secret_key = os.getenv('SECRET_KEY', 'bus-aprendizaje-python-2025')
CORS(app)

# ========== FUNCIONES PARA GEMINI ==========

def get_gemini_key():
    """Lee la clave API desde variable de entorno o archivo gemini.key"""
    # Primero intenta desde variable de entorno (Vercel)
    api_key = os.getenv('GEMINI_API_KEY')
    if api_key:
        return api_key
    
    # Si no está en variables de entorno, intenta archivo local
    try:
        with open("gemini.key", "r") as f:
            return f.read().strip()
    except Exception as e:
        print(f"⚠️  No se encontró gemini.key: {e}")
        return None


def consulta_gemini(pregunta):
    """Realiza una consulta a Gemini API"""
    api_key = get_gemini_key()
    if not api_key:
        return None
    
    try:
        genai = get_genai()
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        response = model.generate_content(pregunta)
        return response.text.strip() if response else None
    except Exception as e:
        print(f"Error Gemini: {e}")
        return None


# ========== CONSTANTES ==========
TOTAL_STOPS = 7
TOTAL_TIRES = 4

# ========== DATOS DEL JUEGO ==========
STOPS_DATA = [
    {
        'id': 'variables',
        'title': 'Variables',
        'description': 'Aprende a declarar y usar variables para almacenar datos.',
        'tip': 'Las variables son contenedores de información que puedes usar y modificar.',
        'exercises': [
            {
                'id': 'var-1',
                'type': 'input',
                'question': 'Si tienes:\nnombre = "Python"\nedad = 30\n\n¿Cuál es el resultado de: nombre + " es " + str(edad)?',
                'expectedAnswer': 'Python es 30',
                'feedback': {
                    'correct': '¡Correcto! La concatenación combina strings.',
                    'incorrect': 'Revisa cómo concatenar strings en Python.'
                }
            }
        ],
        'completed': False
    },
    {
        'id': 'condicionales',
        'title': 'Condicionales',
        'description': 'Usa if, elif, else para tomar decisiones en tu código.',
        'tip': 'Los condicionales permiten que tu programa tome diferentes caminos.',
        'exercises': [
            {
                'id': 'cond-1',
                'type': 'multiple-choice',
                'question': 'Si x = 5, ¿qué imprime este código?\n\nif x > 3:\n    print("Mayor")\nelse:\n    print("Menor")',
                'expectedAnswer': 'Mayor',
                'options': ['Mayor', 'Menor', 'Nada', 'Error'],
                'feedback': {
                    'correct': '¡Exacto! 5 es mayor que 3.',
                    'incorrect': 'Revisa la evaluación de la condición.'
                }
            }
        ],
        'completed': False
    },
    {
        'id': 'bucles_for',
        'title': 'Bucles (for)',
        'description': 'Domina los bucles for para iterar sobre secuencias.',
        'tip': 'El bucle for te permite repetir código un número específico de veces.',
        'exercises': [
            {
                'id': 'for-1',
                'type': 'input',
                'question': 'Completa la salida del código:\n\nfor i in range(3):\n    print(i)\n\n(Escribe los números separados por comas y espacios)',
                'expectedAnswer': '0, 1, 2',
                'feedback': {
                    'correct': '¡Bien! Comprendiste range().',
                    'incorrect': 'range(n) empieza en 0 y termina en n-1.'
                }
            }
        ],
        'completed': False
    },
    {
        'id': 'bucles_while',
        'title': 'Bucles (while)',
        'description': 'Aprende bucles while para condiciones complejas.',
        'tip': 'El bucle while repite mientras una condición sea verdadera.',
        'exercises': [
            {
                'id': 'while-1',
                'type': 'multiple-choice',
                'question': '¿Cuántas veces imprime este código "Hola"?\n\nx = 0\nwhile x < 3:\n    print("Hola")\n    x += 1',
                'expectedAnswer': '3',
                'options': ['1', '2', '3', 'Infinitas'],
                'feedback': {
                    'correct': '¡Correcto! Se imprime 3 veces.',
                    'incorrect': 'Cuenta cuántas veces se ejecuta el bloque.'
                }
            }
        ],
        'completed': False
    },
    {
        'id': 'funciones',
        'title': 'Funciones',
        'description': 'Crea y usa funciones para organizar tu código.',
        'tip': 'Las funciones agrupan código reutilizable en bloques.',
        'exercises': [
            {
                'id': 'func-1',
                'type': 'input',
                'question': 'Si defines:\n\ndef saludar(nombre):\n    return "Hola, " + nombre\n\n¿Cuál es el resultado de saludar("Python")?',
                'expectedAnswer': 'Hola, Python',
                'feedback': {
                    'correct': '¡Perfecto! Las funciones retornan valores.',
                    'incorrect': 'Revisa cómo retornar valores en funciones.'
                }
            }
        ],
        'completed': False
    },
    {
        'id': 'estructuras',
        'title': 'Estructuras',
        'description': 'Trabaja con listas, tuplas y diccionarios.',
        'tip': 'Las estructuras de datos te permiten organizar múltiples valores.',
        'exercises': [
            {
                'id': 'struct-1',
                'type': 'input',
                'question': 'Si tienes: lista = [10, 20, 30]\n\n¿Cuál es el resultado de lista[1] + 5?',
                'expectedAnswer': '25',
                'feedback': {
                    'correct': '¡Bien! Dominas el indexing de listas.',
                    'incorrect': 'Los índices comienzan en 0.'
                }
            }
        ],
        'completed': False
    },
    {
        'id': 'proyecto_final',
        'title': 'Final',
        'description': 'Integra todo lo aprendido en un proyecto.',
        'tip': 'Combina variables, condicionales, bucles y funciones.',
        'exercises': [
            {
                'id': 'final-1',
                'type': 'multiple-choice',
                'question': '¿Cuál es la forma correcta de imprimir números pares del 0 al 10?',
                'expectedAnswer': 'for i in range(0, 11, 2): print(i)',
                'options': [
                    'for i in range(0, 11, 2): print(i)',
                    'for i in range(1, 10): print(i)',
                    'while i <= 10: print(i)',
                    'if i % 2 == 0: print(i)'
                ],
                'feedback': {
                    'correct': '¡Felicidades! ¡Has completado todas las paradas!',
                    'incorrect': 'Repasa la sintaxis de range().'
                }
            }
        ],
        'completed': False
    }
]

# Ejercicio de refuerzo
REFUERZO_EXERCISE = {
    'id': 'refuerzo-1',
    'type': 'multiple-choice',
    'question': '¿Cuál NO es un tipo de dato básico en Python?',
    'expectedAnswer': 'ventana',
    'options': ['int', 'string', 'ventana', 'float'],
    'feedback': {
        'correct': '¡Bien! Has reparado el bus. Puedes continuar.',
        'incorrect': 'Los tipos básicos son int, string, float, bool, etc.'
    }
}


# ========== FUNCIONES AUXILIARES ==========

def init_game_state():
    """Inicializa el estado del juego"""
    return {
        'currentStopIndex': 0,
        'tires': TOTAL_TIRES,
        'progress': 0,
        'inRefuerzo': False,
        'failedAttempts': 0,
        'refuerzoAttempts': 0,
        'stops': json.loads(json.dumps(STOPS_DATA))
    }


def get_ai_hint(question, expected_answer, user_answer, topic):
    """
    Genera una pista inteligente con Gemini cuando el usuario falla
    """
    prompt = f"""Eres un profesor de Python amable y didáctico.

El estudiante está aprendiendo sobre: {topic}

Pregunta: {question}

Respuesta correcta: {expected_answer}

Respuesta del estudiante: {user_answer}

Proporciona una pista BREVE (máximo 2 líneas) que ayude al estudiante a entender por qué su respuesta es incorrecta.
No reveles la respuesta correcta. Se amable y motivador. Responde solo la pista, en español."""

    return consulta_gemini(prompt)


def validate_answer(exercise, user_answer):
    """Valida la respuesta del usuario (case-insensitive)"""
    return user_answer.strip().lower() == exercise['expectedAnswer'].strip().lower()


# ========== RUTAS ==========

@app.route('/api/init-game', methods=['POST'])
def init_game():
    """Inicializa o reinicia el juego"""
    session['gameState'] = init_game_state()
    return jsonify({
        'success': True,
        'gameState': session.get('gameState')
    })


@app.route('/api/game-state', methods=['GET'])
def get_game_state():
    """Obtiene el estado actual del juego"""
    if 'gameState' not in session:
        session['gameState'] = init_game_state()
    
    return jsonify({
        'success': True,
        'gameState': session['gameState']
    })


@app.route('/api/current-stop', methods=['GET'])
def get_current_stop():
    """Obtiene información de la parada actual"""
    if 'gameState' not in session:
        session['gameState'] = init_game_state()
    
    game_state = session['gameState']
    current_idx = game_state['currentStopIndex']
    
    if current_idx >= len(game_state['stops']):
        return jsonify({
            'success': False,
            'message': 'Juego completado'
        }), 400
    
    stop = game_state['stops'][current_idx]
    exercise = stop['exercises'][0] if stop['exercises'] else None
    
    return jsonify({
        'success': True,
        'stop': stop,
        'exercise': exercise,
        'currentIndex': current_idx,
        'totalStops': len(game_state['stops'])
    })


@app.route('/api/submit-answer', methods=['POST'])
def submit_answer():
    """
    Valida la respuesta del usuario
    Esperado: {answer: string}
    """
    if 'gameState' not in session:
        session['gameState'] = init_game_state()
    
    data = request.json
    user_answer = data.get('answer', '').strip()
    
    if not user_answer:
        return jsonify({
            'success': False,
            'error': 'Respuesta vacía'
        }), 400
    
    game_state = session['gameState']
    current_idx = game_state['currentStopIndex']
    
    if current_idx >= len(game_state['stops']):
        return jsonify({
            'success': False,
            'error': 'Juego completado'
        }), 400
    
    stop = game_state['stops'][current_idx]
    exercise = stop['exercises'][0]
    
    # Validar respuesta
    is_correct = validate_answer(exercise, user_answer)
    
    if is_correct:
        # ✅ Respuesta correcta
        stop['completed'] = True
        game_state['failedAttempts'] = 0
        
        # Calcular progreso
        completed_count = sum(1 for s in game_state['stops'] if s['completed'])
        game_state['progress'] = int((completed_count / len(game_state['stops'])) * 100)
        
        # Avanzar a siguiente parada o victoria
        if current_idx < len(game_state['stops']) - 1:
            game_state['currentStopIndex'] += 1
        
        session.modified = True
        
        return jsonify({
            'success': True,
            'isCorrect': True,
            'feedback': exercise['feedback']['correct'],
            'gameState': game_state
        })
    else:
        # ❌ Respuesta incorrecta
        game_state['failedAttempts'] += 1
        game_state['tires'] -= 1
        
        response_data = {
            'success': True,
            'isCorrect': False,
            'feedback': exercise['feedback']['incorrect'],
            'tiresRemaining': game_state['tires']
        }
        
        # Obtener pista de IA
        ai_hint = get_ai_hint(
            exercise['question'],
            exercise['expectedAnswer'],
            user_answer,
            stop['title']
        )
        
        if ai_hint:
            response_data['aiHint'] = ai_hint
        
        # Si pierden todas las llantas
        if game_state['tires'] <= 0:
            game_state['tires'] = 0
            game_state['inRefuerzo'] = True
            response_data['inRefuerzo'] = True
            response_data['message'] = '🚨 ¡Todas las llantas pinchadas! Debes completar el refuerzo.'
        
        session.modified = True
        return jsonify(response_data)


@app.route('/api/refuerzo-exercise', methods=['GET'])
def get_refuerzo_exercise():
    """Obtiene el ejercicio de refuerzo"""
    return jsonify({
        'success': True,
        'exercise': REFUERZO_EXERCISE
    })


@app.route('/api/submit-refuerzo', methods=['POST'])
def submit_refuerzo():
    """Valida respuesta del refuerzo"""
    if 'gameState' not in session:
        return jsonify({'success': False, 'error': 'Sin sesión'}), 400
    
    data = request.json
    user_answer = data.get('answer', '').strip()
    
    if not user_answer:
        return jsonify({'success': False, 'error': 'Respuesta vacía'}), 400
    
    game_state = session['gameState']
    is_correct = validate_answer(REFUERZO_EXERCISE, user_answer)
    
    if is_correct:
        game_state['tires'] = TOTAL_TIRES
        game_state['inRefuerzo'] = False
        game_state['refuerzoAttempts'] += 1
        session.modified = True
        
        return jsonify({
            'success': True,
            'isCorrect': True,
            'feedback': REFUERZO_EXERCISE['feedback']['correct'],
            'gameState': game_state
        })
    else:
        # Pista de IA para refuerzo
        ai_hint = get_ai_hint(
            REFUERZO_EXERCISE['question'],
            REFUERZO_EXERCISE['expectedAnswer'],
            user_answer,
            'Modo Refuerzo'
        )
        
        response_data = {
            'success': True,
            'isCorrect': False,
            'feedback': REFUERZO_EXERCISE['feedback']['incorrect']
        }
        
        if ai_hint:
            response_data['aiHint'] = ai_hint
        
        return jsonify(response_data)


@app.route('/api/reset-game', methods=['POST'])
def reset_game():
    """Reinicia el juego completamente"""
    session['gameState'] = init_game_state()
    session.modified = True
    
    return jsonify({
        'success': True,
        'message': 'Juego reiniciado',
        'gameState': session['gameState']
    })


@app.route('/api/health', methods=['GET'])
def health():
    """Verifica que el servidor está activo"""
    gemini_key = get_gemini_key()
    return jsonify({
        'success': True,
        'status': 'online',
        'aiEnabled': gemini_key is not None
    })
