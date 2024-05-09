from openai import OpenAI
client = OpenAI()

def chat_gpt(message):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": '''Quiero que me ayudes a calificar la siguiente frase siguiendo el siguiente formato:
             Calificación: 1-10
             Tema: [Tema de la oración]
             Justificación: [Justificación de la calificación muy breve]
             ''' + message}
        ]
    )
    return completion.choices[0].message
