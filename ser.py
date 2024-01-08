import os
import g4f
import json

from flask import Flask, render_template, request

app = Flask(__name__)
conversations = []

port = int(os.environ.get("PORT", 5000))


@app.route('/', methods = ['POST', 'GET'])
def home():
    if request.method == 'GET':
        return render_template('ind.html')
    if request.form['question']:
        question = 'Yo: ' + request.form['question']

        response = g4f.ChatCompletion.create(
            model="gpt-3.5-turbo",
            provider=g4f.Provider.Aichat,
            messages=[
                {"role": "user", "content": request.form['question']}
            ],
            stream=True,
        )

        answer = 'AI: '
        for part in response:
            answer += part.format(json.dumps(part))

        conversations.append(question)
        conversations.append(answer)

        return render_template('ind.html', chat = conversations)
    else:
        return render_template('ind.html')


if __name__ == "__main__":
    app.run(port=port)
