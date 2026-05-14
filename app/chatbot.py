from app.memory import Memory
from app.personality import Personality
from app.ai_engine import AIEngine
from app.nlp import procesar_texto
import datetime
import random


class Chatbot:

    def __init__(self):
        self.memory = Memory()
        self.personality = Personality()
        self.ai = AIEngine()

        # Usuario activo
        self.usuario_actual = None
        
    # Funcion para detectar gustos
    def detectar_gustos(self, texto):

        texto = texto.lower().strip()

        # Evitar preguntas como gustos del usuario
        if "?" in texto:
            return

        # Detectar gustos reales
        if texto.startswith("me gusta "):

            gusto = texto.replace("me gusta ", "").strip()

            # limpieza
            basura = ["también", "tambien", ".", ",", "!"]

            for b in basura:
                gusto = gusto.replace(b, "")

            gusto = gusto.strip()

            # evitar basura
            if len(gusto) < 3:
                return

            self.memory.guardar_gusto(
                self.usuario_actual,
                gusto
            )
            
        # Modos de chat: SOLO SI O NO
        if any(p in texto for p in [
            "solo si o no",
            "solo con si o no",
            "solo con si o con no"
        ]):
            self.memory.guardar_preferencia(
                self.usuario_actual,
                "modo_respuesta",
                "si_no"
            )

        # CHAT NORMAL
        if any(p in texto for p in [
            "responde normal",
            "Responde normal",
            "responder normal",
            "vuelve a la normalidad",
            "Vuelve a la normalidad",
            "Puedes volver a la normalidad",
            "puedes volver a la normalidad"
        ]):
            self.memory.guardar_preferencia(
                self.usuario_actual,
                "modo_respuesta",
                "normal"
            )
    
    # Esto es para que el Chatbot no se quede pillado y se pueda manejar mas libremente, aunque suponga una capa mas
    # Pero utiliza datos locales sin necesidad de tener que procesar datos nuevos por el modelo IA
    def detectar_intencion(self, texto):

        texto = texto.lower()

         # saludos
        saludos = ["hola", "buenas", "hey"]
        if any(p in texto for p in saludos):
            return "saludo"

        # hora
        if "que hora" in texto or "qué hora" in texto:
            return "hora"

        # gustos del bot
        if any(p in texto for p in [
            "que te gusta",
            "qué te gusta",
            "cuales son tus gustos",
            "cuáles son tus gustos",
            "tus gustos",
            "a ti que te gusta",
            "te gusta a ti"
        ]):
            return "gustos_bot"

        # gustos del usuario
        if any(p in texto for p in [
            "que me gusta",
            "qué me gusta",
            "mis gustos"
        ]):
            return "gustos_usuario"

        # pregunta general
        if "?" in texto:
            return "pregunta"

        return "normal"

    # Funcion para responder
    def responder(self, mensaje):

        texto = procesar_texto(mensaje)
        
        # Limpieza
        texto = texto.lower()
        texto = texto.replace("¿", "")
        texto = texto.replace("?", "")

        # =========================
        # 1. IDENTIFICACIÓN USUARIO
        # =========================

        if self.usuario_actual is None:
            nombre = texto.lower().strip()

            if not self.memory.existe_usuario(nombre):
                self.memory.crear_usuario(nombre)

            self.usuario_actual = nombre

            respuesta = f"Encantado {nombre}, ya puedo recordarte!!."
        
            # return self.personality.aplicar(respuesta, tipo="positivo")
            return self.personality.aplicar(
                respuesta,
                tipo="saludo"
            )

         # =========================
        # 2. RECUPERAR CONTEXTO
        # =========================
        historial = self.memory.recuperar_historial(self.usuario_actual)
        gustos = self.memory.recuperar_gustos(self.usuario_actual)
        
        # Poder modificar el modo en el que responde el chatbot
        modo_respuesta = self.memory.recuperar_preferencia(
            self.usuario_actual,
            "modo_respuesta"
        )

        # Acceso al hstorial de mensajes
        ultimos_mensajes = historial[-2:]

        # Acceso al contexto antiguo
        # contexto = "\n".join(
        #     f"Usuario: {m['user']}\nAsistente: {m['bot']}"
        #     for m in ultimos_mensajes
        # )

        # =========================
        # 3. INTENCIÓN DEL TEXTO
        # =========================
        intencion = self.detectar_intencion(texto)

        # =========================
        # 4. GENERAR RESPUESTA
        # =========================
        # Aqui detectamos el texto del mensaje, el historial, 
        # los dustos del usuario, la intencion del usuario y el tipo de respuesta a utilizar
        respuesta = self.generar_respuesta(
            texto,
            ultimos_mensajes,
            gustos,
            intencion,
            modo_respuesta
        )

        # =========================
        # 5. PERSONALIDAD
        # =========================
        # Almaceno la frase generada aqui, porque el modelo luego lo mexclaba con las coletillas y se volvia loco
        respuesta_base = respuesta
        
        if modo_respuesta == "si_no":
            respuesta_final = respuesta_base.strip()
        else:
            respuesta_final = self.personality.aplicar(
                respuesta_base,
                tipo=intencion
            )

        # =========================
        # 6. APRENDIZAJE
        # =========================
        self.detectar_gustos(texto)

        # =========================
        # 7. GUARDAR MEMORIA
        # =========================
        # Y guardo en el documento la version del texto generado SIN la muletilla
        self.memory.guardar_conversacion(
            self.usuario_actual,
            mensaje,
            respuesta_base
        )

        # Pero lo muestro por pantalla con ella, esto hace que el modelo no se ralle
        return respuesta_final

    # Aquí definimos todo lo que es el generador de respuestas, 
    # las manuales no consumen memoria computacional y son instantaneas
    def generar_respuesta(self, texto, historial, gustos, intencion, modo_respuesta):

        # =========================
        # RESPUESTAS MANUALES
        # =========================

        if intencion == "saludo":
            return f"Hola {self.usuario_actual} 😄"

        if intencion == "hora":
            now = datetime.datetime.now()
            return f"Ahora son las {now.hour}:{now.minute:02d}"

        if intencion == "gustos_usuario":
            if gustos:
                return f"Te gusta: {', '.join(gustos)} 😄"
            else:
                return "Todavía no conozco muchos de tus gustos 😄"

        if intencion == "gustos_bot":
            return random.choice(self.personality.darryl_gustos)
        
        # =========================
        # MODO SOLO SI / NO
        # =========================

        if modo_respuesta == "si_no":

            messages = [
                {
                    "role": "system",
                    "content": """
                    Responde únicamente con:
                    - Sí
                    - No

                    No añadas explicaciones.
                    No añadas emojis.
                    No añadas texto extra.
                    """
                },
                {
                    "role": "user",
                    "content": texto
                }
            ]

            respuesta = self.ai.generar_respuesta(messages)

            # limpieza extra
            respuesta = respuesta.split(".")[0]
            respuesta = respuesta.split("!")[0]
            respuesta = respuesta.split("?")[0]

            if "sí" in respuesta.lower():
                return "Sí"

            return "No"

        # ===============================
        # Respuestas de la IA GENERATIVA
        # ===============================

        messages = [
            {
                "role": "system",
                "content": f"""
                Eres Darryl.
                Hablas siempre en Español

                REGLAS IMPORTANTES QUE TIENES QUE SEGUIR:
                - responde de forma breve
                - máximo 3 frases
                - no hagas roleplay
                - no inventes historias
                - No inventes gustos
                - No inventes recuerdos
                - no repitas el contexto
                - no inventes usuarios
                - no hables de temas aleatorios
                - responde SOLO a lo que pregunta el usuario
                - si es una pregunta simple, responde simple
                - si el modo de respuesta es "si_no", responde SOLO CON "Si" O "No"
                - no escribas como un asistente técnico
                - No ignores la pregunta del usuario
                - No roleplay

                Modo actual del usuario:
                {modo_respuesta}
                TU PERSONALIDAD:
                {self.personality.descripcion}
                """
                        }
        ]

        # =========================
        # HISTORIAL REAL
        # =========================

        for m in historial:

            messages.append({
                "role": "user",
                "content": m["user"]
            })

            messages.append({
                "role": "assistant",
                "content": m["bot"]
            })

        # =========================
        # MENSAJE ACTUAL
        # =========================

        messages.append({
            "role": "user",
            "content": texto
        })

        respuesta = self.ai.generar_respuesta(
            messages
        )

        return respuesta