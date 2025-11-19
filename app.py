from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

INSTANCE_ID = "7107368022"
API_TOKEN = "1f9e8df4f4ee4354bfb08547cc11ed83639a1764569e43169a"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    body = data.get("body", {})

    msg_type = body.get("typeMessage")
    chat_id = body.get("chatId")

    # TEXT NORMAL
    if msg_type == "textMessage":
        texto = body.get("textMessage", "")
        return responder(chat_id, texto)

    # EXTENDED TEXT
    if msg_type == "extendedTextMessage":
        texto = body.get("extendedTextMessage", {}).get("text", "")
        return responder(chat_id, texto)

    return jsonify({"ignored": msg_type}), 200


def responder(chat_id, texto):
    url = f"https://api.green-api.com/waInstance{INSTANCE_ID}/sendMessage/{API_TOKEN}"
    payload = {"chatId": chat_id, "message": f"Recibí tu mensaje: {texto}"}
    headers = {"Content-Type": "application/json"}

    r = requests.post(url, json=payload, headers=headers)
    print("RESPUESTA DE GREEN:", r.status_code, r.text)

    return jsonify({"sent": True}), 200
