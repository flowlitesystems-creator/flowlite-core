@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        return "Webhook OK", 200

    data = request.json

    print("==== WEBHOOK RECIBIDO ====")
    print(data)

    # Estructura real de Green-API
    msg = data.get("messageData", {})
    type_message = msg.get("typeMessage")
    sender = data.get("senderData", {})
    chat_id = sender.get("chatId")

    # Texto normal
    if type_message == "textMessage":
        text = msg.get("textMessageData", {}).get("textMessage", "")
        return responder(chat_id, text)

    # Texto extendido
    if type_message == "extendedTextMessage":
        text = msg.get("extendedTextMessageData", {}).get("text", "")
        return responder(chat_id, text)

    return jsonify({"ignored": type_message}), 200
