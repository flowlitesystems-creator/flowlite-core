from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.json
        print("Webhook recibido:", data)

        body = data.get("body", {})
        message_data = body.get("messageData", {})
        type_message = message_data.get("typeMessage")

        # -------------------------
        # TEXTMESSAGE NORMAL
        # -------------------------
        if type_message == "textMessage":
            text_message_data = message_data.get("textMessageData", {})
            text = text_message_data.get("textMessage", "")

            print("MENSAJE RECIBIDO:", text)
            return jsonify({"response": f"Recibí tu mensaje: {text}"}), 200

        # -------------------------
        # EXTENDEDTEXTMESSAGE  (EL QUE TE ESTÁ LLEGANDO)
        # -------------------------
        if type_message == "extendedTextMessage":
            ext = message_data.get("extendedTextMessageData", {})
            text = ext.get("text", "")

            print("MENSAJE EXTENDIDO RECIBIDO:", text)
            return jsonify({"response": f"Recibí tu mensaje: {text}"}), 200

        print("Tipo de mensaje no manejado:", type_message)
        return jsonify({"status": "ignored"}), 200

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
