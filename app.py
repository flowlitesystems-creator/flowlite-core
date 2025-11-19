from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "FlowLite is running!", 200


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print("📩 Webhook recibido:", data)

    try:
        msg = data["messageData"]["textMessageData"]["textMessage"]
        sender = data["senderData"]["sender"]
    except:
        return jsonify({"status": "ignored"}), 200

    # RESPUESTA AUTOMÁTICA
    respuesta = f"Hola! Recibí tu mensaje: {msg}"

    print("➡️ Enviando respuesta automática:", respuesta)

    return jsonify({"replyMessage": respuesta}), 200


if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
