from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

GREENAPI_INSTANCE = os.getenv("GREENAPI_INSTANCE_ID")
GREENAPI_TOKEN = os.getenv("GREENAPI_TOKEN")

def enviar_mensaje(numero, texto):
    url = f"https://7107.api.green-api.com/waInstance{GREENAPI_INSTANCE}/SendMessage/{GREENAPI_TOKEN}"
    payload = {
        "chatId": f"{numero}@c.us",
        "message": texto
    }
    requests.post(url, json=payload)

@app.route("/", methods=["GET"])
def home():
    return "FlowLite is running!", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    try:
        mensaje = data['messageData']['textMessageData']['textMessage']
        numero = data['senderData']['chatId'].replace("@c.us", "")
    except:
        return jsonify({"status": "ignored"}), 200

    # RESPUESTA AUTOMÁTICA BÁSICA
    enviar_mensaje(numero, "Hola 👋, recibí tu mensaje correctamente.")

    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)))
