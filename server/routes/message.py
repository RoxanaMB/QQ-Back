from flask import request, jsonify, Blueprint
from functools import wraps 
from server.db import supabase

from models.mistral_7b_instruct import Mistral7bInstruct


# Crear blueprint
message = Blueprint('message', __name__)


# Ruta para obtener todos los mensajes
@message.route('/messages', methods=['GET'])
def get_messages():
    messages = supabase.get_messages()
    return jsonify(messages)



# Ruta para crear un mensaje
@message.route('/message', methods=['POST'])
def create_message():
    data = request.get_json()

    # Añadir mensaje a la tabla messages de la base de datos
    supabase.table('messages').insert([{
      'content': data['content'],
      'topic': data['topic'],
      'rate': data['rate'],
    }]).execute()

    # Mandar mensaje a la IA
    mistral = Mistral7bInstruct()
    mistral.payload['messages'] = [{
        "role": "user",
        "content": data['content']
    }]

    # TODO: dependiendo del data['ia_model'] se selecciona el modelo de IA
    response = mistral.predict().get('choices')[0].get('message').get('content')

    # Añadir respuesta a la tabla messages de la base de datos
    supabase.table('messages').insert([{
      'content': response,
    }]).execute()

    return jsonify({'message': 'Message created', 'response': response})



# # Ruta para obtener un mensaje
# @message.route('/message/<int:id>', methods=['GET'])
# @login_required
# def get_message(id):
#     message = supabase.get_message(id)
#     return jsonify(message)



# # Ruta para obtener los mensajes de un usuario
# @message.route('/user/messages', methods=['GET'])
# @login_required
# def get_user_messages():
#     messages = supabase.get_user_messages()
#     return jsonify(messages)

