import os
import g4f
import json

from flask import Flask, render_template, request

app = Flask(__name__)
conversations = []

port = int(os.environ.get("PORT", 5000))


@app.route('/', methods = ['POST', 'GET'])
def home():
    # Print all available providers
    print([
        provider.__name__
        for provider in g4f.Provider.__providers__
        if provider.working
    ])

    # Providers que funcionan:
    #   - You
    #   - AiChatOnline
    #   - ChatBase (LENTO)
    #   - ChatgptAi (LENTITO)
    #   - ChatgptNext
    #   - DeepInfra (MUY LENTO)
    #   - GptGo (RÁPIDO)
    #   - Koala
    #   - Llama2 (g4f.models.llama2_70b)
    #   - OnlineGpt

    if request.method == 'GET':
        return render_template('ind.html')
    if request.form['question']:
        question = 'Yo: ' + request.form['question']

        response = g4f.ChatCompletion.create(
            model=g4f.models.llama2_70b,
            provider=g4f.Provider.DeepInfra,
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
