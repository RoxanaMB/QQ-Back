import requests
import json
import os

class Llama213bCode:
    def __init__(self):
        self.url = "https://api.fireworks.ai/inference/v1/chat/completions"
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer " + os.getenv('FIREWORKS_API_KEY')
        }
        self.payload = {
            "model": "accounts/fireworks/models/llama-v2-13b-code",
            "max_tokens": 512,
            "top_p": 1,
            "top_k": 40,
            "presence_penalty": 0,
            "frequency_penalty": 0,
            "temperature": 0.6,
            "messages": []
        }

    def predict(self):
        response = requests.request("POST", self.url, headers=self.headers, data=json.dumps(self.payload))
        return response.json()
