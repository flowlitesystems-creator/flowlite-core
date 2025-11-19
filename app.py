from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# 🔥 TU INSTANCIA Y TOKEN AQUÍ
INSTANCE_ID = "7107368022"
API_TOKEN = "1f9e8df4f4ee4354bfb08547cc11ed83639a1764569e43169a"

# =================================
# FUNCIÓN PARA RESPONDER A WHATSAPP
# =================================
def enviar_respuesta(chat_id, texto):
    url = f"https://api.green-api.com/waInstance{INSTANCE_ID}/sendMessage/{API_TOKEN}"

    payload = {
        "chatId": chat_id,
        "message": texto
    }

    r = requests.post(url, json=payload)

    print("📤 RESPUESTA ENVIADA:", r.text)
    return r.status_code


# ===========
# WEBHOOK
# ===========
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print("📩 Webhook recibido:", data)

    body = data.get("body", {})
    msg = body.get("messageData", {})
    msg_type = msg.get("typeMessage")

    chat_id = body.get("senderData", {}).get("chatId", "")

    # mensaje de texto normal
    if msg_type == "textMessage":
        texto = msg.get("textMessageData", {}).get("textMessage", "")
        print("💬 Texto:", texto)
        enviar_respuesta(chat_id, f"Recibí tu mensaje: {texto}")

    # mensaje extendido (la mayoría de celulares)
    elif msg_type == "extendedTextMessage":
        texto = msg.get("extendedTextMessageData", {}).get("text", "")
        print("💬 Texto extendido:", texto)
        enviar_respuesta(chat_id, f"Recibí tu mensaje: {texto}")

    else:
        print("⚠️ Tipo no manejado:", msg_type)

    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
