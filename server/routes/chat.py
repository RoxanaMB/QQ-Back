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


# Obtener mensajes de un chat según su id
@chat.route('/chat/<id>/messages', methods=['GET'])
def get_chat_messages(id):
    # Obtener mensajes
    messages = supabase.table('messages').select('*').eq('chat', id).execute()

    # Ordenar mensajes por fecha
    messages.data.sort(key=lambda x: x['created_at'])
            
    return jsonify(messages.data)
