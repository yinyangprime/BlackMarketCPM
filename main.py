from flask import Flask, request, jsonify
from datetime import datetime
import json
import requests

app = Flask(__name__)
KEYS_FILE = 'YinYangKeys.json'
ENDPOINT_URL = "https://cpmnuker.anasov.ly/api"

class CPMNuker:
    def __init__(self, access_key):
        self.auth_token = None
        self.access_key = access_key

    def login(self, email, password):
        payload = {"account_email": email, "account_password": password}
        params = {"key": self.access_key}
        response = requests.post(f"{ENDPOINT_URL}/account_login", params=params, data=payload)
        data = response.json()
        if data.get("ok"):
            self.auth_token = data.get("auth")
        return data

    def set_player_money(self, amount):
        payload = {"account_auth": self.auth_token, "amount": amount}
        params = {"key": self.access_key}
        response = requests.post(f"{ENDPOINT_URL}/set_money", params=params, data=payload)
        return response.json()

def is_key_valid(user_key):
    try:
        with open(KEYS_FILE, 'r') as f:
            keys = json.load(f)
    except FileNotFoundError:
        return False, "Key database tidak dijumpai."

    for key in keys:
        if key["key"] == user_key:
            expiry = key.get("expiry")
            if expiry and datetime.strptime(expiry, "%Y-%m-%d %H:%M:%S") < datetime.now():
                return False, "Kunci telah tamat tempoh."
            return True, key.get("owner", "Tanpa Nama")
    return False, "Kunci tidak sah atau telah tamat tempoh."

@app.route('/')
def home():
    return jsonify({"by": "Yin Yang Black Market", "status": "🟢 Yin Yang CPM API Aktif!"})

@app.route('/api', methods=['GET'])
def check_key():
    key = request.args.get("key")
    valid, result = is_key_valid(key)
    return jsonify({"valid": valid, "message": result})

@app.route('/nuker/login', methods=['POST'])
def nuker_login():
    key = request.args.get("key")
    email = request.form.get("email")
    password = request.form.get("password")
    valid, _ = is_key_valid(key)
    if not valid:
        return jsonify({"ok": False, "error": "Key tidak sah"})
    nuker = CPMNuker(key)
    return nuker.login(email, password)

@app.route('/nuker/set_money', methods=['POST'])
def set_money():
    key = request.args.get("key")
    amount = request.form.get("amount")
    email = request.form.get("email")
    password = request.form.get("password")
    valid, _ = is_key_valid(key)
    if not valid:
        return jsonify({"ok": False, "error": "Key tidak sah"})
    nuker = CPMNuker(key)
    login_result = nuker.login(email, password)
    if not login_result.get("ok"):
        return jsonify({"ok": False, "error": "Login gagal"})
    return nuker.set_player_money(amount)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
