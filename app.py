from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

INSTANCE_ID = "7107368022"
API_TOKEN = "1f9e8df4f4ee4354bfb08547cc11ed83639a1764569e43169a"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    if data is None:
        return jsonify({"error": "No JSON"}), 200

    body = data.get("body", {})
    msg = body.get("messageData", {})
    type_message = msg.get("typeMessage")

    # ---- TEXT MESSAGE NORMAL ----
    if type_message == "textMessage":
        text = msg.get("textMessageData", {}).get("textMessage", "")
        chat_id = body.get("senderData", {}).get("chatId")
        return enviar_respuesta(chat_id, text)

    # ---- EXTENDED TEXT MESSAGE ----
    if type_message == "extendedTextMessage":
        text = msg.get("extendedTextMessageData", {}).get("text", "")
        chat_id = body.get("senderData", {}).get("chatId")
        return enviar_respuesta(chat_id, text)

    return jsonify({"ignored": type_message}), 200


def enviar_respuesta(chat_id, texto):
    url = f"https://api.green-api.com/waInstance{INSTANCE_ID}/sendMessage/{API_TOKEN}"

    payload = {
        "chatId": chat_id,
        "message": f"Recibí tu mensaje: {texto}"
    }

    headers = {
        "Content-Type": "application/json"
    }

    r = requests.post(url, json=payload, headers=headers)
    print("GREEN API RESPONSE:", r.status_code, r.text)

    return jsonify({"sent": True}), 200


@app.route("/", methods=["GET"])
def home():
    return "FlowLite Webhook OK", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
