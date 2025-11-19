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

    # TEXT NORMAL
    if type_message == "textMessage":
        text = body.get("textMessageData", {}).get("textMessage", "")
        chat_id = body.get("senderData", {}).get("chatId")
        return responder(chat_id, text)

    # EXTENDED TEXT
    if type_message == "extendedTextMessage":
        text = body.get("extendedTextMessageData", {}).get("text", "")
        chat_id = body.get("senderData", {}).get("chatId")
        return responder(chat_id, text)

    return jsonify({"status": "ignored", "reason": type_message}), 200


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

    print("RESPUESTA GREEN-API:", r.text)

    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    # NECESARIO PARA RENDER
    app.run(host="0.0.0.0", port=10000)
