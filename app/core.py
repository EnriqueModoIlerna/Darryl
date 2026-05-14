# Posible remplazo de Chatbot o migrar codigo
from app.memory import Memory
from app.nlp import procesar_texto
from app.generator import Generator
from app.personality import Personality

class ChatbotCore:
    def __init__(self):
        self.memory = Memory()
        self.generator = Generator()
        self.personality = Personality()

    def responder(self, mensaje):
        # 1. procesar texto
        texto = procesar_texto(mensaje)

        # 2. recuperar contexto
        contexto = self.memory.recuperar(texto)

        # 3. generar respuesta base
        respuesta = self.generator.generar_respuesta(texto, contexto)

        # 4. aplicar personalidad
        respuesta_final = self.personality.aplicar(respuesta)

        # 5. guardar memoria
        self.memory.guardar(mensaje, respuesta_final)

        return respuesta_final