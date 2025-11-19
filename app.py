@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.json
        print("Webhook recibido:", data)

        body = data.get("body", {})
        message_data = body.get("messageData", {})
        type_message = message_data.get("typeMessage")

        # 📌 Manejar mensajes de texto normales
        if type_message == "textMessage":
            text = message_data.get("textMessageData", {}).get("textMessage", "")
            print("MENSAJE RECIBIDO:", text)

        # 📌 Manejar mensajes extendedTextMessage (los que tú estás enviando)
        elif type_message == "extendedTextMessage":
            text = message_data.get("extendedTextMessageData", {}).get("text", "")
            print("MENSAJE EXTENDIDO RECIBIDO:", text)

        else:
            print("Tipo de mensaje NO manejado:", type_message)
            return jsonify({"status": "ignored"}), 200

        # RESPUESTA
        respuesta = f"Recibí tu mensaje: {text}"
        print("RESPONDIENDO:", respuesta)
        return jsonify({"status": "ok", "reply": respuesta}), 200

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"error": str(e)}), 500
