from flask import request, jsonify, Blueprint
from server.db import supabase

from models.fire_function_v1 import FireFunctionV1
from models.gemma_7b_instruct import Gemma7bIt
from models.llama2_13b_chat import Llama213bChat
from models.llama2_13b_code_instruct import Llama213bCodeInstruct
from models.llama2_70b_chat import Llama270bChat
from models.mistral_7b_instruct import Mistral7bInstruct
from models.mixtral_8x7b_instruct import Mixtral8x7bInstruct
from models.mythomax_l2_13b import MythomaxL213b
from models.chat_gpt import chat_gpt


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
        'content': data["content"][-1]["content"],
        'topic': data['topic'],
        'rate': data['rate'],
        'chat': data['chat'],
        'role': 'user',
        'name': data['name']
    }]).execute()

    # Mandar mensaje a la IA
    ia_model = Mistral7bInstruct()

    if data['ia_model'] == 'FireFunction v1':
        ia_model = FireFunctionV1()
    elif data['ia_model'] == 'Gemma 7B Instruct':
        ia_model = Gemma7bIt()
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
    response = ia_model.predict().get('choices')[0].get('message').get('content')

    chat_gpt_response = chat_gpt(data["content"][-1]["content"], response).content

    cal = 0
    tema = ""
    just = ""

    if "Calificación: " in chat_gpt_response:
        cal = chat_gpt_response.split("Calificación: ")[1].split("\n")[0]
    if "Tema: " in chat_gpt_response:
        tema = chat_gpt_response.split("Tema: ")[1].split("\n")[0]
    if "Justificación: " in chat_gpt_response:
        just = chat_gpt_response.split("Justificación: ")[1].split("\n")[0]

    # Añadir respuesta a la tabla messages de la base de datos
    if data['ia_model'] == "":
        data['ia_model'] = 'FireFunction v1'

    supabase.table('messages').insert([{
      'content': response,
      'chat': data['chat'],
      'model': data['ia_model'],
      'topic': tema,
      'rate': cal,
      'role': 'assistant',
      'just': just,
      'name': data['ia_model']
    }]).execute()

    # Actualizar calificación del modelo
    rate = get_model_messages(data['ia_model'])

    supabase.table('models').update({
        'rate': rate
    }).eq('name', data['ia_model']).execute()

    return jsonify({'message': 'Message created', 'response': response, 'cal': cal, 'tema': tema, 'just': just})


# Función para obtener las calificaciones de los mensajes de un modelo
def get_model_messages(model):
    messages = supabase.table('messages').select('*').eq('model', model).execute()

    # Recolectar calificaciones
    rates = []
    for message in messages.data:
        if message['rate'] != '':
            rates.append(int(message['rate']))

    # Calcular promedio
    if len(rates) == 0:
        return 0
    else:
        return sum(rates) / len(rates)

