# Archivo main a ejecutar para inicializar el Chatbot
import os
from flask import Flask, render_template, request, jsonify
from app.chatbot import Chatbot

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "../interface"),
    static_folder=os.path.join(BASE_DIR, "../interface")
)

bot = Chatbot()

# Cargamos la página principal
@app.route("/")
def home():
    return render_template("index.html")

# Cargar el primer mensaje para que el usuario lo primero que haga es identificarse
@app.route("/welcome", methods=["GET"])
def welcome():
    return jsonify({
        "message": "¡Buenas! Para hablar contigo primero escribe tu nombre para identificarte"
    })

# La funcionalidad del chatbot
@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    respuesta = bot.responder(user_input)
    return jsonify({"response": respuesta})

if __name__ == "__main__":
    app.run(debug=True)