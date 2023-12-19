import g4f
import os

from flask import Flask

app = Flask(__name__)

port = int(os.environ.get("PORT", 8080))

@app.route('/')
def home():
    # Using automatic a provider for the given model
    ## Streamed completion
    response = g4f.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hola, como estas?"}],
        stream=True,
    )
    sol = ""
    for message in response:
        sol += message
        print(message)
    return sol


@app.route('/about')
def about():
    return 'About'

if __name__ == "__main__":
    app.run(port=port)