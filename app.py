@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        return "Webhook OK", 200

    data = request.json

    print("==== WEBHOOK RECIBIDO ====")
    print(data)

    if not data:
        return jsonify({"error": "no JSON"}), 200

    body = data.get("body", {})
    msg = body.get("messageData", {})
    type_message = msg.get("typeMessage")

    if type_message == "textMessage":
        text = msg.get("textMessageData", {}).get("textMessage", "")
        chat_id = body.get("senderData", {}).get("chatId")
        return responder(chat_id, text)

    if type_message == "extendedTextMessage":
        text = msg.get("extendedTextMessageData", {}).get("text", "")
        chat_id = body.get("senderData", {}).get("chatId")
        return responder(chat_id, text)

    return jsonify({"ignored": type_message}), 200
