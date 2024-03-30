from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import os
import jwt
import datetime
from functools import wraps 
from server.db import supabase
from flask_cors import CORS

# Inicializar app
app = Flask(__name__)
CORS(app)

# Configurar app
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SUPABASE_URL'] = os.environ.get('SUPABASE_URL')

# Crear rutas para un login y un registro de usuarios
# Crear decorador para verificar token
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Verificar si el token esta en el header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        # Si no esta el token
        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            # Verificar token
            data = jwt.decode(token, app.config['SECRET_KEY'])
            # Obtener usuario
            current_user = supabase.table('users').select().eq('id', data['id']).execute().get('data')[0]
        except:
            return jsonify({'message': 'Token is invalid'}), 401

        # Retornar funcion
        return f(current_user, *args, **kwargs)

    return decorated

# Crear ruta para registrar usuario
@app.route('/register', methods=['POST'])
def register():
    # Obtener datos del usuario
    data = request.get_json()

    # Obtener usuario
    res = supabase.auth.sign_up({
      "email": data['email'], 
      "password": data['password'],
      "options": {
        "data": {
          "username": data['username']
        }
      }
    })

    # Crear token
    token = res.session.access_token

    # Retornar token
    return jsonify({'token': token})

# Crear ruta para hacer login
@app.route('/login', methods=['POST'])
def login():
    # Obtener datos del usuario
    data = request.get_json()

    # Obtener usuario
    res = supabase.auth.sign_in_with_password({"email": data['email'], "password": data['password']})
    
    # Si no existe el usuario
    if not res:
        return jsonify({'message': 'User does not exist'}), 401

    # Crear token
    token = res.session.access_token

    # Retornar token
    return jsonify({'token': token})

# Crear ruta para obtener todos los usuarios
@app.route('/users', methods=['GET'])
@token_required
def get_all_users(current_user):
    # Obtener usuarios
    users = supabase.table('users').select().execute().get('data')

    # Retornar usuarios
    return jsonify(users)

# Crear ruta para obtener un usuario
@app.route('/users/<id>', methods=['GET'])
@token_required
def get_one_user(current_user, id):
    # Obtener usuario
    user = supabase.table('users').select().eq('id', id).execute().get('data')[0]

    # Retornar usuario
    return jsonify(user)

# Crear ruta para eliminar un usuario
@app.route('/users/<id>', methods=['DELETE'])
@token_required
def delete_user(current_user, id):
    # Eliminar usuario
    supabase.table('users').delete().eq('id', id).execute()

    # Retornar mensaje
    return jsonify({'message': 'User has been deleted'})

# Crear ruta para actualizar un usuario
@app.route('/users/<id>', methods=['PUT'])
@token_required
def update_user(current_user, id):
    # Obtener datos del usuario
    data = request.get_json()

    # Actualizar usuario
    supabase.table('users').update({
        'username': data['username'],
        'password': generate_password_hash(data['password'], method='sha256')
    }).eq('id', id).execute()

    # Retornar mensaje
    return jsonify({'message': 'User has been updated'})


