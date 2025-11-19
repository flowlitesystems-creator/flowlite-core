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

        # OBTENER NÚMERO DEL REMITENTE
        sender = body.get("senderData", {}).get("sender", "")

        # MENSAJE NORMAL
        if type_message == "textMessage":
            text = message_data.get("textMessageData", {}).get("textMessage", "")
            print("MENSAJE RECIBIDO:", text)
            enviar_respuesta(sender, text)
            return jsonify({"status": "ok"}), 200

        # MENSAJE EXTENDIDO (tu teléfono usa este)
        if type_message == "extendedTextMessage":
            text = message_data.get("extendedTextMessageData", {}).get("text", "")
            print("MENSAJE EXTENDIDO:", text)
            enviar_respuesta(sender, text)
            return jsonify({"status": "ok"}), 200

        print("Tipo de mensaje NO manejado:", type_message)
        return jsonify({"status": "ignored"}), 200

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"error": str(e)}), 500


def enviar_respuesta(numero, texto):
    url = f"https://api.green-api.com/waInstance{INSTANCE_ID}/sendMessage/{API_TOKEN}"

    payload = {
        "chatId": numero,
        "message": f"Recibí tu mensaje: {texto}"
    }

    print("Enviando respuesta a WhatsApp:", payload)

    r = requests.post(url, json=payload)
    print("Respuesta GreenAPI:", r.text)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
