from flask import request, jsonify, Blueprint
import os
from functools import wraps 
from server.db import supabase


# Crear blueprint
chat = Blueprint('chat', __name__)


# Crear un chat
@chat.route('/chat', methods=['POST'])
def create_chat():
    # Obtener datos del chat
    data = request.get_json()

    # Crear chat
    res = supabase.table('chats').insert([{
        'user': data['body'],
    }]).execute()
    return jsonify(res.data)


# # Cambiar modelo de un chat
# @chat.route('/chat/<int:id>', methods=['PUT'])
# def update_chat_model(id):
#     # Obtener datos del chat
#     data = request.get_json()

#     # Actualizar chat
#     res = supabase.table('chats').update({
#         "model": data['model'],
#     }).eq('id', id).execute()
#     return jsonify(res.data)

# return this.http.get(`http://127.0.0.1:5000/chat/${chat_id}/messages`);

# Obtener mensajes de un chat según su id
@chat.route('/chat/<id>/messages', methods=['GET'])
def get_chat_messages(id):
    # Obtener mensajes
    messages = supabase.table('messages').select('*').eq('chat', id).execute()

    ## Añadir role = user si model == NULL o role = assistant si model != NULL
    for message in messages.data:
        if message['model'] == None:
            message['role'] = 'user'
        else:
            message['role'] = 'assistant'
            
    return jsonify(messages.data)
