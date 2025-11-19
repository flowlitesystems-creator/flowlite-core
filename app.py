import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

INSTANCE_ID = os.getenv("GREENAPI_INSTANCE_ID")
TOKEN = os.getenv("GREENAPI_TOKEN")

# URL base de GreenAPI
BASE_URL = f"https://7107.api.green-api.com/waInstance{INSTANCE_ID}"

def enviar_mensaje(chat_id, texto):
    url = f"{BASE_URL}/sendMessage/{TOKEN}"
    payload = {
        "chatId": chat_id,
        "message": texto
    }
    requests.post(url, json=payload)

@app.route("/", methods=["GET"])
def home():
    return "FlowLite is running!", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print("Webhook recibido:", data)

    try:
        msg = data["messageData"]["textMessageData"]["textMessage"]
        chat_id = data["senderData"]["chatId"]

        # RESPUESTA AUTOMÁTICA
        respuesta = f"Recibí tu mensaje: {msg}"
        enviar_mensaje(chat_id, respuesta)

    except:
        pass

    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
