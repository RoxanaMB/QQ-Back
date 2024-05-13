from flask import jsonify, Blueprint
from server.db import supabase


# Crear blueprint
model = Blueprint('model', __name__)


# Ruta para obtener todos los modelos
@model.route('/models', methods=['GET'])
def get_models():
    models = supabase.table('models').select("*").execute()
    print(models)
    return jsonify(models.data)

