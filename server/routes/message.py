from flask import request, jsonify, Blueprint
from functools import wraps 
from server.db import supabase
import json

from models.fire_function_v1 import FireFunctionV1
from models.gemma_7b_instruct import Gemma7bIt
from models.hermes2_pro_mistral_7b import Hermes2ProMistral7b
from models.llama2_13b_chat import Llama213bChat
from models.llama2_13b_code_instruct import Llama213bCodeInstruct
from models.llama2_70b_chat import Llama270bChat
from models.mistral_7b_instruct import Mistral7bInstruct
from models.mixtral_8x7b_instruct import Mixtral8x7bInstruct
from models.mythomax_l2_13b import MythomaxL213b


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
    ia_model = Mistral7bInstruct()

    if data['ia_model'] == 'FireFunction v1':
        ia_model = FireFunctionV1()
    elif data['ia_model'] == 'Gemma 7B Instruct':
        ia_model = Gemma7bIt()
    elif data['ia_model'] == 'Hermes 2 Pro Mistral 7B':
        ia_model = Hermes2ProMistral7b()
    elif data['ia_model'] == 'Llama2 13B Chat':
        ia_model = Llama213bChat()
    elif data['ia_model'] == 'Llama2 13B Code Instruct':
        ia_model = Llama213bCodeInstruct()
    elif data['ia_model'] == 'Llama2 70B Chat':
        ia_model = Llama270bChat()
    elif data['ia_model'] == 'Mistral 7B Instruct':
        ia_model = Mistral7bInstruct()
        print('Mistral 7B Instruct')
    elif data['ia_model'] == 'Mixtral 8x7B Instruct':
        ia_model = Mixtral8x7bInstruct()
    elif data['ia_model'] == 'MythoMax L2 13B':
        ia_model = MythomaxL213b()
    

    ia_model.payload['messages'] = data['content']

    print(ia_model)

    json_data = json.dumps(ia_model.predict())
    print(json_data)

    response = ia_model.predict().get('choices')[0].get('message').get('content')
    # response = ia_model.predict()

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

