# El cerebro de la IA, procesa el mensaje y devuelve una respuesta
import requests


class AIEngine:

    def generar_respuesta(self, messages):
        # Enlace hacia el chatbot al correr el programa, recibe las peticiones y se las manda al bot
        response = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": "phi3",
                "messages": messages,
                "stream": False,
                "options": {
                    "temperature": 0.1,
                    "num_predict": 120
                }
            }
        )

        data = response.json()

        return data["message"]["content"]