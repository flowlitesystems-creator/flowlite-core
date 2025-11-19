from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

INSTANCE_ID = "7107368022"
API_TOKEN = "1f9e8df4f4ee4354bfb08547cc11ed83639a1764569e43169a"

# URL base de Green API
BASE_URL = f"https://api.green-api.com/waInstance{INSTANCE_ID}"


@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.json
        print("Webhook recibido:", data)

        body = data.get("body", {})
        message_data = body.get("messageData", {})
        type_message = message_data.get("typeMessage")

        chat_id = body.get("senderData", {}).get("chatId", "")

        # === MENSAJE DE TEXTO NORMAL ===
        if type_message == "textMessage":
            text = message_data.get("textMessageData", {}).get("textMessage", "")
            print("MENSAJE:", text)
            return send_reply(chat_id, text)

        # === MENSAJE EXTENDIDO ===
        if type_message == "extendedTextMessage":
            text = message_data.get("extendedTextMessageData", {}).get("text", "")
            print("MENSAJE EXTENDIDO:", text)
            return send_reply(chat_id, text)

        print("Tipo de mensaje no manejado:", type_message)
        return jsonify({"status": "ignored"}), 200

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": str(e)}), 500


def send_reply(chat_id, text):
    respuesta = f"Recibí tu mensaje: {text}"
    print("RESPONDIENDO:", respuesta)

    url = f"{BASE_URL}/sendMessage/{API_TOKEN}"
    payload = {
        "chatId": chat_id,
        "message": respuesta
    }

    r = requests.post(url, json=payload)
    print("RESPUESTA GREEN API:", r.text)

    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
