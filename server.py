import json
import g4f
import os

from flask import Flask, Response, stream_with_context
# from flask_socketio import SocketIO

app = Flask(__name__)
# socketio = SocketIO(app)

port = int(os.environ.get("PORT", 8080))

@app.route('/')
def home():
    # question = request.json['question']
    # time.sleep(5)


    response = g4f.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Que pasó en la primera querra mundial?"}],
        stream=True,
    )
    # sol = ""
    # for message in response:
    #     sol += message
    #     print(message)
        
    def generate():
        sol = ""
        for part in response:
            sol += part
            print(part)
            yield part.format(json.dumps(part))

    # return Response(generate(), mimetype='text/event-stream')
    return app.response_class(stream_with_context(generate()))
        
    # return sol


@app.route('/about')
def about():
    return 'About'

if __name__ == "__main__":
    app.run(port=port)