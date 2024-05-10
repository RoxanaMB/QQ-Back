from openai import OpenAI
client = OpenAI()

def chat_gpt(quest, message):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": '''Quiero que me ayudes a calificar la siguiente respuesta siguiendo el siguiente formato:
             Calificación: 1-10
             Tema: [SÓLO uno de estos: Historia, Politica, Arte, Ciencia, Tecnología, Cultura, Deporte, Viajes, Gastronomía, Otros]
             Justificación: [Indicar que le faltaría a la respuesta para mejorarla, o qué le sobra, o qué le cambiarías, etc. sin tener en cuenta el tema]
             IMPORTANTE: Siempre quiero que me des una calificación, un tema y una justificación. Gracias!
             ''' + 'Pregunta:' + quest + 'Respuesta:' + message}
        ]
    )
    return completion.choices[0].message
