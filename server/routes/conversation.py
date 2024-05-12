from flask import request, jsonify, Blueprint
import os
from functools import wraps 
from server.db import supabase


# Crear blueprint
conversation = Blueprint('conversation', __name__)


# Crear un conversation
@conversation.route('/conversation', methods=['POST'])
def create_conversation():
    # Obtener datos del conversation
    data = request.get_json()

    # Obtener los primeros 15 caracteres del título
    title = data['body']['message']

    if len(title) > 30:
        title = title[:30] + '...'
    else:
        title = title

    # Crear conversation
    res = supabase.table('conversations').insert([{
        'user': data['body']['user'],
        'chat_1': data['body']['chat_1'],
        'chat_2': data['body']['chat_2'],
        'title': title,
    }]).execute()

    return jsonify(res.data)


# Obtener todas las conversaciones de un usuario
@conversation.route('/conversations/<user>', methods=['GET'])
def get_conversations(user):
    # Obtener conversaciones
    conversations = supabase.table('conversations').select('*').eq('user', user).execute()
    return jsonify(conversations.data)


# Obtener una conversación
@conversation.route('/conversation/<id>', methods=['GET'])
def get_conversation(id):
    # Obtener conversación
    conversation = supabase.table('conversations').select('*').eq('id', id).execute()
    return jsonify(conversation.data)
