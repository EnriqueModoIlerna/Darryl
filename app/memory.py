import json
import os


class Memory:

    def __init__(self):

        self.file = "data/users.json"

        # Crear archivo si no existe
        if not os.path.exists(self.file):
            with open(self.file, "w") as f:
                json.dump({}, f, indent=2)

    # =========================
    # FUNCIONES INTERNAS
    # =========================
    def cargar_datos(self):

        if not os.path.exists(self.file):
            return {}

        try:
            with open(self.file, "r") as f:
                return json.load(f)

        except json.JSONDecodeError:
            return {}

    def guardar_datos(self, data):
        with open(self.file, "w") as f:
            json.dump(data, f, indent=2)

    # =========================
    # USUARIOS
    # =========================
    def existe_usuario(self, nombre):

        data = self.cargar_datos()

        return nombre in data


    def crear_usuario(self, nombre):

        data = self.cargar_datos()

        data[nombre] = {
            "personalidad": {
                "tono": "informal"
            },

            "gustos": [],
            "historial": [],
            "preferencias": {}
        }

        self.guardar_datos(data)

    # =========================
    # HISTORIAL
    # =========================
    def guardar_conversacion(self, usuario, mensaje_user, mensaje_bot):

        data = self.cargar_datos()

        data[usuario]["historial"].append({
            "user": mensaje_user,
            "bot": mensaje_bot
        })

        self.guardar_datos(data)


    def recuperar_historial(self, usuario):

        data = self.cargar_datos()

        return data[usuario]["historial"]

    # =========================
    # GUSTOS / APRENDIZAJE
    # =========================
    def guardar_gusto(self, usuario, gusto):

        data = self.cargar_datos()

        if gusto not in data[usuario]["gustos"]:
            data[usuario]["gustos"].append(gusto)

        self.guardar_datos(data)


    def recuperar_gustos(self, usuario):

        data = self.cargar_datos()

        return data[usuario]["gustos"]
    
    # ======================================================
    # GUARDAR UNA PREFERENCIA DE CHAT Y USAR PREFERENCIA
    # ======================================================
    def recuperar_preferencia(self, usuario, clave):

        data = self.cargar_datos()

        if usuario not in data:
            return None

        preferencias = data[usuario].get("preferencias", {})

        return preferencias.get(clave, "normal")
    
    
    def guardar_preferencia(self, usuario, clave, valor):

        data = self.cargar_datos()

        if usuario not in data:
            return

        if "preferencias" not in data[usuario]:
            data[usuario]["preferencias"] = {}

        data[usuario]["preferencias"][clave] = valor

        self.guardar_datos(data)