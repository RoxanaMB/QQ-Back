from flask import Flask
from flask_cors import CORS

from server.routes.user import user
from server.routes.message import message


app = Flask(__name__)
CORS(app, supports_credentials=True)

app.register_blueprint(user)
app.register_blueprint(message)

if __name__ == '__main__':
    app.run()
