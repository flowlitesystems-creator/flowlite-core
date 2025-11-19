from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

INSTANCE_ID = "7107368022"
API_TOKEN = "1f9e8df4f4ee4354bfb08547cc11ed83639a1764569e43169a"


@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.json
        print("Webhook recibido:", data)

        body = data.get("body", {})
        message_data = body.get("messageData", {})
        type_message = message_data.get("typeMessage")

        # === Mensaje de texto normal ===
        if type_message == "textMessage":
            text = message_data.get("textMessageData", {}).get("textMessage", "")

        # === Mensaje extendido ===
        elif type_message == "extendedTextMessage":
            text = message_data.get("extendedTextMessageData", {}).get("text", "")

        else:
            print("Tipo no manejado:", type_message)
            return jsonify({"status": "ignored"}), 200

        print("MENSAJE RECIBIDO:", text)

        # ===== RESPUESTA AUTOMÁTICA =====
        enviar_respuesta(text)

        return jsonify({"status": "ok"}), 200

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": str(e)}), 500


def enviar_respuesta(texto):
    url = f"https://7107368022.api.greenapi.com/waSendMessage/{API_TOKEN}"

    payload = {
        "chatId": "913642644@c.us",
        "message": f"Recibí tu mensaje: {texto}"
    }

    r = requests.post(url, json=payload)
    print("RESPUESTA GREEN API:", r.text)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
