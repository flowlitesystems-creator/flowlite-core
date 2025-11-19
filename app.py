from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

GREENAPI_INSTANCE_ID = os.getenv("GREENAPI_INSTANCE_ID")
GREENAPI_TOKEN = os.getenv("GREENAPI_TOKEN")

@app.route("/", methods=["GET"])
def home():
    return "FlowLite is running!", 200


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print("📩 Mensaje recibido:", data)

    try:
        message = data['messageData']['textMessage']
        phone = data['senderData']['chatId'].replace("@c.us", "")

        enviar_respuesta(phone, f"Recibí tu mensaje: {message}")

    except Exception as e:
        print("⚠️ Error procesando mensaje:", e)

    return jsonify({"status": "ok"}), 200


def enviar_respuesta(phone, texto):
    url = f"https://7107.api.green-api.com/waInstance{GREENAPI_INSTANCE_ID}/sendMessage/{GREENAPI_TOKEN}"

    payload = {
        "chatId": f"{phone}@c.us",
        "message": texto
    }

    r = requests.post(url, json=payload)
    print("📤 Enviado:", r.text)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)))
