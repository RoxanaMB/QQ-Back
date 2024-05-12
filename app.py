from flask import Flask
from flask_cors import CORS

from server.routes.user import user
from server.routes.message import message
from server.routes.model import model
from server.routes.chat import chat
from server.routes.conversation import conversation


app = Flask(__name__)
CORS(app, supports_credentials=True)

app.register_blueprint(user)
app.register_blueprint(message)
app.register_blueprint(model)
app.register_blueprint(chat)
app.register_blueprint(conversation)

if __name__ == '__main__':
    app.run()
