from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

INSTANCE_ID = "7107368022"
API_TOKEN = "1f9e8df4f4ee4354bfb08547cc11ed83639a1764569e43169a"


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)

    # GreenAPI envía un array de mensajes
    if isinstance(data, list):
        for msg in data:
            if msg.get("type") == "incoming":
                chat_id = msg.get("chatId")
                text = msg.get("textMessage") or msg.get("extendedTextMessage", {}).get("text", "")

                if chat_id and text:
                    enviar_respuesta(chat_id, text)

    return jsonify({"ok": True}), 200


def enviar_respuesta(chat_id, texto):
    url = f"https://api.green-api.com/waInstance{INSTANCE_ID}/sendMessage/{API_TOKEN}"

    payload = {
        "chatId": chat_id,
        "message": f"Recibido: {texto}"
    }

    headers = {"Content-Type": "application/json"}

    r = requests.post(url, json=payload, headers=headers)
    print("RESPUESTA GREEN-API:", r.status_code, r.text)


# Render usa gunicorn, no agregues app.run()
