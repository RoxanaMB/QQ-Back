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


# Cambiar título de un chat 
@chat.route('/chat/<int:id>', methods=['PUT'])
def update_chat(id):
    # Obtener datos del chat
    data = request.get_json()

    # Actualizar chat
    res = supabase.table('chats').update({
        "title": data['title'],
    }).eq('id', id).execute()
    return jsonify(res.data)


# Cambiar modelo de un chat
@chat.route('/chat/<int:id>', methods=['PUT'])
def update_chat_model(id):
    # Obtener datos del chat
    data = request.get_json()

    # Actualizar chat
    res = supabase.table('chats').update({
        "model": data['model'],
    }).eq('id', id).execute()
    return jsonify(res.data)
