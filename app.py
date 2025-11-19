from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

INSTANCE_ID = "7107368022"
API_TOKEN = "1f9e8df4f4ee4354bfb08547cc11ed83639a1764569e43169a"


@app.route("/", methods=["GET"])
def home():
    return "FlowLite Core OK", 200


@app.route("/webhook", methods=["GET", "POST"])
def webhook():

    # Necesario para que Render y Green-API validen la ruta
    if request.method == "GET":
        return "Webhook OK", 200

    data = request.json

    print("==== WEBHOOK RECIBIDO ====")
    print(data)

    if not data:
        return jsonify({"error": "no JSON"}), 200

    # Formato real de Green-API
    msg = data.get("messageData", {})
    type_message = msg.get("typeMessage")
    sender = data.get("senderData", {})
    chat_id = sender.get("chatId")

    # Texto simple
    if type_message == "textMessage":
        text = msg.get("textMessageData", {}).get("textMessage", "")
        return responder(chat_id, text)

    # Texto extendido
    if type_message == "extendedTextMessage":
        text = msg.get("extendedTextMessageData", {}).get("text", "")
        return responder(chat_id, text)

    return jsonify({"ignored": type_message}), 200


def responder(chat_id, texto):
    url = f"https://api.green-api.com/waInstance{INSTANCE_ID}/sendMessage/{API_TOKEN}"

    payload = {
        "chatId": chat_id,
        "message": f"Recibí tu mensaje: {texto}"
    }

    headers = {"Content-Type": "application/json"}

    print("=== ENVIANDO RESPUESTA A GREEN-API ===")
    print("URL:", url)
    print("PAYLOAD:", payload)

    try:
        r = requests.post(url, json=payload, headers=headers)
        print("STATUS:", r.status_code)
        print("RESPUESTA GREEN-API:", r.text)
    except Exception as e:
        print("ERROR AL ENVIAR:", e)

    return jsonify({"sent": True}), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
