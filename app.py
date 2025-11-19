from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

INSTANCE_ID = "7107368022"
API_TOKEN = "1f9e8df4f4ee4354bfb08547cc11ed83639a1764569e43169a"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print("Webhook recibido:", data)

    body = data.get("body", {})
    message_data = body.get("messageData", {})
    type_message = message_data.get("typeMessage")

    if type_message == "textMessage":
        text = message_data.get("textMessageData", {}).get("textMessage", "")
        return enviar_respuesta(text)

    if type_message == "extendedTextMessage":
        text = message_data.get("extendedTextMessageData", {}).get("text", "")
        return enviar_respuesta(text)

    print("Tipo no manejado:", type_message)
    return jsonify({"status": "ignored"}), 200


def enviar_respuesta(text):
    url = f"https://api.greenapi.com/waInstance{INSTANCE_ID}/sendMessage/{API_TOKEN}"

    payload = {
        "chatId": "51990852170@c.us",
        "message": f"Recibí tu mensaje: {text}"
    }

    r = requests.post(url, json=payload)
    print("Respuesta enviada:", r.text)

    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
