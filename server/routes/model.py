from flask import request, jsonify, Blueprint
import os
from functools import wraps 
from server.db import supabase


# Crear blueprint
model = Blueprint('model', __name__)


# Ruta para obtener todos los modelos
@model.route('/models', methods=['GET'])
def get_models():
    models = supabase.table('models').select("*").execute()
    return jsonify(models.data)