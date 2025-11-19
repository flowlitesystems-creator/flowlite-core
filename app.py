from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.json
        print("Webhook recibido:", data)

        body = data.get("body", {})

        # El typeMessage está AQUÍ
        type_message = body.get("typeMessage")

        # Mensaje de texto
        if type_message == "textMessage":
            text = body.get("textMessageData", {}).get("textMessage", "")
            print("MENSAJE RECIBIDO:", text)

            respuesta = f"Recibido tu mensaje: {text}"
            print("RESPONDIENDO:", respuesta)

            return jsonify({"status": "ok", "reply": respuesta}), 200

        print("Tipo de mensaje no manejado:", type_message)
        return jsonify({"status": "ignored"}), 200

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
