from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

INSTANCE_ID = "7107368022"
API_TOKEN = "1f9e8df4f4ee4354bfb08547cc11ed83639a1764569e43169a"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    body = data.get("body", {})
    type_message = body.get("typeMessage")
    chat_id = body.get("chatId")
    text = ""

    # ---- textMessage ----
    if type_message == "textMessage":
        text = body.get("textMessage")

    # ---- extendedTextMessage ----
    if type_message == "extendedTextMessage":
        text = body.get("extendedTextMessage", {}).get("text", "")

    # Si no hay texto, ignoramos
    if not text or not chat_id:
        return jsonify({"ignored": True}), 200

    enviar_respuesta(chat_id, text)
    return jsonify({"ok": True}), 200


def enviar_respuesta(chat_id, text):
    url = f"https://api.green-api.com/waInstance{INSTANCE_ID}/sendMessage/{API_TOKEN}"

    payload = {
        "chatId": chat_id,
        "message": f"Recibí tu mensaje: {text}"
    }

    headers = {"Content-Type": "application/json"}

    r = requests.post(url, json=payload, headers=headers)
    print("RESPUESTA GREEN-API:", r.status_code, r.text)
