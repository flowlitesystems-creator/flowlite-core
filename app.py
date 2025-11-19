from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

GREENAPI_ID = os.getenv("GREENAPI_INSTANCE_ID")
GREENAPI_TOKEN = os.getenv("GREENAPI_TOKEN")

@app.route("/", methods=["GET"])
def home():
    return "FlowLite is running!", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print("💬 Mensaje recibido:", data)

    try:
        msg = data.get("messageData", {}).get("textMessageData", {}).get("textMessage", "")
        sender = data.get("senderData", {}).get("chatId", "")

        if msg and sender:
            reply_message(sender, msg)

    except Exception as e:
        print("Error procesando mensaje:", e)

    return jsonify({"status": "ok"}), 200


def reply_message(chat_id, incoming_text):
    url = f"https://7107.api.green-api.com/waInstance{GREENAPI_ID}/sendMessage/{GREENAPI_TOKEN}"

    payload = {
        "chatId": chat_id,
        "message": f"Recibí tu mensaje: {incoming_text}"
    }

    response = requests.post(url, json=payload)
    print("📤 Respuesta enviada:", response.text)


if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
