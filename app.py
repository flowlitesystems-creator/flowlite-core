from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.json
        print("Webhook recibido:", data)

        # OJO: messageData está directamente en data
        message_data = data.get("messageData", {})
        type_message = message_data.get("typeMessage")

        # === MENSAJE DE TEXTO NORMAL ===
        if type_message == "textMessage":
            text = message_data.get("textMessageData", {}).get("textMessage", "")
            print("MENSAJE TEXTO:", text)
            return responder(text)

        # === MENSAJE DE TEXTO EXTENDIDO ===
        if type_message == "extendedTextMessage":
            text = message_data.get("extendedTextMessageData", {}).get("text", "")
            print("MENSAJE EXTENDIDO:", text)
            return responder(text)

        print("Tipo de mensaje no manejado:", type_message)
        return jsonify({"status": "ignored"}), 200

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": str(e)}), 500


def responder(texto):
    respuesta = f"Recibí tu mensaje: {texto}"
    print("RESPONDIENDO:", respuesta)
    return jsonify({"status": "ok", "reply": respuesta}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
