import json
import g4f
import os

from flask import Flask, stream_with_context

app = Flask(__name__)

port = int(os.environ.get("PORT", 8080))


@app.route("/")
def home():
    response = g4f.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "Que pasó en la primera querra mundial?"}
        ],
        stream=True,
    )

    def generate():
        for part in response:
            yield part.format(json.dumps(part))

    return app.response_class(stream_with_context(generate()))


if __name__ == "__main__":
    app.run(port=port)
