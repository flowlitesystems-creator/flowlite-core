from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

INSTANCE_ID = "7107368022"
API_TOKEN = "1f9e8df4f4ee4354bfb08547cc11ed83639a1764569e43169a"


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    body = data.get("body", {})
    msg = body.get("messageData", {})
    type_message = msg.get("typeMessage")

    # EXTRAER chatId
    chat_id = body.get("senderData", {}).get("chatId")

    # EXTRAER texto del mensaje SEGÚN TU JSON REAL
    # (siempre viene como textMessage o extendedTextMessage.text)
    texto = (
        msg.get("textMessage")
        or msg.get("extendedTextMessage", {}).get("text")
        or ""
    )

    if texto and chat_id:
        return responder(chat_id, texto)

    # si llega algo que no es texto
    return jsonify({"ignored": type_message}), 200


def responder(chat_id, texto):
    url = f"https://api.green-api.com/waInstance{INSTANCE_ID}/sendMessage/{API_TOKEN}"
    payload = {
        "chatId": chat_id,
        "message": f"Recibí tu mensaje: {texto}"
    }
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "FlowLite-Render/1.0"
    }

    r = requests.post(url, json=payload, headers=headers)
    print("GREEN-API RESPONSE:", r.status_code, r.text)

    return jsonify({"sent": True}), 200
