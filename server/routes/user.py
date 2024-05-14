from flask import request, jsonify, Blueprint
from werkzeug.security import generate_password_hash
from functools import wraps 
from server.db import supabase


# Crear blueprint
user = Blueprint('user', __name__)



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
            # Verificar token con supabase
            data = supabase.auth.get_user(token)
            # Obtener usuario
            current_user = data.user
        except Exception as e:
            return jsonify({'message': 'Token is invalid'}), 401

        # Retornar funcion
        return f(current_user, *args, **kwargs)

    return decorated



# Crear ruta para registrar usuario
@user.route('/register', methods=['POST'])
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
@user.route('/login', methods=['POST'])
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
    return jsonify({'token': token, 'user_name': res.user.user_metadata['username'], 'user_id': res.user.id, 'email': res.user.email})



# Crear ruta para obtener todos los usuarios
@user.route('/users', methods=['GET'])
@token_required
def get_all_users(current_user):
    # Obtener usuarios
    users = supabase.table('users').select().execute().get('data')

    # Retornar usuarios
    return jsonify(users)



# Crear ruta para obtener un usuario
@user.route('/user', methods=['GET'])
@token_required
def get_one_user(current_user):

    # Retornar usuario
    return jsonify({'user_name': current_user.user_metadata['username'], 'user_id': current_user.id, 'email': current_user.email})



# Crear ruta para eliminar un usuario
@user.route('/users/<id>', methods=['DELETE'])
@token_required
def delete_user(current_user, id):
    # Eliminar usuario
    supabase.table('users').delete().eq('id', id).execute()

    # Retornar mensaje
    return jsonify({'message': 'User has been deleted'})



# Crear ruta para actualizar un usuario
@user.route('/users/<id>', methods=['PUT'])
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